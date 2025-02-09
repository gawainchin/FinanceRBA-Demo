#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Any
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from pathlib import Path
import sys
import autogen

def get_customer_profile(name: str = "") -> Dict[str, Any]:
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

def initialize_llama_index(pdf_dir: Path) -> VectorStoreIndex:
    """Initialize the LlamaIndex with document data."""
    if not pdf_dir.exists():
        print(f"Error: {pdf_dir} directory does not exist.")
        sys.exit(1)
    documents = SimpleDirectoryReader(str(pdf_dir)).load_data()
    return VectorStoreIndex.from_documents(documents)

def llama_index_query(query: str, index: VectorStoreIndex) -> str:
    """
    Queries the LlamaIndex engine for financial market insights.

    Args:
        query (str): A natural language question related to financial markets
        index (VectorStoreIndex): The initialized LlamaIndex instance

    Returns:
        str: A structured response containing financial insights
    """
    query_engine = index.as_query_engine()
    result = query_engine.query(query)
    return result.response

def custom_speaker_selection_func(last_speaker: autogen.Agent, groupchat: autogen.GroupChat) -> autogen.Agent:
    """Define a customized speaker selection function."""
    messages = groupchat.messages

    if len(messages) <= 1:
        return groupchat.agents[1]  # Return the advisor agent

    if last_speaker.name == "user":
        if "APPROVE" in messages[-1]["content"]:
            return next(agent for agent in groupchat.agents if agent.name == "PortfolioRecommendationAgent")
        elif len(messages) >= 2 and messages[-2]["name"] == "FinancialAdvisor":
            return next(agent for agent in groupchat.agents if agent.name == "FinancialAdvisor")
        else:
            return "auto"

    elif last_speaker.name == "PortfolioRecommendationAgent":
        if "PROPOSAL DONE" in messages[-1]["content"]:
            return next(agent for agent in groupchat.agents if agent.name == "user")
        elif "CHECK NEEDED" in messages[-1]["content"]:
            return next(agent for agent in groupchat.agents if agent.name == "RegulatoryComplianceAgent")
        else:
            return next(agent for agent in groupchat.agents if agent.name == "MarketDataAgent")

    elif last_speaker.name == "MarketDataAgent":
        return next(agent for agent in groupchat.agents if agent.name == "PortfolioRecommendationAgent")

    elif last_speaker.name == "RegulatoryComplianceAgent":
        return next(agent for agent in groupchat.agents if agent.name == "PortfolioRecommendationAgent")

    else:
        return "auto" 