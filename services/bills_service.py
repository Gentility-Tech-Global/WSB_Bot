from schemas.bills_ import BillPaymentRequest, BillPaymentResponse
import uuid
import re

# Simulated partner integration validation
ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

async def validate_partner(channel_partner: str) -> bool:
    return channel_partner in ALLOWED_PARTNERS

async def process_bill_payment(request: BillPaymentRequest) -> BillPaymentResponse:
    if not validate_partner(request.channel_partner):
        return BillPaymentResponse(
            status="failed",
            message=f"Unauthorized partner: {request.channel_partner}"
        )

    # Simulate processing and create transaction reference
    transaction_id = f"BILL-{uuid.uuid4().hex[:12].upper()}"

    # In real integration, add logic to call vendor API and return result
    return BillPaymentResponse(
        status="success",
        message=f"{request.bill_type.title()} bill payment processed successfully.",
        transaction_id=transaction_id
    )


async def handle_bill_payment(text: str, sender: str) -> str:
    # Example input: Pay bill 5000 for electricity to 1234567890
    match = re.search(r'pay bill\s+(\d+)\s+for\s+(\w+)\s+(to\s+)?(\d+)', text)
    if not match:
        return "Please use: Pay bill 5000 for electricity to 1234567890"

    amount = int(match.group(1))
    bill_type = match.group(2)
    account = match.group(4)

    # Add payment integration logic here
    return f"✅ Bill payment of ₦{amount:,} for {bill_type} to account {account} has been received."