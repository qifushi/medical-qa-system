import os
import json
from typing import List, Dict, Any
from .knowledge_base import get_knowledge_base

class KnowledgeQueryService:
    """知识查询服务"""
    
    def __init__(self):
        # 初始化三个知识库
        self.report_kb = get_knowledge_base('report_analysis')
        self.medicine_kb = get_knowledge_base('medicine_analysis')
        self.medical_service_kb = get_knowledge_base('medical_service')
    
    def determine_knowledge_base(self, query: str) -> str:
        """根据查询内容确定使用哪个知识库"""
        # 关键词匹配
        report_keywords = ['报告', '检验', '检查', '指标', '血常规', '肝功能', '肾功能']
        medicine_keywords = ['药物', '药品', '用药', '副作用', '适应症', '禁忌症']
        service_keywords = ['医院', '科室', '医生', '就医', '流程', '推荐']
        
        report_count = sum(1 for keyword in report_keywords if keyword in query)
        medicine_count = sum(1 for keyword in medicine_keywords if keyword in query)
        service_count = sum(1 for keyword in service_keywords if keyword in query)
        
        if report_count >= medicine_count and report_count >= service_count:
            return 'report'
        elif medicine_count >= report_count and medicine_count >= service_count:
            return 'medicine'
        else:
            return 'service'
    
    def query_knowledge(self, query: str) -> Dict[str, Any]:
        """查询知识库"""
        # 确定使用哪个知识库
        kb_type = self.determine_knowledge_base(query)
        
        # 根据类型选择知识库
        if kb_type == 'report':
            kb = self.report_kb
        elif kb_type == 'medicine':
            kb = self.medicine_kb
        elif kb_type == 'service':
            kb = self.medical_service_kb
        else:
            raise ValueError(f"未知的知识库类型: {kb_type}")
        
        # 查询知识库
        results = kb.query(query, n_results=10)
        
        # 处理查询结果
        entities = []
        relations = []
        
        for result in results:
            if result['metadata']['type'] == 'entity':
                entities.append({
                    'id': result['id'],
                    'type': result['metadata']['entity_type'],
                    'name': result['metadata']['entity_name'],
                    'properties': {k: v for k, v in result['metadata'].items() if k not in ['type', 'entity_type', 'entity_name']}
                })
            elif result['metadata']['type'] == 'relation':
                relations.append({
                    'id': result['id'],
                    'subject_id': result['metadata']['subject_id'],
                    'predicate': result['metadata']['predicate'],
                    'object_id': result['metadata']['object_id'],
                    'properties': {k: v for k, v in result['metadata'].items() if k not in ['type', 'subject_id', 'predicate', 'object_id']}
                })
        
        return {
            'query': query,
            'knowledge_base': kb_type,
            'entities': entities,
            'relations': relations
        }
    
    def build_knowledge_prompt(self, query: str) -> str:
        """构建知识提示"""
        # 查询知识库
        knowledge = self.query_knowledge(query)
        
        # 构建提示
        prompt = f"用户问题: {query}\n\n相关知识:\n"
        
        # 添加实体
        if knowledge['entities']:
            prompt += "## 相关实体\n"
            for entity in knowledge['entities'][:5]:  # 最多显示5个实体
                prompt += f"- {entity['type']}: {entity['name']}\n"
                if entity['properties']:
                    for key, value in entity['properties'].items():
                        prompt += f"  - {key}: {value}\n"
            prompt += "\n"
        
        # 添加关系
        if knowledge['relations']:
            prompt += "## 相关关系\n"
            for relation in knowledge['relations'][:5]:  # 最多显示5个关系
                prompt += f"- {relation['predicate']}\n"
            prompt += "\n"
        
        prompt += "请根据以上知识，为用户提供详细、准确的回答。"
        
        return prompt

def get_knowledge_query_service() -> KnowledgeQueryService:
    """获取知识查询服务实例"""
    return KnowledgeQueryService()