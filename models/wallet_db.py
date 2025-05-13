from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="wallet")

class TransactionLog(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    amount = Column(Numeric(12, 2))
    timestamp = Column(DateTime, default=datetime.utcnow)
