import asyncio
import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseSpider(ABC):
    """爬虫基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(name)
        self.session = None
        self.deduplicator = None
        self.url_queue = []  # 待爬取的详情页链接队列
        self.visited_urls = set()  # 已访问的URL集合
        self.max_depth = config.get('max_depth', 2)  # 最大爬取深度
        self.driver = None
    
    async def __aenter__(self):
        """进入上下文管理器"""
        self.session = aiohttp.ClientSession()
        # 初始化Selenium驱动
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        if self.session:
            await self.session.close()
        if self.driver:
            self.driver.quit()
    
    async def fetch(self, url: str) -> str:
        """获取页面内容"""
        try:
            self.logger.info(f"正在获取URL: {url}")
            
            # 为丁香医生详情页使用Selenium
            if 'dxy.com' in url and '/diseases/' in url:
                self.logger.info("使用Selenium获取页面内容")
                
                # 使用Selenium获取页面
                self.driver.get(url)
                # 等待页面加载
                time.sleep(5)
                
                # 获取页面内容
                text = self.driver.page_source
                self.logger.info(f"获取到内容长度: {len(text)} 字符")
                self.logger.debug(f"前500个字符: {text[:500]}")  # 调试用
                return text
            else:
                # 普通页面使用aiohttp
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Referer': 'https://dxy.com/',
                    'Cache-Control': 'max-age=0',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'DNT': '1',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                
                async with self.session.get(url, headers=headers, timeout=30, allow_redirects=True) as response:
                    self.logger.info(f"响应状态码: {response.status}")
                    self.logger.info(f"最终URL: {str(response.url)}")
                    
                    if response.status == 200:
                        text = await response.text()
                        self.logger.info(f"获取到内容长度: {len(text)} 字符")
                        self.logger.debug(f"前500个字符: {text[:500]}")  # 调试用
                        return text
                    else:
                        self.logger.error(f"HTTP错误: {response.status}")
                        return ""
        except Exception as e:
            self.logger.error(f"获取页面失败: {url}, 错误: {str(e)}")
            return ""
    
    async def fetch_with_retry(self, url: str, max_retries: int = 3) -> str:
        """带重试的获取页面内容"""
        for i in range(max_retries):
            try:
                result = await self.fetch(url)
                if result:
                    return result
                else:
                    if i < max_retries - 1:
                        wait_time = (i + 1) * 2
                        self.logger.warning(f"第{i+1}次失败，{wait_time}秒后重试")
                        await asyncio.sleep(wait_time)
                    else:
                        self.logger.error(f"最终失败: {url}")
                        return ""
            except Exception as e:
                if i < max_retries - 1:
                    wait_time = (i + 1) * 2
                    self.logger.warning(f"第{i+1}次失败，{wait_time}秒后重试: {str(e)}")
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(f"最终失败: {url}, 错误: {str(e)}")
                    return ""
    
    @abstractmethod
    async def parse(self, html: str) -> List[Dict[str, Any]]:
        """解析页面内容"""
        pass
    
    @abstractmethod
    async def crawl(self, url: str) -> List[Dict[str, Any]]:
        """爬取指定URL"""
        pass
    
    async def crawl_with_delay(self, url: str) -> List[Dict[str, Any]]:
        """带延迟的爬取"""
        delay = self.config.get('delay', 2)
        self.logger.info(f"延迟 {delay} 秒后开始爬取")
        await asyncio.sleep(delay)
        return await self.crawl(url)
    
    async def crawl_with_depth(self, url: str, current_depth: int = 1) -> List[Dict[str, Any]]:
        """带深度控制的爬取"""
        if current_depth > self.max_depth:
            return []
        
        if url in self.visited_urls:
            return []
        
        self.visited_urls.add(url)
        articles = await self.crawl(url)
        
        # 处理队列中的链接
        while self.url_queue:
            next_url = self.url_queue.pop(0)
            if next_url not in self.visited_urls:
                articles.extend(await self.crawl_with_depth(next_url, current_depth + 1))
        
        return articles
    
    def add_to_queue(self, url: str):
        """添加链接到队列"""
        if url not in self.visited_urls and url not in self.url_queue:
            self.url_queue.append(url)
            self.logger.info(f"添加链接到队列: {url}")
    
    def set_deduplicator(self, deduplicator):
        """设置去重器"""
        self.deduplicator = deduplicator
    
    def is_url_crawled(self, url: str) -> bool:
        """检查URL是否已爬取
        
        现在总是返回False，允许重新爬取相同的链接以获取最新内容
        """
        return False
    
    def mark_url_crawled(self, url: str, title: str):
        """标记URL已爬取
        
        暂时不使用去重，允许重新爬取相同的链接
        """
        pass
