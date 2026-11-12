# -*- coding: utf-8 -*-
r"""构造检索评估集：原始问句 + LLM 改写问句。

- verbatim：直接使用知识库实体的 question 字段（与现有子串检索同源，作为强基线）；
- paraphrase：调用本地 Ollama 对问句进行改写，避免与知识库原文逐字重合，
  用于检验检索方法在「自然语言改写」下的泛化能力。

结果写入 论文/实验数据/eval_dataset.json，支持中断续跑。

用法：
    .\.venv\Scripts\python.exe scripts\build_eval_dataset.py --n-verbatim 40 --n-paraphrase 20
"""

import argparse
import json
import os
import random
import re
import sys
import time
from typing import Dict, List

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from apps.common.knowledge.knowledge_base import KnowledgeBase  # noqa: E402

KB_NAMES = ("report_analysis", "medicine_analysis", "medical_service")
OUT_PATH = os.path.join(ROOT, "论文", "实验数据", "eval_dataset.json")

OLLAMA_URL = os.getenv("OLLAMA_CHAT_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.getenv("LMSTUDIO_MODEL", "qwen2.5vl:3b")

PROMPT_TEMPLATE = """请把下面这位患者的提问改写成一句新的中文口语化问题。
要求：
1. 保留核心症状、部位、检查指标或药物名称；
2. 不要照抄原句，不要直接出现原标题中的完整疾病名称；
3. 只输出改写后的问题，不要解释，不要加引号。

原问题：{question}
改写："""


def sample_entities(kb: KnowledgeBase, n: int, seed: int) -> List[Dict]:
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
        {"kb": kb_name_of(kb), "gold_id": doc_id, "query": question, "gold_name": name}
        for doc_id, question, name in candidates[:n]
    ]


def kb_name_of(kb: KnowledgeBase) -> str:
    return kb.db_name


def clean_rewrite(text: str) -> str:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    if not lines:
        return ""
    result = lines[0]
    result = re.sub(r"^(改写后?|改写结果|问题|输出)\s*[:：]\s*", "", result).strip()
    result = result.strip("“”\"'` ")
    return result


def rewrite(question: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": PROMPT_TEMPLATE.format(question=question)}],
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 128},
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return clean_rewrite(response.json()["message"]["content"])


def build_paraphrase(items: List[Dict], target: int) -> List[Dict]:
    """对 verbatim 样本做改写，过滤泄露完整实体名/长度异常的结果。"""
    results: List[Dict] = []
    for item in items:
        if len(results) >= target:
            break
        question = item["query"]
        gold_name = item["gold_name"]
        rewritten = ""
        for attempt in range(2):
            try:
                rewritten = rewrite(question)
                print(f"  [{item['kb']}] {question[:30]} -> {rewritten[:40]}")
            except Exception as exc:
                print(f"  改写失败：{exc}")
                break
            if not rewritten:
                continue
            if gold_name and gold_name in rewritten:
                print("  !! 改写结果包含完整实体名，重试")
                continue
            if len(rewritten) < 6 or len(rewritten) > 160:
                print("  !! 改写长度异常，重试")
                continue
            break
        if not rewritten or (gold_name and gold_name in rewritten):
            continue
        results.append(
            {
                "kb": item["kb"],
                "gold_id": item["gold_id"],
                "query": rewritten,
                "gold_name": gold_name,
                "source_query": question,
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-verbatim", type=int, default=40)
    parser.add_argument("--n-paraphrase", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    dataset = {"meta": vars(args), "verbatim": [], "paraphrase": []}

    for kb_name in KB_NAMES:
        print(f"\n===== 构造 {kb_name} 评估集 =====")
        kb = KnowledgeBase(kb_name)
        verbatim = sample_entities(kb, args.n_verbatim, args.seed)
        dataset["verbatim"].extend(verbatim)
        print(f"verbatim 样本：{len(verbatim)}")

        print(f"开始改写 {kb_name} 问句（目标 {args.n_paraphrase} 条）...")
        start = time.time()
        paraphrases = build_paraphrase(verbatim, args.n_paraphrase)
        dataset["paraphrase"].extend(paraphrases)
        print(
            f"paraphrase 样本：{len(paraphrases)}，耗时 {time.time() - start:.1f}s"
        )
        del kb

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"\n评估集已写入：{OUT_PATH}")
    print(f"verbatim={len(dataset['verbatim'])}, paraphrase={len(dataset['paraphrase'])}")


if __name__ == "__main__":
    main()
