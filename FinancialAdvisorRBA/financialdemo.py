#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Annotated
import autogen
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, Agent
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import sys
from pathlib import Path

def setup_environment():
    """Set up the environment variables and configurations."""
    # Load environment variables from .env file
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print("Error: .env file not found in the FinancialAdvisorRBA directory.")
        print("Please create a .env file with your OPENAI_API_KEY.")
        sys.exit(1)
    
    load_dotenv(env_path)
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please add your OpenAI API key to the .env file.")
        sys.exit(1)
    
    os.environ['OPENAI_API_KEY'] = api_key
    return {
        "config_list": [{
            "model": "gpt-4o-mini",
            "api_key": api_key
        }]
    }

def initialize_llama_index():
    """Initialize the LlamaIndex with document data."""
    pdf_dir = Path(__file__).parent / "sample_pdf"
    if not pdf_dir.exists():
        print(f"Error: {pdf_dir} directory does not exist.")
        sys.exit(1)
    documents = SimpleDirectoryReader(str(pdf_dir)).load_data()
    return VectorStoreIndex.from_documents(documents)

def llama_index_query(query: Annotated[str, "User query for market data"]) -> str:
    """
    Queries the LlamaIndex engine for financial market insights.

    Args:
        query (str): A natural language question related to financial markets

    Returns:
        str: A structured response containing financial insights
    """
    query_engine = index.as_query_engine()
    result = query_engine.query(query)
    return result.response

def get_customer_profile(
    name: Annotated[str, "Query string where it should be empty."] = ""
) -> dict:
    """Get the customer's financial profile."""
    return {
        "monthly_income": "50000HKD",
        "monthly_expense": "20000HKD",
        "asset": {
            "saving": "100000HKD",
            "fixed_income": "100000HKD",
            "high_risk_stock": "500000HKD",
            "Bitcoin": "100000HKD"
        }
    }

def create_advisor_agent(llm_config):
    """Create the financial advisor agent."""
    return autogen.AssistantAgent(
        name="FinancialAdvisor",
        system_message="""You are an expert financial advisor specializing in personal finance and investment planning.
        Your role is to:
        1. Ask relevant questions about the client's financial situation
        2. Adapt your questions based on their responses
        3. Focus on key areas: financial goals, risk tolerance, income, expenses, investments, and timeline
        4. Stop asking questions once you have gathered sufficient information
        5. Generate a comprehensive financial summary report

        Important guidelines:
        - Ask one or two question at a time
        - Each response should be focused and concise
        - Maintain a professional yet friendly tone
        - You can call the tool to get the customer Profile. But one your get the profile, please dont call again.
        - When you have gathered enough information, generate a report instead of asking more questions (Try to keep the conversaion in 4-5times)
        - Say END if the report is generated
        - Once the report is generated, please ask the User to APPROVE""",
        llm_config=llm_config,
    )

def create_user_proxy():
    """Create the user proxy agent."""
    return autogen.UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        code_execution_config=False,
        is_termination_msg=lambda msg: isinstance(msg.get("content"), str) and "END" in msg["content"].upper()
    )

def create_portfolio_agent(llm_config):
    """Create the portfolio recommendation agent."""
    return autogen.AssistantAgent(
        name="PortfolioRecommendationAgent",
        system_message="""You are an AI-powered financial advisor specializing in investment portfolio optimization.
        Your role is to analyze a financial assessment and generate investment strategies based on market conditions.
        You collaborate with the Market Data Agent to fetch relevant financial insights before making recommendations.

        Capabilities:
        - Interpret financial risk assessments and client investment goals.
        - Generate targeted investment queries for the Market Data Agent.
        - Suggest asset allocations based on market conditions.
        - Optimize portfolio diversification across equities, bonds, commodities, and alternatives.
        - Ensure recommendations align with modern portfolio theory and risk tolerance.

        Guidelines:
        - Always verify market trends before making a recommendation.
        - If unsure about a specific asset, request insights from the Market Data Agent.
        - Provide allocation percentages when suggesting portfolios.

        Example Workflow:
        1. Read Financial Profile: Risk Tolerance = Moderate, Investment Horizon = 10 Years.
        2. Before drafting the recommendaiton, ask Market Data Agent to get more ideas
        2. Generate Queries for Market Data Agent: 'What is the current outlook on Gold prices?'
        3. Retrieve Market Data Insights.
        4. Provide Recommendations:
        5. In the recommendation please provide your rationale on why this is your choice of recommendation
        6. Please send to RegulatoryComplianceAgent for approval before sending to User, in the proposal please say CHECK NEEDED
        7. IF Done drafting the recommendation and Approved by RegulatoryComplianceAgent, please say PROPOSAL DONE""",
        llm_config=llm_config,
    )

