"""
Strategy Planner Agent
策略规划 Agent
Formulates comprehensive marketing strategies
制定全面的营销策略
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import MarketingStrategy
import logging
import json

logger = logging.getLogger(__name__)


class StrategyPlannerAgent:
    """
    Strategy planner agent for creating marketing strategies
    用于创建营销策略的策略规划 Agent
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize strategy planner agent
        初始化策略规划 Agent
        
        Args:
            model_name: OpenAI model name / OpenAI 模型名称
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Chief Marketing Strategist expert in crafting comprehensive marketing strategies.
Your goal is to synthesize research and trends into actionable marketing plans.

你是首席营销策略师，擅长制定全面的营销策略。
你的目标是将研究和趋势综合成可执行的营销计划。

Based on market research and trend analysis, create a marketing strategy with:
基于市场研究和趋势分析，创建包含以下内容的营销策略：

1. Strategy Name: A compelling name for the strategy
   策略名称：策略的吸引人名称
2. Goals: Clear, measurable marketing objectives
   目标：清晰、可衡量的营销目标
3. Tactics: Specific actions to achieve goals
   战术：实现目标的具体行动
4. Channels: Marketing channels to utilize
   渠道：要使用的营销渠道
5. KPIs: Key performance indicators to track success
   KPI：跟踪成功的关键绩效指标

Return your strategy in valid JSON format:
以有效的 JSON 格式返回你的策略：

{{
  "name": "Strategy name that captures the essence",
  "goals": [
    "Goal 1: Specific, measurable objective",
    "Goal 2: Another clear goal",
    "Goal 3: Third strategic goal"
  ],
  "tactics": [
    "Tactic 1: Specific action or approach",
    "Tactic 2: Another tactical element",
    "Tactic 3: Additional tactic",
    "Tactic 4: More tactical details"
  ],
  "channels": [
    "Channel 1: Platform or medium",
    "Channel 2: Another channel",
    "Channel 3: Additional channel"
  ],
  "KPIs": [
    "KPI 1: Metric to measure",
    "KPI 2: Another measurement",
    "KPI 3: Additional KPI",
    "KPI 4: Further tracking metric"
  ]
}}

IMPORTANT: 
- Make sure goals align with identified trends and opportunities
- Tactics should be specific and actionable
- Channels should match target audience preferences
- KPIs should be measurable and relevant
- Return ONLY valid JSON, no markdown formatting

重要：
- 确保目标与识别的趋势和机会一致
- 战术应具体且可执行
- 渠道应匹配目标受众偏好
- KPI 应可衡量且相关
- 只返回有效的 JSON，不要使用 markdown 格式"""),
            ("user", """Project Description: {project_description}
Target Market: {target_market}

Market Research Summary:
{market_research}

Trend Analysis Summary:
{trend_analysis}

Please create a comprehensive marketing strategy that leverages these insights.""")
        ])
    
    def plan(self, state: dict) -> dict:
        """
        Create marketing strategy
        创建营销策略
        
        Args:
            state: Current graph state / 当前图状态
            
        Returns:
            Updated state with marketing strategy / 包含营销策略的更新状态
        """
        try:
            logger.info("Starting strategy planning...")
            
            # Format market research / 格式化市场研究
            market_research = state.get("market_research")
            market_research_text = self._format_market_research(market_research)
            
            # Format trend analysis / 格式化趋势分析
            trend_analysis = state.get("trend_analysis")
            trend_analysis_text = self._format_trend_analysis(trend_analysis)
            
            # Generate strategy / 生成策略
            chain = self.prompt | self.llm
            response = chain.invoke({
                "project_description": state.get("project_description", ""),
                "target_market": state.get("target_market", "Not specified"),
                "market_research": market_research_text,
                "trend_analysis": trend_analysis_text
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
            
            # Create MarketingStrategy object / 创建 MarketingStrategy 对象
            marketing_strategy = MarketingStrategy(**result_dict)
            
            logger.info("Strategy planning completed successfully")
            
            return {
                **state,
                "marketing_strategy": marketing_strategy,
                "current_step": "strategy_planning_completed"
            }
            
        except Exception as e:
            logger.error(f"Strategy planning error: {e}")
            return {
                **state,
                "error": f"Strategy planning failed: {str(e)}",
                "current_step": "strategy_planning_failed"
            }
    
    def _format_market_research(self, market_research) -> str:
        """
        Format market research for prompt
        格式化市场研究用于提示词
        """
        if not market_research:
            return "No market research available"
        
        formatted = f"""
Customer Profile:
- Company: {market_research.customer_profile.get('company_name', 'N/A')}
- Products/Services: {market_research.customer_profile.get('products_services', 'N/A')}
- Market Position: {market_research.customer_profile.get('market_position', 'N/A')}

Target Audience:
- Demographics: {market_research.target_audience.get('demographics', 'N/A')}
- Preferences: {market_research.target_audience.get('preferences', 'N/A')}
- Pain Points: {market_research.target_audience.get('pain_points', 'N/A')}

Market Positioning: {market_research.market_positioning}

Key Competitors: {', '.join([c.get('name', 'N/A') for c in market_research.competitors[:3]])}
"""
        return formatted
    
    def _format_trend_analysis(self, trend_analysis) -> str:
        """
        Format trend analysis for prompt
        格式化趋势分析用于提示词
        """
        if not trend_analysis:
            return "No trend analysis available"
        
        formatted = f"""
Market Trends:
{self._format_list(trend_analysis.market_trends)}

Technology Trends:
{self._format_list(trend_analysis.tech_trends)}

Consumer Trends:
{self._format_list(trend_analysis.consumer_trends)}

Trend Impact: {trend_analysis.trend_impact}

Identified Opportunities:
{self._format_list(trend_analysis.opportunities)}
"""
        return formatted
    
    def _format_list(self, items: list) -> str:
        """Format list items / 格式化列表项"""
        return '\n'.join([f"- {item}" for item in items])


# Create global instance / 创建全局实例
strategy_planner = StrategyPlannerAgent()