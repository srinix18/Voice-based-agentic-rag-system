# Financial RAG Agent - NCFE e-Library Assistant

A voice-enabled AI agent that answers financial literacy questions using Google's Agent Development Kit (ADK) and the NCFE e-Library content.

## 🌟 Features

- **Voice-Enabled Interface**: Speak questions and hear responses using ADK Web UI
- **RAG-Powered**: Retrieval-Augmented Generation using NCFE e-Library PDFs
- **Accurate & Honest**: Only uses source material, never hallucinates
- **Safety Guardrails**: Built-in content filtering and safety measures
- **Fast Semantic Search**: FAISS-based vector search with caching
- **Educational Focus**: Designed for financial literacy and awareness

## 📋 Prerequisites

- Python 3.10 or higher
- Google API key for Gemini models
- Windows/Linux/Mac OS
- At least 2GB RAM (for embeddings)

## 🚀 Quick Start

### 1. Installation

```powershell
# Navigate to the project directory
cd "c:\Users\srini\Downloads\dev\speech agent\financial_rag_agent"

# Create and activate virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Edit .env and add your Google API key
notepad .env
```

Set your Google API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Add PDF Content

Place your NCFE e-Library PDF files in the `data/ncfe_books/` directory:

```powershell
# Example: Copy PDFs to the directory
Copy-Item "path\to\your\pdfs\*.pdf" "data\ncfe_books\"
```

The system will automatically:

- Extract text from all PDFs
- Create embeddings
- Build a FAISS index
- Cache the index for fast subsequent loads

### 4. Run the Agent

#### Option A: CLI Mode (Text-based testing)

```powershell
python main_agent.py
```

This starts an interactive command-line interface where you can type questions and see responses.

#### Option B: ADK Web UI (Voice-enabled)

```powershell
adk serve main_agent.py
```

This launches the ADK web interface with voice input/output capabilities. Open the provided URL in your browser.

## 📁 Project Structure

```
financial_rag_agent/
├── main_agent.py              # Main agent implementation with ADK
├── tools/
│   ├── __init__.py
│   └── financial_rag_search.py  # RAG retriever tool
├── config/
│   └── adk_config.yaml        # Configuration settings
├── data/
│   └── ncfe_books/            # Place PDF files here
│       └── (your PDFs)
├── tests/
│   ├── __init__.py
│   └── test_agent.py          # Test suite
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🧪 Testing

Run the test suite to verify everything works:

```powershell
# Run all tests
pytest tests/test_agent.py -v

# Run with output
pytest tests/test_agent.py -v -s

# Run specific test
pytest tests/test_agent.py::test_pdf_directory_exists -v
```

### Example Test Queries

Try these questions to test the system:

1. "What is compound interest?"
2. "Explain the role of SEBI in financial markets"
3. "What is the difference between equity and debt?"
4. "What is a mutual fund?"
5. "Explain inflation and its impact on savings"

## 🔧 How It Works

### 1. PDF Ingestion & Indexing

```
PDFs → Text Extraction → Text Chunking → Embeddings → FAISS Index
```

- Uses PyPDF2 for text extraction
- Splits text into 500-word chunks with 50-word overlap
- Creates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores in FAISS vector database for fast retrieval

### 2. Query Processing

```
User Question → Query Embedding → FAISS Search → Top-K Passages → LLM Context
```

- Converts query to embedding
- Searches FAISS index for similar passages
- Returns top 3 most relevant chunks
- Passes to Gemini with source citations

### 3. Response Generation

```
Context + System Instructions → Gemini 2.0 → Validated Response → User
```

- Uses Gemini 2.0 Flash for fast responses
- System instructions enforce truthfulness
- Returns "I don't have that information" if no relevant data found
- Includes source citations from PDFs

## 🛡️ Safety Features

- **Content Filtering**: Blocks harmful, hateful, explicit content
- **Source Attribution**: Always cites PDF sources
- **Truthfulness**: Never generates information beyond sources
- **Scope Limiting**: Focuses only on financial education
- **No Personal Advice**: Disclaims personalized investment advice

## 🎤 Voice Features (ADK Web UI)

When using `adk serve`:

1. **Voice Input**: Click microphone to speak your question
2. **Voice Output**: Agent speaks the response aloud
3. **Visual Chat**: See conversation history
4. **Real-time Processing**: Watch tool calls in action

## 📊 Performance

- **Initial Index Build**: 1-5 minutes (depends on PDF count)
- **Subsequent Loads**: <5 seconds (uses cached index)
- **Query Response**: 2-5 seconds
- **Voice I/O Latency**: ~1 second

## 🔄 Rebuilding the Index

If you add or modify PDFs:

```python
from tools.financial_rag_search import FinancialRAGRetriever

retriever = FinancialRAGRetriever("data/ncfe_books")
retriever.rebuild_index()
```

Or delete the cache file:

```powershell
Remove-Item data\faiss_index.pkl
```

The index will rebuild automatically on next run.

## ⚙️ Configuration

Edit `config/adk_config.yaml` to customize:

```yaml
rag:
  chunk_size: 500 # Words per chunk
  chunk_overlap: 50 # Overlap between chunks
  top_k_results: 3 # Number of passages to retrieve
  score_threshold: 1.5 # Relevance threshold

agent:
  model: "gemini-2.0-flash-exp"
  temperature: 0.7
  max_tokens: 1024
```

## 🐛 Troubleshooting

### No PDFs Found

```
⚠️  No PDF files found in data/ncfe_books
```

**Solution**: Add PDF files to the `data/ncfe_books/` directory.

### API Key Error

```
❌ Google API key not found
```

**Solution**: Set `GOOGLE_API_KEY` environment variable:

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

### Import Errors

```
ModuleNotFoundError: No module named 'faiss'
```

**Solution**: Install dependencies:

```powershell
pip install -r requirements.txt
```

### Slow First Run

The first run builds the index, which takes a few minutes. Subsequent runs use the cached index.

### "I don't have that information"

This is working correctly! The agent only responds when relevant information is found in the PDFs. Try:

- Adding more comprehensive PDFs
- Rephrasing your question
- Asking about topics covered in your PDFs

## 📝 Example Usage

```python
from main_agent import FinancialRAGAgent

# Initialize agent
agent = FinancialRAGAgent()

# Ask a question
response = agent.chat("What is compound interest?")
print(response)

# Continue conversation with context
response = agent.chat(
    "Can you give me an example?",
    chat_history=[...]  # Previous messages
)
```

## 🤝 Contributing

Suggestions for improvement:

1. Add more sophisticated chunking strategies
2. Implement hybrid search (keyword + semantic)
3. Add conversation memory across sessions
4. Support more document formats (DOCX, TXT, etc.)
5. Add citation click-through in UI
6. Implement user feedback loop

## 📄 License

This project is for educational purposes. Ensure you have rights to use the NCFE e-Library content.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the test suite for examples
3. Check ADK documentation: https://github.com/google/adk-toolkit
4. Verify your Google API key is valid

## 🎯 Next Steps

1. ✅ Add PDF content to `data/ncfe_books/`
2. ✅ Set up your Google API key
3. ✅ Install dependencies
4. ✅ Run tests to verify setup
5. ✅ Start the agent in CLI or Web UI mode
6. ✅ Ask financial questions!

---

**Built with ❤️ using Google ADK for financial literacy education**
