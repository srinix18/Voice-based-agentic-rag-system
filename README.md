# Voice-Based Agentic RAG System

A voice-enabled financial literacy assistant powered by Google's Agent Development Kit (ADK), Gemini 2.0, and RAG (Retrieval-Augmented Generation) using NCFE e-Library content.

## Features

- 🎤 **Voice Input/Output**: Ask questions via voice or text, get spoken responses
- 🤖 **AI-Powered Agent**: Built with Google ADK and Gemini 2.0 Flash
- 📚 **RAG System**: Retrieves accurate information from NCFE e-Library PDFs
- 🔍 **FAISS Vector Search**: Fast semantic search with sentence-transformers
- 🛡️ **Hallucination Prevention**: Only answers from knowledge base, no fabrication
- 🌐 **Web UI**: Interactive chat interface at localhost:5000

## Architecture

```
User Question (Voice/Text)
    ↓
Google ADK Agent (Gemini 2.0)
    ↓
RAG Search Tool (FAISS + Embeddings)
    ↓
NCFE e-Library PDF Knowledge Base
    ↓
AI Response (Voice/Text)
```

## Tech Stack

- **Google ADK v1.17.0**: Agent orchestration framework
- **Google Gemini 2.0 Flash Exp**: Large language model
- **FAISS-CPU v1.7.4**: Vector similarity search
- **sentence-transformers v5.1.2**: Text embeddings (all-MiniLM-L6-v2)
- **PyPDF2 v3.0.0**: PDF text extraction
- **Python 3.12+**: Runtime environment

## Installation

### Prerequisites

- Python 3.12 or higher
- Google API Key ([Get one here](https://aistudio.google.com/apikey))
- Windows PowerShell (or bash on Linux/Mac)

### Setup

1. **Clone the repository**

```powershell
git clone https://github.com/srinix18/Voice-based-agentic-rag-system.git
cd Voice-based-agentic-rag-system/financial_rag_agent
```

2. **Create virtual environment**

```powershell
python -m venv ../.venv
& "../.venv/Scripts/Activate.ps1"  # Windows
# source ../.venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**

```powershell
pip install -r requirements.txt
```

4. **Set up environment variables**
   Create a `.env` file in `financial_rag_agent/` directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

5. **Add NCFE PDFs**
   Place your NCFE e-Library PDF files in:

```
financial_rag_agent/data/ncfe_books/
```

Example PDF used: `BEAWARE07032022.pdf` (Financial fraud awareness guide)

## Usage

### Start the Voice-Enabled Web UI

```powershell
cd financial_rag_agent
& "../.venv/Scripts/Activate.ps1"
adk web agents --port 5000
```

Then open your browser to: **http://127.0.0.1:5000**

### Using the Interface

- **Text Input**: Type your question in the chat box
- **Voice Input**: Click the microphone 🎤 icon and speak
- **Voice Output**: Responses are automatically spoken (ensure speakers are on)

### Example Questions

- "What is phishing?"
- "Tell me about credit card fraud"
- "How can I protect myself from screen sharing scams?"
- "What are common types of financial fraud?"

### CLI Mode (Text-only testing)

```powershell
python main_agent.py
```

## Project Structure

```
financial_rag_agent/
├── agents/
│   └── financial_agent/
│       ├── __init__.py
│       └── agent.py              # ADK agent with voice support
├── tools/
│   └── financial_rag_search.py   # RAG search function
├── data/
│   ├── ncfe_books/               # PDF knowledge base
│   └── faiss_index.pkl           # Vector index cache
├── main_agent.py                 # CLI version for testing
├── test_e2e.py                   # End-to-end test suite
├── requirements.txt              # Python dependencies
└── .env                          # API keys (not in repo)
```

## How It Works

### 1. PDF Processing

- Extracts text from NCFE e-Library PDFs
- Splits into 500-word chunks with 50-word overlap
- Creates embeddings using all-MiniLM-L6-v2 model

### 2. Vector Search (FAISS)

- Indexes chunks in FAISS for fast similarity search
- User query → embedding → find top 3 relevant chunks
- Returns sources with full context

### 3. Agent Decision Making

- Gemini 2.0 receives user question + system instructions
- Decides to call `search_financial_knowledge_base` tool
- Analyzes retrieved context and formulates answer
- Cites sources (PDF name and page context)

### 4. Voice Output

- ADK automatically converts text response to speech
- Uses Google's TTS with natural voice
- Streamed to browser via WebSocket

## Configuration

### Agent Settings (`agents/financial_agent/agent.py`)

```python
root_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='financial_rag_agent',
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_financial_knowledge_base]
)
```

### RAG Parameters (`tools/financial_rag_search.py`)

```python
CHUNK_SIZE = 500        # words per chunk
CHUNK_OVERLAP = 50      # word overlap between chunks
TOP_K_RESULTS = 3       # number of results to retrieve
```

## Testing

Run the comprehensive test suite:

```powershell
python test_e2e.py
```

Tests include:

- ✅ Gemini API connectivity
- ✅ RAG retrieval quality
- ✅ Token configuration
- ✅ PDF data loading
- ✅ Full agent integration
- ✅ Edge case handling

## Safety & Guidelines

The agent follows strict safety guidelines:

- ✅ Only uses NCFE e-Library knowledge base
- ✅ Says "I don't have that information" when unsure
- ✅ No hallucinations or made-up facts
- ✅ No personalized investment advice
- ✅ Educational content only
- ✅ Content safety filters enabled

## Troubleshooting

### No audio output?

- Check browser audio permissions
- Enable speaker icon in UI (top right)
- Ensure system volume is on

### RAG not finding information?

- Verify PDFs are in `data/ncfe_books/`
- Delete `data/faiss_index.pkl` to rebuild index
- Check PDF text extraction quality

### Agent errors?

- Verify `GOOGLE_API_KEY` in `.env`
- Check Python version (3.12+)
- Reinstall dependencies: `pip install -r requirements.txt`

### Import errors?

- Activate virtual environment first
- Run from `financial_rag_agent/` directory

## Future Enhancements

- [ ] Add more NCFE e-Library PDFs
- [ ] Conversation history persistence
- [ ] Multi-language support
- [ ] Voice customization (speed, pitch, voice type)
- [ ] Deployment to cloud (Google Cloud Run)
- [ ] Analytics dashboard for usage tracking
- [ ] Mobile app integration

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. NCFE e-Library content remains property of NCFE.

## Acknowledgments

- **Google ADK Team**: For the excellent agent framework
- **NCFE**: For financial literacy educational content
- **sentence-transformers**: For embedding models
- **FAISS**: For fast vector search

## Contact

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ using Google ADK and Gemini 2.0**
