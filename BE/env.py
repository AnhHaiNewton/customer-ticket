import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file based on APP_ENV
app_env = os.getenv("APP_ENV", "local")
if app_env == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

class Env(BaseSettings):
    APP_ENV: str = "local"
    DEBUG: bool = True
    SECRET_KEY: str = "secret"

    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "kiros_triage"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    # Gemini
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

env = Env()