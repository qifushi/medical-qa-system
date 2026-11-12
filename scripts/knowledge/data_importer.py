import os
import json
import uuid
from typing import List, Dict, Any
from .knowledge_base import get_knowledge_base

class DataImporter:
    """数据导入器"""
    
    def __init__(self):
        # 初始化三个知识库
        self.report_kb = get_knowledge_base('report_analysis')
        self.medicine_kb = get_knowledge_base('medicine_analysis')
        self.medical_service_kb = get_knowledge_base('medical_service')
    
    def import_data(self, processed_data_path: str, knowledge_base_type: str) -> None:
        """导入数据到知识库"""
        # 根据类型选择知识库
        if knowledge_base_type == 'report':
            kb = self.report_kb
        elif knowledge_base_type == 'medicine':
            kb = self.medicine_kb
        elif knowledge_base_type == 'service':
            kb = self.medical_service_kb
        else:
            raise ValueError(f"未知的知识库类型: {knowledge_base_type}")
        
        # 读取处理后的数据
        with open(processed_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 导入实体和关系
        for item in data:
            if 'processed' in item:
                processed = item['processed']
                
                # 导入实体
                for entity_type, entity_name in processed['entities']:
                    entity_id = str(uuid.uuid4())
                    kb.add_entity(entity_id, entity_type, entity_name)
                
                # 导入关系
                for triple in processed['triples']:
                    if len(triple) == 3:
                        subject, predicate, object_ = triple
                        relation_id = str(uuid.uuid4())
                        # 这里需要根据实际情况获取实体ID
                        # 简化处理，使用实体名称作为ID
                        subject_id = str(uuid.uuid4())
                        object_id = str(uuid.uuid4())
                        kb.add_relation(relation_id, subject_id, predicate, object_id)
        
        print(f"数据导入完成，导入到 {knowledge_base_type} 知识库")
    
    def import_directory(self, directory: str, knowledge_base_type: str) -> None:
        """导入目录中的所有数据"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    print(f"导入文件: {file_path}")
                    self.import_data(file_path, knowledge_base_type)

def get_data_importer() -> DataImporter:
    """获取数据导入器实例"""
    return DataImporter()