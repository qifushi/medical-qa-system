# -*- coding: utf-8 -*-
"""医疗知识库混合检索器。

三个检索通道：
1. 稀疏词法通道：TF-IDF（jieba 分词 + 1~2 gram）余弦相似度，承担精确术语匹配；
2. 语义向量通道：TF-IDF 矩阵经 TruncatedSVD 降维得到稠密语义向量（LSA），承担同义/改写召回；
3. 实体覆盖通道：查询词与候选实体名称、科室、检查/用药/治疗标签的覆盖率，承担实体级重排。

三通道在候选集内做归一化后加权融合，输出统一的知识库结果格式。
索引按知识库缓存到 data/index_cache，避免每次启动重复训练。
"""

import os
import re
import pickle
import time
from typing import Any, Dict, List, Optional

import jieba
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

jieba.setLogLevel(20)

_INDEX_VERSION = 4
_DEFAULT_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../../../data/index_cache"
)
_TOKEN_CLEAN = re.compile(r"[^\u4e00-\u9fffA-Za-z0-9]+")

# 高频虚词/泛化词，避免把 "怎么办"、"请问" 之类的词当成检索信号
_STOPWORDS = {
    "的", "了", "是", "在", "有", "和", "与", "及", "或", "而", "也", "就", "都",
    "我", "你", "他", "她", "它", "我们", "你们", "他们", "自己",
    "这", "那", "这个", "那个", "这些", "那些", "什么", "怎么", "怎样", "如何",
    "请问", "为什么", "哪些", "哪个", "是否", "能否", "可以", "可能", "需要",
    "患者", "病人", "情况", "问题", "时候", "如果", "因为", "所以", "但是",
    "已经", "还是", "还有", "以及", "一个", "一些", "没有", "不是", "就是",
    "吗", "呢", "啊", "吧", "呀", "哦", "其", "之", "于", "并", "等", "被", "把",
}

# 参与实体覆盖计算的字段
_TAG_FIELDS = ("check", "recommand_drug", "cure_way", "symptom", "food", "drug")

# ---------------------------------------------------------------- 文本构建


def flatten_entity(entity: Dict[str, Any]) -> Dict[str, Any]:
    """把 properties 下的字段展开到顶层，顶层已有字段优先。

    疾病百科 / 药品条目的详细字段都嵌在 properties 下，问答类条目本身就是
    扁平结构，该函数对它们原样返回。
    """
    detail = entity.get("properties")
    if not isinstance(detail, dict) or not detail:
        return entity
    merged = {key: value for key, value in detail.items() if key not in entity}
    merged.update(entity)
    return merged


def tokenize(text: str) -> List[str]:
    """jieba 搜索模式分词，过滤标点与停用词。"""
    text = (text or "").lower()
    tokens: List[str] = []
    for token in jieba.lcut_for_search(text):
        token = token.strip()
        if not token or _TOKEN_CLEAN.fullmatch(token):
            continue
        if token in _STOPWORDS:
            continue
        tokens.append(token)
    return tokens


def _join_values(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str) and value:
        return [value]
    return []


def build_document(entity: Dict[str, Any], answer_chars: int = 120) -> str:
    """把一条知识库实体拼接成用于检索的短文本。

    索引包含实体名称、问题描述、科室与结构化标签；答案只取前 120 字，
    避免长答案稀释词频。

    这里刻意不展开 properties：疾病百科条目的详情（desc、用法用量、发病率）
    体量远大于病名，一旦并入索引会把病名权重稀释掉，导致"肩-手综合征"这类
    完整病名输给泛化词重合的问答条目。详情由 cmekg_client 在拼提示词时补上。
    """
    parts: List[str] = []
    name = entity.get("entity_name") or entity.get("name") or ""
    if name:
        parts.append(str(name))
    question = entity.get("question")
    if isinstance(question, str) and question:
        parts.append(question[:160])
    department = entity.get("department")
    if isinstance(department, str) and department:
        parts.append(department)
    for field in _TAG_FIELDS:
        parts.extend(_join_values(entity.get(field)))
    answer = entity.get("answer")
    if isinstance(answer, str) and answer:
        parts.append(answer[:answer_chars])
    return " ".join(parts)


