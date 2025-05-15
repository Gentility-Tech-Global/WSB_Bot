from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    API_SECRET_KEY: str
    TRANSFER_LIMIT: int = 100000
    DEBUG: bool = True
    fernet_secret_key: str
    webhook_url: str = "https://your-fallback-webhook.com/notify"  # default/fallback
    app_name: str = "My App"
    whatsapp_access_token: str
    whatsapp_api_url: str


    class Config:
        env_file = ".env"

settings = Settings()