def create_market_data_agent(llm_config):
    """Create the market data agent."""
    return autogen.AssistantAgent(
        name="MarketDataAgent",
        system_message="""You are a financial market intelligence assistant.
        Your role is to provide financial market insights,
        economic indicators, and investment trends based on user queries.
        You can retrieve data from LlamaIndex summarize key takeaways.
        Provide data-backed insights in a structured format, including trends, risks, and opportunities.

        Capabilities:
        - Retrieve stock, commodity, and bond market trends.
        - Summarize analyst reports and financial news sentiment.
        - Provide economic data (interest rates, inflation, employment trends).
        - Identify opportunities and risks in different asset classes.
        - Keep responses concise but informative, providing sources if available.

        Examples:
        User: What is the outlook for GOLD in the next quarter?
        Response: Gold prices have risen 5% in the last quarter due to Fed rate expectations. Analysts predict a further 2-3% upside in Q2. Sentiment is bullish.

        User: How is the S&P 500 performing this year?
        Response: The S&P 500 is up 10% YTD, with strong performance in the tech sector. Volatility remains moderate, and earnings reports suggest continued growth.""",
        llm_config=llm_config,
    )

def create_compliance_agent(llm_config):
    """Create the regulatory compliance agent."""
    return autogen.AssistantAgent(
        name="RegulatoryComplianceAgent",
        system_message='''You are the Regulatory Compliance Agent responsible for ensuring AI-driven financial recommendations comply with SEC, MiFID II, FINRA, and GDPR regulations.
        - Validate all investment suggestions for compliance.
        - Flag non-compliant recommendations with clear justifications.
        - Maintain fairness, transparency, and adherence to ethical financial guidelines.

        ### Response Format:
        1. **Verdict:** Compliant / Non-Compliant
        2. **Reason for Decision:** [Detailed explanation based on regulations]
        3. **Applicable Regulation:** [Reference to specific financial laws]
        4. **Suggested Fix (if non-compliant):** [How to adjust the recommendation]''',
        llm_config=llm_config,
    )

def custom_speaker_selection_func(last_speaker: Agent, groupchat: autogen.GroupChat):
    """Define a customized speaker selection function."""
    messages = groupchat.messages

    if len(messages) <= 1:
        return advisor

    if last_speaker is user_proxy:
        if "APPROVE" in messages[-1]["content"]:
            return portfolio_agent
        elif messages[-2]["name"] == "FinancialAdvisor":
            return advisor
        else:
            return "auto"

    elif last_speaker is portfolio_agent:
        if "PROPOSAL DONE" in messages[-1]["content"]:
            return user_proxy
        elif "CHECK NEEDED" in messages[-1]["content"]:
            return compliance_agent
        else:
            return market_data_agent

    elif last_speaker is market_data_agent:
        return portfolio_agent

    elif last_speaker is compliance_agent:
        return portfolio_agent

    else:
        return "auto"

def setup_chat_environment():
    """Set up the chat environment with all agents."""
    llm_config = setup_environment()
    
    global advisor, user_proxy, portfolio_agent, market_data_agent, compliance_agent, index
    
    # Initialize LlamaIndex
    index = initialize_llama_index()
    
    # Create agents
    advisor = create_advisor_agent(llm_config)
    user_proxy = create_user_proxy()
    portfolio_agent = create_portfolio_agent(llm_config)
    market_data_agent = create_market_data_agent(llm_config)
    compliance_agent = create_compliance_agent(llm_config)
    
    # Register functions
    autogen.register_function(
        get_customer_profile,
        caller=advisor,
        executor=user_proxy,
        description="A function to get the customer profile, please input a empty string",
    )

    autogen.register_function(
        llama_index_query,
        caller=market_data_agent,
        executor=portfolio_agent,
        description="A function to get the market insights, please input question for market insights",
    )
    
    # Create group chat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, advisor, portfolio_agent, market_data_agent, compliance_agent],
        messages=[],
        max_round=30,
        speaker_selection_method=custom_speaker_selection_func
    )
    
    return autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

def main():
    """Main function to run the financial advisor chat."""
    manager = setup_chat_environment()
    user_proxy.initiate_chat(
        manager,
        message="I want to review my portfolio and make new investment strategy for 2025"
    )

if __name__ == "__main__":
    main()