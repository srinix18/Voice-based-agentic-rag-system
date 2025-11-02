"""
Example script demonstrating agent usage
Run this to see the agent in action with sample queries
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main_agent import FinancialRAGAgent
from tools.financial_rag_search import search_financial_knowledge_base


def test_retriever_only():
    """Test just the retriever without the full agent."""
    print("\n" + "="*80)
    print("Testing RAG Retriever Only")
    print("="*80)
    
    test_queries = [
        "What is compound interest?",
        "Explain the role of SEBI",
        "What is a mutual fund?",
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 80)
        result = search_financial_knowledge_base(query)
        print(result)
        print()


def test_full_agent():
    """Test the full agent with conversation."""
    print("\n" + "="*80)
    print("Testing Full Agent with Gemini")
    print("="*80)
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠️  GOOGLE_API_KEY not set. Skipping agent test.")
        print("To test the full agent, set your API key:")
        print('$env:GOOGLE_API_KEY="your_api_key_here"')
        return
    
    try:
        agent = FinancialRAGAgent()
        
        test_queries = [
            "What is compound interest? Explain it simply.",
            "Tell me about SEBI's role in financial markets.",
        ]
        
        for query in test_queries:
            print(f"\n🙋 User: {query}")
            print("-" * 80)
            print("🤖 Agent: ", end="", flush=True)
            response = agent.chat(query)
            print(response)
            print()
    
    except Exception as e:
        print(f"\n❌ Error testing agent: {e}")


def check_setup():
    """Check if the setup is complete."""
    print("\n" + "="*80)
    print("Checking Setup")
    print("="*80)
    
    # Check PDF directory
    pdf_dir = Path(__file__).parent / "data" / "ncfe_books"
    print(f"\n📁 PDF Directory: {pdf_dir}")
    
    if not pdf_dir.exists():
        print("   ❌ Directory does not exist!")
        return False
    else:
        print("   ✅ Directory exists")
    
    # Check for PDFs
    pdf_files = list(pdf_dir.glob("*.pdf"))
    print(f"\n📚 PDF Files: {len(pdf_files)} found")
    
    if pdf_files:
        print("   ✅ PDFs found:")
        for pdf in pdf_files[:5]:
            print(f"      - {pdf.name}")
        if len(pdf_files) > 5:
            print(f"      ... and {len(pdf_files) - 5} more")
    else:
        print("   ⚠️  No PDF files found!")
        print("   Please add PDF files to data/ncfe_books/")
    
    # Check API key
    print(f"\n🔑 API Key:")
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print(f"   ✅ Set (length: {len(api_key)})")
    else:
        print("   ⚠️  Not set")
        print('   Set with: $env:GOOGLE_API_KEY="your_key_here"')
    
    # Check dependencies
    print(f"\n📦 Dependencies:")
    required = [
        "PyPDF2",
        "faiss",
        "sentence_transformers",
        "google.generativeai"
    ]
    
    for package in required:
        try:
            __import__(package.replace("-", "_").split(".")[0])
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Run: pip install {package}")
    
    print("\n" + "="*80)
    return len(pdf_files) > 0


def main():
    """Main demo function."""
    print("\n" + "="*80)
    print("Financial RAG Agent - Demo & Test")
    print("="*80)
    
    # Check setup
    setup_ok = check_setup()
    
    if not setup_ok:
        print("\n⚠️  Setup incomplete. Please:")
        print("   1. Add PDF files to data/ncfe_books/")
        print("   2. Set GOOGLE_API_KEY environment variable")
        print("   3. Install dependencies: pip install -r requirements.txt")
        return
    
    # Test retriever
    print("\n" + "="*80)
    print("Running Tests...")
    print("="*80)
    
    test_retriever_only()
    
    # Test full agent if API key is set
    if os.environ.get("GOOGLE_API_KEY"):
        test_full_agent()
    else:
        print("\n💡 Tip: Set GOOGLE_API_KEY to test the full agent with Gemini")
    
    print("\n" + "="*80)
    print("Demo Complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Run in CLI mode: python main_agent.py")
    print("2. Run with voice UI: adk serve main_agent.py")
    print("3. Run tests: pytest tests/test_agent.py -v")
    print()


if __name__ == "__main__":
    main()
