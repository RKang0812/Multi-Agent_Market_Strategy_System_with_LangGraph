"""
Market Researcher Agent

"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import MarketResearch
from tools.web_search import web_search_tool
from tools.web_scraper import web_scraper_tool
import logging
import json

logger = logging.getLogger(__name__)


class MarketResearcherAgent:
    """
    Market research agent for analyzing market landscape
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        Initialize market researcher agent
        
        Args:
            model_name: OpenAI model name
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Lead Market Analyst expert in analyzing companies, competitors, and target audiences.
Your goal is to conduct thorough market research and provide actionable insights.
Based on the provided information and search results, analyze:

1. Customer Profile: Company background, products/services, market position
2. Competitors: Main competitors, their strengths/weaknesses, differentiation
3. Target Audience: Demographics, preferences, pain points, behavior
4. Market Positioning: How the company positions itself in the market

Return your analysis in valid JSON format matching this structure:

{{
  "customer_profile": {{
    "company_name": "string",
    "industry": "string",
    "products_services": "string",
    "market_position": "string"
  }},
  "competitors": [
    {{
      "name": "string",
      "strengths": "string",
      "weaknesses": "string",
      "differentiation": "string"
    }}
  ],
  "target_audience": {{
    "demographics": "string",
    "preferences": "string",
    "pain_points": "string",
    "behavior": "string"
  }},
  "market_positioning": "string"
}}

IMPORTANT: Return ONLY valid JSON, no markdown formatting or additional text."""),
            ("user", """Company Domain: {company_domain}
Industry: {industry}
Project Description: {project_description}
Target Market: {target_market}

Search Results:
{search_results}

Company Website Content:
{company_content}

Please provide comprehensive market research analysis.""")
        ])
    
    def analyze(self, state: dict) -> dict:
        """
        Analyze market landscape
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with market research
        """
        try:
            logger.info("Starting market research analysis...")
            
            # Gather information using tools
            company_domain = state.get("company_domain", "")
            industry = state.get("industry", "")
            
            # Search for competitors
            competitor_results = web_search_tool.search_competitors(company_domain, industry)
            
            # Search for target audience
            audience_results = web_search_tool.search_target_audience(
                industry, 
                state.get("project_description", "")[:100]
            )
            
            # Scrape company website
            company_content = web_scraper_tool.scrape_company_info(company_domain)
            
            # Format search results
            search_results = self._format_search_results(
                competitor_results, 
                audience_results
            )
            
            # Generate analysis
            chain = self.prompt | self.llm
            response = chain.invoke({
                "company_domain": state.get("company_domain", ""),
                "industry": state.get("industry", ""),
                "project_description": state.get("project_description", ""),
                "target_market": state.get("target_market", "Not specified"),
                "search_results": search_results,
                "company_content": company_content or "No content available"
            })
            
            # Parse JSON response
            result_text = response.content.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result_dict = json.loads(result_text)
            
            # Create MarketResearch object
            market_research = MarketResearch(**result_dict)
            
            logger.info("Market research completed successfully")
            
            return {
                **state,
                "market_research": market_research,
                "current_step": "market_research_completed"
            }
            
        except Exception as e:
            logger.error(f"Market research error: {e}")
            return {
                **state,
                "error": f"Market research failed: {str(e)}",
                "current_step": "market_research_failed"
            }
    
    def _format_search_results(self, competitor_results: list, audience_results: list) -> str:
        """
        Format search results for prompt
        """
        formatted = "=== Competitor Information ===\n"
        for i, result in enumerate(competitor_results[:3], 1):
            formatted += f"\n{i}. {result.get('title', '')}\n"
            formatted += f"   {result.get('snippet', '')}\n"
        
        formatted += "\n=== Target Audience Information ===\n"
        for i, result in enumerate(audience_results[:3], 1):
            formatted += f"\n{i}. {result.get('title', '')}\n"
            formatted += f"   {result.get('snippet', '')}\n"
        
        return formatted


# Create global instance / 创建全局实例
market_researcher = MarketResearcherAgent()
