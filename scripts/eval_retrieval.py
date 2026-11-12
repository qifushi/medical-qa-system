# -*- coding: utf-8 -*-
r"""医疗知识库检索评估脚本。

评估集由 scripts/build_eval_dataset.py 生成，包含两个子集：
    verbatim   : 直接使用知识库 question 字段（子串检索的强项场景）
    paraphrase : 本地 LLM 改写后的问句（检验语义泛化）

比较四种检索方式：
    substring  : 现有实现（query 子串匹配全部字段）
    lexical    : TF-IDF 稀疏词法检索
    semantic   : TF-IDF + SVD(LSA) 语义向量检索
    hybrid     : 三通道加权融合（本文方法）

指标：Recall@1/5/10、MRR@10、nDCG@10、平均延迟。

用法：
    .\.venv\Scripts\python.exe scripts\eval_retrieval.py
"""

import argparse
import json
import math
import os
import random
import sys
import time
from typing import Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from apps.common.knowledge.hybrid_retriever import HybridRetriever  # noqa: E402
from apps.common.knowledge.knowledge_base import KnowledgeBase  # noqa: E402

KB_NAMES = ("report_analysis", "medicine_analysis", "medical_service")
METHODS = ("substring", "lexical", "semantic", "hybrid")
DATASET_PATH = os.path.join(ROOT, "论文", "实验数据", "eval_dataset.json")
OUT_PATH = os.path.join(ROOT, "论文", "实验数据", "retrieval_eval.json")


def build_verbatim(kb: KnowledgeBase, kb_name: str, n: int, seed: int) -> List[Dict]:
    rng = random.Random(seed)
    candidates = []
    for doc_id, entity in kb.entities.items():
        question = str(entity.get("question") or "").strip()
        name = str(entity.get("entity_name") or "").strip()
        if len(question) < 8 or len(question) > 120 or len(name) < 4:
            continue
        candidates.append((doc_id, question, name))
    rng.shuffle(candidates)
    return [
        {"kb": kb_name, "gold_id": doc_id, "query": question, "gold_name": name}
        for doc_id, question, name in candidates[:n]
    ]


def load_dataset(n_verbatim: int, seed: int) -> Dict[str, List[Dict]]:
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    print("未找到评估集，临时按 verbatim 规则构造")
    dataset = {"verbatim": [], "paraphrase": []}
    for kb_name in KB_NAMES:
        kb = KnowledgeBase(kb_name)
        dataset["verbatim"].extend(build_verbatim(kb, kb_name, n_verbatim, seed))
        del kb
    return dataset


def metrics(ranks: List[int]) -> Dict[str, float]:
    total = len(ranks)
    if total == 0:
        return {}
    result = {
        "recall@1": sum(1 for r in ranks if r == 1) / total,
        "recall@5": sum(1 for r in ranks if 1 <= r <= 5) / total,
        "recall@10": sum(1 for r in ranks if 1 <= r <= 10) / total,
        "mrr@10": sum(1.0 / r for r in ranks if 1 <= r <= 10) / total,
        "ndcg@10": sum(1.0 / math.log2(r + 1) for r in ranks if 1 <= r <= 10) / total,
        "miss": sum(1 for r in ranks if r <= 0) / total,
    }
    return {key: round(value, 4) for key, value in result.items()}


