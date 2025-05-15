import base64
import io
import re
from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import pytesseract

from schemas.ocr import OCRImageUploadRequest, ExtractedAccountDetails, OCRPaymentRequest, OCRPaymentResponse
from models.wallet_db import Wallet, TransactionLog
from services.notification_service import send_whatsapp_message, send_webhook_fallback


def extract_text_from_image(base64_str: str) -> str:
    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to process image")


def extract_account_details(text: str) -> ExtractedAccountDetails:
    account_number = re.search(r'(Account\s?(number|no|#)[:\-]?\s*)(\d{10})', text, re.IGNORECASE)
    account_name = re.search(r'(Account\s?name[:\-]?\s*)([A-Za-z\s]{3,})', text, re.IGNORECASE)
    bank_name = re.search(r'(Bank(\sname)?[:\-]?\s*)([A-Za-z\s]{3,})', text, re.IGNORECASE)

    if not account_number or not account_name or not bank_name:
        raise HTTPException(status_code=400, detail="Could not extract all account details")

    return ExtractedAccountDetails(
        account_number=account_number.group(3).strip(),
        account_name=account_name.group(2).strip(),
        bank_name=bank_name.group(3).strip()
    )


def process_ocr_image(req: OCRImageUploadRequest) -> ExtractedAccountDetails:
    text = extract_text_from_image(req.image_base64)
    return extract_account_details(text)


def process_ocr_payment(payload: OCRPaymentRequest, db: Session) -> OCRPaymentResponse:
    sender_wallet = db.query(Wallet).filter(Wallet.user_id == payload.user_id).first()
    if not sender_wallet or sender_wallet.balance < float(payload.amount):
        raise HTTPException(status_code=400, detail="Insufficient funds")

    receiver_wallet = db.query(Wallet).filter(Wallet.user_id == payload.account_number).first()
    if not receiver_wallet:
        raise HTTPException(status_code=404, detail="Receiver wallet not found")

    sender_wallet.balance -= float(payload.amount)
    receiver_wallet.balance += float(payload.amount)

    transaction = TransactionLog(
        sender_id=payload.user_id,
        receiver_id=payload.account_number,
        amount=Decimal(payload.amount),
        timestamp=datetime.utcnow()
    )

    db.add(transaction)
    db.commit()

    user_msg = f"✅ You paid ₦{payload.amount} to {payload.account_name} successfully."
    receiver_msg = f"💰 You received ₦{payload.amount} from {payload.user_id}"

    try:
        send_whatsapp_message(payload.user_phone, user_msg)
        send_whatsapp_message(payload.user_phone, receiver_msg)
    except Exception as e:
        print(f"[WhatsAppError] {str(e)} — triggering fallback webhook.")
        send_webhook_fallback({
            "user_id": payload.user_id,
            "account_number": payload.account_number,
            "amount": payload.amount,
            "account_name": payload.account_name
        })

    return OCRPaymentResponse(
        status="success",
        message="OCR Payment Successful",
        transaction_id=str(transaction.id),
        timestamp=datetime.utcnow()
    )
