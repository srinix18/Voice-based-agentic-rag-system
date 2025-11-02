"""
Financial RAG Agent - NCFE e-Library Voice Assistant

A voice-enabled AI agent that answers financial literacy questions using
Google's Agent Development Kit (ADK) and the NCFE e-Library content.

Main Components:
- main_agent: FinancialRAGAgent class for agent interaction
- tools.financial_rag_search: RAG retriever for PDF content

Example Usage:
    >>> from financial_rag_agent import FinancialRAGAgent
    >>> agent = FinancialRAGAgent()
    >>> response = agent.chat("What is compound interest?")
    >>> print(response)

For more information, see README.md
"""

__version__ = "1.0.0"
__author__ = "Financial RAG Agent Team"
__description__ = "Voice-enabled financial literacy assistant using ADK and RAG"

# This file allows the project to be imported as a package
# But the main usage is through the CLI or ADK serve command
