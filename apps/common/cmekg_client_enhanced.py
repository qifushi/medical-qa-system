import os
import sys
import json

# 添加 CMeKG 路径
CMEKG_PATH = os.path.join(os.path.dirname(__file__), '../../CMeKG_tools-main/CMeKG')
sys.path.append(CMEKG_PATH)

class CMeKGClient:
    """CMeKG 本地知识库客户端 - 增强版"""
    
    def __init__(self):
        self.re_models = None  # 关系抽取模型（可能返回多个）
        self.ner_model = None
        self.cws_model = None
        self.get_triples = None
        self._load_models()
    
    def _load_models(self):
        """加载三个模型"""
        try:
            # 1. 关系抽取
            print("正在加载关系抽取模型...")
            re_path = os.path.join(CMEKG_PATH, 'medical_re')
            sys.path.insert(0, re_path)
            
            from medical_re import load_schema, load_model, get_triples
            load_schema()
            self.re_models = load_model()  # 可能返回多个模型
            self.get_triples = get_triples
            print("✅ 关系抽取模型加载成功")
            
            # 2. 实体识别
            print("正在加载实体识别模型...")
            ner_path = os.path.join(CMEKG_PATH, 'medical_ner')
            sys.path.insert(0, ner_path)
            
            from run import medical_ner
            self.ner_model = medical_ner()
            print("✅ 实体识别模型加载成功")
            
            # 3. 分词
            print("正在加载分词模型...")
            cws_path = os.path.join(CMEKG_PATH, 'medical_cws')
            sys.path.insert(0, cws_path)
            
            from run import medical_cws
            self.cws_model = medical_cws()
            print("✅ 分词模型加载成功")
            
            print("\n✅ CMeKG 所有模型加载成功")
        except Exception as e:
            print(f"⚠️ CMeKG 模型加载失败：{e}")
            import traceback
            traceback.print_exc()
    
    def extract_entities(self, text):
        """提取医学实体"""
        if not self.ner_model:
            return []
        
        try:
            result = self.ner_model.predict_sentence(text)
            
            # 处理输出格式
            entities = []
            if isinstance(result, list):
                for item in result:
                    if isinstance(item, tuple) and len(item) >= 2:
                        entity_type, entity_text = item[0], item[1]
                        # 过滤掉单个字的实体
                        if len(entity_text) > 1:
                            entities.append((entity_type, entity_text))
            
            # 去重
            unique_entities = []
            seen = set()
            for entity in entities:
                entity_key = f"{entity[0]}:{entity[1]}"
                if entity_key not in seen:
                    seen.add(entity_key)
                    unique_entities.append(entity)
            
            return unique_entities
        except Exception as e:
            print(f"实体提取失败：{e}")
            return []
    
    def extract_relations(self, text):
        """抽取关系三元组"""
        if not self.re_models or not self.get_triples:
            return []
        
        try:
            # 处理多个模型的情况
            if isinstance(self.re_models, (list, tuple)):
                res = self.get_triples(text, *self.re_models)
            else:
                res = self.get_triples(text, self.re_models)
            
            # 解析结果
            relations = []
            if res and len(res) > 0:
                for item in res:
                    if 'triples' in item:
                        for triple in item['triples']:
                            if isinstance(triple, list) and len(triple) >= 3:
                                relations.append({
                                    'subject': triple[0],
                                    'predicate': triple[1],
                                    'object': triple[2]
                                })
            
            return relations
        except Exception as e:
            print(f"关系抽取失败：{e}")
            return []
    
    def segment(self, text):
        """医学分词"""
        if not self.cws_model:
            return text.split()
        
        try:
            result = self.cws_model.predict_sentence(text)
            if isinstance(result, list):
                return result
            return text.split()
        except Exception as e:
            print(f"分词失败：{e}")
            return text.split()
    
    def query(self, user_input):
        """对外接口：根据用户输入返回结构化知识"""
        result = {
            "entities": [],
            "relations": [],
            "segmented": [],
            "summary": ""
        }
        
        try:
            # 1. 分词
            words = self.segment(user_input)
            result["segmented"] = words
            
            # 2. 提取实体
            entities = self.extract_entities(user_input)
            result["entities"] = entities
            
            # 3. 抽取关系
            relations = self.extract_relations(user_input)
            result["relations"] = relations
            
            # 4. 构建知识摘要
            knowledge_summary = ""
            if entities:
                knowledge_summary += "📋 识别到的医学实体:\n"
                for e_type, e_text in entities:
                    knowledge_summary += f"  - {e_type}: {e_text}\n"
            
            if relations:
                knowledge_summary += "\n🔗 抽取到的医学关系:\n"
                for rel in relations:
                    knowledge_summary += f"  - {rel['subject']} → {rel['predicate']} → {rel['object']}\n"
            
            result["summary"] = knowledge_summary
            
        except Exception as e:
            print(f"CMeKG 查询失败：{e}")
        
        return result

# 单例模式
_cmekg_client = None

def get_cmekg_client():
    global _cmekg_client
    if _cmekg_client is None:
        _cmekg_client = CMeKGClient()
    return _cmekg_client