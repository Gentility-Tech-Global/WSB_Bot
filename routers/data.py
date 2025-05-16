from fastapi import APIRouter, HTTPException
from schemas.data_ import DataTopUpRequest, DataTopUpResponse
from services.data_service import process_data_topup


router = APIRouter(prefix="/data", tags=["Data TopUp"])

@router.post("/topup", response_model=DataTopUpResponse)
def data_topup(request: DataTopUpRequest):
    try:
        response = process_data_topup(request)
        if response.status == "failed":
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))