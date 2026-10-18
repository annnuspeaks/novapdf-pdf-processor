from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NOVA PDF API"
    app_version: str = "1.0.0"
    debug: bool = True

    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    max_upload_size_mb: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()