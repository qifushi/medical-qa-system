# -*- coding: utf-8 -*-
r"""从 Markdown 重新生成带完整样式的毕设论文 Word 版。

功能：
- 解析 Markdown，渲染为 docx 元素（标题/段落/列表/代码块/表格/图片/引用）
- 自动插入目录（TOC 域）、页眉、页脚页码
- 表格使用 Grid 样式 + 表头加粗底纹 + 奇偶行交替
- 代码块使用 Consolas 等宽字体，带浅灰底
- 图表题注居中，自动编号

用法：
    .\.venv\Scripts\python.exe scripts/export_thesis_docx.py
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.shared import Pt, Cm, RGBColor

ROOT = Path(__file__).resolve().parent.parent
THESIS_MD = ROOT / '论文' / '基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.md'
THESIS_DOCX = ROOT / '论文' / '基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx'
FIG_DIR = ROOT / '论文' / '实验数据' / 'figures'


# ======================================================
# 样式辅助
# ======================================================
def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)


def set_run_font(run, cn_font='宋体', en_font='Times New Roman', size=Pt(10.5),
                 bold=False, color=None):
    run.font.name = en_font
    run._element.rPr.rFonts.set(qn('w:eastAsia'), cn_font)
    run.font.size = size
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor(*color)


def add_paragraph_styled(doc, text, cn_font='宋体', en_font='Times New Roman',
                         size=Pt(12), bold=False, first_line_indent=True,
                         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(6)):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_after = space_after
    pf.line_spacing = 1.5
    if first_line_indent:
        pf.first_line_indent = Cm(0.74)  # 2 chars at 12pt
    run = p.add_run(text)
    set_run_font(run, cn_font, en_font, size, bold)
    return p


def add_heading_styled(doc, text, level=1):
    """使用 Word 内置 Heading 样式（TOC 域必需！），然后覆盖字体。"""
    if level == 0:
        # 封面大标题，用 Normal 即可（不入 TOC）
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = p.paragraph_format
        pf.space_after = Pt(18)
        pf.line_spacing = 1.5
        run = p.add_run(text)
        set_run_font(run, '黑体', 'Times New Roman', Pt(22), bold=True)
        return p

    # level 1-4：用内置 Heading X 样式，Word TOC 域依赖这个来识别标题级别
    p = doc.add_heading(text, level=min(level, 4))
    pf = p.paragraph_format
    pf.line_spacing = 1.5

    # 覆盖字体为黑体 + 对应字号
    sizes = {1: Pt(16), 2: Pt(14), 3: Pt(12), 4: Pt(12)}
    run = p.runs[0] if p.runs else p.add_run(text)
    set_run_font(run, '黑体', 'Times New Roman', sizes.get(level, Pt(12)), bold=True)

    # 段落间距
    spacing = {
        1: (Pt(18), Pt(10)),
        2: (Pt(12), Pt(6)),
        3: (Pt(8), Pt(4)),
        4: (Pt(6), Pt(4)),
    }
    before, after = spacing.get(level, (Pt(6), Pt(4)))
    pf.space_before = before
    pf.space_after = after
    return p


def add_code_block(doc, code):
    # 用等宽字体的段落，浅灰底
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.5)
    pf.right_indent = Cm(0.5)
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.15
    # 背景色
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F2F2F2')
    pPr.append(shd)

    lines = code.rstrip('\n').split('\n')
    for i, line in enumerate(lines):
        run = p.add_run(line if line else ' ')
        run.font.name = 'Consolas'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        if i < len(lines) - 1:
            run.add_break()
    return p


def add_table_styled(doc, md_lines):
    """md_lines 是 markdown 表格行列表（不含分隔行 ---）"""
    rows_data = []
    for line in md_lines:
        if re.match(r'^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$', line):
            continue  # 跳过分隔行
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows_data.append(cells)
    if not rows_data:
        return

    n_rows = len(rows_data)
    n_cols = max(len(r) for r in rows_data)
    table = doc.add_table(rows=n_rows, cols=n_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for ri, row in enumerate(rows_data):
        for ci, val in enumerate(row):
            cell = table.cell(ri, ci)
            cell.text = ''
            # 解析粗体 **x**
            parts = re.split(r'(\*\*[^*]+\*\*)', val)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    bold = True
                else:
                    run = p.add_run(part)
                    bold = False
                set_run_font(run, '宋体', 'Times New Roman', Pt(10), bold=bold)

            # 表头加粗底纹
            if ri == 0:
                set_cell_shading(cell, 'D9E1F2')
            elif ri % 2 == 1:
                set_cell_shading(cell, 'F2F2F2')
    return table


def _add_field(paragraph, instr_text, placeholder='', font_size=Pt(10)):
    """在段落中插入一个完整的 Word 域（begin + instrText + separate + result + end）。
    必须用 w:instrText XML 元素（不是普通 w:t）Word 才会识别为域指令。"""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # 1) fldChar begin
    run_begin = paragraph.add_run()
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    run_begin._r.append(fld_begin)

    # 2) instrText（域指令，必须用 w:instrText 元素！）
    run_instr = paragraph.add_run()
    instr_elem = OxmlElement('w:instrText')
    instr_elem.set(qn('xml:space'), 'preserve')
    instr_elem.text = instr_text
    run_instr._r.append(instr_elem)

    # 3) fldChar separate
    run_sep = paragraph.add_run()
    fld_sep = OxmlElement('w:fldChar')
    fld_sep.set(qn('w:fldCharType'), 'separate')
    run_sep._r.append(fld_sep)

    # 4) 域结果占位（Word 更新域后会替换这里）
    if placeholder:
        run_result = paragraph.add_run(placeholder)
        run_result.font.size = font_size

    # 5) fldChar end
    run_end = paragraph.add_run()
    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')
    run_end._r.append(fld_end)


def _write_inline_with_citations(paragraph, text, bold=False,
                                  in_ref_section=False, is_ref_entry=False):
    """把一段文本写入段落，其中 [数字] 渲染为上标角标。

    - 参考文献区正文：直接写（文献编号不是角标）
    - 参考文献条目行（以 [数字] 开头）：直接写（条目编号）
    - 其它正文：按 [数字] 拆分，数字部分做 superscript
    """
    if in_ref_section or is_ref_entry:
        # 不拆，整段写入
        run = paragraph.add_run(text)
        set_run_font(run, '宋体', 'Times New Roman', Pt(12), bold=bold)
        return

    # 按 [数字] 拆分（支持 [1] 和 [1,2,3] 格式）
    segments = re.split(r'(\[\d+(?:,\d+)*\])', text)
    for seg in segments:
        if not seg:
            continue
        if re.match(r'^\[\d+(?:,\d+)*\]$', seg):
            # 引用角标 → 上标
            run = paragraph.add_run(seg)
            set_run_font(run, '宋体', 'Times New Roman', Pt(12), bold=bold)
            run.font.superscript = True
            run.font.size = Pt(9)  # 角标略小一点
        else:
            run = paragraph.add_run(seg)
            set_run_font(run, '宋体', 'Times New Roman', Pt(12), bold=bold)


def add_toc_field(doc):
    """在新页插入目录域（Word 打开后按 F9 更新）"""
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('目  录')
    set_run_font(run, '黑体', 'Times New Roman', Pt(18), bold=True)

    # TOC 域
    p2 = doc.add_paragraph()
    _add_field(p2, r'TOC \o "1-3" \h \z \u',
               placeholder='（右键此处 → 更新域 以刷新目录）',
               font_size=Pt(10))
    doc.add_page_break()


# ======================================================
# Markdown → Document 主循环
# ======================================================
def render_markdown(md_text, doc):
    lines = md_text.split('\n')
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []
    in_reference_section = False  # 是否进入了"参考文献"章节

    while i < len(lines):
        line = lines[i]

        # -------- 检测参考文献区起点 --------
        if re.match(r'^##\s+参考文献', line.strip()):
            in_reference_section = True

        # -------- 代码块 --------
        if line.strip().startswith('```'):
            if in_code:
                add_code_block(doc, '\n'.join(code_buf))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # -------- 表格 --------
        if line.strip().startswith('|'):
            in_table = True
            table_buf.append(line)
            i += 1
            continue
        elif in_table:
            # 表格结束
            add_table_styled(doc, table_buf)
            table_buf = []
            in_table = False
            # 当前 line 是表格外的行，让外层循环处理
            continue

        # -------- 水平分割线 --------
        if re.match(r'^-{3,}$', line.strip()):
            i += 1
            continue

        # -------- 标题 --------
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            add_heading_styled(doc, text, level=level)
            i += 1
            continue

        # -------- 图片引用 <img ...> --------
        img_m = re.match(r'^!\[(.*?)\]\((.*?)\)\s*$', line)
        if img_m:
            alt, src = img_m.group(1), img_m.group(2)
            # src 可能是相对路径，尝试在 FIG_DIR 下找
            fig_path = (ROOT / src).resolve()
            if not fig_path.exists():
                fig_path = (FIG_DIR / Path(src).name).resolve()
            if fig_path.exists():
                try:
                    doc.add_picture(str(fig_path), width=Cm(15))
                    last = doc.paragraphs[-1]
                    last.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    # 图题
                    caption = doc.add_paragraph(alt if alt else fig_path.stem)
                    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    caption_pf = caption.paragraph_format
                    caption_pf.space_before = Pt(4)
                    caption_pf.space_after = Pt(10)
                    caption_run = caption.add_run(alt if alt else fig_path.stem)
                    set_run_font(caption_run, '宋体', 'Times New Roman', Pt(10.5), bold=True)
                except Exception as e:
                    add_paragraph_styled(doc, f'[图片未能插入: {src} ({e})]')
            else:
                add_paragraph_styled(doc, f'[图片缺失: {src}]')
            i += 1
            continue

        # -------- 列表 --------
        list_m = re.match(r'^(\s*)([-*+])\s+(.*)', line)
        num_m = re.match(r'^(\s*)(\d+)\.\s+(.*)', line)
        if list_m or num_m:
            indent = len(list_m.group(1)) if list_m else len(num_m.group(1))
            text = (list_m.group(3) if list_m else num_m.group(3)).strip()
            bullet_char = '●' if list_m else f"{num_m.group(2)}."
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = Cm(0.74 + indent * 0.5)
            pf.first_line_indent = Cm(-0.5)
            pf.space_after = Pt(2)
            pf.line_spacing = 1.4
            run = p.add_run(f"{bullet_char}  {text}")
            set_run_font(run, '宋体', 'Times New Roman', Pt(12))
            i += 1
            continue

        # -------- 引用 --------
        if line.strip().startswith('>'):
            text = line.strip().lstrip('>').strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf = p.paragraph_format
            pf.left_indent = Cm(1.0)
            pf.right_indent = Cm(1.0)
            pf.space_after = Pt(4)
            run = p.add_run(text)
            set_run_font(run, '宋体', 'Times New Roman', Pt(10.5),
                         color=(0x55, 0x55, 0x55))
            i += 1
            continue

        # -------- 空行 --------
        if not line.strip():
            i += 1
            continue

        # -------- 普通段落（解析 inline **粗体**、`代码`、[引用角标]） --------
        parts = re.split(r'(\*\*[^*]+\*\*)', line)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0.74)
        pf.line_spacing = 1.5
        pf.space_after = Pt(6)

        # 参考文献条目行：以 [数字] 开头 → 不做上标
        is_ref_entry = bool(re.match(r'^\[\d+\]', line.strip()))

        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                t = part[2:-2]
                # 粗体内部也可能有引用角标
                _write_inline_with_citations(p, t, bold=True,
                                              in_ref_section=in_reference_section,
                                              is_ref_entry=is_ref_entry)
            else:
                # 处理行内代码 `...`
                code_parts = re.split(r'(`[^`]+`)', part)
                for cp in code_parts:
                    if cp.startswith('`') and cp.endswith('`'):
                        run = p.add_run(cp[1:-1])
                        run.font.name = 'Consolas'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')
                        run.font.size = Pt(10)
                        run.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
                    elif cp:
                        _write_inline_with_citations(p, cp, bold=False,
                                                      in_ref_section=in_reference_section,
                                                      is_ref_entry=is_ref_entry)
        i += 1

    # flush 末尾残留
    if in_code:
        add_code_block(doc, '\n'.join(code_buf))
    if in_table:
        add_table_styled(doc, table_buf)


def setup_document(doc):
    # 默认正文字体
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.font.size = Pt(12)

    # 页边距
    section = doc.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

    # 页眉
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = hp.add_run('基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现')
    set_run_font(run, '宋体', 'Times New Roman', Pt(9),
                 color=(0x80, 0x80, 0x80))

    # 页脚（页码 PAGE 域）
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_prefix = fp.add_run('— ')
    set_run_font(run_prefix, '宋体', 'Times New Roman', Pt(9))
    _add_field(fp, 'PAGE', placeholder='1', font_size=Pt(9))
    run_suffix = fp.add_run(' —')
    set_run_font(run_suffix, '宋体', 'Times New Roman', Pt(9))


def main():
    md_text = THESIS_MD.read_text(encoding='utf-8')

    doc = Document()
    setup_document(doc)

    # 封面页
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(120)
    run = p_title.add_run('基于多源医学知识融合与混合检索的\n医疗智能问答系统设计与实现')
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x2B, 0x4B)

    doc.add_paragraph()
    doc.add_paragraph()

    for line in ['毕   业   设   计', '（论文）']:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line)
        set_run_font(run, '黑体', 'Times New Roman', Pt(18))

    doc.add_paragraph()
    doc.add_paragraph()

    info_lines = [
        '学    院：__________',
        '专    业：__________',
        '学生姓名：__________',
        '指导教师：__________',
        '完成日期：2026 年 11 月',
    ]
    for l in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(l)
        set_run_font(run, '宋体', 'Times New Roman', Pt(14))

    doc.add_page_break()

    # 目录
    add_toc_field(doc)

    # 正文（从摘要开始，跳过封面那段标题）
    # Markdown 第一行是 H1 论文标题，已经由封面呈现，所以渲染正文时跳过它
    lines = md_text.split('\n')
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith('# 基于多源医学知识融合'):
            body_start = i + 1
            break
    body_text = '\n'.join(lines[body_start:])

    # 在渲染正文前，把 Markdown 里的占位图引用替换为真实图片路径
    # （当前 Markdown 里可能还没引用图，这里做防御性处理）
    render_markdown(body_text, doc)

    doc.save(str(THESIS_DOCX))
    print(f'Word 版已生成：{THESIS_DOCX}')


if __name__ == '__main__':
    main()
