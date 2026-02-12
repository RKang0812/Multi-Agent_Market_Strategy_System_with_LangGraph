"""
LangGraph workflow for marketing strategy system
"""

from langgraph.graph import StateGraph, END
from graph.state import GraphState
from agents.market_researcher import market_researcher
from agents.trend_analyzer import trend_analyzer
from agents.strategy_planner import strategy_planner
from agents.content_creator import content_creator
import logging

logger = logging.getLogger(__name__)


def create_workflow() -> StateGraph:
    """
    Create the marketing strategy workflow graph
    
    Workflow:
    START -> Market Research -> Trend Analysis -> Strategy Planning -> Content Creation -> END
    
    Returns:
        Compiled workflow graph
    """
    
    # Define node functions
    
    def market_research_node(state: GraphState) -> GraphState:
        """
        Market research node
        """
        logger.info("Executing market research node")
        return market_researcher.analyze(state)
    
    def trend_analysis_node(state: GraphState) -> GraphState:
        """
        Trend analysis node
        """
        logger.info("Executing trend analysis node")
        return trend_analyzer.analyze(state)
    
    def strategy_planning_node(state: GraphState) -> GraphState:
        """
        Strategy planning node
        """
        logger.info("Executing strategy planning node")
        return strategy_planner.plan(state)
    
    def content_creation_node(state: GraphState) -> GraphState:
        """
        Content creation node
        """
        logger.info("Executing content creation node")
        return content_creator.create(state)
    
    # Create workflow graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("market_research", market_research_node)
    workflow.add_node("trend_analysis", trend_analysis_node)
    workflow.add_node("strategy_planning", strategy_planning_node)
    workflow.add_node("content_creation", content_creation_node)
    
    # Add edges
    workflow.set_entry_point("market_research")
    workflow.add_edge("market_research", "trend_analysis")
    workflow.add_edge("trend_analysis", "strategy_planning")
    workflow.add_edge("strategy_planning", "content_creation")
    workflow.add_edge("content_creation", END)
    
    # Compile the workflow 
    return workflow.compile()


# Create global workflow instance
marketing_workflow = create_workflow()
