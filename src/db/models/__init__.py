# Таблицы
from .prompts.models import Prompts
from .requests.models import Requests
from .scores.models import Scores

from .cars.models import Cars
from .users.models import Users

# Репозитории
from .prompts.repository import PromptsRepository
from .requests.repository import RequestsRepository

from .cars.repository import CarsRepository
from .users.repository import UsersRepository
from .scores.repository import ScoresRepository