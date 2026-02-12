"""
Marketing Strategy Analysis System - Main Application

A LangGraph-powered system for comprehensive marketing strategy analysis
"""

import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import streamlit as st
import yaml
from graph.workflow import marketing_workflow
from graph.state import GraphState
from utils.logger import setup_logger
from utils.helpers import validate_input
import logging

# Setup logging
logger = setup_logger()

# Page configuration
st.set_page_config(
    page_title="Marketing Strategy System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1F77B4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-indicator {
        background-color: #E8F4F8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #D4EDDA;
        border-left: 4px solid #28A745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #F8D7DA;
        border-left: 4px solid #DC3545;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def load_examples():
    """
    Load example data from YAML
    """
    try:
        with open('config/examples.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('examples', [])
    except Exception as e:
        logger.error(f"Failed to load examples: {e}")
        return []


def display_header():
    """
    Display application header
    """
    st.markdown('<div class="main-header">🎯 Marketing Strategy Analysis System</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Market Research, Trend Analysis & Strategy Planning</div>', 
                unsafe_allow_html=True)
    st.markdown("---")


def display_input_form():
    """
    Display input form
    
    Returns:
        Tuple of (company_domain, industry, project_description, target_market)
    """
    st.subheader("📝 Input Your Marketing Project")

    # Check if example data is loaded
    if 'example_data' in st.session_state:
        ex = st.session_state['example_data']
        default_domain = ex.get('company_domain', '')
        default_industry = ex.get('industry', 'AI & Automation')
        default_description = ex.get('project_description', '')
        default_market = ex.get('target_market', '')
    else:
        default_domain = ''
        default_industry = 'AI & Automation'
        default_description = ''
        default_market = ''
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_domain = st.text_input(
            "Company Domain",
            value=default_domain,
            placeholder="e.g., yourcompany.com or Your Company Name",
            help="Enter your company domain or name"
        )
        
        industry_options = [
            "AI & Automation",
            "Fashion & Retail",
            "Business Consulting",
            "Financial Technology",
            "Health & Wellness",
            "Technology",
            "E-commerce",
            "SaaS",
            "Education",
            "Manufacturing",
            "Other"
        ]
        industry = st.selectbox(
            "Industry",
            industry_options,
            index=industry_options.index(default_industry) if default_industry in industry_options else 0,
            help="Select your industry"
        )
    
    with col2:
        target_market = st.text_input(
            "Target Market (Optional)",
            value=default_market,
            placeholder="e.g., Enterprise clients in North America",
            help="Specify your target market if known"
        )
    
    project_description = st.text_area(
        "Project Description",
        value=default_description,
        placeholder="Describe your marketing project, goals, and target audience...",
        height=150,
        help="Provide detailed description of your marketing project (minimum 50 characters)"
    )
    
    return company_domain, industry, project_description, target_market


def display_example_loader():
    """
    Display example data loader
    """
    examples = load_examples()
    
    if examples:
        st.sidebar.subheader("📄 Load Example Data")
        
        example_names = [f"{ex['name']}" for ex in examples]
        selected_example = st.sidebar.selectbox(
            "Choose an example",
            [""] + example_names
        )
        
        if selected_example and st.sidebar.button("Load Example"):
            for ex in examples:
                if ex['name'] == selected_example:
                    st.session_state['example_data'] = ex
                    st.rerun()


def run_analysis(company_domain: str, industry: str, project_description: str, target_market: str):
    """
    Run marketing strategy analysis
    """
    # Initialize state
    initial_state: GraphState = {
        "company_domain": company_domain,
        "industry": industry,
        "project_description": project_description,
        "target_market": target_market,
        "market_research": None,
        "trend_analysis": None,
        "marketing_strategy": None,
        "campaign_content": None,
        "current_step": "initialized",
        "error": None
    }
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Market Research
    status_text.markdown('<div class="step-indicator">🔍 Step 1/4: Analyzing market landscape...</div>', 
                        unsafe_allow_html=True)
    progress_bar.progress(25)
    
    try:
        # Execute workflow 
        result = marketing_workflow.invoke(initial_state)
        
        # Check for errors
        if result.get("error"):
            st.error(f"Analysis failed: {result['error']}")
            return None
        
        # Update progress through steps
        progress_bar.progress(100)
        status_text.markdown('<div class="success-box">✅ Analysis completed successfully!</div>', 
                            unsafe_allow_html=True)
        
        return result
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        st.error(f"An error occurred during analysis: {str(e)}")
        return None


def display_results(result: dict):
    """
    Display analysis results in tabs
    """
    if not result:
        return
    
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Market Research",
        "📈 Trend Analysis",
        "🎯 Marketing Strategy",
        "✍️ Campaign Content",
    ])
    
    # Tab 1: Market Research
    with tab1:
        market_research = result.get("market_research")
        if market_research:
            st.markdown("### Customer Profile")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Company Name:**", market_research.customer_profile.get('company_name', 'N/A'))
                st.write("**Industry:**", market_research.customer_profile.get('industry', 'N/A'))
            with col2:
                st.write("**Products/Services:**", market_research.customer_profile.get('products_services', 'N/A'))
                st.write("**Market Position:**", market_research.customer_profile.get('market_position', 'N/A'))
            
            st.markdown("### Target Audience")
            st.write("**Demographics:**", market_research.target_audience.get('demographics', 'N/A'))
            st.write("**Preferences:**", market_research.target_audience.get('preferences', 'N/A'))
            st.write("**Pain Points:**", market_research.target_audience.get('pain_points', 'N/A'))
            st.write("**Behavior:**", market_research.target_audience.get('behavior', 'N/A'))
            
            st.markdown("### Competitors")
            for i, comp in enumerate(market_research.competitors, 1):
                with st.expander(f"Competitor {i}: {comp.get('name', 'N/A')}"):
                    st.write("**Strengths:**", comp.get('strengths', 'N/A'))
                    st.write("**Weaknesses:**", comp.get('weaknesses', 'N/A'))
                    st.write("**Differentiation:**", comp.get('differentiation', 'N/A'))
            
            st.markdown("### Market Positioning")
            st.write(market_research.market_positioning)
    
    # Tab 2: Trend Analysis
    with tab2:
        trend_analysis = result.get("trend_analysis")
        if trend_analysis:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Market Trends")
                for trend in trend_analysis.market_trends:
                    st.write(f"• {trend}")
                
                st.markdown("### 🔮 Technology Trends")
                for trend in trend_analysis.tech_trends:
                    st.write(f"• {trend}")
            
            with col2:
                st.markdown("### 🛍️ Consumer Trends")
                for trend in trend_analysis.consumer_trends:
                    st.write(f"• {trend}")
                
                st.markdown("### 💡 Opportunities")
                for opp in trend_analysis.opportunities:
                    st.write(f"• {opp}")
            
            st.markdown("### Impact Assessment")
            st.info(trend_analysis.trend_impact)
    
    # Tab 3: Marketing Strategy
    with tab3:
        strategy = result.get("marketing_strategy")
        if strategy:
            st.markdown(f"## {strategy.name}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Goals")
                for goal in strategy.goals:
                    st.write(f"• {goal}")
                
                st.markdown("### 🛠️ Tactics")
                for tactic in strategy.tactics:
                    st.write(f"• {tactic}")
            
            with col2:
                st.markdown("### 📺 Channels")
                for channel in strategy.channels:
                    st.write(f"• {channel}")
                
                st.markdown("### 📊 KPIs")
                for kpi in strategy.KPIs:
                    st.write(f"• {kpi}")
    
    # Tab 4: Campaign Content
    with tab4:
        campaign_content = result.get("campaign_content")
        if campaign_content:
            st.markdown("### Campaign Ideas & Copies")
            
            for i, (idea, copy) in enumerate(zip(campaign_content.campaign_ideas, campaign_content.copies), 1):
                with st.expander(f"Campaign {i}: {idea.name}"):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**Campaign Idea**")
                        st.write("**Description:**", idea.description)
                        st.write("**Target Audience:**", idea.audience)
                        st.write("**Channel:**", idea.channel)
                    
                    with col2:
                        st.markdown("**Marketing Copy**")
                        st.write(f"**Title:** {copy.title}")
                        st.write(f"**Body:** {copy.body}")

