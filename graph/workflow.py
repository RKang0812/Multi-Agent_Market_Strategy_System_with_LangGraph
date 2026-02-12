"""
LangGraph workflow for marketing strategy system
营销策略系统的 LangGraph 工作流
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
    创建营销策略工作流图
    
    Workflow:
    工作流：
    START -> Market Research -> Trend Analysis -> Strategy Planning -> Content Creation -> END
    开始 -> 市场研究 -> 趋势分析 -> 策略规划 -> 内容创作 -> 结束
    
    Returns:
        Compiled workflow graph / 编译的工作流图
    """
    
    # Define node functions / 定义节点函数
    
    def market_research_node(state: GraphState) -> GraphState:
        """
        Market research node
        市场研究节点
        """
        logger.info("Executing market research node")
        return market_researcher.analyze(state)
    
    def trend_analysis_node(state: GraphState) -> GraphState:
        """
        Trend analysis node
        趋势分析节点
        """
        logger.info("Executing trend analysis node")
        return trend_analyzer.analyze(state)
    
    def strategy_planning_node(state: GraphState) -> GraphState:
        """
        Strategy planning node
        策略规划节点
        """
        logger.info("Executing strategy planning node")
        return strategy_planner.plan(state)
    
    def content_creation_node(state: GraphState) -> GraphState:
        """
        Content creation node
        内容创作节点
        """
        logger.info("Executing content creation node")
        return content_creator.create(state)
    
    # Create workflow graph / 创建工作流图
    workflow = StateGraph(GraphState)
    
    # Add nodes / 添加节点
    workflow.add_node("market_research", market_research_node)
    workflow.add_node("trend_analysis", trend_analysis_node)
    workflow.add_node("strategy_planning", strategy_planning_node)
    workflow.add_node("content_creation", content_creation_node)
    
    # Add edges / 添加边
    workflow.set_entry_point("market_research")
    workflow.add_edge("market_research", "trend_analysis")
    workflow.add_edge("trend_analysis", "strategy_planning")
    workflow.add_edge("strategy_planning", "content_creation")
    workflow.add_edge("content_creation", END)
    
    # Compile the workflow / 编译工作流
    return workflow.compile()


# Create global workflow instance / 创建全局工作流实例
marketing_workflow = create_workflow()
