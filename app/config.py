from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBED_DIM: int = 384

    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MODEL: str = "mistral:latest"

    GMAIL_MAX_MESSAGES: int = 200

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
