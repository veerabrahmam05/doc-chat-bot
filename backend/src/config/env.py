from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    upload_dir: str = ""
    ollama_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()