#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Financial Advisor AI Demo
------------------------
A sophisticated AI-powered financial advisory system using multiple autonomous agents.
"""

import autogen
import sys
from typing import Annotated
from .config import load_config
from .agents import (
    create_advisor_agent,
    create_portfolio_agent,
    create_market_data_agent,
    create_compliance_agent,
    create_user_proxy
)
from .utils import (
    get_customer_profile,
    initialize_llama_index,
    llama_index_query,
    custom_speaker_selection_func
)

def setup_chat_environment():
    """Set up the chat environment with all agents."""
    # Load configuration
    config = load_config()
    if config is None:
        sys.exit(1)
    
    # Initialize LlamaIndex
    index = initialize_llama_index(config["pdf_dir"])
    
    # Create agents
    advisor = create_advisor_agent(config["llm_config"])
    user_proxy = create_user_proxy()
    portfolio_agent = create_portfolio_agent(config["llm_config"])
    market_data_agent = create_market_data_agent(config["llm_config"])
    compliance_agent = create_compliance_agent(config["llm_config"])
    
    # Register functions
    autogen.register_function(
        get_customer_profile,
        caller=advisor,
        executor=user_proxy,
        description="A function to get the customer profile, please input a empty string",
    )

    def query_market_data(query: Annotated[str, "The market data query"]) -> str:
        """Query market data using LlamaIndex."""
        return llama_index_query(query, index)

    autogen.register_function(
        query_market_data,
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
    
    return autogen.GroupChatManager(groupchat=groupchat, llm_config=config["llm_config"])

def main():
    """Main function to run the financial advisor chat."""
    try:
        manager = setup_chat_environment()
        user_proxy = [agent for agent in manager.groupchat.agents if agent.name == "user"][0]
        user_proxy.initiate_chat(
            manager,
            message="I want to review my portfolio and make new investment strategy for 2025"
        )
    except Exception as e:
        print(f"Error running Financial Advisor AI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()