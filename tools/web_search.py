"""
Web search tool using OpenAI or search APIs
"""

import os
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class WebSearchTool:
    """
    Web search tool for gathering market information
    """
    
    def __init__(self):
        """Initialize search tool"""
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.use_serper = self.serper_api_key is not None
        
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for information
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        if self.use_serper:
            return self._search_with_serper(query, num_results)
        else:
            # Fallback to simulated search if no API key
            logger.warning("No SERPER_API_KEY found, using simulated search")
            return self._simulated_search(query, num_results)
    
    def _search_with_serper(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Search using Serper API
        """
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("organic", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", "")
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Serper search error: {e}")
            return self._simulated_search(query, num_results)
    
    def _simulated_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Simulated search for demo purposes
        """
        # Return simulated results based on query keywords
        results = [
            {
                "title": f"Search result for: {query}",
                "snippet": f"This is a simulated search result. In production, this would return real data from search engines.",
                "link": f"https://example.com/search?q={query.replace(' ', '+')}"
            }
        ]
        return results * min(num_results, 3)  # Return up to 3 simulated results
    
    def search_competitors(self, company_domain: str, industry: str) -> List[Dict[str, str]]:
        """
        Search for competitors in the industry
        """
        query = f"{industry} companies competitors of {company_domain}"
        return self.search(query, num_results=5)
    
    def search_market_trends(self, industry: str) -> List[Dict[str, str]]:
        """
        Search for market trends
        """
        query = f"{industry} market trends 2024 2025"
        return self.search(query, num_results=5)
    
    def search_target_audience(self, industry: str, product: str) -> List[Dict[str, str]]:
        """
        Search for target audience information
        """
        query = f"{industry} {product} target audience demographics"
        return self.search(query, num_results=5)


# Create global instance
web_search_tool = WebSearchTool()
