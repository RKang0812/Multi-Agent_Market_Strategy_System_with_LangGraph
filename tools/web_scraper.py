"""
Web scraping tool for extracting content from URLs
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WebScraperTool:
    """
    Web scraper for extracting content from websites
    """
    
    def __init__(self):
        """Initialize scraper"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self, url: str, max_length: int = 5000) -> Optional[str]:
        """
        Scrape content from a URL
        
        Args:
            url: URL to scrape
            max_length: Maximum content length
            
        Returns:
            Scraped text content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return text
            
        except Exception as e:
            logger.error(f"Scraping error for {url}: {e}")
            return None
    
    def scrape_company_info(self, domain: str) -> Optional[str]:
        """
        Scrape company information from domain
        """
        url = f"https://{domain}" if not domain.startswith("http") else domain
        return self.scrape(url)


# Create global instance
web_scraper_tool = WebScraperTool()
