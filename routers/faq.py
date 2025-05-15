from fastapi import APIRouter, HTTPException
from schemas.faq_ import FAQResponse, PartnerRequest
from services.faq_service import get_faqs


router = APIRouter(prefix="/faq", tags=["FAQs"])

@router.post("/", response_model=FAQResponse)
async def fetch_faqs(request: PartnerRequest):
    response = get_faqs(request)
    if response.status == "failed":
        raise HTTPException(status_code=403, detail=response.message)
    return response

