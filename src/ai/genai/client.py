import asyncio

import google.generativeai as genai

from ai.base_client import BaseAIClient
from config import settings


class GoogleGenAIClient(BaseAIClient):
    def __init__(self, token: str, model: str = "gemini-2.0-flash"):
        super().__init__(token, model)
        self.configured = False

    async def initialize(self):
        """Настройка клиента с асинхронной оберткой"""
        if not self.configured:
            await asyncio.to_thread(
                genai.configure,
                api_key=self.token,
                transport="grpc_asyncio"
            )
            self.client = genai.GenerativeModel(self.model)
            self.configured = True

    async def create(self, prompt: str, text: str) -> str:
        """Асинхронная генерация контента"""
        await self.initialize()

        try:
            response = await self.client.generate_content_async(f"{prompt}. {text}")
            return response.text
        except Exception as e:
            raise RuntimeError(f"Generation error: {str(e)}") from e


genai_client = GoogleGenAIClient(token=settings.GOOGLE_TOKEN)