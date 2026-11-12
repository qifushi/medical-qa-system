from bs4 import BeautifulSoup
from typing import List, Dict, Any
from apps.common.spider.base_spider import BaseSpider

class HospitalSpider(BaseSpider):
    """医院信息爬虫"""
    
    async def parse(self, html: str) -> List[Dict[str, Any]]:
        """解析页面内容"""
        try:
            self.logger.info("开始解析医院信息页面")
            
            if not html:
                self.logger.error("HTML内容为空")
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            self.logger.info(f"页面标题: {soup.title.string if soup.title else '无标题'}")
            
            # 尝试不同的选择器来找到文章
            articles = []
            
            # 尝试找到主要内容区域
            main_content = soup.find('main') or soup.find('div', class_='main-content') or soup.find('div', id='content')
            
            if main_content:
                self.logger.info("找到主要内容区域")
                # 尝试找到新闻列表
                news_elements = main_content.find_all(['div', 'li'], class_=['news-item', 'item', 'post'])
                self.logger.info(f"找到 {len(news_elements)} 个新闻元素")
                
                for news in news_elements:
                    # 提取标题
                    title_elem = news.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
                    title = title_elem.text.strip() if title_elem else "无标题"
                    
                    # 提取链接
                    link_elem = news.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    
                    # 提取摘要
                    summary_elem = news.find(['div', 'p'], class_=['summary', 'desc', 'content'])
                    content = summary_elem.text.strip() if summary_elem else ""
                    
                    if title or content:
                        articles.append({
                            'title': title,
                            'url': link,
                            'content': content,
                            'source': 'hospital',
                            'crawled_at': self.config.get('crawled_at', '')
                        })
            else:
                # 如果没有找到主要内容区域，尝试找到所有链接
                links = soup.find_all('a', href=True)
                self.logger.info(f"找到 {len(links)} 个链接")
                
                for link in links:
                    title = link.text.strip()
                    url = link['href']
                    
                    # 过滤掉无效链接
                    if title and url and ('http' in url or url.startswith('/')):
                        articles.append({
                            'title': title,
                            'url': url,
                            'content': '',
                            'source': 'hospital',
                            'crawled_at': self.config.get('crawled_at', '')
                        })
            
            self.logger.info(f"解析完成，找到 {len(articles)} 篇文章")
            return articles
        except Exception as e:
            self.logger.error(f"解析失败: {str(e)}")
            return []
    
    async def crawl(self, url: str) -> List[Dict[str, Any]]:
        """爬取指定URL"""
        try:
            # 检查URL是否已爬取
            if self.is_url_crawled(url):
                self.logger.info(f"URL已爬取，跳过: {url}")
                return []
            
            # 获取页面内容
            html = await self.fetch_with_retry(url)
            
            if not html:
                self.logger.error(f"获取页面内容失败: {url}")
                return []
            
            # 解析页面
            articles = await self.parse(html)
            
            # 标记URL已爬取
            self.mark_url_crawled(url, f"医院信息页面: {url}")
            
            return articles
        except Exception as e:
            self.logger.error(f"爬取失败: {url}, 错误: {str(e)}")
            return []
