from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    LOG_LEVEL: str = Field(default="info")

    # Add OpenAI API key here 👇
    OPENAI_API_KEY: Optional[str] = None
    EMBEDDING_MODEL_NAME: str = Field(default="text-embedding-3-small")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
