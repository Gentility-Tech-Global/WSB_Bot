from fastapi import APIRouter, HTTPException
from schemas.airtime_ import AirtimeTopUpRequest, AirtimeTopUpResponse
from services.airtime_services import process_airtime_topup


router = APIRouter(prefix="/airtime", tags=["Airtim"])


@router.post("/topup", response_model=AirtimeTopUpResponse)
def airtime_topup(request: AirtimeTopUpRequest):
   try:
      response =  process_airtime_topup(request)
      if response.status == "failed":
         raise HTTPException(status_code=400, detail=response.message)
      return response
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))