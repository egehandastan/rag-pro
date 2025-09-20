from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    LOG_LEVEL: str = Field(default="info")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
