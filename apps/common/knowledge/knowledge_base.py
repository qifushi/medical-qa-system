import os
import json
from typing import List, Dict, Any, Tuple

class KnowledgeBase:
    """知识库存储模块"""
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        # 修复路径计算，确保目录存在
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '../../../data/knowledge_bases', db_name)
        self.db_path = os.path.abspath(self.db_path)
        print(f"创建知识库目录: {self.db_path}")
        os.makedirs(self.db_path, exist_ok=True)
        
        # 初始化存储
        self.entities = {}
        self.relations = {}
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        entities_file = os.path.join(self.db_path, 'entities.json')
        relations_file = os.path.join(self.db_path, 'relations.json')
        
        if os.path.exists(entities_file):
            try:
                # 使用二进制模式读取，手动处理 BOM
                with open(entities_file, 'rb') as f:
                    raw_bytes = f.read()
                # 移除 BOM 标记
                if raw_bytes.startswith(b'\xef\xbb\xbf'):
                    raw_bytes = raw_bytes[3:]
                content = raw_bytes.decode('utf-8')
                self.entities = json.loads(content)
            except Exception as e:
                print(f"加载 entities.json 失败：{e}，使用空字典")
                self.entities = {}
        
        if os.path.exists(relations_file):
            try:
                with open(relations_file, 'rb') as f:
                    raw_bytes = f.read()
                if raw_bytes.startswith(b'\xef\xbb\xbf'):
                    raw_bytes = raw_bytes[3:]
                content = raw_bytes.decode('utf-8')
                self.relations = json.loads(content)
            except Exception as e:
                print(f"加载 relations.json 失败：{e}，使用空字典")
                self.relations = {}
    
    def _save_data(self):
        """保存数据"""
        entities_file = os.path.join(self.db_path, 'entities.json')
        relations_file = os.path.join(self.db_path, 'relations.json')
        
        with open(entities_file, 'w', encoding='utf-8-sig') as f:
            json.dump(self.entities, f, ensure_ascii=False, indent=2)
        
        with open(relations_file, 'w', encoding='utf-8-sig') as f:
            json.dump(self.relations, f, ensure_ascii=False, indent=2)
    
    def add_entity(self, entity_id: str, entity_type: str, entity_name: str, properties: Dict[str, Any] = None) -> None:
        """添加实体"""
        if properties is None:
            properties = {}
        
        self.entities[entity_id] = {
            'type': 'entity',
            'entity_type': entity_type,
            'entity_name': entity_name,
            **properties
        }
        
        self._save_data()
    
    def add_relation(self, relation_id: str, subject_id: str, predicate: str, object_id: str, properties: Dict[str, Any] = None) -> None:
        """添加关系"""
        if properties is None:
            properties = {}
        
        self.relations[relation_id] = {
            'type': 'relation',
            'subject_id': subject_id,
            'predicate': predicate,
            'object_id': object_id,
            **properties
        }
        
        self._save_data()
    
    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """查询知识库 - 支持全文搜索"""
        results = []
        
        # 全文本匹配（包括所有属性）
        for entity_id, entity in self.entities.items():
            # 搜索 entity_name 和 entity_type
            if query_text in entity.get('entity_name', '') or query_text in entity.get('entity_type', ''):
                results.append({
                    'id': entity_id,
                    'document': f"{entity.get('entity_type', '')}: {entity.get('entity_name', '')}",
                    'metadata': entity,
                    'distance': 0.0
                })
                continue
            
            # 搜索所有其他属性（name, desc, check, recommand_drug, cure_way 等）
            for key, value in entity.items():
                if key in ['type', 'entity_type', 'entity_name']:
                    continue
                
                # 处理字符串类型
                if isinstance(value, str) and query_text in value:
                    results.append({
                        'id': entity_id,
                        'document': f"{entity.get('entity_type', '')}: {entity.get('entity_name', '')} - {key}",
                        'metadata': entity,
                        'distance': 0.0
                    })
                    break
                
                # 处理列表类型
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, str) and query_text in item:
                            results.append({
                                'id': entity_id,
                                'document': f"{entity.get('entity_type', '')}: {entity.get('entity_name', '')} - {key}",
                                'metadata': entity,
                                'distance': 0.0
                            })
                            break
                    else:
                        continue
                    break
        
        for relation_id, relation in self.relations.items():
            if query_text in relation['predicate']:
                results.append({
                    'id': relation_id,
                    'document': f"{relation['subject_id']} {relation['predicate']} {relation['object_id']}",
                    'metadata': relation,
                    'distance': 0.0
                })
        
        # 限制结果数量
        return results[:n_results]
    
    def get_entity_by_id(self, entity_id: str) -> Dict[str, Any]:
        """根据ID获取实体"""
        if entity_id in self.entities:
            return self.entities[entity_id]
        return None
    
    def get_relations(self, subject_id: str = None, predicate: str = None, object_id: str = None) -> List[Dict[str, Any]]:
        """获取关系"""
        results = []
        
        for relation_id, relation in self.relations.items():
            if subject_id and relation['subject_id'] != subject_id:
                continue
            if predicate and relation['predicate'] != predicate:
                continue
            if object_id and relation['object_id'] != object_id:
                continue
            results.append({
                'id': relation_id,
                'document': f"{relation['subject_id']} {relation['predicate']} {relation['object_id']}",
                'metadata': relation
            })
        
        return results

def get_knowledge_base(db_name: str) -> KnowledgeBase:
    """获取知识库实例"""
    return KnowledgeBase(db_name)