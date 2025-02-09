"""
Financial Advisor AI
------------------

A sophisticated AI-powered financial advisory system using multiple autonomous agents.
This package provides a complete solution for AI-driven financial planning and portfolio management.
"""

__version__ = "1.0.0"
__author__ = "Gawain"

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