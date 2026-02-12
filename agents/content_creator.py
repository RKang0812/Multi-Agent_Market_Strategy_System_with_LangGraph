"""
Content Creator Agent

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
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize content creator agent
        
        Args:
            model_name: OpenAI model name
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Creative Content Creator expert in crafting compelling marketing campaigns.
Your goal is to create innovative campaign ideas and persuasive marketing copies.

Based on the marketing strategy, create:

1. Campaign Ideas (5): Innovative, engaging concepts aligned with strategy
2. Marketing Copies (5): Compelling copy for each campaign idea

Each campaign should:
每个活动应该：
- Be innovative and memorable
- Target the right audience
- Use appropriate channels
- Align with overall strategy

Each copy should:

- Have an attention-grabbing title
- Include persuasive body text
- Be clear and actionable
- Match the campaign idea

Return your content in valid JSON format:

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
- Return ONLY valid JSON, no markdown formatting"""),
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
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with campaign content
        """
        try:
            logger.info("Starting content creation...")
            
            # Format marketing strategy
            marketing_strategy = state.get("marketing_strategy")
            strategy_text = self._format_strategy(marketing_strategy)
            
            # Format target audience 
            market_research = state.get("market_research")
            audience_text = self._format_audience(market_research)
            
            # Generate content
            chain = self.prompt | self.llm
            response = chain.invoke({
                "project_description": state.get("project_description", ""),
                "marketing_strategy": strategy_text,
                "target_audience": audience_text
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
            
            # Create CampaignContent object
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
        """Format list items"""
        return '\n'.join([f"- {item}" for item in items])


# Create global instance
content_creator = ContentCreatorAgent()
