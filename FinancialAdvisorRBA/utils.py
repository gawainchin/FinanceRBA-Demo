#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions for the Financial Advisor AI system."""

from typing import Dict, Any, Optional
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from pathlib import Path
import sys
import autogen

def get_customer_profile(name: str = "") -> Dict[str, Any]:
    """
    Get the customer's financial profile.
    
    Args:
        name (str, optional): Customer name. Defaults to empty string.
        
    Returns:
        Dict[str, Any]: Customer financial profile containing income, expenses, and assets.
    """
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

def initialize_llama_index(pdf_dir: Path) -> Optional[VectorStoreIndex]:
    """
    Initialize the LlamaIndex with document data.
    
    Args:
        pdf_dir (Path): Directory containing PDF documents to index.
        
    Returns:
        Optional[VectorStoreIndex]: Initialized index or None if initialization fails.
        
    Raises:
        SystemExit: If the PDF directory does not exist.
    """
    if not pdf_dir.exists():
        print(f"Error: {pdf_dir} directory does not exist.")
        sys.exit(1)
    
    try:
        documents = SimpleDirectoryReader(str(pdf_dir)).load_data()
        return VectorStoreIndex.from_documents(documents)
    except Exception as e:
        print(f"Error initializing LlamaIndex: {str(e)}")
        return None

def llama_index_query(query: str, index: VectorStoreIndex) -> str:
    """
    Query the LlamaIndex engine for financial market insights.

    Args:
        query (str): Natural language question related to financial markets.
        index (VectorStoreIndex): Initialized LlamaIndex instance.

    Returns:
        str: Structured response containing financial insights.
    """
    query_engine = index.as_query_engine()
    result = query_engine.query(query)
    return result.response

def get_agent_by_name(groupchat: autogen.GroupChat, agent_name: str) -> Optional[autogen.Agent]:
    """
    Helper function to get an agent by name from the groupchat.
    
    Args:
        groupchat (autogen.GroupChat): The group chat containing agents.
        agent_name (str): Name of the agent to find.
        
    Returns:
        Optional[autogen.Agent]: The found agent or None if not found.
    """
    try:
        return next(agent for agent in groupchat.agents if agent.name == agent_name)
    except StopIteration:
        return None

def custom_speaker_selection_func(last_speaker: autogen.Agent, groupchat: autogen.GroupChat) -> autogen.Agent:
    """
    Define a customized speaker selection function to control agent interactions.
    
    Args:
        last_speaker (autogen.Agent): The agent who spoke last.
        groupchat (autogen.GroupChat): The group chat containing all agents.
        
    Returns:
        Union[autogen.Agent, str]: The next agent to speak, or a string from ['auto', 'manual', 'random', 'round_robin'].
    """
    messages = groupchat.messages

    # Initial stage - Financial Advisor starts the conversation
    if len(messages) <= 1:
        return get_agent_by_name(groupchat, "FinancialAdvisor")

    # User interaction stage (Approval Handling)
    if last_speaker.name == "user":
        if "APPROVE" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "PortfolioRecommendationAgent")
        elif len(messages) >= 2 and messages[-2]["name"] == "FinancialAdvisor":
            return get_agent_by_name(groupchat, "FinancialAdvisor")
        else:
            return "auto"

    # Portfolio Recommendation Process
    elif last_speaker.name == "PortfolioRecommendationAgent":
        if "PROPOSAL DONE" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "user")
        elif "CHECK NEEDED" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "RegulatoryComplianceAgent")
        elif "RISK EVALUATION NEEDED" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "RiskAssessmentAgent")
        elif "MARKET DATA NEEDED" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "MarketDataAgent")
        else:
            return "auto"

    # Risk Assessment Agent Process
    elif last_speaker.name == "RiskAssessmentAgent":
        if "MARKET DATA REQUIRED" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "MarketDataAgent")
        else:
            return get_agent_by_name(groupchat, "PortfolioRecommendationAgent")

    # Market Data Retrieval (for both Portfolio & Risk Assessment)
    elif last_speaker.name == "MarketDataAgent":
        # Determine the agent that made the request
        if len(messages) >= 2:
            requesting_agent = messages[-2]["name"]
            if requesting_agent == "PortfolioRecommendationAgent":
                return get_agent_by_name(groupchat, "PortfolioRecommendationAgent")
            elif requesting_agent == "RiskAssessmentAgent":
                return get_agent_by_name(groupchat, "RiskAssessmentAgent")
        return "auto"

    # Compliance Review
    elif last_speaker.name == "RegulatoryComplianceAgent":
        if "APPROVED" in messages[-1]["content"] or "REQUIRES CHANGES" in messages[-1]["content"]:
            return get_agent_by_name(groupchat, "PortfolioRecommendationAgent")
        else:
            return "auto"

    # Default Fallback
    return "auto" 