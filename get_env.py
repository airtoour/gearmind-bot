import os
from dotenv import load_dotenv

load_dotenv()

def get_env(value, default=None):
    return os.getenv(value, default)
