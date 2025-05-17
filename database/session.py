from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Lazy import to avoid circular import
def get_database_url():
    from core.config import settings
    return settings.DATABASE_URL

def get_debug_mode():
    from core.config import settings
    return settings.DEBUG

# Create engine and session factory
engine = create_engine(
    get_database_url(),
    echo=get_debug_mode(),
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
