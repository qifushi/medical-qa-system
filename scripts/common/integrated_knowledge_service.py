import os
import sys
from typing import List, Dict, Any

# 添加 apps 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from common.knowledge.knowledge_base import get_knowledge_base
from common.cmekg_client import get_cmekg_client

class IntegratedMedicalKnowledgeService:
    """集成医疗知识服务 - 结合 CMeKG 和本地知识库"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("知贝医疗问答系统 - 加载知识库和 CMeKG 模型")
        print("="*60)
        
        # 初始化本地知识库
        self.report_kb = get_knowledge_base('report_analysis')
        self.medicine_kb = get_knowledge_base('medicine_analysis')
        self.medical_service_kb = get_knowledge_base('medical_service')
        
        # 初始化 CMeKG
        self.cmekg = get_cmekg_client()
        
        print("\n✅ 知贝医疗问答系统初始化完成")
        print(f"  - 报告分析知识库：{len(self.report_kb.entities)} 个实体")
        print(f"  - 药品分析知识库：{len(self.medicine_kb.entities)} 个实体")
        print(f"  - 就医服务知识库：{len(self.medical_service_kb.entities)} 个实体")
        print(f"  - CMeKG 医学 NLP 工具：已加载")
        print("="*60 + "\n")
    
    def determine_knowledge_base(self, query: str) -> str:
        """根据查询内容确定使用哪个知识库"""
        report_keywords = ['报告', '检验', '检查', '指标', '血常规', '肝功能', '肾功能']
        medicine_keywords = ['药物', '药品', '用药', '副作用', '适应症', '禁忌症', '治疗']
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
    
    def query(self, user_input: str) -> Dict[str, Any]:
        """查询集成知识服务"""
        result = {
            "query": user_input,
            "cmekg_result": None,
            "kb_result": None,
            "summary": ""
        }
        
        # 1. 使用 CMeKG 进行医学 NLP 分析
        cmekg_result = self.cmekg.query(user_input)
        result["cmekg_result"] = cmekg_result
        
        # 2. 使用本地知识库查询
        kb_type = self.determine_knowledge_base(user_input)
        if kb_type == 'report':
            kb = self.report_kb
        elif kb_type == 'medicine':
            kb = self.medicine_kb
        else:
            kb = self.medical_service_kb
        
        kb_results = kb.query(user_input, n_results=10)
        result["kb_result"] = {
            "type": kb_type,
            "results": kb_results
        }
        
        # 3. 构建综合知识摘要
        summary_parts = []
        
        # CMeKG 部分
        if cmekg_result["summary"]:
            summary_parts.append("【CMeKG 医学分析】")
            summary_parts.append(cmekg_result["summary"])
        
        # 本地知识库部分
        if kb_results:
            summary_parts.append(f"【{kb_type}知识库】")
            for i, res in enumerate(kb_results[:5], 1):
                if res['metadata']['type'] == 'entity':
                    entity_name = res['metadata'].get('entity_name', '')
                    entity_type = res['metadata'].get('entity_type', '')
                    
                    # 添加关键属性
                    props = []
                    for key in ['desc', 'symptom', 'recommand_drug', 'check']:
                        if key in res['metadata'] and res['metadata'][key]:
                            value = res['metadata'][key]
                            if isinstance(value, list):
                                props.append(f"{key}: {', '.join(str(v) for v in value[:3])}")
                            else:
                                props.append(f"{key}: {str(value)[:100]}")
                    
                    if props:
                        summary_parts.append(f"{i}. {entity_name} ({entity_type})")
                        for prop in props:
                            summary_parts.append(f"   - {prop}")
        
        result["summary"] = "\n".join(summary_parts)
        
        return result
    
    def build_knowledge_prompt(self, query: str) -> str:
        """构建知识提示"""
        knowledge = self.query(query)
        
        prompt = f"用户问题：{query}\n\n相关知识:\n"
        
        if knowledge["summary"]:
            prompt += knowledge["summary"]
        else:
            prompt += "未找到相关知识"
        
        prompt += "\n\n请根据以上知识，为用户提供详细、准确的回答。"
        
        return prompt

# 单例模式
_knowledge_service = None

def get_integrated_knowledge_service():
    global _knowledge_service
    if _knowledge_service is None:
        _knowledge_service = IntegratedMedicalKnowledgeService()
    return _knowledge_service