from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    upload_dir: str = ""
    ollama_url: str = ""
    database_url: str = ""
    hf_token: str = ""
    jwt_secret: str = ""
    jwt_algorithm: str = ""
    token_expires_in: int = 15

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()