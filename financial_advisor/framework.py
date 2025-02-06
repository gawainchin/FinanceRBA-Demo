from crewai import Agent, Task, Crew
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Initialize LLM (choose one)
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define custom tools
@tool
def financial_data_analysis(query: str) -> str:
    """Fetch and analyze real-time financial data"""
    # Connect to financial APIs (e.g., Alpha Vantage, Yahoo Finance)
    # Implement data analysis logic
    return f"Analysis of {query} shows..."

@tool
def risk_assessment(profile: dict) -> str:
    """Evaluate client risk tolerance and investment suitability"""
    # Implement risk assessment logic
    return "Moderate risk profile recommended"

# Define specialist agents
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide detailed market analysis and investment recommendations",
    backstory="Expert in global markets with 15 years experience at major banks",
    tools=[financial_data_analysis],
    llm=llm,
    verbose=True
)

risk_manager = Agent(
    role="Risk Management Specialist",
    goal="Assess and mitigate investment risks",
    backstory="Former chief risk officer at hedge fund",
    tools=[risk_assessment],
    llm=llm,
    verbose=True
)

client_advisor = Agent(
    role="Client Advisor",
    goal="Translate complex analysis into client-friendly advice",
    backstory="Skilled financial communicator with CFP certification",
    llm=llm,
    verbose=True
)

# Create tasks with context sharing
analysis_task = Task(
    description="Analyze current market conditions for {client_query}",
    agent=financial_analyst,
    expected_output="Detailed market analysis report"
)

risk_task = Task(
    description="Assess risks for {client_query} based on profile {client_profile}",
    agent=risk_manager,
    expected_output="Risk assessment report with mitigation strategies",
    context=[analysis_task]
)

advice_task = Task(
    description="Create client-friendly recommendation based on analysis and risk assessment",
    agent=client_advisor,
    expected_output="Clear investment recommendation with rationale",
    context=[analysis_task, risk_task]
)

# Assemble the crew
financial_crew = Crew(
    agents=[financial_analyst, risk_manager, client_advisor],
    tasks=[analysis_task, risk_task, advice_task],
    verbose=2
)

# Run the crew (example usage)
def get_financial_advice(query: str, profile: dict) -> str:
    return financial_crew.kickoff(
        inputs={
            'client_query': query,
            'client_profile': profile
        }
    ) 