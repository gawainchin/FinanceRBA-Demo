#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Financial Advisor AI Demo
------------------------
A sophisticated AI-powered financial advisory system using multiple autonomous agents.

This module serves as the main entry point for the Financial Advisor AI system,
setting up the chat environment and managing agent interactions.
"""

import autogen
import sys
import logging
from typing import Optional
from .config import load_config
from .agents import (
    create_advisor_agent,
    create_portfolio_agent,
    create_market_data_agent,
    create_risk_assessment_agent,
    create_compliance_agent,
    create_user_proxy
)
from .utils import (
    get_customer_profile,
    initialize_llama_index,
    llama_index_query,
    custom_speaker_selection_func
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_chat_environment() -> Optional[autogen.GroupChatManager]:
    """
    Set up the chat environment with all agents.
    
    Returns:
        Optional[autogen.GroupChatManager]: Configured group chat manager or None if setup fails.
    """
    try:
        # Load configuration
        config = load_config()
        if config is None:
            logger.error("Failed to load configuration")
            return None
        
        # Initialize LlamaIndex
        index = initialize_llama_index(config["pdf_dir"])
        if index is None:
            logger.error("Failed to initialize LlamaIndex")
            return None
        
        # Create agents
        advisor = create_advisor_agent(config["llm_config"])
        user_proxy = create_user_proxy()
        portfolio_agent = create_portfolio_agent(config["llm_config"])
        market_data_agent = create_market_data_agent(config["llm_config"])
        compliance_agent = create_compliance_agent(config["llm_config"])
        risk_assessment_agent = create_risk_assessment_agent(config["llm_config"])

        # Register functions
        autogen.register_function(
            get_customer_profile,
            caller=advisor,
            executor=user_proxy,
            description="A function to get the customer profile, please input an empty string",
        )

        def query_market_data(query: str) -> str:
            """Query market data using LlamaIndex."""
            return llama_index_query(query, index)

        autogen.register_function(
            query_market_data,
            caller=market_data_agent,
            executor=portfolio_agent,
            description="A function to get market insights, please input question for market insights",
        )

        autogen.register_function(
            query_market_data,
            caller=market_data_agent,
            executor=risk_assessment_agent,
            description="A function to get market insights, please input question for market insights",
        )

        # Create group chat
        groupchat = autogen.GroupChat(
            agents=[user_proxy, advisor, portfolio_agent, market_data_agent, compliance_agent, risk_assessment_agent],
            messages=[],
            max_round=30,
            speaker_selection_method=custom_speaker_selection_func
        )
        
        return autogen.GroupChatManager(groupchat=groupchat, llm_config=config["llm_config"])
    
    except Exception as e:
        logger.error(f"Error setting up chat environment: {str(e)}")
        return None

def main() -> None:
    """
    Main function to run the financial advisor.
    
    This function initializes the chat environment and starts the conversation
    with a default investment strategy request.
    """
    try:
        manager = setup_chat_environment()
        if manager is None:
            logger.error("Failed to set up chat environment")
            sys.exit(1)
            
        user_proxy = next(
            (agent for agent in manager.groupchat.agents if agent.name == "user"),
            None
        )
        if user_proxy is None:
            logger.error("User proxy agent not found in group chat")
            sys.exit(1)
            
        user_proxy.initiate_chat(
            manager,
            message="I want to review my portfolio and make new investment strategy for 2025"
        )
        
    except Exception as e:
        logger.error(f"Error running Financial Advisor AI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()