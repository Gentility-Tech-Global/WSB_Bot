from sqlalchemy import Column, String, Integer, DateTime, Enum, Date
from database.session import Base
from datetime import datetime
import enum
from sqlalchemy.orm import relationship

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    partner = "partner"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    bvn = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    tier = Column(Integer, default=1)
    nin_url = Column(String, nullable=True)
    address_proof_url = Column(String, nullable=True)
    kyc_status = Column(String, default="pending")
    date_of_birth = Column(Date, nullable=False)
    partner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    wallet = relationship("Wallet", uselist=False, back_populates="user")