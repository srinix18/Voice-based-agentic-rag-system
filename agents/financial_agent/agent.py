"""
ADK-compatible Financial RAG Agent
Voice-enabled financial literacy assistant using NCFE e-Library data
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import tools
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from google.adk.agents.llm_agent import Agent

# Import our RAG search function
from tools.financial_rag_search import search_financial_knowledge_base

# System instructions
SYSTEM_INSTRUCTION = """You are a knowledgeable financial assistant specializing in financial literacy and awareness. 

Your role is to:
1. Answer questions about financial concepts, markets, institutions, and personal finance
2. Use ONLY information from the NCFE e-Library knowledge base via the search_financial_knowledge_base tool
3. If the knowledge base doesn't contain relevant information, respond with: "I don't have that information in my knowledge base."
4. Never guess or make up information
5. Provide clear, educational explanations suitable for someone learning about finance
6. Cite sources when providing information

Safety guidelines:
- Do not provide personalized investment advice
- Do not make predictions about specific stocks or market movements
- Stick to educational content only
- If asked about something outside financial education, politely decline and redirect to financial topics

Always be helpful, accurate, and honest about the limits of your knowledge."""

# Create the root agent using ADK's Agent class - set to a live-capable Gemini model
# Use a model that supports bidiGenerateContent so the ADK Web UI can open a live
# websocket conversation (microphone input / streaming audio).
root_agent = Agent(
    model='gemini-2.0-flash-live-001',
    name='financial_rag_agent',
    description='Financial literacy assistant using NCFE e-Library knowledge base (live mode)',
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_financial_knowledge_base],  # Pass function directly as a callable tool
)