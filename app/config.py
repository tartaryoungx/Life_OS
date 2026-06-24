import json
from typing import Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    GEMINI_API_KEY: str
#    GOOGLE_CALENDAR_CREDENTIALS: Dict[str, Any]
    DATABASE_URL: str
    GOOGLE_TOKEN_JSON: str
        
    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()

