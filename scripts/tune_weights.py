# -*- coding: utf-8 -*-
r"""融合权重调参脚本（一次性实验工具）。

在 verbatim / paraphrase 两套评估集上比较不同通道权重组合的检索效果，
用于确定 HybridRetriever 的默认权重。

用法：
    .\.venv\Scripts\python.exe scripts/tune_weights.py
"""

import json
import os
import sys
from typing import Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from apps.common.knowledge.hybrid_retriever import HybridRetriever  # noqa: E402
from apps.common.knowledge.knowledge_base import KnowledgeBase  # noqa: E402

KB_NAMES = ("report_analysis", "medicine_analysis", "medical_service")
DATASET_PATH = os.path.join(ROOT, "论文", "实验数据", "eval_dataset.json")

CONFIGS = {
    "A 0.45/0.35/0.20": {"lexical": 0.45, "semantic": 0.35, "coverage": 0.20},
    "B 0.60/0.10/0.30": {"lexical": 0.60, "semantic": 0.10, "coverage": 0.30},
    "C 0.65/0.05/0.30": {"lexical": 0.65, "semantic": 0.05, "coverage": 0.30},
    "D 0.70/0.00/0.30": {"lexical": 0.70, "semantic": 0.00, "coverage": 0.30},
    "E 0.55/0.15/0.30": {"lexical": 0.55, "semantic": 0.15, "coverage": 0.30},
    "F 0.50/0.25/0.25": {"lexical": 0.50, "semantic": 0.25, "coverage": 0.25},
}


def rank_of(ids: List[str], gold_id: str) -> int:
    for pos, doc_id in enumerate(ids, start=1):
        if doc_id == gold_id:
            return pos
    return 0


def summarize(ranks: List[int]) -> str:
    total = max(1, len(ranks))
    r1 = sum(1 for r in ranks if r == 1) / total
    r5 = sum(1 for r in ranks if 1 <= r <= 5) / total
    r10 = sum(1 for r in ranks if 1 <= r <= 10) / total
    mrr = sum(1.0 / r for r in ranks if 1 <= r <= 10) / total
    import math
    ndcg = sum(1.0 / math.log2(r + 1) for r in ranks if 1 <= r <= 10) / total
    return f"R@1={r1:.4f} R@5={r5:.4f} R@10={r10:.4f} MRR={mrr:.4f} nDCG={ndcg:.4f}"


def main() -> None:
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    ranks = {
        set_name: {name: [] for name in CONFIGS}
        for set_name in ("verbatim", "paraphrase")
    }

    for kb_name in KB_NAMES:
        print(f"加载 {kb_name} ...")
        kb = KnowledgeBase(kb_name)
        retriever = HybridRetriever(kb_name, kb.entities)
        for set_name in ("verbatim", "paraphrase"):
            items = [i for i in dataset[set_name] if i.get("kb") == kb_name]
            for item in items:
                for name, weights in CONFIGS.items():
                    results = retriever.search(
                        item["query"], top_k=10, mode="hybrid", weights=weights
                    )
                    ranks[set_name][name].append(
                        rank_of([r["id"] for r in results], item["gold_id"])
                    )
        del retriever
        del kb

    for set_name in ("verbatim", "paraphrase"):
        print(f"\n===== {set_name} =====")
        for name in CONFIGS:
            print(f"{name}: {summarize(ranks[set_name][name])}")


if __name__ == "__main__":
    main()
