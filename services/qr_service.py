import json
from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import fernet
from models.wallet_db import Wallet, TransactionLog
from schemas.qr_ import (
    QRScanRequest,
    QRMerchantDetails,
    QRPaymentResponse,
    QRPaymentInitiate,
    MerchantRegisterRequest,
    MerchantRegisterResponse,
)
from services.notification_service import send_whatsapp_message, send_webhook_fallback

# Temporary in-memory store; replace with DB in production
MERCHANTS = {}


# QR Data Encryption & Decryption

def encrypt_qr_data(payload: dict) -> str:
    return fernet.encrypt(json.dumps(payload).encode()).decode()


def decrypt_qr_data(encrypted_str: str) -> dict:
    try:
        decrypted = fernet.decrypt(encrypted_str.encode()).decode()
        return json.loads(decrypted)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted QR code")


# Merchant Registration

def register_merchant(req: MerchantRegisterRequest) -> MerchantRegisterResponse:
    if req.merchant_id in MERCHANTS:
        raise HTTPException(status_code=400, detail="Merchant already registered")

    merchant_data = {
        "merchant_id": req.merchant_id,
        "merchant_name": req.merchant_name,
        "account_number": req.account_number,
        "bank_name": req.bank_name
    }

    qr_payload = {
        "merchant_id": req.merchant_id,
        "account_number": req.account_number,
        "bank_name": req.bank_name
    }

    encrypted_data = encrypt_qr_data(qr_payload)
    MERCHANTS[req.merchant_id] = merchant_data

    return MerchantRegisterResponse(
        status="success",
        qr_code_data=encrypted_data,
        message="Merchant successfully onboarded"
    )



# QR Scan Handling

def scan_qr_code(data: QRScanRequest) -> QRMerchantDetails:
    qr_data = decrypt_qr_data(data.qr_code_data)
    merchant_id = qr_data.get("merchant_id")

    merchant = MERCHANTS.get(merchant_id)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return QRMerchantDetails(
        merchant_id=merchant["merchant_id"],
        merchant_name=merchant.get("merchant_name"),
        merchant_account_number=merchant.get("account_number"),
        merchant_bank=merchant.get("bank_name")
    )


# QR Payment Processing

def process_qr_payment(payload: QRPaymentInitiate, db: Session) -> QRPaymentResponse:
    merchant = MERCHANTS.get(payload.merchant_id)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    sender_wallet = db.query(Wallet).filter(Wallet.user_id == payload.user_id).first()
    if not sender_wallet or sender_wallet.balance < float(payload.amount):
        raise HTTPException(status_code=400, detail="Insufficient funds")

    receiver_wallet = db.query(Wallet).filter(Wallet.user_id == merchant["merchant_id"]).first()
    if not receiver_wallet:
        raise HTTPException(status_code=404, detail="Merchant wallet not found")

    # Perform the transfer
    sender_wallet.balance -= float(payload.amount)
    receiver_wallet.balance += float(payload.amount)

    transaction = TransactionLog(
        sender_id=payload.user_id,
        receiver_id=merchant["merchant_id"],
        amount=Decimal(payload.amount),
        timestamp=datetime.utcnow()
    )

    db.add(transaction)
    db.commit()

    # Send WhatsApp notifications (with webhook fallback)
    user_msg = f"✅ You paid ₦{payload.amount} to {merchant['merchant_name']} successfully."
    merchant_msg = f"💰 You received ₦{payload.amount} from {payload.user_id}"

    try:
        send_whatsapp_message(payload.user_phone, user_msg)
        send_whatsapp_message(payload.merchant_phone, merchant_msg)
    except Exception as e:
        print(f"[WhatsAppError] {str(e)} — triggering fallback webhook.")
        send_webhook_fallback({
            "user_id": payload.user_id,
            "merchant_id": payload.merchant_id,
            "amount": payload.amount,
            "merchant_name": merchant["merchant_name"]
        })

    return QRPaymentResponse(
        status="success",
        message="Payment Successful",
        transaction_id=str(transaction.id),
        timestamp=datetime.utcnow()
    )
