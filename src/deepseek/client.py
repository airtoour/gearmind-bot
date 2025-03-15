import httpx

from db.models.prompts.repository import PromptsRepository
from db.models.users.repository import UsersRepository

from logger import logger


class DeepSeekAPIClient:
    def __init__(self, token: str, email: str, password: str):
        self.token = token
        self.email = email
        self.password = password

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        self.client = httpx.AsyncClient(headers=self.headers)
        self.chat_session_id = None

    async def send_message(self, message: str):
        try:
            if not self.chat_session_id:
                await self._create_chat_session()

            response = await self.client.post(
                url="https://chat.deepseek.com/api/v0/chat/completion",
                json={
                    "chat_session_id": self.chat_session_id,
                    "prompt": message,
                    "ref_file_ids": [],
                    "search_enabled": False,
                    "thinking_enabled": True,
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise

    async def _get_cookies(self, email: str, password: str):
        login_response = await self.client.post(
            url="https://chat.deepseek.com/sign_in",
            json={"email": email, "password": password}
        )
        self.client.cookies.update(login_response.cookies)

    async def _create_chat_session(self):
        try:
            response = await self.client.post(
                url="https://chat.deepseek.com/api/v0/chat_session/create"
            )
            response.raise_for_status()
            self.chat_session_id = response.json()["data"]["biz_data"]["id"]
            self.headers["Referer"] = f"https://chat.deepseek.com/a/chat/s/{self.chat_session_id}"
        except Exception as e:
            logger.error(f"Chat session error: {e}")
            raise

    async def _get_prompt(self, message: str, prompt_type: str):
        car_info = ""

        prompt = await PromptsRepository.find_one_or_none(type=prompt_type)
        user = await UsersRepository.find_one_or_none(tg_user_id=123123123)

        for car in user.cars:
            car_info = f"{car.brand_name} {car.model_name} {car.gen_name} {car.year}"

        result = (
            f"{
                prompt.text
                .replace("<username>", user.name)
                .replace("<carinfo>", car_info)
                .replace("<message>", message)
            }\n"
        )

        return result
