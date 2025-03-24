from io import BytesIO
from typing import Union

from openai import AsyncOpenAI

from ai.base_client import BaseAIClient
from config import settings
from logger import logger


class OpenAIClient(BaseAIClient):
    def __init__(self, token: str, model: str = Union["gpt-4o-mini", "whisper-1"]):
        super().__init__(token, model)
        self.configured = False

    async def initialize(self):
        self.client = AsyncOpenAI(api_key=self.token)
        self.configured = True

    async def create(self, prompt: str, text: str):
        """Метод работы с текстом OpenAI"""
        await self.initialize()

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                stream=False,
                store=True,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(e)

    async def audio(self, prompt: str, file: BytesIO):
        """Получение транскрипции от OpenAI и получение ответа"""
        try:
            transcriptions = await self.client.audio.transcriptions.create(
                model=self.model,
                file=file
            )
            response = await self.create(prompt, transcriptions.text)
            return response
        except Exception as e:
            logger.error(e)


openai_client = OpenAIClient(token=settings.OPENAI_TOKEN)
