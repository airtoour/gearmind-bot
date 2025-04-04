from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import GameProgressUsers
from services.game.schemas import NewLevelReturnSchema

from logger import logger


class GearGameService:
    def __init__(self, tg_user_id: int, session: AsyncSession, progress: GameProgressUsers):
        self.tg_id = tg_user_id
        self.session = session
        self.progress = progress

    async def wash(self, xp: int) -> NewLevelReturnSchema:
        """Метод обновляющий уровень игрока"""
        try:
            if not self.progress:
                return False

            new_level, new_xp = self.calculate_new_level(
                self.progress.level,
                self.progress.experience,
                xp
            )

            self.progress.level = new_level
            self.progress.experience = new_xp
            self.progress.last_wash_car_time = datetime.now()

            # Исправление передачи опыта в схему
            level_data = NewLevelReturnSchema(
                level=self.progress.level,
                experience=self.progress.experience,
                upped=(new_level > self.progress.level)
            )

            await self.session.commit()
            return level_data
        except Exception as e:
            await self.session.rollback()
            logger.error(e)
            raise

    @staticmethod
    def calculate_new_level(current_level: int, current_experience: int, added_experience: int) -> tuple[int, int]:
        """
        Опыт для уровня ``n`` рассчитывается как сумма арифметической прогрессии

        `XP = 25 * (n) * (n + 3)`, где n = текущий уровень - `1`

        :param current_level: Текущий уровень игрока
        :param current_experience: Текущее значение опыта
        :param added_experience: Количество добавляемого опыта

        :return: Полученный уровень игрока
        """
        total_experience = current_experience + added_experience
        new_level = current_level
        xp_required = 100 + 50 * (new_level - 1)  # Опыт для перехода на следующий уровень

        while total_experience >= xp_required:
            total_experience -= xp_required
            new_level += 1
            xp_required = 100 + 50 * (new_level - 1)  # Обновляем требуемый опыт для нового уровня

        return new_level, total_experience

    @staticmethod
    def xp_required(level: int) -> int:
        """Получение требуемого количества опыта для повышения опыта"""
        if level < 1:
            return 0

        n = level - 1

        return 25 * n * (n + 3)