import re
from typing import Dict, List, Any

class DataClassifier:
    """数据分类器，将爬取的数据分配到不同的知识库"""
    
    def __init__(self):
        # 初始化分类规则
        self.report_keywords = [
            '报告', '检查', '诊断', '化验', '检验', '结果', '指标', '血常规', '尿常规',
            'CT', 'MRI', 'B超', 'X光', '心电图', '脑电图', '病理', '活检', '影像'
        ]
        
        self.medicine_keywords = [
            '药品', '药物', ' medicine', 'drug', 'medication', 'pill', 'tablet', 'capsule',
            '胶囊', '片剂', '注射', '口服', '剂量', '用法', '用量', '副作用', '不良反应',
            '适应症', '禁忌症', '注意事项', '药理', '药效', '药代', '药动', '处方', '非处方'
        ]
        
        self.medical_service_keywords = [
            '医院', '诊所', '医生', '科室', '就诊', '挂号', '预约', '住院', '门诊',
            '手术', '治疗', '护理', '康复', '医保', '报销', '费用', '流程', '指南'
        ]
    
    def classify_article(self, article: Dict[str, Any]) -> List[str]:
        """分类文章到不同的知识库
        
        Args:
            article: 文章数据，包含title和content字段
            
        Returns:
            分类结果列表，包含对应的知识库名称
        """
        categories = []
        text = f"{article.get('title', '')} {article.get('content', '')}".lower()
        
        # 检查报告分析知识库
        if any(keyword in text for keyword in self.report_keywords):
            categories.append('report_analysis')
        
        # 检查药品分析知识库
        if any(keyword in text for keyword in self.medicine_keywords):
            categories.append('medicine_analysis')
        
        # 检查就医知识库
        if any(keyword in text for keyword in self.medical_service_keywords):
            categories.append('medical_service')
        
        # 如果没有匹配的分类，默认分配到就医知识库
        if not categories:
            categories.append('medical_service')
        
        return categories
    
    def classify_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """分类多篇文章
        
        Args:
            articles: 文章列表
            
        Returns:
            分类结果字典，键为知识库名称，值为对应的文章列表
        """
        classified = {
            'report_analysis': [],
            'medicine_analysis': [],
            'medical_service': []
        }
        
        for article in articles:
            categories = self.classify_article(article)
            for category in categories:
                classified[category].append(article)
        
        return classified

def get_data_classifier() -> DataClassifier:
    """获取数据分类器实例"""
    return DataClassifier()
