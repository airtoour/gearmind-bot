# Таблицы
from .prompts.models import Prompts
from .requests.models import Requests
from .scores.models import Scores

from .cars.models import Cars

from .users.models import Users
from .game_progress.models import GameProgressUsers

# Репозитории
from .prompts.repository import PromptsRepository
from .requests.repository import RequestsRepository
from .scores.repository import ScoresRepository

from .cars.repository import CarsRepository

from .users.repository import UsersRepository
from .game_progress.repository import GameProgressUsersRepository