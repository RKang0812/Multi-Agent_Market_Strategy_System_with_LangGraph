"""
Market Researcher Agent
市场研究 Agent
Analyzes customers, competitors, and target audience
分析客户、竞争对手和目标受众
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
    用于分析市场格局的市场研究 Agent
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        Initialize market researcher agent
        初始化市场研究 Agent
        
        Args:
            model_name: OpenAI model name / OpenAI 模型名称
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Lead Market Analyst expert in analyzing companies, competitors, and target audiences.
Your goal is to conduct thorough market research and provide actionable insights.

你是一位首席市场分析师，擅长分析公司、竞争对手和目标受众。
你的目标是进行深入的市场研究并提供可操作的见解。

Based on the provided information and search results, analyze:
基于提供的信息和搜索结果，分析：

1. Customer Profile: Company background, products/services, market position
   客户概况：公司背景、产品/服务、市场地位
2. Competitors: Main competitors, their strengths/weaknesses, differentiation
   竞争对手：主要竞争对手、优劣势、差异化
3. Target Audience: Demographics, preferences, pain points, behavior
   目标受众：人口统计、偏好、痛点、行为
4. Market Positioning: How the company positions itself in the market
   市场定位：公司如何在市场中定位自己

Return your analysis in valid JSON format matching this structure:
以有效的 JSON 格式返回你的分析，匹配以下结构：

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

IMPORTANT: Return ONLY valid JSON, no markdown formatting or additional text.
重要：只返回有效的 JSON，不要使用 markdown 格式或额外文本。"""),
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
        分析市场格局
        
        Args:
            state: Current graph state / 当前图状态
            
        Returns:
            Updated state with market research / 包含市场研究的更新状态
        """
        try:
            logger.info("Starting market research analysis...")
            
            # Gather information using tools / 使用工具收集信息
            company_domain = state.get("company_domain", "")
            industry = state.get("industry", "")
            
            # Search for competitors / 搜索竞争对手
            competitor_results = web_search_tool.search_competitors(company_domain, industry)
            
            # Search for target audience / 搜索目标受众
            audience_results = web_search_tool.search_target_audience(
                industry, 
                state.get("project_description", "")[:100]
            )
            
            # Scrape company website / 抓取公司网站
            company_content = web_scraper_tool.scrape_company_info(company_domain)
            
            # Format search results / 格式化搜索结果
            search_results = self._format_search_results(
                competitor_results, 
                audience_results
            )
            
            # Generate analysis / 生成分析
            chain = self.prompt | self.llm
            response = chain.invoke({
                "company_domain": state.get("company_domain", ""),
                "industry": state.get("industry", ""),
                "project_description": state.get("project_description", ""),
                "target_market": state.get("target_market", "Not specified"),
                "search_results": search_results,
                "company_content": company_content or "No content available"
            })
            
            # Parse JSON response / 解析 JSON 响应
            result_text = response.content.strip()
            
            # Remove markdown code blocks if present / 移除可能存在的 markdown 代码块
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result_dict = json.loads(result_text)
            
            # Create MarketResearch object / 创建 MarketResearch 对象
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
        格式化搜索结果用于提示词
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