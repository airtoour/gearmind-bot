from pydantic import BaseModel


class CompletionCreateSchema(BaseModel):
    """Схема запроса к YandexGPT"""
    url: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    prompt: str
    text: str
    temperature: float = 0.2
    max_tokens: str = "2000"


class UsageCreateSchema(BaseModel):
    """Схема использования токенов запроса"""
    input_tokens: str
    completion_tokens: str
    total_tokens: str


class ReturnCreateSchema(BaseModel):
    """Схема получения ответа от YandexGPT"""
    text: str
    usage: UsageCreateSchema
