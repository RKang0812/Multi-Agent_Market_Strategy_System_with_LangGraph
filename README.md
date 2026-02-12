# Multi-Agent Market Strategy System with LangGraph

A lightweight engineering project demonstrating how to design and orchestrate a multi-agent LLM system for structured business analysis using LangGraph and Streamlit.

This project focuses on system architecture, agent collaboration, and reproducible workflows rather than marketing presentation.

[▶ Watch the Demo](demo.mp4)

## Project Overview

This application builds a multi-step workflow that generates a complete marketing strategy report from structured user input.

It uses multiple specialized LLM agents coordinated by LangGraph to perform market research, trend analysis, strategy formulation, and content generation in sequence.

The goal of the project is to demonstrate:
- Multi-agent orchestration with LangGraph
- Prompt and workflow design for complex reasoning tasks
- Clear separation of responsibilities between agents
- Practical integration of LLM systems with a simple web UI

## Features

- Market and competitor analysis
- Trend identification (market, technology, consumer behavior)
- Strategy planning with goals, channels, and KPIs
- Campaign and copy generation
- Streamlit-based interactive interface
- Modular agent-based architecture

## Architecture

```
User Input (Streamlit Interface)
    ↓
LangGraph Workflow Orchestration
    ↓
┌─────────────────────────────┐
│  Market Research Node       │  ← Customer, Competitor, Audience Analysis
│  (market_researcher.py)     │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  Trend Analysis Node        │  ← Market, Tech, Consumer Trends
│  (trend_analyzer.py)        │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  Strategy Planning Node     │  ← Goals, Tactics, Channels, KPIs
│  (strategy_planner.py)      │
└──────────┬──────────────────┘
           ↓
┌─────────────────────────────┐
│  Content Creation Node      │  ← Campaign Ideas & Copies
│  (content_creator.py)       │
└──────────┬──────────────────┘
           ↓
    Streamlit Display
```

## Project Structure

```
marketing_strategy_system/
│
├── main.py                    
├── requirements.txt         
├── .env.example                
├── .gitignore                  
│
├── agents/                    
│   ├── market_researcher.py   
│   ├── trend_analyzer.py     
│   ├── strategy_planner.py  
│   └── content_creator.py     
│
├── graph/                    
│   ├── state.py                
│   └── workflow.py          
│
├── models/                    
│   └── schemas.py            
│
├── tools/                     
│   ├── web_search.py        
│   └── web_scraper.py         
│
├── config/                  
│   └── examples.yaml          
│
└── utils/                   
    ├── logger.py              
    └── helpers.py             
               
```

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


## Configuration

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional
```

## Running the Application 

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`


## AI Agents

### 1. Market Researcher Agent
- **Model**: GPT-4o-mini
- **Function**: Analyzes customers, competitors, and target audiences
- **Tools**: Web Search, Web Scraper

### 2. Trend Analyzer Agent
- **Model**: GPT-4o-mini
- **Function**: Identifies market, technology, and consumer trends
- **Tools**: Web Search

### 3. Strategy Planner Agent
- **Model**: GPT-4o
- **Function**: Formulates comprehensive marketing strategies
- **Tools**: None (synthesis-based)

### 4. Content Creator Agent
- **Model**: GPT-4o
- **Function**: Creates campaign ideas and marketing copies
- **Tools**: None (creative generation)
