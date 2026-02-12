"""
Trend Analyzer Agent
趋势分析 Agent
Analyzes market, technology, and consumer trends
分析市场、技术和消费趋势
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
    用于识别市场趋势和机会的趋势分析 Agent
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        Initialize trend analyzer agent
        初始化趋势分析 Agent
        
        Args:
            model_name: OpenAI model name / OpenAI 模型名称
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.4,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Trend Analysis Expert specializing in market intelligence and future forecasting.
Your goal is to identify current trends, predict future developments, and spot opportunities.

你是趋势分析专家，擅长市场情报和未来预测。
你的目标是识别当前趋势、预测未来发展并发现机会。

Based on the market research and search results, analyze:
基于市场研究和搜索结果，分析：

1. Market Trends: Industry growth, market dynamics, emerging segments
   市场趋势：行业增长、市场动态、新兴细分市场
2. Technology Trends: Emerging technologies, digital transformation, innovation
   技术趋势：新兴技术、数字化转型、创新
3. Consumer Trends: Behavior changes, preference shifts, new demands
   消费趋势：行为变化、偏好转变、新需求
4. Trend Impact: How trends affect the customer's business
   趋势影响：趋势如何影响客户业务
5. Opportunities: Market gaps, growth areas based on trends
   机会点：基于趋势的市场空白、增长领域

Return your analysis in valid JSON format:
以有效的 JSON 格式返回你的分析：

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

IMPORTANT: Return ONLY valid JSON, no markdown formatting or additional text.
重要：只返回有效的 JSON，不要使用 markdown 格式或额外文本。"""),
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
        分析市场趋势
        
        Args:
            state: Current graph state / 当前图状态
            
        Returns:
            Updated state with trend analysis / 包含趋势分析的更新状态
        """
        try:
            logger.info("Starting trend analysis...")
            
            # Search for market trends / 搜索市场趋势
            industry = state.get("industry", "")
            trend_results = web_search_tool.search_market_trends(industry)
            
            # Format market research / 格式化市场研究
            market_research = state.get("market_research")
            market_research_text = self._format_market_research(market_research)
            
            # Format trend search results / 格式化趋势搜索结果
            trend_results_text = self._format_trend_results(trend_results)
            
            # Generate analysis / 生成分析
            chain = self.prompt | self.llm
            response = chain.invoke({
                "industry": state.get("industry", ""),
                "company_domain": state.get("company_domain", ""),
                "market_research": market_research_text,
                "trend_results": trend_results_text
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
            
            # Create TrendAnalysis object / 创建 TrendAnalysis 对象
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
        格式化市场研究用于提示词
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
        格式化趋势搜索结果用于提示词
        """
        formatted = ""
        for i, result in enumerate(trend_results[:5], 1):
            formatted += f"\n{i}. {result.get('title', '')}\n"
            formatted += f"   {result.get('snippet', '')}\n"
        return formatted


# Create global instance / 创建全局实例
trend_analyzer = TrendAnalyzerAgent()