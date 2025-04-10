import re
from typing import List, Dict
from db.models import Cars

class FindProducts:
    """Сервис получения товаров и формирования ссылок на Маркетплейс OZON"""
    def __init__(self, car: Cars, text: str):
        self.car = car
        self.text = text
        self.urls: List[str] = []
        self.candidates: List[str] = []

    def get_urls_list(self) -> Dict[str, str]:
        """Поиск названий товаров в тексте ответа"""
        products_names_list = self._get_products_names()
        products_urls_list = self._get_urls(products_names_list)

        return dict(zip(products_names_list, products_urls_list))

    def _get_products_names(self) -> List[str]:
        """Метод получения названий товаров из ответа ИИ в список"""
        cleaned_text = self._clean()

        numbered = re.findall(pattern=r"\d+\.\s*(.+?):", string=cleaned_text)

        if numbered:
            self.candidates.extend(numbered)

        if not self.candidates:
            # Если нет номеров, ищем по буллетам
            bullets = re.findall(r"•\s*(.+?):", cleaned_text)

            if bullets:
                self.candidates.extend(bullets)

        if not self.candidates:
            # Если нет двоеточий, но есть жирный текст
            bold = re.findall(r"<b>(.+?)</b>", cleaned_text)

            if bold:
                self.candidates.extend(bold)

        return list({item.strip() for item in self.candidates})

    def _get_urls(self, products: List[str]) -> List[str]:
        """Метод получения URL`ов для товаров"""
        for product in products:
            product += f" для автомобиля {self.car.full}"

            url = (
                f"https://www.ozon.ru/search/?text={product.replace(" ", "+")}&from_global=true"
            )
            self.urls.append(url)

        return self.urls

    def _clean(self):
        """Убираем HTML- и Markdown-разметку"""
        text = re.sub(r"</?b>", "", self.text)
        text = re.sub(r"</?strong>", "", text)

        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)

        return text


TEXT = """
📌 **Требования:** 5W-40

🎯 **Варианты:**
1. **Mobil Super 2000 X1 5W-40**: синтетика, защита от износа, подходит для холодного климата. Цена: ~3999 руб.
2. **ZIC X5 5W-40**: хорошая текучесть при низких температурах, защита двигателя. Цена: ~3499 руб.
3. **Роснефть Maximum 5W-40**: доступная цена, защита двигателя. Цена: ~1999 руб.

💡 **Совет:** Mobil Super 2000 и ZIC X5 обеспечивают хорошую защиту двигателя и подходят для различных 
климатических условий. При выборе масла обращайте внимание на его вязкость и спецификации, чтобы 
обеспечить оптимальную работу двигателя вашего автомобиля.
"""


if __name__ == "__main__":
    import asyncio
    from db.models import CarsRepository
    from db.db_config import async_session_maker

    async def main():
        async with async_session_maker() as session:
            car = await CarsRepository.find_one_or_none(session, user_id="eee49b86-13fd-443d-8ebd-a5feb9e6e76f")

        find = FindProducts(car, TEXT)
        print(find.get_urls_list())

    asyncio.run(main())