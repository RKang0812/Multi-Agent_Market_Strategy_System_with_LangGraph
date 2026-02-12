"""
Web scraping tool for extracting content from URLs
从 URL 提取内容的网页抓取工具
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WebScraperTool:
    """
    Web scraper for extracting content from websites
    从网站提取内容的网页抓取器
    """
    
    def __init__(self):
        """Initialize scraper / 初始化抓取器"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self, url: str, max_length: int = 5000) -> Optional[str]:
        """
        Scrape content from a URL
        从 URL 抓取内容
        
        Args:
            url: URL to scrape / 要抓取的 URL
            max_length: Maximum content length / 最大内容长度
            
        Returns:
            Scraped text content / 抓取的文本内容
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            # 移除 script 和 style 元素
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content / 获取文本内容
            text = soup.get_text()
            
            # Clean up text / 清理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long / 如果太长则截断
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return text
            
        except Exception as e:
            logger.error(f"Scraping error for {url}: {e}")
            return None
    
    def scrape_company_info(self, domain: str) -> Optional[str]:
        """
        Scrape company information from domain
        从域名抓取公司信息
        """
        url = f"https://{domain}" if not domain.startswith("http") else domain
        return self.scrape(url)


# Create global instance / 创建全局实例
web_scraper_tool = WebScraperTool()
