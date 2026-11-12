import os
import re

MAX_CHARS = 20000
OCR_MAX_PAGES = int(os.getenv('OCR_MAX_PAGES', '10'))
OCR_DPI = int(os.getenv('OCR_DPI', '200'))
OCR_MIN_TEXT = int(os.getenv('OCR_MIN_TEXT', '20'))
OCR_ENABLED = os.getenv('OCR_ENABLED', 'True').lower() in ('1', 'true', 'yes', 'on')

PLAIN_TEXT_EXTENSIONS = {'.txt', '.md', '.csv', '.json', '.log', '.xml'}

_ocr_engine = None
_ocr_error = None


def _get_ocr_engine():
    """懒加载 PaddleOCR，首次调用时才初始化，避免拖慢服务启动。"""
    global _ocr_engine, _ocr_error
    if _ocr_engine is not None:
        return _ocr_engine
    if _ocr_error:
        raise RuntimeError(_ocr_error)

    try:
        from paddleocr import PaddleOCR

        kwargs = {'lang': os.getenv('OCR_LANG', 'ch'), 'enable_mkldnn': False}
        try:
            # PaddleOCR 3.x（关闭 oneDNN，规避部分 CPU 上的 PIR/oneDNN 兼容问题）
            _ocr_engine = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                **kwargs
            )
        except TypeError:
            # PaddleOCR 2.x
            _ocr_engine = PaddleOCR(use_angle_cls=True, show_log=False, **kwargs)
        return _ocr_engine
    except Exception as e:
        _ocr_error = f'PaddleOCR 初始化失败：{e}'
        raise RuntimeError(_ocr_error)


def _ocr_image(image_bgr):
    """对单张 BGR 图片做 OCR，返回按行拼接的文本。"""
    engine = _get_ocr_engine()

    if hasattr(engine, 'predict'):
        try:
            results = engine.predict(image_bgr)
        except TypeError:
            results = engine.predict(input=image_bgr)

        lines = []
        for result in results:
            texts = None
            try:
                # OCRResult 支持下标访问
                texts = result['rec_texts']
            except Exception:
                texts = getattr(result, 'rec_texts', None)
                if texts is None and hasattr(result, 'get'):
                    texts = result.get('rec_texts')
            if texts:
                lines.extend(str(t) for t in texts)
        return "\n".join(lines).strip()

    # PaddleOCR 2.x
    result = engine.ocr(image_bgr, cls=True)
    lines = []
    for page in result or []:
        for item in page or []:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                value = item[1]
                text = value[0] if isinstance(value, (list, tuple)) else value
                if text:
                    lines.append(str(text))
    return "\n".join(lines).strip()


def _render_page_to_bgr(page, dpi):
    import numpy as np

    pix = page.get_pixmap(dpi=dpi)
    array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if array.shape[2] > 3:
        array = array[:, :, :3]
    return np.ascontiguousarray(array[:, :, ::-1])


def _extract_pdf_with_fitz(path):
    import fitz

    document = fitz.open(path)
    pages = []
    ocr_pages = 0
    try:
        for index, page in enumerate(document, 1):
            text = page.get_text('text').strip()

            if OCR_ENABLED and len(text) < OCR_MIN_TEXT and ocr_pages < OCR_MAX_PAGES:
                try:
                    ocr_text = _ocr_image(_render_page_to_bgr(page, OCR_DPI))
                except Exception as e:
                    print(f"第{index}页 OCR 失败：{e}")
                    ocr_text = ''
                if ocr_text and len(ocr_text) > len(text):
                    text = ocr_text
                    ocr_pages += 1

            if text:
                pages.append(f"第{index}页:\n{text}")
    finally:
        document.close()

    result = "\n\n".join(pages)
    if ocr_pages >= OCR_MAX_PAGES:
        result += f"\n...(扫描页较多，仅对前 {OCR_MAX_PAGES} 页做了 OCR)"
    return result


def _extract_pdf_with_pypdf(path):
    from PyPDF2 import PdfReader

    reader = PdfReader(path)
    if reader.is_encrypted:
        try:
            reader.decrypt('')
        except Exception:
            pass

    pages = []
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        if text.strip():
            pages.append(f"第{index}页:\n{text.strip()}")
    return "\n\n".join(pages)


def _extract_pdf(path):
    try:
        return _extract_pdf_with_fitz(path)
    except ImportError:
        return _extract_pdf_with_pypdf(path)


def _extract_plain_text(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def _extract_docx(path):
    from docx import Document

    document = Document(path)
    parts = []
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            parts.append(paragraph.text.strip())

    for table_index, table in enumerate(document.tables, 1):
        rows = []
        for row in table.rows:
            cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
            if any(cells):
                rows.append(' | '.join(cells))
        if rows:
            parts.append(f"表格{table_index}:\n" + "\n".join(rows))

    return "\n".join(parts)


def extract_text(file_path, max_chars=MAX_CHARS):
    """提取 PDF（含扫描件 OCR）/ Word(docx) / 纯文本文件内容。"""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        text = _extract_pdf(file_path)
    elif ext == '.docx':
        text = _extract_docx(file_path)
    elif ext in PLAIN_TEXT_EXTENSIONS:
        text = _extract_plain_text(file_path)
    elif ext == '.doc':
        raise ValueError('暂不支持 .doc 旧格式，请另存为 .docx 或 PDF 后再上传')
    else:
        raise ValueError(f'暂不支持的文件类型：{ext or "未知"}')

    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    if len(text) > max_chars:
        text = text[:max_chars] + f'\n...(内容过长，已截断至前 {max_chars} 字)'
    return text
