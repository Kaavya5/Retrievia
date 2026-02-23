import os
import logging
from typing import List, Dict
from google import genai

logger = logging.getLogger(__name__)

# Fallback basic API key to prevent crashing without it, but will fail actual calls.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

class LLMService:
    def __init__(self):
        # Allow initialization without a valid API key for testing purposes
        api_key = GEMINI_API_KEY if GEMINI_API_KEY else "dummy_key_for_testing"
        self.client = genai.Client(api_key=api_key)

    def generate_chat_response(self, query: str, context_chunks: List[Dict], history: List[Dict] = None) -> str:
        """Generates a response using retrieved context chunks from RAG."""
        
        system_prompt = (
            "You are a helpful 'Second Brain' assistant. You answer questions based heavily on the provided context. "
            "If the context doesn't contain the answer, you can use your general knowledge, but you must mention that. "
            "Help the user extract value from their uploaded documents."
        )

        # Build context string
        context_text = "\n\n".join([f"Source [{chunk.get('document_name')}]:\n{chunk.get('text')}" for chunk in context_chunks])
        
        user_message = f"Answer this question: {query}\n\nContext:\n{context_text}"

        messages = []
        
        if history:
            # We want to format history. Only take last few messages to save tokens.
            for msg in history[-6:]:
                # Gemini strictly requires "user" or "model" as roles
                role = "model" if msg.get("role") == "assistant" else msg.get("role", "user")
                messages.append(
                    {"role": role, "parts": [{"text": msg.get("content", "")}]}
                )
                
        messages.append({"role": "user", "parts": [{"text": user_message}]})
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=messages,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini completion failed: {e}")
            return "Sorry, I could not generate a response at this time. Please check your API key."

    def summarize_document(self, document_text: str) -> str:
        """Generates a high-level summary of a document."""
        # Trim text to fit in prompt easily to avoid token limits.
        max_chars = 30000 
        trimmed_text = document_text[:max_chars]
        
        message = f"Summarize the following document:\n\n{trimmed_text}"
        
        try:
             response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=message,
                config=genai.types.GenerateContentConfig(
                     system_instruction="You are a helpful expert summarizer. Return a clear and concise summary of the provided text, capturing the main ideas.",
                     temperature=0.5,
                )
            )
             return response.text
        except Exception as e:
             logger.error(f"Summarize completion failed: {e}")
             return "Could not generate summary."

llm_service = LLMService()
