from schemas.data_ import DataTopUpRequest, DataTopUpResponse
import re
import uuid


ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}
# Mocked Logis - replace with real 3rd-party API integrations
async def process_data_topup(request: DataTopUpRequest) -> DataTopUpResponse:
    transaction_id = str(uuid.uuid4())

    if request.network.lower() not in ["mtn", "glo", "airtel", "9mobile"]:
        return DataTopUpResponse(
            status="failed",
            transaction_id=transaction_id,
            message=f"Unsupported network: {request.network}"
        )
    
    # Simulated Logic for plan types
    if request.Plan_type.lower() not in ["daily", "weekly", "monthly"]:
        return DataTopUpResponse(
            status="failed",
            transaction_id=transaction_id,
            message=f"Invalid plan type: {request.Plan_type}"
        )
    
    return DataTopUpResponse(
        status="success",
        transaction_id=transaction_id,
        message=f"{request.Plan_type.capitalize()} data of #{request.amount} sent to {request.phone_number} on request.network"
    )


async def data_topup(text: str, sender: str) -> str:
    match = re.search(r'data\s+(\d+)\s+(to\s+)?(\d{10,11})', text)
    if not match:
        return "Please provide data top-up request in format: Data 1000 to 08012345678"

    amount = int(match.group(1))
    phone = match.group(3)

    # Add actual data top-up integration here
    return f"✅ Data top-up of ₦{amount} to {phone} is being processed."