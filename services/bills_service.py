from schemas.bills_ import BillPaymentRequest, BillPaymentResponse
import uuid

# Simulated partner integration validation
ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

def validate_partner(channel_partner: str) -> bool:
    return channel_partner in ALLOWED_PARTNERS

def process_bill_payment(request: BillPaymentRequest) -> BillPaymentResponse:
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
