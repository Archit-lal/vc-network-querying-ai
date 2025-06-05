# SpringBank VC Network Querying AI

An intelligent AI-powered tool for querying and analyzing venture capital network data. This application leverages advanced language models to provide insights about VC networks, investments, and relationships.

## Features

- Interactive query interface for VC network analysis
- Natural language processing of complex network queries
- Integration with multiple data sources (Affinity, Harmonic)
- Real-time data processing and visualization
- User-friendly Streamlit interface

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Affinity API credentials (if using Affinity data source)
- Harmonic API credentials (if using Harmonic data source)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Archit-lal/springbank-vc-network-querying-ai.git
cd springbank-vc-network-querying-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
AFFINITY_API_KEY=your_affinity_api_key
HARMONIC_API_KEY=your_harmonic_api_key
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the interface to:
   - Query VC network data
   - Analyze investment patterns
   - Explore relationships between investors and companies
   - Generate insights about the venture capital ecosystem

## Project Structure

```
springbank-vc-network-querying-ai/
├── src/
│   ├── agent.py          # Main AI agent implementation
│   ├── prompts.py        # System prompts and templates
│   ├── ui.py            # Streamlit UI components
│   └── tools/           # Data source integrations
│       ├── affinity_tools.py
│       ├── harmonic_tools.py
│       └── utils.py
├── tests/               # Test suite
├── app.py              # Main application entry point
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Development

To run tests:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is private and proprietary. All rights reserved.

## Support

For support, please contact the repository maintainers. 