def _minmax(values: np.ndarray) -> np.ndarray:
    if values.size == 0:
        return values
    low = float(values.min())
    high = float(values.max())
    if high - low < 1e-9:
        return np.zeros_like(values, dtype=np.float32)
    return ((values - low) / (high - low)).astype(np.float32)


def _top_indices(scores: np.ndarray, k: int) -> np.ndarray:
    if scores.size == 0 or float(scores.max()) <= 0:
        return np.array([], dtype=np.int64)
    k = min(k, scores.size - 1)
    indices = np.argpartition(-scores, k)[:k]
    indices = indices[scores[indices] > 0]
    return indices.astype(np.int64)


class HybridRetriever:
    """单个知识库的混合检索索引。"""

    def __init__(
        self,
        kb_name: str,
        entities: Dict[str, Dict[str, Any]],
        cache_dir: Optional[str] = None,
        n_components: int = 96,
        max_features: int = 50000,
        force_rebuild: bool = False,
    ):
        self.kb_name = kb_name
        self.entities = entities
        self.doc_ids: List[str] = list(entities.keys())
        self.doc_texts: List[str] = [
            build_document(entities[doc_id]) for doc_id in self.doc_ids
        ]
        self.cache_dir = cache_dir or _DEFAULT_CACHE_DIR
        self.n_components = n_components
        self.max_features = max_features

        self.vectorizer: Optional[TfidfVectorizer] = None
        self.matrix = None
        self.svd: Optional[TruncatedSVD] = None
        self.lsa = None

        self._load_or_build(force_rebuild)

    # ---------------------------------------------------------------- 索引
    @property
    def cache_path(self) -> str:
        return os.path.join(
            self.cache_dir,
            f"hybrid_v{_INDEX_VERSION}_{self.kb_name}_{len(self.doc_ids)}.pkl",
        )

    def _load_or_build(self, force_rebuild: bool) -> None:
        os.makedirs(self.cache_dir, exist_ok=True)
        if not force_rebuild and os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "rb") as f:
                    payload = pickle.load(f)
                if (
                    payload.get("version") == _INDEX_VERSION
                    and len(payload.get("doc_ids", [])) == len(self.doc_ids)
                ):
                    self.doc_ids = payload["doc_ids"]
                    self.vectorizer = payload["vectorizer"]
                    self.matrix = payload["matrix"]
                    self.svd = payload["svd"]
                    self.lsa = payload["lsa"]
                    print(
                        f"[hybrid] 载入索引 {self.kb_name}: "
                        f"{len(self.doc_ids)} 条实体, 词表 {len(self.vectorizer.vocabulary_)}"
                    )
                    return
            except Exception as exc:  # 缓存损坏则重建
                print(f"[hybrid] 索引缓存不可用({exc})，重新构建 {self.kb_name}")
        self.build()

    def build(self) -> None:
        start = time.time()
        print(f"[hybrid] 开始构建索引 {self.kb_name}，文档数 {len(self.doc_texts)}")
        vectorizer = TfidfVectorizer(
            tokenizer=tokenize,
            token_pattern=None,
            lowercase=False,
            ngram_range=(1, 2),
            min_df=2,
            max_features=self.max_features,
            sublinear_tf=True,
            dtype=np.float32,
        )
        matrix = vectorizer.fit_transform(self.doc_texts).tocsr()

        n_components = min(self.n_components, max(2, matrix.shape[1] - 1))
        svd = TruncatedSVD(n_components=n_components, random_state=42, n_iter=5)
        lsa = svd.fit_transform(matrix).astype(np.float32)
        norms = np.linalg.norm(lsa, axis=1, keepdims=True) + 1e-9
        lsa = lsa / norms

        self.vectorizer = vectorizer
        self.matrix = matrix
        self.svd = svd
        self.lsa = lsa

        payload = {
            "version": _INDEX_VERSION,
            "kb_name": self.kb_name,
            "doc_ids": self.doc_ids,
            "vectorizer": vectorizer,
            "matrix": matrix,
            "svd": svd,
            "lsa": lsa,
        }
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(payload, f, protocol=4)
        except Exception as exc:
            print(f"[hybrid] 索引缓存写入失败：{exc}")
        print(
            f"[hybrid] 索引构建完成 {self.kb_name}: 文档 {matrix.shape[0]}, "
            f"词表 {matrix.shape[1]}, 非零项 {matrix.nnz}, "
            f"耗时 {time.time() - start:.1f}s"
        )

    # ---------------------------------------------------------------- 检索
    def _channel_scores(self, query: str, q_tokens: List[str]):
        joined = " ".join(q_tokens)
        q_vec = self.vectorizer.transform([joined])

        lexical = np.asarray((self.matrix @ q_vec.T).todense()).ravel().astype(np.float32)

        q_lsa = self.svd.transform(q_vec).astype(np.float32)
        norm = float(np.linalg.norm(q_lsa))
        if norm > 0:
            q_lsa = q_lsa / norm
        semantic = (self.lsa @ q_lsa.ravel()).astype(np.float32)
        return lexical, semantic

    def _coverage_and_bonus(self, query: str, q_tokens: List[str], indices: np.ndarray):
        q_set = set(q_tokens)
        coverage = np.zeros(len(indices), dtype=np.float32)
        bonus = np.zeros(len(indices), dtype=np.float32)
        for pos, idx in enumerate(indices):
            doc_id = self.doc_ids[idx]
            entity = self.entities[doc_id]
            name = str(entity.get("entity_name") or entity.get("name") or "")
            doc_tokens = set(tokenize(self.doc_texts[idx]))
            if q_set:
                coverage[pos] = len(q_set & doc_tokens) / float(len(q_set))
            name_tokens = set(tokenize(name))
            if name and (name in query or query in name):
                bonus[pos] = 1.0
            elif name_tokens and q_set:
                bonus[pos] = len(name_tokens & q_set) / float(len(name_tokens))
        return coverage, bonus

    def search(
        self,
        query: str,
        top_k: int = 5,
        recall_k: int = 60,
        mode: str = "hybrid",
        weights: Optional[Dict[str, float]] = None,
    ) -> List[Dict[str, Any]]:
        """检索入口。

        mode: hybrid / lexical / semantic
        返回格式与 KnowledgeBase.query 兼容（id/document/metadata/distance），
        并额外附带 score 字段用于解释排序。
        """
        query = (query or "").strip()
        if not query or not self.doc_ids:
            return []
        q_tokens = tokenize(query)
        if not q_tokens:
            return []

        lexical, semantic = self._channel_scores(query, q_tokens)

        if mode == "lexical":
            candidates = _top_indices(lexical, recall_k)
        elif mode == "semantic":
            candidates = _top_indices(semantic, recall_k)
        else:
            candidates = np.union1d(
                _top_indices(lexical, recall_k), _top_indices(semantic, recall_k)
            )
        if candidates.size == 0:
            return []

        coverage, name_bonus = self._coverage_and_bonus(query, q_tokens, candidates)
        lexical_n = _minmax(lexical[candidates])
        semantic_n = _minmax(semantic[candidates])

        if mode == "lexical":
            fused = lexical_n
        elif mode == "semantic":
            fused = semantic_n
        else:
            w = {"lexical": 0.60, "semantic": 0.10, "coverage": 0.30}
            if weights:
                w.update(weights)
            fused = (
                w["lexical"] * lexical_n
                + w["semantic"] * semantic_n
                + w["coverage"] * coverage
            )
            fused = np.minimum(fused + 0.10 * name_bonus, 1.5)

        order = np.argsort(-fused)[:top_k]
        results: List[Dict[str, Any]] = []
        for pos in order:
            idx = int(candidates[pos])
            doc_id = self.doc_ids[idx]
            entity = self.entities[doc_id]
            results.append(
                {
                    "id": doc_id,
                    "document": f"{entity.get('entity_type', '')}: "
                    f"{entity.get('entity_name', '')}",
                    "metadata": entity,
                    "distance": float(1.0 - min(fused[pos], 1.0)),
                    "score": float(fused[pos]),
                }
            )
        return results


_retrievers: Dict[str, HybridRetriever] = {}


def get_hybrid_retriever(
    kb_name: str, kb, cache_dir: Optional[str] = None, force_rebuild: bool = False
) -> HybridRetriever:
    """按知识库名称缓存检索器实例。kb 需提供 .entities 字典。"""
    if force_rebuild or kb_name not in _retrievers:
        _retrievers[kb_name] = HybridRetriever(
            kb_name,
            kb.entities,
            cache_dir=cache_dir,
            force_rebuild=force_rebuild,
        )
    return _retrievers[kb_name]
