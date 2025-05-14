import uuid
from schemas.airtime_ import AirtimeTopUpRequest, AirtimeTopUpResponse


ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}
# Mocked external API or Logic

def process_airtime_topup(request: AirtimeTopUpRequest) -> AirtimeTopUpResponse:
    # Simulate processing (can integrate with external APIs)
    transaction_id = str(uuid.uuid4())

    # Example mock check (this should call real 3rd party services)
    if request.network.lower() not in ["mtn", "glo", "airtel", "9mobile"]:
        return AirtimeTopUpResponse(
            status="failed",
            transaction_id=transaction_id,
            message=f"Unsupported network: {request.network}"
        )
    
    return AirtimeTopUpResponse(
        status="success",
        transaction_id=transaction_id,
        message=f"Airtiem of #{request.amount} sent to {request.phone_number} on {request.network}"
    )