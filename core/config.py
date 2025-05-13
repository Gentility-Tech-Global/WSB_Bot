import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/botdb")
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "fallback_key")
    TRANSFER_LIMIT: int = int(os.getenv("TRANSFER_LIMIT", 100000))

Settings = Settings()