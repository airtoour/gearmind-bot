from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    Tasks,
    UsersGameProfiles,
    UsersGameProfilesRepository,
    TasksRepository,
    UsersTasksRepository
)
from services.game.schemas import (
    NewLevelReturnSchema,
    CreateProfileSchema
)
from logger import logger


class GearGameService:
    """Сервис работы GearGame"""
    def __init__(
        self,
        session: AsyncSession,
        profile: Optional[UsersGameProfiles] = None
    ):
        self.session = session
        self.profile = profile

    async def create_profile(self, data: CreateProfileSchema) -> UsersGameProfiles:
        """Метод создания профиля"""
        try:
            # Проверяем, существует ли уже профиль для данного user_id
            existing_profile = await UsersGameProfilesRepository.find_one_or_none(self.session, user_id=data.user_id)

            if existing_profile:
                raise ValueError("Профиль с данным user_id уже существует")

            # Создаем новый профиль в БД
            new_profile = await UsersGameProfilesRepository.add(
                self.session, user_id=data.user_id, car_id=data.car_id
            )

            # Получаем все активные задания
            tasks = await TasksRepository.find_all(self.session, is_active=True)

            # Если нет активных заданий, просто возвращаем профиль
            if not tasks:
                return new_profile

            # Для каждого задания создаем запись в таблице users_tasks
            if new_profile:
                for task in tasks:
                    await UsersTasksRepository.add(
                        self.session,
                        profile_id=new_profile.id,
                        task_id=task.id,
                    )

            return new_profile
        except Exception as e:
            logger.error(f"Ошибка при создании профиля: {e}")
            raise

    async def process_task(self, task: Tasks) -> bool:
        try:
            # Ищем текущий прогресс по заданию пользователя
            user_task = await UsersTasksRepository.find_one_or_none(
                self.session, profile_id=self.profile.id, task_id=task.id
            )

            if not user_task:
                return False  # если задача не найдена

            # Если текущий прогресс достиг целевого, завершаем задание
            if user_task.current_value >= user_task.task.target_value:
                user_task.is_completed = True
                user_task.completed_at = datetime.now()

                # Добавляем опыт пользователю только при завершении задания
                await UsersGameProfilesRepository.reward_user_experience(
                    self.session, self.profile, task.reward_xp
                )
            else:
                # Просто увеличиваем прогресс, если задание не завершено
                await UsersTasksRepository.increment_task(self.session, user_task)

            await self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            await self.session.rollback()
            return False

    async def wash(self, xp: int) -> NewLevelReturnSchema:
        """Метод обновляющий уровень игрока"""
        try:
            if not self.profile:
                return False

            new_level, new_xp = self._calculate_new_level(
                self.profile.level,
                self.profile.experience,
                xp
            )

            self.profile.level = new_level
            self.profile.experience = new_xp
            self.profile.last_wash_car_time = datetime.now()

            # Исправление передачи опыта в схему
            level_data = NewLevelReturnSchema(
                level=self.profile.level,
                experience=self.profile.experience,
                upped=(new_level > self.profile.level)
            )

            await self.session.commit()
            return level_data
        except Exception as e:
            await self.session.rollback()
            logger.error(e)
            raise

    @staticmethod
    def _calculate_new_level(current_level: int, current_experience: int, added_experience: int) -> tuple[int, int]:
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