def main():
    """
    Main application function
    """
    # Display header
    display_header()
    
    # Sidebar / 侧边栏
    with st.sidebar:
        st.markdown("### About")
        st.info("""
        This system uses AI to analyze markets, identify trends, and create comprehensive marketing strategies.
        
        **Workflow:**
        1. Market Research
        2. Trend Analysis
        3. Strategy Planning
        4. Content Creation
        """)
        
        st.markdown("---")
        display_example_loader()
    
    # Display input form
    company_domain, industry, project_description, target_market = display_input_form()
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🔄 Clear", use_container_width=True)
    
    # Clear results
    if clear_button:
        if 'analysis_result' in st.session_state:
            del st.session_state['analysis_result']
        if 'example_data' in st.session_state:
            del st.session_state['example_data']
        st.rerun()
    
    # Run analysis
    if analyze_button:
        # Validate input
        is_valid, error_msg = validate_input(company_domain, industry, project_description)
        
        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("Analyzing... This may take 1-2 minutes"):
                result = run_analysis(company_domain, industry, project_description, target_market)
                if result:
                    st.session_state['analysis_result'] = result
                    st.success("Analysis completed!")
    
    # Display results if available
    if 'analysis_result' in st.session_state:
        display_results(st.session_state['analysis_result'])


if __name__ == "__main__":
    main()
