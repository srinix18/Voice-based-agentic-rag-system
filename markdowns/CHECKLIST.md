# ✅ Getting Started Checklist

Complete this checklist to get your Financial RAG Agent running!

---

## 📋 Pre-Setup Checklist

- [ ] Python 3.10 or higher installed

  ```powershell
  python --version
  ```

- [ ] PowerShell available (comes with Windows)

- [ ] Internet connection active

- [ ] Google account for API key

---

## 🔧 Setup Checklist

### 1. Navigate to Project

- [ ] Open PowerShell
- [ ] Navigate to project directory:
  ```powershell
  cd "c:\Users\srini\Downloads\dev\speech agent\financial_rag_agent"
  ```

### 2. Run Setup Script

- [ ] Execute setup:
  ```powershell
  .\setup.ps1
  ```
- [ ] Verify "Setup Complete!" message appears
- [ ] Note any warnings or errors

### 3. Get Google API Key

- [ ] Visit: https://makersuite.google.com/app/apikey
- [ ] Sign in with Google account
- [ ] Click "Create API Key"
- [ ] Copy the key (starts with `AIza...`)

### 4. Configure Environment

- [ ] Open .env file:
  ```powershell
  notepad .env
  ```
- [ ] Paste your API key:
  ```
  GOOGLE_API_KEY=AIzaSy...your_actual_key...
  ```
- [ ] Save and close

### 5. Add PDF Content

- [ ] Visit NCFE e-Library: https://ncfe.org.in/e-library/
- [ ] Download relevant PDFs on financial topics
- [ ] Copy PDFs to the directory:
  ```powershell
  Copy-Item "C:\path\to\downloads\*.pdf" "data\ncfe_books\"
  ```
- [ ] Verify PDFs are there:
  ```powershell
  ls data\ncfe_books\*.pdf
  ```

---

## 🧪 Testing Checklist

### Run Demo Script

- [ ] Activate virtual environment:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- [ ] Run demo:
  ```powershell
  python demo.py
  ```
- [ ] Check all items show ✅ (green checkmarks)
- [ ] Verify PDFs were loaded
- [ ] Verify API key is set
- [ ] Read the test results

### Expected Demo Output:

```
✅ PDF Directory exists
✅ PDFs found: X files
✅ API Key: Set
✅ Dependencies installed
```

---

## 🚀 Launch Checklist

### Option A: CLI Mode (Text)

- [ ] Run the agent:
  ```powershell
  python main_agent.py
  ```
- [ ] Wait for "Agent initialized successfully!" message
- [ ] Type a test question: "What is compound interest?"
- [ ] Verify you get a response with source citations
- [ ] Type 'quit' to exit

### Option B: Voice UI Mode (Recommended)

- [ ] Start ADK server:
  ```powershell
  adk serve main_agent.py
  ```
- [ ] Note the URL (usually http://localhost:5000)
- [ ] Open the URL in Chrome or Edge browser
- [ ] Allow microphone access when prompted
- [ ] Click the microphone icon
- [ ] Speak a question clearly
- [ ] Wait for response
- [ ] Listen to the audio response

---

## ✅ Verification Checklist

### System Verification

- [ ] Virtual environment activates without errors
- [ ] All dependencies install successfully
- [ ] No import errors when running demo
- [ ] PDF files are detected and loaded
- [ ] FAISS index builds successfully

### Functionality Verification

- [ ] Agent initializes with API key
- [ ] CLI mode accepts text input
- [ ] Agent returns responses (not errors)
- [ ] Responses cite sources from PDFs
- [ ] "I don't have that information" appears for out-of-scope queries
- [ ] Voice input works in Web UI (if using)
- [ ] Voice output plays in Web UI (if using)

### Quality Verification

- [ ] Responses are relevant to questions
- [ ] Sources are correctly attributed
- [ ] Agent doesn't hallucinate (makes up info)
- [ ] Agent stays on topic (financial education)
- [ ] Response quality is good

---

## 📝 Test Queries Checklist

Try each of these and verify results:

- [ ] "What is compound interest?"

  - Should return: Definition and explanation from PDFs
  - Should cite: Source PDF name

- [ ] "Explain the role of SEBI"

  - Should return: Information about SEBI if in PDFs
  - Should cite: Source PDF name

- [ ] "What is quantum physics?"

  - Should return: "I don't have that information..."
  - Reason: Out of scope

- [ ] "What's the difference between equity and debt?"

  - Should return: Comparative explanation if in PDFs
  - Should cite: Source PDF name(s)

- [ ] "Tell me about [random nonsense]"
  - Should return: "I don't have that information..."
  - Reason: Not in knowledge base

---

## 🐛 Troubleshooting Checklist

If something doesn't work, check:

- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] You're in the correct directory
- [ ] GOOGLE_API_KEY is set correctly (no spaces, quotes)
- [ ] PDF files exist in data/ncfe_books/
- [ ] Internet connection is working
- [ ] Firewall isn't blocking connections
- [ ] Antivirus isn't interfering

If still stuck:

- [ ] Read TROUBLESHOOTING.md
- [ ] Check error messages carefully
- [ ] Try running demo.py for diagnostics
- [ ] Try reinstalling: Delete venv folder and run setup.ps1 again

---

## 📊 Performance Checklist

### First Run (Expected)

- [ ] Index building takes 1-5 minutes
- [ ] "Creating embeddings..." message appears
- [ ] faiss_index.pkl file is created in data/
- [ ] Progress bars show (if using verbose mode)

### Subsequent Runs (Expected)

- [ ] Index loads in <5 seconds
- [ ] "Loading cached index..." message appears
- [ ] No embedding creation needed
- [ ] Queries respond in 2-5 seconds

---

## 🎯 Success Indicators

You'll know everything works when:

✅ Setup script completes without errors
✅ Demo script shows all green checkmarks
✅ Agent starts and says "initialized successfully"
✅ Test queries return relevant answers
✅ Sources are cited in responses
✅ Voice input/output works (if using Web UI)
✅ No Python errors or tracebacks
✅ Responses are fast (<5 seconds)

---

## 📚 Next Steps Checklist

Once everything works:

- [ ] Add more PDFs for better coverage
- [ ] Test with your own financial questions
- [ ] Show to colleagues or friends
- [ ] Customize system instructions (main_agent.py)
- [ ] Adjust RAG parameters (config/adk_config.yaml)
- [ ] Run test suite: `pytest tests/test_agent.py -v`
- [ ] Consider deploying to production
- [ ] Read full README.md for advanced features

---

## 🎉 Completion

When all checkmarks are done:

**CONGRATULATIONS! 🎊**

Your Financial RAG Agent is fully operational and ready to answer financial literacy questions!

---

## 📞 Quick Reference

| Task          | Command                              |
| ------------- | ------------------------------------ |
| Setup         | `.\setup.ps1`                        |
| Activate venv | `.\venv\Scripts\Activate.ps1`        |
| Run demo      | `python demo.py`                     |
| CLI mode      | `python main_agent.py`               |
| Voice UI      | `adk serve main_agent.py`            |
| Run tests     | `pytest tests/test_agent.py -v`      |
| Help          | Read README.md or TROUBLESHOOTING.md |

---

**Print this checklist and mark items as you complete them!** ✏️
