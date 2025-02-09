# Financial Advisor AI

An advanced AI-powered financial advisory system that leverages Large Language Models (LLMs) and autonomous agents to provide sophisticated investment guidance. The system combines real-time market analysis, intelligent portfolio management, and automated regulatory compliance checks through a multi-agent architecture.

## Overview

This system utilizes state-of-the-art AI technologies:
- **GPT-4**: Powers natural language understanding and generation
- **LlamaIndex**: Enables intelligent processing of financial documents
- **AutoGen**: Orchestrates multiple AI agents for complex decision-making
- **Vector Embeddings**: For semantic search and document analysis

## Features

- **Autonomous Multi-Agent System**:
  - Financial Advisor Agent: Leads client interactions and financial planning
  - Portfolio Recommendation Agent: Generates data-driven investment strategies
  - Market Data Agent: Analyzes market trends and provides real-time insights
  - Regulatory Compliance Agent: Ensures adherence to financial regulations

- **Intelligent Market Analysis**:
  - Advanced NLP processing of market research documents
  - Real-time market trend analysis
  - Semantic search across financial reports
  - Data-backed investment insights

- **AI-Driven Portfolio Management**:
  - Personalized portfolio recommendations
  - Dynamic risk assessment and optimization
  - Machine learning-based asset allocation
  - Automated portfolio rebalancing suggestions

- **Automated Compliance**:
  - Real-time regulatory compliance verification
  - SEC, MiFID II, FINRA, and GDPR compliance checks
  - AI-powered documentation review
  - Automated risk assessment

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Market research PDFs in the `sample_pdf` directory

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd FinanceRBA-Demo
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the `FinancialAdvisorRBA` directory
   - Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Market Research Documents:
   The system comes with sample market research PDFs:
   - `Hong_Kong_Major_Report.pdf`: Comprehensive analysis of Hong Kong markets
   - `2025-outlook-greater-china-equities.pdf`: Future outlook for Greater China equities
   - `article_equitymarketcommentaryjanuary2025.pdf`: January 2025 equity market analysis
   - `outlook-2025-building-on-strength.pdf`: 2025 market outlook and strategy
   - `wpb-investment-monthly-jan-25.pdf`: January 2025 investment insights
   
   You can add your own market research PDFs to `FinancialAdvisorRBA/sample_pdf/`

## Usage

Run the financial advisor:
```bash
python FinancialAdvisorRBA/financialdemo.py
```

The system will:
1. Initialize the AI agent network
2. Process and embed market research documents
3. Start an interactive session for personalized financial advice

## Project Structure

```
FinanceRBA-Demo/
├── requirements.txt
└── FinancialAdvisorRBA/
    ├── financialdemo.py
    ├── .env
    └── sample_pdf/
        ├── Hong_Kong_Major_Report.pdf
        ├── 2025-outlook-greater-china-equities.pdf
        ├── article_equitymarketcommentaryjanuary2025.pdf
        ├── outlook-2025-building-on-strength.pdf
        └── wpb-investment-monthly-jan-25.pdf
```

## Technical Stack

- **Core AI Components**:
  - pyautogen: Advanced multi-agent orchestration
  - llama-index: Intelligent document processing and retrieval
  - openai: GPT-4 integration for natural language understanding
  - Vector embeddings for semantic document analysis

- **Supporting Technologies**:
  - python-dotenv: Environment management
  - LlamaIndex components for embeddings and LLM support
  - PDF processing and analysis tools

## System Architecture

The system employs a sophisticated multi-agent architecture where each AI agent specializes in specific aspects of financial advisory:

1. **Financial Advisor Agent**:
   - Manages client interactions
   - Coordinates with other agents
   - Generates comprehensive financial plans

2. **Portfolio Agent**:
   - Analyzes investment opportunities
   - Generates portfolio recommendations
   - Optimizes asset allocation

3. **Market Data Agent**:
   - Processes market research
   - Provides real-time insights
   - Analyzes market trends

4. **Compliance Agent**:
   - Ensures regulatory compliance
   - Validates recommendations
   - Maintains documentation standards

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Acknowledgments

- OpenAI for GPT-4 API and advanced language models
- LlamaIndex for sophisticated document processing capabilities
- AutoGen for autonomous agent framework
- The open-source AI community for various tools and libraries 