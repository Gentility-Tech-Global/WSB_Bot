from pydantic import BaseModel, constr, condecimal
from typing import Optional, Annotated
from datetime import datetime

AmountToPay = Annotated[int, condecimal(gt=0)]
AccountNumber = Annotated[str,constr(min_length=10, max_length=10)]

class MerchantRegisterRequest(BaseModel):
    merchant_name: str
    account_number: AccountNumber
    bank_code: str
    merchant_id: str

class MerchantRegisterResponse(BaseModel):
    status: str
    qr_code_data: str
    message: str
    
class QRScanRequest(BaseModel):
    qr_code_data: str

class QRMerchantDetails(BaseModel):
    merchant_id: str
    merchant_name: str
    merchant_account_number: str
    merchant_bank: str

class QRPaymentInitiate(BaseModel):
    user_id: str
    merchant_id: str
    amount: AmountToPay
    narration: Optional[str] = "OR Payment"

class QRPaymentResponse(BaseModel):
    status: str
    message: str
    transaction_id: Optional[str] = None
    timestamp: Optional[datetime] = None