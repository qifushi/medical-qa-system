import asyncio
import os
import sys
import json
from typing import List, Dict, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from apps.common.spider.spider_manager import SpiderManager
from apps.common.pipeline.data_classifier import get_data_classifier
from apps.common.pipeline.processing_pipeline import get_processing_pipeline
from apps.common.knowledge.knowledge_base import get_knowledge_base

class DataIntegration:
    """数据集成模块，实现爬取、分类、处理和存储的完整流程"""
    
    def __init__(self):
        self.spider_manager = SpiderManager()
        self.classifier = get_data_classifier()
        self.pipeline = get_processing_pipeline()
        
        # 初始化知识库
        self.knowledge_bases = {
            'report_analysis': get_knowledge_base('report_analysis'),
            'medicine_analysis': get_knowledge_base('medicine_analysis'),
            'medical_service': get_knowledge_base('medical_service')
        }
    
    async def run_integration(self):
        """运行完整的集成流程"""
        print("=== 开始数据集成流程 ===")
        
        # 1. 爬取数据
        print("1. 正在爬取数据...")
        articles = await self.spider_manager.crawl_all()
        print(f"爬取完成，共获取 {len(articles)} 篇文章")
        
        # 2. 分类数据
        print("2. 正在分类数据...")
        classified_articles = self.classifier.classify_articles(articles)
        
        # 打印分类结果
        for kb_name, kb_articles in classified_articles.items():
            print(f"{kb_name}: {len(kb_articles)} 篇文章")
        
        # 3. 处理和存储数据
        print("3. 正在处理和存储数据...")
        max_knowledge_per_base = 10000  # 每个知识库的最大知识量
        
        for kb_name, kb_articles in classified_articles.items():
            print(f"处理 {kb_name} 知识库的数据...")
            knowledge_base = self.knowledge_bases[kb_name]
            
            # 检查知识库当前大小
            current_size = len(knowledge_base.entities) + len(knowledge_base.relations)
            print(f"  当前知识库大小: {current_size} 条")
            
            # 如果知识库已经达到最大大小，跳过处理
            if current_size >= max_knowledge_per_base:
                print(f"  知识库 {kb_name} 已达到最大大小，跳过处理")
                continue
            
            # 计算还可以添加的知识量
            remaining = max_knowledge_per_base - current_size
            print(f"  还可以添加 {remaining} 条知识")
            
            processed_count = 0
            for i, article in enumerate(kb_articles):
                # 检查是否已经达到最大知识量
                current_size = len(knowledge_base.entities) + len(knowledge_base.relations)
                if current_size >= max_knowledge_per_base:
                    print(f"  知识库 {kb_name} 已达到最大大小，停止处理")
                    break
                
                print(f"  处理第 {i+1} 篇文章: {article.get('title', '无标题')}")
                
                # 处理文本
                content = article.get('content', '')
                # 即使内容为空，也要处理，因为标题可能包含有价值的信息
                if content or article.get('title', ''):
                    # 如果内容为空，使用标题作为内容
                    text_to_process = content if content else article.get('title', '')
                    processed = self.pipeline.process_text(text_to_process)
                    
                    # 存储实体和关系
                    self._store_to_knowledge_base(knowledge_base, article, processed)
                    processed_count += 1
            
            print(f"  处理完成，共处理 {processed_count} 篇文章")
        
        print("=== 数据集成流程完成 ===")
    
    def _store_to_knowledge_base(self, knowledge_base, article, processed):
        """将处理后的数据存储到知识库"""
        print(f"处理文章: {article.get('title', '无标题')}")
        
        # 直接存储完整文章，而不是碎片化的实体
        article_id = f"article_{hash(article.get('title', '') + article.get('url', ''))}"
        
        # 确定文章类型
        article_type = 'article'
        title = article.get('title', '').lower()
        
        if any(keyword in title for keyword in ['药品', '药物', 'medicine', 'drug']):
            article_type = 'medicine'
        elif any(keyword in title for keyword in ['医生', '医院', '科室', '就诊']):
            article_type = 'medical_service'
        elif any(keyword in title for keyword in ['检查', '报告', '诊断', '化验']):
            article_type = 'report'
        
        # 存储完整文章
        knowledge_base.add_entity(
            entity_id=article_id,
            entity_type=article_type,
            entity_name=article.get('title', '无标题'),
            properties={
                'source': article.get('source', ''),
                'url': article.get('url', ''),
                'content': article.get('content', ''),
                'crawled_at': article.get('crawled_at', '')
            }
        )
        
        print(f"添加文章: {article.get('title', '无标题')} (类型: {article_type})")

async def main():
    """主函数"""
    integration = DataIntegration()
    await integration.run_integration()

if __name__ == "__main__":
    asyncio.run(main())
