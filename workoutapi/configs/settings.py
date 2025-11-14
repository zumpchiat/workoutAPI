from decouple import config
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = Field(default=config("DB_ENV_URL"))


settings = Settings()
