# 🔧 Troubleshooting Guide

Common issues and solutions for the Financial RAG Agent.

---

## Installation Issues

### Problem: "Python not found"

**Symptoms:**

```
'python' is not recognized as an internal or external command
```

**Solutions:**

1. Install Python from https://www.python.org/downloads/
2. Ensure "Add Python to PATH" was checked during installation
3. Restart PowerShell after installation
4. Try `python3` instead of `python`

---

### Problem: "pip install fails"

**Symptoms:**

```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions:**

1. **Upgrade pip:**

   ```powershell
   python -m pip install --upgrade pip
   ```

2. **Try installing individually:**

   ```powershell
   pip install google-adk
   pip install PyPDF2
   pip install faiss-cpu
   pip install sentence-transformers
   ```

3. **Check Python version:**
   ```powershell
   python --version  # Should be 3.10+
   ```

---

### Problem: FAISS installation fails

**Symptoms:**

```
ERROR: Failed building wheel for faiss
```

**Solutions:**

**Windows:**

```powershell
pip install faiss-cpu
```

**If that fails, try:**

```powershell
pip install faiss-cpu --no-cache-dir
```

**Or install conda and use:**

```powershell
conda install -c conda-forge faiss-cpu
```

---

## Configuration Issues

### Problem: "Google API key not found"

**Symptoms:**

```
ValueError: Google API key not found
```

**Solutions:**

1. **Set environment variable (temporary):**

   ```powershell
   $env:GOOGLE_API_KEY="your_api_key_here"
   python main_agent.py
   ```

2. **Create .env file (permanent):**

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   Add:

   ```
   GOOGLE_API_KEY=your_actual_key_here
   ```

3. **Verify it's set:**

   ```powershell
   $env:GOOGLE_API_KEY
   ```

4. **Get a new key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Create new API key
   - Copy and use it

---

### Problem: "Invalid API key"

**Symptoms:**

```
google.api_core.exceptions.PermissionDenied: 403 API key not valid
```

**Solutions:**

1. **Check key format:**

   - Should look like: `AIzaSy...` (39 characters)
   - No spaces or quotes in .env file

2. **Enable the API:**

   - Go to Google Cloud Console
   - Enable "Generative Language API"

3. **Check billing:**

   - Some APIs require billing enabled

4. **Generate new key:**
   - Old key may be revoked
   - Create fresh key from Google AI Studio

---

## PDF & Data Issues

### Problem: "No PDF files found"

**Symptoms:**

```
WARNING: No PDF files found in data/ncfe_books
```

**Solutions:**

1. **Check directory exists:**

   ```powershell
   Test-Path "data\ncfe_books"
   ```

2. **Check for PDFs:**

   ```powershell
   ls data\ncfe_books\*.pdf
   ```

3. **Add PDFs:**

   ```powershell
   Copy-Item "C:\path\to\pdfs\*.pdf" "data\ncfe_books\"
   ```

4. **Download from NCFE:**
   - Visit: https://ncfe.org.in/e-library/
   - Download relevant PDFs
   - Save to `data/ncfe_books/`

---

### Problem: "No text extracted from PDF"

**Symptoms:**

```
WARNING: No text extracted from filename.pdf
```

**Causes:**

- PDF contains scanned images (not text)
- PDF is password-protected
- PDF is corrupted

**Solutions:**

1. **Check PDF type:**

   - Open PDF in a reader
   - Try to select/copy text
   - If you can't, it's an image-based PDF

2. **Convert scanned PDFs:**

   - Use OCR software (Adobe Acrobat, Tesseract)
   - Or find text-based versions

3. **Try different PDFs:**
   - NCFE e-Library has text-based PDFs
   - Download directly from source

---

### Problem: Index build is very slow

**Symptoms:**

- Takes 10+ minutes to build index
- Computer becomes unresponsive

**Solutions:**

1. **Reduce PDF count:**

   - Start with 5-10 PDFs
   - Add more gradually

2. **Use smaller PDFs:**

   - Large PDFs (100+ pages) take longer
   - Consider splitting large PDFs

3. **Increase chunk size:**

   - Edit `tools/financial_rag_search.py`
   - Change `chunk_size=500` to `chunk_size=1000`

4. **Use GPU (if available):**
   ```powershell
   pip uninstall faiss-cpu
   pip install faiss-gpu
   ```

---

## Runtime Issues

### Problem: "I don't have that information" for everything

**Symptoms:**
Agent always responds with "I don't have that information"

**Causes:**

- No PDFs loaded
- PDFs don't contain relevant content
- Score threshold too strict

**Solutions:**

1. **Check PDFs are loaded:**

   ```powershell
   python demo.py  # Look for "Found X PDF files"
   ```

2. **Check PDF content:**

   - Open PDFs manually
   - Verify they contain financial information
   - Ensure they match your queries

3. **Lower score threshold:**

   Edit `tools/financial_rag_search.py`:

   ```python
   # Change from
   def search(self, query: str, top_k: int = 3, score_threshold: float = 1.5)

   # To
   def search(self, query: str, top_k: int = 3, score_threshold: float = 2.0)
   ```

4. **Rebuild index:**
   ```powershell
   Remove-Item data\faiss_index.pkl
   python demo.py
   ```

---

### Problem: Responses are irrelevant

**Symptoms:**
Agent returns content that doesn't match the question

**Solutions:**

1. **Make queries more specific:**

   - Instead of: "Tell me about interest"
   - Try: "What is compound interest and how is it calculated?"

2. **Increase top_k:**

   Edit `tools/financial_rag_search.py`:

   ```python
   def search(self, query: str, top_k: int = 5, ...)  # Changed from 3
   ```

3. **Check embedding model:**

   - Default model: `all-MiniLM-L6-v2`
   - For better results, try: `all-mpnet-base-v2`

   Edit `tools/financial_rag_search.py`:

   ```python
   self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
   ```

---

### Problem: "adk: command not found"

**Symptoms:**

```
adk : The term 'adk' is not recognized
```

**Solutions:**

1. **Verify installation:**

   ```powershell
   pip show google-adk
   ```

2. **Reinstall ADK:**

   ```powershell
   pip install --upgrade google-adk
   ```

3. **Check PATH:**

   - ADK might not be in your PATH
   - Try: `python -m adk serve main_agent.py`

4. **Use alternative:**
   - Run in CLI mode: `python main_agent.py`
   - Use demo: `python demo.py`

---

## Voice/Web UI Issues

### Problem: Microphone not working

**Solutions:**

1. **Check browser permissions:**

   - Allow microphone access
   - Try Chrome or Edge (best compatibility)

2. **Test microphone:**

   - Try in other apps first
   - Check Windows sound settings

3. **Use HTTPS:**
   - Some browsers require HTTPS for microphone
   - Or use localhost (usually works)

---

### Problem: No voice output

**Solutions:**

1. **Check browser settings:**

   - Enable audio
   - Unmute tab

2. **Check system volume:**

   - Ensure speakers/headphones work
   - Check Windows audio settings

3. **Try text mode:**
   - Use CLI mode as fallback
   - `python main_agent.py`

---

## Performance Issues

### Problem: Slow responses

**Symptoms:**
Queries take 30+ seconds

**Solutions:**

1. **Check internet connection:**

   - Gemini API requires internet
   - Test: `ping google.com`

2. **Reduce context:**

   - Lower `top_k` from 3 to 2
   - Reduce `max_tokens` in config

3. **Use faster model:**

   Edit `main_agent.py`:

   ```python
   self.model_name = "gemini-1.5-flash"  # Faster than 2.0
   ```

4. **Check API quota:**
   - You may have hit rate limits
   - Wait a few minutes and retry

---

### Problem: High memory usage

**Symptoms:**
Python uses 2+ GB RAM

**Causes:**

- Large embedding model
- Many PDFs indexed
- Multiple queries cached

**Solutions:**

1. **Use smaller embedding model:**

   ```python
   # In financial_rag_search.py
   self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Smallest
   ```

2. **Reduce PDF count:**

   - Start with essential PDFs only
   - Add more gradually

3. **Clear cache:**
   ```powershell
   Remove-Item data\faiss_index.pkl
   ```

---

## Testing Issues

### Problem: Tests fail

**Symptoms:**

```
pytest tests/test_agent.py
FAILED tests/test_agent.py::test_...
```

**Solutions:**

1. **Check test requirements:**

   ```powershell
   pip install pytest pytest-cov
   ```

2. **Run specific test:**

   ```powershell
   pytest tests/test_agent.py::test_pdf_directory_exists -v
   ```

3. **Skip agent tests (no API key):**

   ```powershell
   pytest tests/test_agent.py -k "not agent" -v
   ```

4. **View detailed output:**
   ```powershell
   pytest tests/test_agent.py -v -s
   ```

---

## Import Errors

### Problem: "No module named 'tools'"

**Solutions:**

1. **Run from correct directory:**

   ```powershell
   cd "c:\Users\srini\Downloads\dev\speech agent\financial_rag_agent"
   python main_agent.py
   ```

2. **Check **init**.py exists:**

   ```powershell
   Test-Path "tools\__init__.py"
   ```

3. **Use absolute imports:**
   - The code already uses relative imports
   - Should work from project root

---

## General Debugging

### Enable debug logging

Add to top of `main_agent.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check component individually

1. **Test retriever only:**

   ```powershell
   python tools\financial_rag_search.py
   ```

2. **Test agent only:**

   ```powershell
   python main_agent.py
   ```

3. **Run demo:**
   ```powershell
   python demo.py
   ```

---

## Getting Help

If nothing works:

1. **Check logs:**

   - Look for error messages
   - Note the full traceback

2. **Verify environment:**

   ```powershell
   python --version
   pip list
   $env:GOOGLE_API_KEY
   ls data\ncfe_books\
   ```

3. **Try fresh install:**

   ```powershell
   Remove-Item -Recurse venv
   .\setup.ps1
   ```

4. **Check ADK documentation:**
   - https://github.com/google/adk-toolkit
   - Look for similar issues

---

## Still Stuck?

Create a detailed issue report with:

1. Your Python version (`python --version`)
2. Your OS (Windows version)
3. Full error message/traceback
4. What you tried
5. Output of: `pip list | Select-String "google|faiss|sentence"`

---

**Most issues are resolved by:**

- ✅ Setting GOOGLE_API_KEY correctly
- ✅ Adding PDF files to data/ncfe_books/
- ✅ Installing dependencies properly
- ✅ Running from the correct directory

Good luck! 🍀
