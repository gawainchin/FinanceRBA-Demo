# Financial Advisor RBA (Rule-Based AI)

An intelligent financial advisory system that combines market data analysis, portfolio management, and regulatory compliance using AI agents.

## Features

- **Multi-Agent System**:
  - Financial Advisor Agent: Conducts initial assessment and portfolio planning
  - Portfolio Recommendation Agent: Generates investment strategies
  - Market Data Agent: Provides real-time market insights
  - Regulatory Compliance Agent: Ensures recommendations meet regulatory standards

- **Market Analysis**:
  - Processes market research PDFs
  - Analyzes current market trends
  - Provides data-backed investment insights

- **Portfolio Management**:
  - Custom portfolio recommendations
  - Risk assessment and management
  - Asset allocation strategies

- **Regulatory Compliance**:
  - SEC, MiFID II, FINRA, and GDPR compliance checks
  - Automated compliance verification
  - Regulatory documentation support

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
1. Load and process market research documents
2. Initialize AI agents
3. Start an interactive session for portfolio review and investment strategy

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

## Dependencies

- pyautogen: Multi-agent conversation framework
- llama-index: Document processing and querying
- openai: GPT-4 integration
- python-dotenv: Environment variable management
- Additional LlamaIndex components for embeddings and LLM support

## Configuration

The system uses several key configurations:
- OpenAI GPT-4 for natural language processing
- LlamaIndex for document processing and querying
- Custom speaker selection for multi-agent interactions
- Automated compliance checking workflows

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your chosen license]

## Acknowledgments

- OpenAI for GPT-4 API
- LlamaIndex for document processing capabilities
- AutoGen for multi-agent framework 