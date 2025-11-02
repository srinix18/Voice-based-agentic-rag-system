# 🚀 Quick Start Guide

Get your Financial RAG Agent running in 5 minutes!

## Prerequisites

- ✅ Python 3.10 or higher installed
- ✅ Google API key ([Get one here](https://makersuite.google.com/app/apikey))
- ✅ PDF files from NCFE e-Library

---

## Step 1: Automated Setup (Recommended)

Run the setup script:

```powershell
cd "c:\Users\srini\Downloads\dev\speech agent\financial_rag_agent"
.\setup.ps1
```

This will:

- Create a virtual environment
- Install all dependencies
- Set up the .env file
- Check your PDF directory

**Then skip to Step 5!**

---

## Step 2: Manual Setup (Alternative)

If you prefer manual setup:

### Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Step 3: Configure API Key

### Option A: Environment Variable (Temporary)

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

### Option B: .env File (Permanent)

Create a `.env` file:

```powershell
Copy-Item .env.example .env
notepad .env
```

Add your key:

```
GOOGLE_API_KEY=your_actual_google_api_key_here
```

---

## Step 4: Add PDF Content

Copy your NCFE e-Library PDFs:

```powershell
Copy-Item "C:\path\to\your\pdfs\*.pdf" "data\ncfe_books\"
```

Or download directly from: https://ncfe.org.in/e-library/

---

## Step 5: Test Your Setup

Run the demo script:

```powershell
python demo.py
```

This will:

- ✅ Verify your setup
- ✅ Test PDF loading
- ✅ Test the retriever
- ✅ Test the agent (if API key is set)

---

## Step 6: Run the Agent

### Option A: CLI Mode (Text Chat)

```powershell
python main_agent.py
```

Example interaction:

```
🙋 You: What is compound interest?
🤖 Agent: Compound interest is...
```

### Option B: Web UI with Voice (Recommended)

```powershell
adk serve main_agent.py
```

Then:

1. Open the URL shown in your browser (usually http://localhost:5000)
2. Click the microphone icon
3. Speak your question
4. Listen to the response!

---

## 🎯 Example Queries

Try asking:

1. **"What is compound interest?"**

   - Tests basic financial concepts

2. **"Explain the role of SEBI in financial markets"**

   - Tests specific institution knowledge

3. **"What is the difference between equity and debt?"**

   - Tests comparative understanding

4. **"What is a mutual fund?"**

   - Tests investment concepts

5. **"Tell me about financial planning"**
   - Tests broader topics

---

## ✅ Verification Checklist

Before running, ensure:

- [ ] Python 3.10+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list | Select-String "google-adk"`)
- [ ] GOOGLE_API_KEY set (check with: `$env:GOOGLE_API_KEY`)
- [ ] PDF files in `data/ncfe_books/` (check with: `ls data\ncfe_books\*.pdf`)

---

## 🐛 Common Issues

### "No module named 'google.adk'"

**Solution:**

```powershell
pip install google-adk google-generativeai
```

### "Google API key not found"

**Solution:**

```powershell
$env:GOOGLE_API_KEY="your_key_here"
```

Or edit `.env` file.

### "No PDF files found"

**Solution:**

```powershell
# Check directory exists
Test-Path "data\ncfe_books"

# Add PDFs
Copy-Item "path\to\pdfs\*.pdf" "data\ncfe_books\"
```

### Slow First Run

**This is normal!** The first run builds the FAISS index, which takes 1-5 minutes depending on PDF count. Subsequent runs are fast (<5 seconds).

---

## 🎓 Understanding the Output

When you ask a question, you'll see:

```
Based on the NCFE e-Library content:

[Source 1: financial_basics.pdf]
Compound interest is the interest calculated on both the initial
principal and the accumulated interest from previous periods...

[Source 2: banking_guide.pdf]
This concept is fundamental in banking and finance...
```

The agent:

- ✅ Cites sources
- ✅ Only uses provided content
- ✅ Says "I don't have that information" when unsure

---

## 🚀 Next Steps

1. **Add more PDFs** for better coverage
2. **Run tests**: `pytest tests/test_agent.py -v`
3. **Customize** settings in `config/adk_config.yaml`
4. **Deploy** to production (see deployment guide)

---

## 📞 Need Help?

Check:

1. **README.md** - Full documentation
2. **demo.py** - Working examples
3. **tests/test_agent.py** - Test cases
4. **ADK docs** - https://github.com/google/adk-toolkit

---

## 🎉 Success Indicators

You'll know it's working when:

- ✅ Demo script passes all checks
- ✅ Agent responds to questions
- ✅ Source citations appear
- ✅ "I don't have that information" for out-of-scope queries
- ✅ Voice input/output works in Web UI

---

**Ready to go? Run `python demo.py` now!** 🚀
