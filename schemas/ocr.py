from pydantic import BaseModel
from typing import Optional


class OCRImageUploadRequest(BaseModel):
    image_base64: str  # base64-encoded image string
    user_id: str
    user_phone: str


class ExtractedAccountDetails(BaseModel):
    account_number: str
    account_name: str
    bank_name: str


class OCRPaymentRequest(BaseModel):
    user_id: str
    user_phone: str
    account_number: str
    account_name: str
    bank_name: str
    amount: float


class OCRPaymentResponse(BaseModel):
    status: str
    message: str
    transaction_id: Optional[str]
    timestamp: Optional[str]
