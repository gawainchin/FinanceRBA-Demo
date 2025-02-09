#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import autogen
from typing import Dict, Any

def create_advisor_agent(llm_config: Dict[str, Any]) -> autogen.AssistantAgent:
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

def create_portfolio_agent(llm_config: Dict[str, Any]) -> autogen.AssistantAgent:
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

def create_market_data_agent(llm_config: Dict[str, Any]) -> autogen.AssistantAgent:
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
        - Keep responses concise but informative, providing sources if available.""",
        llm_config=llm_config,
    )

def create_compliance_agent(llm_config: Dict[str, Any]) -> autogen.AssistantAgent:
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

def create_user_proxy() -> autogen.UserProxyAgent:
    """Create the user proxy agent."""
    return autogen.UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        code_execution_config=False,
        is_termination_msg=lambda msg: isinstance(msg.get("content"), str) and "END" in msg["content"].upper()
    ) 