import os
import sys
import json
import jieba

try:
    from .knowledge.hybrid_retriever import get_hybrid_retriever, flatten_entity
except ImportError:  # 兼容以 common.cmekg_client 的绝对路径导入
    from knowledge.hybrid_retriever import get_hybrid_retriever, flatten_entity

# 添加 CMeKG 路径
CMEKG_PATH = os.path.join(os.path.dirname(__file__), '../../tools/CMeKG_tools-main/CMeKG')
sys.path.append(CMEKG_PATH)

# 添加项目根目录到 Python 路径，以便导入知识库模块
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../../')
sys.path.insert(0, PROJECT_ROOT)

class CMeKGClient:
    """CMeKG 本地知识库客户端"""
    
    def __init__(self):
        self.re_model = None
        self.ner_model = None
        self.cws_model = None
        self.get_triples = None  # 保存函数引用
        self.local_knowledge_bases = {}  # 本地知识库
        self._load_models()
        self._load_local_knowledge_bases()
    
    def _load_models(self):
        """加载三个模型（按需加载，避免占用内存）"""
        try:
            # 关系抽取
            re_path = os.path.join(CMEKG_PATH, 'medical_re')
            sys.path.append(re_path)
            import importlib.util
            spec = importlib.util.spec_from_file_location("medical_re", os.path.join(re_path, "medical_re.py"))
            medical_re = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(medical_re)
            medical_re.load_schema()
            self.re_model = medical_re.load_model()
            self.get_triples = medical_re.get_triples  # 保存函数
            
            # 实体识别
            ner_path = os.path.join(CMEKG_PATH, 'medical_ner')
            sys.path.append(ner_path)
            spec = importlib.util.spec_from_file_location("run_ner", os.path.join(ner_path, "run.py"))
            run_ner = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_ner)
            self.ner_model = run_ner.medical_ner()
            
            # 分词
            cws_path = os.path.join(CMEKG_PATH, 'medical_cws')
            sys.path.append(cws_path)
            spec = importlib.util.spec_from_file_location("run_cws", os.path.join(cws_path, "run.py"))
            run_cws = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_cws)
            self.cws_model = run_cws.medical_cws()
            
            print("✅ CMeKG 模型加载成功")
        except Exception as e:
            print(f"⚠️ CMeKG 模型加载失败：{e}")
    
    def _load_local_knowledge_bases(self):
        """加载本地知识库"""
        try:
            from apps.common.knowledge.knowledge_base import get_knowledge_base
            
            # 加载三个知识库
            kb_names = ['report_analysis', 'medicine_analysis', 'medical_service']
            for kb_name in kb_names:
                try:
                    kb = get_knowledge_base(kb_name)
                    self.local_knowledge_bases[kb_name] = kb
                    print(f"✅ 加载本地知识库：{kb_name}")
                except Exception as e:
                    print(f"⚠️ 加载本地知识库 {kb_name} 失败：{e}")
        except Exception as e:
            print(f"⚠️ 加载本地知识库失败：{e}")
    
    def _search_knowledge_base(self, kb_name, kb, query_text, n_results=5):
        """优先使用混合检索，异常时回退到原有子串检索。"""
        try:
            retriever = get_hybrid_retriever(kb_name, kb)
            return retriever.search(query_text, top_k=n_results, mode='hybrid')
        except Exception as e:
            print(f"混合检索 {kb_name} 失败，回退子串检索：{e}")
            try:
                return kb.query(query_text, n_results=n_results)
            except Exception as inner:
                print(f"查询本地知识库 {kb_name} 失败：{inner}")
                return []

    def _query_local_knowledge_bases(self, query_text, kb_type=None):
        """查询本地知识库"""
        results = []
        
        # 根据 kb_type 决定查询哪些知识库
        if kb_type:
            # 只查询指定的知识库
            if kb_type in self.local_knowledge_bases:
                kb_results = self._search_knowledge_base(
                    kb_type, self.local_knowledge_bases[kb_type], query_text
                )
                if kb_results:
                    results.append({
                        'kb_name': kb_type,
                        'results': kb_results
                    })
        else:
            # 查询所有知识库
            for kb_name, kb in self.local_knowledge_bases.items():
                kb_results = self._search_knowledge_base(kb_name, kb, query_text)
                if kb_results:
                    results.append({
                        'kb_name': kb_name,
                        'results': kb_results
                    })
        return results
    
    def extract_entities(self, text):
        """提取医学实体"""
        if not self.ner_model:
            return []
        
        # 直接对整个句子进行实体识别
        result = self.ner_model.predict_sentence(text)
        
        # 处理可能的输出格式
        entities = []
        if isinstance(result, list):
            for item in result:
                if isinstance(item, tuple) and len(item) >= 2:
                    entity_type, entity_text = item[0], item[1]
                    # 过滤掉单个字的实体（但保留"发烧"这种两个字的）
                    if len(entity_text) > 1:
                        entities.append((entity_type, entity_text))
                elif isinstance(item, str):
                    # 如果是纯字符串格式，按规则解析
                    entities.append(("ENTITY", item))
        
        # 去重
        unique_entities = []
        seen = set()
        for entity in entities:
            entity_key = f"{entity[0]}:{entity[1]}"
            if entity_key not in seen:
                seen.add(entity_key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def extract_relations(self, text):
        """抽取关系三元组"""
        if not self.re_model or not self.get_triples:
            return []
        return self.get_triples(text, *self.re_model)
    
    def segment(self, text):
        """医学分词"""
        return jieba.lcut(text)
    
    def query(self, user_input, kb_type=None):
        """对外接口：根据用户输入返回结构化知识"""
        # 1. 先分词
        words = self.segment(user_input)
        
        # 2. 提取实体
        entities = self.extract_entities(user_input)
        
        # 3. 抽取关系
        relations = self.extract_relations(user_input)
        
        # 4. 查询本地知识库
        local_kb_results = self._query_local_knowledge_bases(user_input, kb_type)
        
        # 5. 构建结构化的知识摘要
        knowledge_summary = ""
        if entities:
            knowledge_summary += "识别到的医学实体:\n"
            for e_type, e_text in entities:
                knowledge_summary += f"- {e_type}: {e_text}\n"
        
        if relations:
            knowledge_summary += "\n抽取到的医学关系:\n"
            for rel in relations:
                if isinstance(rel, list) and len(rel) >= 3:
                    knowledge_summary += f"- {rel[0]} {rel[1]} {rel[2]}\n"
        
        # 添加本地知识库结果
        if local_kb_results:
            knowledge_summary += "\n本地知识库匹配结果:\n"
            for kb_result in local_kb_results:
                kb_name = kb_result['kb_name']
                results = kb_result['results']
                if results:
                    knowledge_summary += f"\n【{kb_name}】找到 {len(results)} 个相关条目:\n"
                    for i, result in enumerate(results[:3]):  # 只取前 3 个结果
                        # 疾病百科 / 药品条目的字段嵌在 properties 下，先展开
                        meta = flatten_entity(result.get('metadata', {}))
                        entity_name = meta.get('entity_name', '')
                        entity_type = meta.get('entity_type', '')

                        knowledge_summary += f"  {i+1}. {entity_name} ({entity_type})"

                        overview = meta.get('answer') or meta.get('desc') or ''
                        if isinstance(overview, str) and overview.strip():
                            knowledge_summary += f"\n     说明：{overview.strip()[:180]}"

                        for label, key in (
                            ('检查项目', 'check'),
                            ('推荐药物', 'recommand_drug'),
                            ('治疗方法', 'cure_way'),
                            ('常见症状', 'symptom'),
                            ('宜吃', 'do_eat'),
                            ('忌吃', 'not_eat'),
                            ('适应证', 'indications'),
                            ('用法用量', 'usage'),
                        ):
                            values = meta.get(key) or []
                            if isinstance(values, str):
                                values = [values]
                            values = [str(v).strip()[:80] for v in values if v][:2]
                            if values:
                                knowledge_summary += f"\n     {label}：{', '.join(values)}"

                        facts = []
                        for label, key in (
                            ('别名', 'alias'),
                            ('发病率', 'get_prob'),
                            ('治愈率', 'cured_prob'),
                            ('治疗周期', 'cure_lasttime'),
                            ('费用', 'cost_money'),
                            ('医保', 'yibao_status'),
                            ('剂型', 'dosage_form'),
                            ('禁忌', 'contraindications'),
                            ('注意事项', 'precautions'),
                            ('不良反应', 'adverse_reactions'),
                            ('相互作用', 'interactions'),
                        ):
                            value = meta.get(key)
                            if isinstance(value, str) and value.strip():
                                facts.append(f"{label}：{value.strip()[:60]}")
                        if facts:
                            knowledge_summary += "\n     " + "；".join(facts)

                        knowledge_summary += "\n"
        
        return {
            "entities": entities,
            "relations": relations,
            "segmented": words,
            "summary": knowledge_summary,
            "local_kb_results": local_kb_results
        }

# 单例模式
_cmekg_client = None

def get_cmekg_client():
    global _cmekg_client
    if _cmekg_client is None:
        _cmekg_client = CMeKGClient()
    return _cmekg_client