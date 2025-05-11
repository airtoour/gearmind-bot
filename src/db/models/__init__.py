# Таблицы
from .prompts.models import Prompts
from .requests.models import Requests
from .scores.models import Scores

from .users_game_profiles.models import UsersGameProfiles

from .cars.models import Cars
from .users.models import Users

from .tasks.models import Tasks
from .users_tasks.models import UsersTasks

# Репозитории
from .prompts.repository import PromptsRepository
from .requests.repository import RequestsRepository
from .scores.repository import ScoresRepository

from .users_game_profiles.repository import UsersGameProfilesRepository

from .cars.repository import CarsRepository
from .users.repository import UsersRepository

from .tasks.repository import TasksRepository
from .users_tasks.repository import UsersTasksRepository
