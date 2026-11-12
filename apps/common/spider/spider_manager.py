import yaml
import asyncio
import os
import sys
from typing import List, Dict, Any
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from apps.common.spider.merck_manual_spider import MerckManualSpider
from apps.common.spider.dingxiang_spider import DingXiangSpider
from apps.common.spider.hospital_spider import HospitalSpider
from apps.common.spider.db_deduplicator import get_deduplicator

class SpiderManager:
    """爬虫管理器"""
    
    def __init__(self, config_path: str = "config/spider_config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.spiders = self.init_spiders()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def init_spiders(self) -> Dict[str, Any]:
        """初始化爬虫"""
        spiders = {}
        sources = self.config.get('sources', {})
        
        # 暂时不使用去重器，以便重新爬取数据进行测试
        # deduplicator = get_deduplicator(use_postgres=False)  # 开发环境使用SQLite
        
        # 初始化默沙东诊疗手册爬虫
        if 'merck_manual' in sources:
            spiders['merck_manual'] = MerckManualSpider('merck_manual', sources['merck_manual'])
            # spiders['merck_manual'].set_deduplicator(deduplicator)
        
        # 初始化丁香医生爬虫
        if 'dingxiang' in sources:
            spiders['dingxiang'] = DingXiangSpider('dingxiang', sources['dingxiang'])
            # spiders['dingxiang'].set_deduplicator(deduplicator)
        
        # 初始化医院信息爬虫
        if 'hospital' in sources:
            spiders['hospital'] = HospitalSpider('hospital', sources['hospital'])
            # spiders['hospital'].set_deduplicator(deduplicator)
        
        return spiders
    
    async def crawl_all(self) -> List[Dict[str, Any]]:
        """爬取所有数据源，支持深度爬取"""
        all_articles = []
        
        for name, spider in self.spiders.items():
            print(f"开始爬取 {name}")
            test_url = spider.config.get('test_url')
            if test_url:
                async with spider:
                    articles = await spider.crawl_with_depth(test_url)
                    all_articles.extend(articles)
                    print(f"{name} 爬取完成，找到 {len(articles)} 篇文章")
            else:
                print(f"{name} 没有配置 test_url")
        
        return all_articles
    
    async def crawl_source(self, source_name: str) -> List[Dict[str, Any]]:
        """爬取指定数据源"""
        if source_name not in self.spiders:
            print(f"数据源 {source_name} 不存在")
            return []
        
        spider = self.spiders[source_name]
        test_url = spider.config.get('test_url')
        if not test_url:
            print(f"{source_name} 没有配置 test_url")
            return []
        
        async with spider:
            articles = await spider.crawl_with_delay(test_url)
            print(f"{source_name} 爬取完成，找到 {len(articles)} 篇文章")
            return articles
    
    def get_spider(self, name: str):
        """获取爬虫实例"""
        return self.spiders.get(name)

# 测试函数
async def test_spider_manager():
    """测试爬虫管理器"""
    manager = SpiderManager()
    
    # 爬取所有数据源
    print("=== 爬取所有数据源 ===")
    all_articles = await manager.crawl_all()
    print(f"\n所有数据源爬取完成，共找到 {len(all_articles)} 篇文章")
    
    # 打印前5篇文章
    print("\n=== 前5篇文章 ===")
    for i, article in enumerate(all_articles[:5]):
        print(f"{i+1}. {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   来源: {article['source']}")
        print()

if __name__ == "__main__":
    asyncio.run(test_spider_manager())
