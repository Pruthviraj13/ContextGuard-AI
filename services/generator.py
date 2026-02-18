import httpx
import os
from app.core.logging import logger

class LLMGenerator:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama3-8b-8192"

        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY not set")

    async def generate(self, question: str, context_chunks: list[str]) -> str:
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are an assistant that answers ONLY using the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers strictly from provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0,
            "max_tokens": 512
        }


        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"LLM API error: {e.response.status_code}")
            return "LLM service is temporarily unavailable."

        except Exception as e:
            logger.error(f"Unexpected LLM error: {str(e)}")
            return "Unable to generate answer at this time."
