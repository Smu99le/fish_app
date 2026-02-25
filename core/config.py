import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_PATH: str = os.getenv("DB_PATH", "db.sqlite")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_ENV: str = os.getenv("APP_ENV", "dev")

settings = Settings()