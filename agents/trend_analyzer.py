"""
Trend Analyzer Agent
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import TrendAnalysis
from tools.web_search import web_search_tool
import logging
import json

logger = logging.getLogger(__name__)


class TrendAnalyzerAgent:
    """
    Trend analyzer agent for identifying market trends and opportunities
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        Initialize trend analyzer agent
        
        Args:
            model_name: OpenAI model name
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.4,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Trend Analysis Expert specializing in market intelligence and future forecasting.
Your goal is to identify current trends, predict future developments, and spot opportunities.
Based on the market research and search results, analyze:

1. Market Trends: Industry growth, market dynamics, emerging segments
2. Technology Trends: Emerging technologies, digital transformation, innovation
3. Consumer Trends: Behavior changes, preference shifts, new demands
4. Trend Impact: How trends affect the customer's business
5. Opportunities: Market gaps, growth areas based on trends

Return your analysis in valid JSON format:

{{
  "market_trends": [
    "Trend 1",
    "Trend 2",
    "Trend 3"
  ],
  "tech_trends": [
    "Tech trend 1",
    "Tech trend 2",
    "Tech trend 3"
  ],
  "consumer_trends": [
    "Consumer trend 1",
    "Consumer trend 2",
    "Consumer trend 3"
  ],
  "trend_impact": "Detailed analysis of how these trends impact the customer's business and market positioning",
  "opportunities": [
    "Opportunity 1 based on trends",
    "Opportunity 2 based on trends",
    "Opportunity 3 based on trends"
  ]
}}

IMPORTANT: Return ONLY valid JSON, no markdown formatting or additional text."""),
            ("user", """Industry: {industry}
Company Domain: {company_domain}

Market Research Results:
{market_research}

Trend Search Results:
{trend_results}

Please provide comprehensive trend analysis and identify opportunities.""")
        ])
    
    def analyze(self, state: dict) -> dict:
        """
        Analyze market trends
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with trend analysis
        """
        try:
            logger.info("Starting trend analysis...")
            
            # Search for market trends
            industry = state.get("industry", "")
            trend_results = web_search_tool.search_market_trends(industry)
            
            # Format market research
            market_research = state.get("market_research")
            market_research_text = self._format_market_research(market_research)
            
            # Format trend search results
            trend_results_text = self._format_trend_results(trend_results)
            
            # Generate analysis
            chain = self.prompt | self.llm
            response = chain.invoke({
                "industry": state.get("industry", ""),
                "company_domain": state.get("company_domain", ""),
                "market_research": market_research_text,
                "trend_results": trend_results_text
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
            
            # Create TrendAnalysis object
            trend_analysis = TrendAnalysis(**result_dict)
            
            logger.info("Trend analysis completed successfully")
            
            return {
                **state,
                "trend_analysis": trend_analysis,
                "current_step": "trend_analysis_completed"
            }
            
        except Exception as e:
            logger.error(f"Trend analysis error: {e}")
            return {
                **state,
                "error": f"Trend analysis failed: {str(e)}",
                "current_step": "trend_analysis_failed"
            }
    
    def _format_market_research(self, market_research) -> str:
        """
        Format market research for prompt
        """
        if not market_research:
            return "No market research available"
        
        formatted = f"""
Customer: {market_research.customer_profile.get('company_name', 'N/A')}
Industry: {market_research.customer_profile.get('industry', 'N/A')}
Market Position: {market_research.customer_profile.get('market_position', 'N/A')}

Target Audience:
- Demographics: {market_research.target_audience.get('demographics', 'N/A')}
- Preferences: {market_research.target_audience.get('preferences', 'N/A')}
- Pain Points: {market_research.target_audience.get('pain_points', 'N/A')}

Top Competitors:
"""
        for comp in market_research.competitors[:3]:
            formatted += f"- {comp.get('name', 'N/A')}: {comp.get('differentiation', 'N/A')}\n"
        
        return formatted
    
    def _format_trend_results(self, trend_results: list) -> str:
        """
        Format trend search results for prompt
        """
        formatted = ""
        for i, result in enumerate(trend_results[:5], 1):
            formatted += f"\n{i}. {result.get('title', '')}\n"
            formatted += f"   {result.get('snippet', '')}\n"
        return formatted


# Create global instance
trend_analyzer = TrendAnalyzerAgent()
