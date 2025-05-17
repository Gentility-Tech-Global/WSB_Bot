from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    API_SECRET_KEY: str
    FERNET_SECRET_KEY: str
    WHATSAPP_ACCESS_TOKEN: str
    WHATSAPP_API_URL: str
    SECRET_KEY: str

    TRANSFER_LIMIT: int = 100_000
    DEBUG: bool = True
    webhook_url: str = "https://your-fallback-webhook.com/notify"
    app_name: str = "My App"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()
print(settings.DATABASE_URL)
