from abc import ABC, abstractmethod


class BaseAIClient(ABC):
    def __init__(self, token: str, model: str):
        self.token = token
        self.model = model
        self.client = None

    @abstractmethod
    async def initialize(self):
        """Инициализация клиента"""
        pass

    @abstractmethod
    async def create(self, prompt: str, text: str):
        """Генерация контента"""
        pass
