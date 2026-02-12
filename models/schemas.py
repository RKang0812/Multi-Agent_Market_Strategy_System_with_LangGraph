"""
Data models for marketing strategy system
营销策略系统的数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# ============ Input Models / 输入模型 ============

class MarketingInput(BaseModel):
    """User input for marketing analysis / 用户输入的营销分析参数"""
    company_domain: str = Field(..., description="Company domain or name / 公司域名或名称")
    industry: str = Field(..., description="Industry sector / 所属行业")
    project_description: str = Field(..., description="Project description / 项目描述")
    target_market: Optional[str] = Field(None, description="Target market (optional) / 目标市场（可选）")


# ============ Output Models / 输出模型 ============

class MarketResearch(BaseModel):
    """Market research results / 市场研究结果"""
    customer_profile: Dict[str, str] = Field(..., description="Customer profile / 客户概况")
    competitors: List[Dict[str, str]] = Field(..., description="List of competitors / 竞争对手列表")
    target_audience: Dict[str, str] = Field(..., description="Target audience profile / 目标受众画像")
    market_positioning: str = Field(..., description="Market positioning / 市场定位")


class TrendAnalysis(BaseModel):
    """Trend analysis results / 趋势分析结果"""
    market_trends: List[str] = Field(..., description="Market trends / 市场趋势")
    tech_trends: List[str] = Field(..., description="Technology trends / 技术趋势")
    consumer_trends: List[str] = Field(..., description="Consumer behavior trends / 消费趋势")
    trend_impact: str = Field(..., description="Impact assessment / 趋势影响评估")
    opportunities: List[str] = Field(..., description="Identified opportunities / 识别的机会点")


class MarketingStrategy(BaseModel):
    """Marketing strategy / 营销策略"""
    name: str = Field(..., description="Strategy name / 策略名称")
    goals: List[str] = Field(..., description="Marketing goals / 营销目标")
    tactics: List[str] = Field(..., description="Tactics / 战术手段")
    channels: List[str] = Field(..., description="Marketing channels / 营销渠道")
    KPIs: List[str] = Field(..., description="Key performance indicators / 关键绩效指标")


class CampaignIdea(BaseModel):
    """Campaign idea / 活动创意"""
    name: str = Field(..., description="Campaign name / 活动名称")
    description: str = Field(..., description="Campaign description / 活动描述")
    audience: str = Field(..., description="Target audience / 目标受众")
    channel: str = Field(..., description="Marketing channel / 营销渠道")


class Copy(BaseModel):
    """Marketing copy / 营销文案"""
    title: str = Field(..., description="Copy title / 文案标题")
    body: str = Field(..., description="Copy body / 文案正文")


class CampaignContent(BaseModel):
    """Campaign content / 活动内容"""
    campaign_ideas: List[CampaignIdea] = Field(..., description="List of campaign ideas / 活动创意列表")
    copies: List[Copy] = Field(..., description="Marketing copies / 营销文案列表")


# ============ Graph State / 图状态 ============

class GraphState(BaseModel):
    """State for LangGraph workflow / LangGraph 工作流状态"""
    
    # Input / 输入
    company_domain: str
    industry: str
    project_description: str
    target_market: Optional[str] = None
    
    # Intermediate results / 中间结果
    market_research: Optional[MarketResearch] = None
    trend_analysis: Optional[TrendAnalysis] = None
    marketing_strategy: Optional[MarketingStrategy] = None
    campaign_content: Optional[CampaignContent] = None
    
    # Metadata / 元数据
    current_step: str = "initialized"
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True