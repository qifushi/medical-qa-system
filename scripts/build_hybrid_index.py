# -*- coding: utf-8 -*-
r"""构建三个医疗知识库的混合检索索引。

用法：
    .\.venv\Scripts\python.exe scripts\build_hybrid_index.py [--rebuild]

索引缓存在 data/index_cache/ 下，按「版本 + 知识库名 + 文档数」命名。
"""

import argparse
import gc
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from apps.common.knowledge.hybrid_retriever import HybridRetriever  # noqa: E402
from apps.common.knowledge.knowledge_base import KnowledgeBase  # noqa: E402

KB_NAMES = ("report_analysis", "medicine_analysis", "medical_service")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="强制重建索引")
    args = parser.parse_args()

    for kb_name in KB_NAMES:
        print(f"\n===== {kb_name} =====")
        kb = KnowledgeBase(kb_name)
        retriever = HybridRetriever(
            kb_name, kb.entities, force_rebuild=args.rebuild
        )
        print(
            f"{kb_name}: 文档 {len(retriever.doc_ids)}，"
            f"索引缓存 {retriever.cache_path}"
        )
        del retriever
        del kb
        gc.collect()

    print("\n全部索引构建完成。")


if __name__ == "__main__":
    main()
