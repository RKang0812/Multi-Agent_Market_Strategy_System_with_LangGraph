"""
Graph state definition for LangGraph workflow
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
    """
    
    # Input fields
    company_domain: str
    industry: str
    project_description: str
    target_market: Optional[str]
    
    # Analysis results
    market_research: Optional[MarketResearch]
    trend_analysis: Optional[TrendAnalysis]
    marketing_strategy: Optional[MarketingStrategy]
    campaign_content: Optional[CampaignContent]
    
    # Metadata
    current_step: str
    error: Optional[str]
