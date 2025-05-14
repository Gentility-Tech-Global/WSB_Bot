from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.ocr import (
    OCRImageUploadRequest,
    ExtractedAccountDetails,
    OCRPaymentRequest,
    OCRPaymentResponse
)
from services.ocr_service import process_ocr_image, process_ocr_payment

router = APIRouter(prefix="/image-ocr", tags=["Image OCR Payment"])


@router.post("/extract", response_model=ExtractedAccountDetails)
def extract_details_from_image(req: OCRImageUploadRequest):
    try:
        return process_ocr_image(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pay", response_model=OCRPaymentResponse)
def pay_from_ocr_extraction(req: OCRPaymentRequest, db: Session = Depends(get_db)):
    try:
        return process_ocr_payment(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
