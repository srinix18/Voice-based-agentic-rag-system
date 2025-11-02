"""
Main Financial RAG Agent using Google ADK
Voice-enabled financial literacy assistant using NCFE e-Library data
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from google import genai
from google.genai import types
from tools.financial_rag_search import search_financial_knowledge_base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# System instructions for the agent
SYSTEM_INSTRUCTION = """You are a knowledgeable financial assistant specializing in financial literacy and awareness. 

Your role is to:
1. Answer questions about financial concepts, markets, institutions, and personal finance
2. Use ONLY information from the NCFE e-Library knowledge base
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


class FinancialRAGAgent:
    """
    Voice-enabled financial RAG agent using Google ADK.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Financial RAG Agent.
        
        Args:
            api_key: Google API key. If None, reads from GOOGLE_API_KEY environment variable
        """
        # Set up API key
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Configure the client
        self.client = genai.Client(api_key=self.api_key)
        
        # Define the tool for the agent
        self.tools = [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="search_financial_knowledge_base",
                        description="Search the NCFE e-Library financial knowledge base for information about financial concepts, institutions, markets, and personal finance. Use this tool whenever you need to answer questions about financial topics.",
                        parameters=types.Schema(
                            type=types.Type.OBJECT,
                            properties={
                                "query": types.Schema(
                                    type=types.Type.STRING,
                                    description="The financial question or topic to search for in the knowledge base"
                                )
                            },
                            required=["query"]
                        )
                    )
                ]
            )
        ]
        
        # Model configuration
        self.model_name = "gemini-2.0-flash-exp"
        
        # Safety settings to prevent harmful content
        self.safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
        ]
        
        logger.info("Financial RAG Agent initialized")
    
    def _execute_tool_call(self, function_call) -> str:
        """
        Execute a tool call and return the result.
        
        Args:
            function_call: The function call from the model
            
        Returns:
            The result of the tool execution
        """
        function_name = function_call.name
        function_args = function_call.args
        
        logger.info(f"Executing tool: {function_name} with args: {function_args}")
        
        if function_name == "search_financial_knowledge_base":
            query = function_args.get("query", "")
            result = search_financial_knowledge_base(query)
            return result
        else:
            return f"Unknown tool: {function_name}"
    
    def chat(self, user_message: str, chat_history: Optional[list] = None) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            user_message: The user's question or message
            chat_history: Optional list of previous messages for context
            
        Returns:
            The agent's response
        """
        try:
            # Build messages
            messages = chat_history or []
            messages.append(types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            ))
            
            # Generate response with tools
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=self.tools,
                    safety_settings=self.safety_settings,
                    temperature=0.7,
                    max_output_tokens=1024,
                )
            )
            
            # Handle tool calls
            while response.candidates and response.candidates[0].content.parts and \
                  len(response.candidates[0].content.parts) > 0 and \
                  hasattr(response.candidates[0].content.parts[0], 'function_call') and \
                  response.candidates[0].content.parts[0].function_call:
                
                function_call = response.candidates[0].content.parts[0].function_call
                
                # Execute the tool
                tool_result = self._execute_tool_call(function_call)
                
                # Add tool response to messages
                messages.append(response.candidates[0].content)
                messages.append(types.Content(
                    role="user",
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call.name,
                            response={"result": tool_result}
                        )
                    )]
                ))
                
                # Get next response
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=messages,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=self.tools,
                        safety_settings=self.safety_settings,
                        temperature=0.7,
                        max_output_tokens=1024,
                    )
                )
            
            # Extract final text response
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                logger.info(f"Candidate finish_reason: {candidate.finish_reason if hasattr(candidate, 'finish_reason') else 'N/A'}")
                
                if candidate.content and candidate.content.parts and len(candidate.content.parts) > 0:
                    for idx, part in enumerate(candidate.content.parts):
                        logger.info(f"Part {idx}: {type(part)}, has text: {hasattr(part, 'text')}")
                        if hasattr(part, 'text') and part.text:
                            final_response = part.text
                            logger.info(f"Agent response: {final_response[:100]}...")
                            return final_response
            
            logger.warning(f"No valid response found. Candidates: {len(response.candidates) if response.candidates else 0}")
            return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"An error occurred: {str(e)}"


def main():
    """
    Main function to run the agent in CLI mode for testing.
    """
    print("=" * 80)
    print("Financial RAG Agent - NCFE e-Library Assistant")
    print("=" * 80)
    print("\nInitializing agent...")
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠️  GOOGLE_API_KEY environment variable not set!")
        print("Please set it with: $env:GOOGLE_API_KEY='your-api-key-here'")
        return
    
    try:
        agent = FinancialRAGAgent()
        print("✅ Agent initialized successfully!\n")
        
        print("You can ask questions about financial topics.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        chat_history = []
        
        while True:
            try:
                user_input = input("\n🙋 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Stay financially informed!")
                    break
                
                print("\n🤖 Agent: ", end="", flush=True)
                response = agent.chat(user_input, chat_history)
                print(response)
                
                # Update chat history
                chat_history.append(types.Content(
                    role="user",
                    parts=[types.Part(text=user_input)]
                ))
                chat_history.append(types.Content(
                    role="model",
                    parts=[types.Part(text=response)]
                ))
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
    
    except Exception as e:
        print(f"\n❌ Failed to initialize agent: {e}")
        return


# For ADK Web UI integration
def create_agent():
    """
    Factory function to create the agent for ADK serve.
    """
    return FinancialRAGAgent()


if __name__ == "__main__":
    main()
