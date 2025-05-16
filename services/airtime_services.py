import uuid
import re
from schemas.airtime_ import AirtimeTopUpRequest, AirtimeTopUpResponse


ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}
# Mocked external API or Logic

async def process_airtime_topup(request: AirtimeTopUpRequest) -> AirtimeTopUpResponse:
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
        message=f"Airtime of #{request.amount} sent to {request.phone_number} on {request.network}"
    )

async def airtime_topup(text: str, sender: str) -> str:
    try:
        match = re.search(r"airtime (\\d+) to (\\d{11})", text)
        if not match:
            return "Invalid format. Use: Airtime 500 to 08012345678"

        amount = float(match.group(1))
        number = match.group(2)

        # airtime_purchase(sender, number, amount)
        return f"Purchasing ₦{amount} airtime for {number}..."

    except Exception as e:
        return f"Error processing airtime topup: {str(e)}"
