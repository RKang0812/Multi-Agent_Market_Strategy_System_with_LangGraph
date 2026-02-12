"""
Content Creator Agent
内容创作 Agent
Creates campaign ideas and marketing copies
创建活动创意和营销文案
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import CampaignContent, CampaignIdea, Copy
import logging
import json

logger = logging.getLogger(__name__)


class ContentCreatorAgent:
    """
    Content creator agent for generating marketing content
    用于生成营销内容的内容创作 Agent
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize content creator agent
        初始化内容创作 Agent
        
        Args:
            model_name: OpenAI model name / OpenAI 模型名称
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Creative Content Creator expert in crafting compelling marketing campaigns.
Your goal is to create innovative campaign ideas and persuasive marketing copies.

你是创意内容创作者，擅长制作引人注目的营销活动。
你的目标是创建创新的活动创意和有说服力的营销文案。

Based on the marketing strategy, create:
基于营销策略，创建：

1. Campaign Ideas (5): Innovative, engaging concepts aligned with strategy
   活动创意（5个）：创新、引人入胜的概念，与策略一致
2. Marketing Copies (5): Compelling copy for each campaign idea
   营销文案（5个）：每个活动创意的引人注目文案

Each campaign should:
每个活动应该：
- Be innovative and memorable / 创新且令人难忘
- Target the right audience / 针对正确的受众
- Use appropriate channels / 使用合适的渠道
- Align with overall strategy / 与整体策略一致

Each copy should:
每个文案应该：
- Have an attention-grabbing title / 有吸引注意力的标题
- Include persuasive body text / 包含有说服力的正文
- Be clear and actionable / 清晰且可操作
- Match the campaign idea / 匹配活动创意

Return your content in valid JSON format:
以有效的 JSON 格式返回你的内容：

{{
  "campaign_ideas": [
    {{
      "name": "Campaign 1 Name",
      "description": "Detailed description of the campaign concept and execution",
      "audience": "Specific target audience segment",
      "channel": "Primary marketing channel (e.g., Social Media, Email, Content Marketing)"
    }},
    ... (4 more campaigns)
  ],
  "copies": [
    {{
      "title": "Attention-grabbing headline for Campaign 1",
      "body": "Compelling body copy that persuades and includes clear call-to-action. Should be 2-3 sentences highlighting value proposition."
    }},
    ... (4 more copies matching the campaigns)
  ]
}}

IMPORTANT: 
- Create exactly 5 campaign ideas and 5 corresponding copies
- Copies should match campaign ideas in order
- Return ONLY valid JSON, no markdown formatting

重要：
- 创建恰好 5 个活动创意和 5 个对应文案
- 文案应按顺序匹配活动创意
- 只返回有效的 JSON，不要使用 markdown 格式"""),
            ("user", """Project Description: {project_description}

Marketing Strategy:
{marketing_strategy}

Target Audience:
{target_audience}

Please create 5 innovative campaign ideas and compelling marketing copies.""")
        ])
    
    def create(self, state: dict) -> dict:
        """
        Create marketing content
        创建营销内容
        
        Args:
            state: Current graph state / 当前图状态
            
        Returns:
            Updated state with campaign content / 包含活动内容的更新状态
        """
        try:
            logger.info("Starting content creation...")
            
            # Format marketing strategy / 格式化营销策略
            marketing_strategy = state.get("marketing_strategy")
            strategy_text = self._format_strategy(marketing_strategy)
            
            # Format target audience / 格式化目标受众
            market_research = state.get("market_research")
            audience_text = self._format_audience(market_research)
            
            # Generate content / 生成内容
            chain = self.prompt | self.llm
            response = chain.invoke({
                "project_description": state.get("project_description", ""),
                "marketing_strategy": strategy_text,
                "target_audience": audience_text
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
            
            # Create CampaignContent object / 创建 CampaignContent 对象
            campaign_ideas = [CampaignIdea(**idea) for idea in result_dict["campaign_ideas"]]
            copies = [Copy(**copy) for copy in result_dict["copies"]]
            
            campaign_content = CampaignContent(
                campaign_ideas=campaign_ideas,
                copies=copies
            )
            
            logger.info("Content creation completed successfully")
            
            return {
                **state,
                "campaign_content": campaign_content,
                "current_step": "content_creation_completed"
            }
            
        except Exception as e:
            logger.error(f"Content creation error: {e}")
            return {
                **state,
                "error": f"Content creation failed: {str(e)}",
                "current_step": "content_creation_failed"
            }
    
    def _format_strategy(self, marketing_strategy) -> str:
        """
        Format marketing strategy for prompt
        格式化营销策略用于提示词
        """
        if not marketing_strategy:
            return "No marketing strategy available"
        
        formatted = f"""
Strategy Name: {marketing_strategy.name}

Goals:
{self._format_list(marketing_strategy.goals)}

Tactics:
{self._format_list(marketing_strategy.tactics)}

Channels:
{self._format_list(marketing_strategy.channels)}

KPIs:
{self._format_list(marketing_strategy.KPIs)}
"""
        return formatted
    
    def _format_audience(self, market_research) -> str:
        """
        Format target audience for prompt
        格式化目标受众用于提示词
        """
        if not market_research:
            return "No audience information available"
        
        audience = market_research.target_audience
        formatted = f"""
Demographics: {audience.get('demographics', 'N/A')}
Preferences: {audience.get('preferences', 'N/A')}
Pain Points: {audience.get('pain_points', 'N/A')}
Behavior: {audience.get('behavior', 'N/A')}
"""
        return formatted
    
    def _format_list(self, items: list) -> str:
        """Format list items / 格式化列表项"""
        return '\n'.join([f"- {item}" for item in items])


# Create global instance / 创建全局实例
content_creator = ContentCreatorAgent()
