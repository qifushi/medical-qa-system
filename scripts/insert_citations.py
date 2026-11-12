# -*- coding: utf-8 -*-
r"""在论文 Markdown 正文里自动插入参考文献引用角标 [数字]。

策略：
  1) 基于"参考文献编号 → 关键词"映射表扫描正文
  2) 按出现顺序给每个关键词后面追加 [编号]（避免重复追加）
  3) 跳过标题行、代码块、表格行、图片行、参考文献区本身

用法：
    .\.venv\Scripts\python.exe scripts/insert_citations.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / '论文' / '基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.md'
BACKUP = MD_PATH.with_suffix('.md.bak')

# ======================================================
# 参考文献编号 → 触发关键词（小写匹配 + 精确匹配）
# 每个元组：(编号, 关键词列表)
# 注：关键词要覆盖中文变体、英文原名和缩写
# ======================================================
CITATION_MAP = [
    (1,  ['检索增强生成', 'Retrieval-Augmented Generation', ' RAG ', '（RAG）', '(RAG)']),
    (2,  ['BM25', 'Robertson']),
    (3,  ['潜在语义分析', 'Latent Semantic Analysis', ' LSA ', '（LSA）', '(LSA)',
          'TruncatedSVD', '奇异值分解']),
    (4,  ['倒数排名融合', 'Reciprocal Rank Fusion', ' RRF ', '（RRF）', '(RRF)', 'Cormack']),
    (5,  ['稠密段落检索', 'Dense Passage Retrieval', ' DPR ']),
    (6,  ['中文医学知识图谱', ' CMeKG ']),
    (7,  [' BERT ', '预训练语言模型']),
    (8,  ['Med-PaLM', 'Singhal']),
    (9,  [' Qwen ', '通义']),
    (10, [' OCR ', '光学字符识别', 'PP-OCR']),
    (11, ['Gao Y', 'RAG 的综述']),
    (12, ['nDCG', 'Cumulated Gain', 'Järvelin', 'Kekäläinen']),
    (13, ['Information Retrieval', 'Manning']),
    (14, ['cMedQA', '中文医疗问答匹配']),
    (15, ['Zhao W X', '大语言模型综述']),
    (16, ['RLHF', '人类反馈强化学习', 'InstructGPT', 'Ouyang']),
    (17, ['scikit-learn', 'sklearn']),
    (18, ['Django']),
    (19, ['Vue.js', 'Vue 3']),
    (20, ['Ollama']),
]

# 跳过的标题行模式（这些行内即使有匹配词也不加引用）
SKIP_TITLE_PATTERNS = [
    r'^#',                    # 所有 Markdown 标题
    r'^---+\s*$',            # 分割线
    r'^\|',                   # 表格行
    r'^!\[',                  # 图片行
    r'^> ',                   # 引用块
    r'^```',                  # 代码块边界
]


def is_skippable(line: str) -> bool:
    """判断该行是否应跳过（标题/表格/代码等）"""
    if not line.strip():
        return True
    for pat in SKIP_TITLE_PATTERNS:
        if re.search(pat, line):
            return True
    return False


def insert_citations_in_line(line: str, existing_refs: set) -> tuple[str, set]:
    """在一行内按关键词顺序插入 [编号]，返回 (新行, 新增的ref集合)。"""
    new_line = line
    added = set()

    # 先收集这一行里所有关键词匹配的 (位置, 编号)
    matches = []
    for ref_num, keywords in CITATION_MAP:
        if ref_num in existing_refs and ref_num not in added:
            # 已加过的编号不在同一行重复加（除非是不同句子）
            # 简化策略：同一编号在一行里最多出现一次
            pass
        for kw in keywords:
            for m in re.finditer(re.escape(kw), new_line):
                pos = m.end()
                matches.append((pos, ref_num, kw))

    # 按位置从前到后排序，避免后插的偏移影响前插的位置
    matches.sort(key=lambda x: x[0])

    # 去重同一位置（取最大编号？不，我们要所有命中的编号）
    # 简化：每个编号一行只加一次，选最早出现的位置
    seen_refs_this_line = set()
    final_inserts = {}  # pos -> list of ref_nums
    for pos, ref_num, kw in matches:
        if ref_num in seen_refs_this_line:
            continue
        seen_refs_this_line.add(ref_num)
        if pos not in final_inserts:
            final_inserts[pos] = []
        final_inserts[pos].append(ref_num)

    # 从后往前插入，前面的位置不会受影响
    for pos in sorted(final_inserts.keys(), reverse=True):
        ref_nums = sorted(final_inserts[pos])
        # 检查插入位置后面是否已经紧跟 [数字]
        after = new_line[pos:pos+3]
        if re.match(r'^\[\d+\]', after):
            continue  # 已有引用了
        tag = '[' + ','.join(str(n) for n in ref_nums) + ']'
        new_line = new_line[:pos] + tag + new_line[pos:]
        for n in ref_nums:
            added.add(n)

    return new_line, added


def process_markdown(md_text: str) -> str:
    lines = md_text.split('\n')
    out = []
    in_code_block = False
    in_reference_section = False
    existing_refs = set()  # 已经出现过的引用编号

    for i, line in enumerate(lines):
        # 代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            out.append(line)
            continue
        if in_code_block:
            out.append(line)
            continue

        # 参考文献区起点
        if line.strip() == '## 参考文献':
            in_reference_section = True
            out.append(line)
            continue
        if in_reference_section:
            out.append(line)
            continue

        # 跳过标题、表格等
        if is_skippable(line):
            out.append(line)
            continue

        # 普通正文段落 → 插入引用
        new_line, added = insert_citations_in_line(line, existing_refs)
        existing_refs.update(added)
        out.append(new_line)

    print(f'共插入 {len(existing_refs)} 个不同的引用编号: '
          f'[{",".join(str(n) for n in sorted(existing_refs))}]')
    return '\n'.join(out)


def main():
    original = MD_PATH.read_text(encoding='utf-8')

    # 备份
    if not BACKUP.exists():
        BACKUP.write_text(original, encoding='utf-8')
        print(f'备份 → {BACKUP}')

    modified = process_markdown(original)

    # 写回
    MD_PATH.write_text(modified, encoding='utf-8')
    print(f'已写回 → {MD_PATH}')

    # 简单统计：正文里现在有多少 [数字]
    body_section = modified.split('## 参考文献')[0]
    refs_found = re.findall(r'\[(\d+(?:,\d+)*)\]', body_section)
    total = 0
    for r in refs_found:
        nums = r.split(',')
        total += len(nums)
    print(f'正文引用角标总数: {total} (分布在 {len(refs_found)} 处)')


if __name__ == '__main__':
    main()
