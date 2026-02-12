"""
Data models for marketing strategy system
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# ============ Input Models ============

class MarketingInput(BaseModel):
    """User input for marketing analysis"""
    company_domain: str = Field(..., description="Company domain or name ")
    industry: str = Field(..., description="Industry sector")
    project_description: str = Field(..., description="Project description")
    target_market: Optional[str] = Field(None, description="Target market (optional)")


# ============ Output Models ============

class MarketResearch(BaseModel):
    """Market research results"""
    customer_profile: Dict[str, str] = Field(..., description="Customer profile")
    competitors: List[Dict[str, str]] = Field(..., description="List of competitors")
    target_audience: Dict[str, str] = Field(..., description="Target audience profile")
    market_positioning: str = Field(..., description="Market positioning")


class TrendAnalysis(BaseModel):
    """Trend analysis results"""
    market_trends: List[str] = Field(..., description="Market trends")
    tech_trends: List[str] = Field(..., description="Technology trends")
    consumer_trends: List[str] = Field(..., description="Consumer behavior trends")
    trend_impact: str = Field(..., description="Impact assessment")
    opportunities: List[str] = Field(..., description="Identified opportunities")


class MarketingStrategy(BaseModel):
    """Marketing strategy"""
    name: str = Field(..., description="Strategy name")
    goals: List[str] = Field(..., description="Marketing goals")
    tactics: List[str] = Field(..., description="Tactics")
    channels: List[str] = Field(..., description="Marketing channels")
    KPIs: List[str] = Field(..., description="Key performance indicators")


class CampaignIdea(BaseModel):
    """Campaign idea"""
    name: str = Field(..., description="Campaign name")
    description: str = Field(..., description="Campaign description")
    audience: str = Field(..., description="Target audience")
    channel: str = Field(..., description="Marketing channel")


class Copy(BaseModel):
    """Marketing copy"""
    title: str = Field(..., description="Copy title")
    body: str = Field(..., description="Copy body")


class CampaignContent(BaseModel):
    """Campaign content"""
    campaign_ideas: List[CampaignIdea] = Field(..., description="List of campaign ideas")
    copies: List[Copy] = Field(..., description="Marketing copies")


# ============ Graph State ============

class GraphState(BaseModel):
    """State for LangGraph workflow / LangGraph"""
    
    # Input
    company_domain: str
    industry: str
    project_description: str
    target_market: Optional[str] = None
    
    # Intermediate results
    market_research: Optional[MarketResearch] = None
    trend_analysis: Optional[TrendAnalysis] = None
    marketing_strategy: Optional[MarketingStrategy] = None
    campaign_content: Optional[CampaignContent] = None
    
    # Metadata
    current_step: str = "initialized"
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
