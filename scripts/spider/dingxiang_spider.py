from bs4 import BeautifulSoup
from typing import List, Dict, Any
from apps.common.spider.base_spider import BaseSpider
import re

class DingXiangSpider(BaseSpider):
    """丁香医生爬虫"""
    
    async def parse(self, html: str) -> List[Dict[str, Any]]:
        """解析页面内容，区分目录页和详情页"""
        try:
            self.logger.info("开始解析丁香医生页面")
            
            if not html:
                self.logger.error("HTML内容为空")
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            page_title = soup.title.string if soup.title else '无标题'
            self.logger.info(f"页面标题: {page_title}")
            
            articles = []
            
            # 1. 解析列表页/目录页
            self.logger.info("解析列表页/目录页")
            
            # 找到主要内容区域
            main_content = soup.find('main') or soup.find('div', class_='main-content') or soup.find('div', id='content')
            
            if main_content:
                # 尝试找到疾病列表或链接
                links = main_content.find_all('a', href=True)
                self.logger.info(f"找到 {len(links)} 个链接")
                
                for link in links:
                    title = link.text.strip()
                    url = link['href']
                    
                    # 构建完整URL
                    if url.startswith('/'):
                        url = f"https://dxy.com{url}"
                    
                    # 过滤掉无效链接和导航链接
                    if (title and url and 
                        not any(keyword in title.lower() for keyword in ['下载', 'app', '首页', '登录', '注册', '客服', '联系我们'])):
                        
                        # 判断是否是详情页链接
                        if '/diseases/' in url and url.count('/') >= 4 and not url.endswith('/'):
                            # 是详情页链接，添加到队列
                            self.add_to_queue(url)
                            self.logger.info(f"添加详情页到队列: {url}")
                        else:
                            # 是目录页链接，作为导航记录
                            articles.append({
                                'title': title,
                                'url': url,
                                'content': '',
                                'source': 'dingxiang',
                                'type': 'navigation',
                                'crawled_at': self.config.get('crawled_at', '')
                            })
            else:
                # 如果没有找到主要内容区域，尝试找到所有链接
                links = soup.find_all('a', href=True)
                self.logger.info(f"找到 {len(links)} 个链接")
                
                for link in links:
                    title = link.text.strip()
                    url = link['href']
                    
                    # 构建完整URL
                    if url.startswith('/'):
                        url = f"https://dxy.com{url}"
                    
                    # 过滤掉无效链接和导航链接
                    if (title and url and 
                        not any(keyword in title.lower() for keyword in ['下载', 'app', '首页', '登录', '注册', '客服', '联系我们'])):
                        
                        # 判断是否是详情页链接
                        if '/diseases/' in url and url.count('/') >= 4 and not url.endswith('/'):
                            # 是详情页链接，添加到队列
                            self.add_to_queue(url)
                            self.logger.info(f"添加详情页到队列: {url}")
                        else:
                            # 是目录页链接，作为导航记录
                            articles.append({
                                'title': title,
                                'url': url,
                                'content': '',
                                'source': 'dingxiang',
                                'type': 'navigation',
                                'crawled_at': self.config.get('crawled_at', '')
                            })
            
            # 去重
            seen_urls = set()
            unique_articles = []
            for article in articles:
                url = article['url']
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_articles.append(article)
            
            self.logger.info(f"解析完成，找到 {len(unique_articles)} 篇文章")
            return unique_articles
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
            
            # 检查是否是详情页
            if '/diseases/' in url and url.count('/') >= 4 and not url.endswith('/'):
                # 是详情页，直接提取内容
                self.logger.info(f"处理详情页: {url}")
                soup = BeautifulSoup(html, 'html.parser')
                all_text = soup.get_text(separator='\n', strip=True)
                
                # 提取标题
                title_elem = soup.find(['h1', 'h2', 'h3'])
                title = title_elem.text.strip() if title_elem else "无标题"
                
                # 提取链接
                canonical_link = soup.find('link', rel='canonical')
                canonical_url = canonical_link['href'] if canonical_link else url
                
                # 构建文章对象
                article = {
                    'title': title,
                    'url': canonical_url,
                    'content': all_text,
                    'source': 'dingxiang',
                    'type': 'article',
                    'crawled_at': self.config.get('crawled_at', '')
                }
                
                self.logger.info(f"提取到详情页: {title}，内容长度: {len(all_text)} 字符")
                
                # 标记URL已爬取
                self.mark_url_crawled(url, f"丁香医生页面: {url}")
                
                return [article]
            else:
                # 是目录页，使用原来的解析方法
                articles = await self.parse(html)
                
                # 标记URL已爬取
                self.mark_url_crawled(url, f"丁香医生页面: {url}")
                
                return articles
        except Exception as e:
            self.logger.error(f"爬取失败: {url}, 错误: {str(e)}")
            return []
