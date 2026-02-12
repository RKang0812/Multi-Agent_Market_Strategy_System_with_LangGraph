"""
Graph state definition for LangGraph workflow
LangGraph 工作流的图状态定义
"""

from typing import TypedDict, Optional
from models.schemas import (
    MarketResearch,
    TrendAnalysis,
    MarketingStrategy,
    CampaignContent
)


class GraphState(TypedDict):
    """
    State for the marketing strategy workflow graph
    营销策略工作流图的状态
    """
    
    # Input fields / 输入字段
    company_domain: str
    industry: str
    project_description: str
    target_market: Optional[str]
    
    # Analysis results / 分析结果
    market_research: Optional[MarketResearch]
    trend_analysis: Optional[TrendAnalysis]
    marketing_strategy: Optional[MarketingStrategy]
    campaign_content: Optional[CampaignContent]
    
    # Metadata / 元数据
    current_step: str
    error: Optional[str]
