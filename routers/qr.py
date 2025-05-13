from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Simulated QR Code Database (in-memory)
QR_DATABASE = {
    "qr12345": {
        "account_name": "John Doe",
        "account_number": "0123456789",
        "bank": "SmartBank"
    }
}

class QRScanRequest(BaseModel):
    qr_code_id: str  # extracted from scanned QR code

class QRPaymentRequest(BaseModel):
    qr_code_id: str
    amount: float
    sender_account: str

@router.post("/scan")
def scan_qr(qr_data: QRScanRequest):
    if qr_data.qr_code_id not in QR_DATABASE:
        raise HTTPException(status_code=404, detail="QR Code not recognized")

    account_info = QR_DATABASE[qr_data.qr_code_id]
    return {
        "status": "success",
        "message": "Scan successful. Enter amount.",
        "recipient_details": account_info
    }

@router.post("/pay")
def complete_payment(payment: QRPaymentRequest):
    if payment.qr_code_id not in QR_DATABASE:
        raise HTTPException(status_code=404, detail="Invalid QR Code")

    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    recipient = QR_DATABASE[payment.qr_code_id]

    # Simulate transfer processing logic
    return {
        "status": "success",
        "message": f"{payment.amount} sent to {recipient['account_name']} ({recipient['account_number']})",
        "from": payment.sender_account,
        "to": recipient
    }