def rank_of(ids: List[str], gold_id: str) -> int:
    for pos, doc_id in enumerate(ids, start=1):
        if doc_id == gold_id:
            return pos
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-verbatim", type=int, default=40)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--topk", type=int, default=10)
    args = parser.parse_args()

    dataset = load_dataset(args.n_verbatim, args.seed)
    print(
        f"评估集：verbatim={len(dataset.get('verbatim', []))}, "
        f"paraphrase={len(dataset.get('paraphrase', []))}"
    )

    set_names = [name for name in ("verbatim", "paraphrase") if dataset.get(name)]
    ranks: Dict[str, Dict[str, List[int]]] = {
        name: {method: [] for method in METHODS} for name in set_names
    }
    latency: Dict[str, Dict[str, List[float]]] = {
        name: {method: [] for method in METHODS} for name in set_names
    }
    per_kb: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {
        name: {} for name in set_names
    }
    examples: List[Dict] = []

    for kb_name in KB_NAMES:
        print(f"\n===== 评估知识库 {kb_name} =====")
        kb = KnowledgeBase(kb_name)
        retriever = HybridRetriever(kb_name, kb.entities)

        for set_name in set_names:
            items = [item for item in dataset[set_name] if item.get("kb") == kb_name]
            if not items:
                continue
            kb_ranks = {method: [] for method in METHODS}
            kb_latency = {method: [] for method in METHODS}

            for item in items:
                query = item["query"]
                gold_id = item["gold_id"]

                start = time.perf_counter()
                baseline = kb.query(query, n_results=args.topk)
                kb_latency["substring"].append(time.perf_counter() - start)
                kb_ranks["substring"].append(
                    rank_of([row["id"] for row in baseline], gold_id)
                )

                for mode in ("lexical", "semantic", "hybrid"):
                    start = time.perf_counter()
                    results = retriever.search(query, top_k=args.topk, mode=mode)
                    kb_latency[mode].append(time.perf_counter() - start)
                    kb_ranks[mode].append(rank_of([row["id"] for row in results], gold_id))

                if (
                    len(examples) < 10
                    and kb_ranks["substring"][-1] <= 0
                    and 1 <= kb_ranks["hybrid"][-1] <= 5
                ):
                    examples.append(
                        {
                            "set": set_name,
                            "kb": kb_name,
                            "query": query,
                            "gold": item.get("gold_name", ""),
                            "substring_rank": kb_ranks["substring"][-1],
                            "hybrid_rank": kb_ranks["hybrid"][-1],
                            "hybrid_top3": [
                                row["metadata"].get("entity_name", "")
                                for row in retriever.search(query, top_k=3)
                            ],
                        }
                    )

            per_kb[set_name][kb_name] = {}
            for method in METHODS:
                per_kb[set_name][kb_name][method] = metrics(kb_ranks[method])
                per_kb[set_name][kb_name][method]["latency_ms"] = round(
                    sum(kb_latency[method]) / max(1, len(kb_latency[method])) * 1000, 1
                )
                ranks[set_name][method].extend(kb_ranks[method])
                latency[set_name][method].extend(kb_latency[method])

        del retriever
        del kb

    report: Dict[str, object] = {
        "config": {
            "seed": args.seed,
            "topk": args.topk,
            "kb_names": list(KB_NAMES),
        },
        "sets": {},
        "examples": examples,
    }

    for set_name in set_names:
        overall = {}
        for method in METHODS:
            overall[method] = metrics(ranks[set_name][method])
            overall[method]["latency_ms"] = round(
                sum(latency[set_name][method]) / max(1, len(latency[set_name][method]) * 1.0)
                * 1000,
                1,
            )
        report["sets"][set_name] = {
            "size": len(ranks[set_name]["substring"]),
            "overall": overall,
            "per_kb": per_kb[set_name],
        }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    for set_name in set_names:
        print(f"\n===== 汇总：{set_name}（{report['sets'][set_name]['size']} 条） =====")
        print(
            f"{'method':<10}{'R@1':>8}{'R@5':>8}{'R@10':>8}"
            f"{'MRR@10':>8}{'nDCG@10':>9}{'ms':>8}"
        )
        for method in METHODS:
            m = report["sets"][set_name]["overall"][method]
            print(
                f"{method:<10}{m['recall@1']:>8.4f}{m['recall@5']:>8.4f}"
                f"{m['recall@10']:>8.4f}{m['mrr@10']:>8.4f}{m['ndcg@10']:>9.4f}"
                f"{m['latency_ms']:>8.1f}"
            )

    print(f"\n结果已写入：{OUT_PATH}")


if __name__ == "__main__":
    main()
