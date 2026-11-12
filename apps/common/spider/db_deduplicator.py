import psycopg2
from datetime import datetime
from contextlib import contextmanager
import os

class DatabaseDeduplicator:
    """基于PostgreSQL的持久化去重"""
    
    def __init__(self, db_host: str = "localhost", db_port: int = 5432, 
                 db_name: str = "smartbrain", db_user: str = "postgres", 
                 db_password: str = "123456"):
        """初始化数据库连接参数"""
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.init_db()
    
    def init_db(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # 创建爬取URL表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS crawled_urls (
                        url TEXT PRIMARY KEY,
                        title TEXT,
                        spider TEXT,
                        crawled_at TIMESTAMP
                    )
                """)
                
                # 创建内容哈希表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS content_hashes (
                        hash TEXT PRIMARY KEY,
                        url TEXT,
                        spider TEXT,
                        crawled_at TIMESTAMP
                    )
                """)
                
                # 创建索引
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_spider_time
                    ON crawled_urls(spider, crawled_at)
                """)
                
                # 提交事务
                conn.commit()
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            yield conn
        finally:
            if conn:
                conn.close()
    
    def is_url_crawled(self, url: str, spider: str = None) -> bool:
        """检查URL是否已爬取"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                if spider:
                    cursor.execute(
                        "SELECT 1 FROM crawled_urls WHERE url = %s AND spider = %s",
                        (url, spider)
                    )
                else:
                    cursor.execute(
                        "SELECT 1 FROM crawled_urls WHERE url = %s",
                        (url,)
                    )
                result = cursor.fetchone()
                return result is not None
    
    def mark_url_crawled(self, url: str, title: str, spider: str):
        """标记URL已爬取"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO crawled_urls (url, title, spider, crawled_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        title = EXCLUDED.title,
                        spider = EXCLUDED.spider,
                        crawled_at = EXCLUDED.crawled_at
                """, (url, title, spider, datetime.now()))
                conn.commit()
    
    def get_duplicate_stats(self, spider: str = None) -> dict:
        """获取重复统计"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                if spider:
                    cursor.execute(
                        "SELECT COUNT(*) FROM crawled_urls WHERE spider = %s",
                        (spider,)
                    )
                else:
                    cursor.execute(
                        "SELECT COUNT(*) FROM crawled_urls"
                    )
                total = cursor.fetchone()[0]
                return {"total_crawled": total}

# 兼容SQLite的实现（用于开发环境）
class SQLiteDeduplicator:
    """基于SQLite的持久化去重"""
    
    def __init__(self, db_path: str = "data/crawled_data/crawled.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """初始化数据库"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crawled_urls (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    spider TEXT,
                    crawled_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS content_hashes (
                    hash TEXT PRIMARY KEY,
                    url TEXT,
                    spider TEXT,
                    crawled_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_spider_time
                ON crawled_urls(spider, crawled_at)
            """)
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def is_url_crawled(self, url: str, spider: str = None) -> bool:
        """检查URL是否已爬取"""
        with self.get_connection() as conn:
            if spider:
                result = conn.execute(
                    "SELECT 1 FROM crawled_urls WHERE url = ? AND spider = ?",
                    (url, spider)
                ).fetchone()
            else:
                result = conn.execute(
                    "SELECT 1 FROM crawled_urls WHERE url = ?",
                    (url,)
                ).fetchone()
            return result is not None
    
    def mark_url_crawled(self, url: str, title: str, spider: str):
        """标记URL已爬取"""
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO crawled_urls (url, title, spider, crawled_at) VALUES (?, ?, ?, ?)",
                (url, title, spider, datetime.now())
            )
    
    def get_duplicate_stats(self, spider: str = None):
        """获取重复统计"""
        with self.get_connection() as conn:
            if spider:
                total = conn.execute(
                    "SELECT COUNT(*) FROM crawled_urls WHERE spider = ?",
                    (spider,)
                ).fetchone()[0]
            else:
                total = conn.execute(
                    "SELECT COUNT(*) FROM crawled_urls"
                ).fetchone()[0]
            return {"total_crawled": total}

# 根据环境选择去重器
def get_deduplicator(use_postgres: bool = True) -> DatabaseDeduplicator:
    """获取去重器实例"""
    if use_postgres:
        return DatabaseDeduplicator()
    else:
        return SQLiteDeduplicator()
