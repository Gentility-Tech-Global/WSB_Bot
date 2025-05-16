from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    scans = relationship("QRScanLog", back_populates="merchant")

class QRScanLog(Base):
    __tablename__ = "qr_scan_logs"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, ForeignKey("merchants.merchant_id"), index=True)
    user_id = Column(String, nullable=False)
    status = Column(String, default="success")
    raw_qr_data = Column(Text)
    scanned_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("Merchant", back_populates="scans")
    