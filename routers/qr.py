from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.qr_ import QRScanRequest, QRMerchantDetails, QRPaymentInitiate, QRPaymentResponse, MerchantRegisterRequest, MerchantRegisterResponse
from services.qr_service import scan_qr_code, process_qr_payment, register_merchant
from database.session import get_db

router = APIRouter(prefix="/qr", tags=["QR Payment"])

@router.post("/register_merchant", response_model=MerchantRegisterResponse)
def onboard_merchant(request: MerchantRegisterRequest):
    try:
        return register_merchant(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")


@router.post("/scan", response_model=QRMerchantDetails)
def handle_qr_scan(data: QRScanRequest):
    try:
        return scan_qr_code(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pay", response_model=QRPaymentResponse)
def handle_qr_payment(payload: QRPaymentInitiate, db: Session = Depends(get_db)):
    try:
        return process_qr_payment(payload, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
