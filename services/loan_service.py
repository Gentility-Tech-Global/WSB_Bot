from schemas.loan import LoanRequest, LoanResponse
import uuid

ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

def validate_partner(channel_partner: str) -> bool:
    return channel_partner in ALLOWED_PARTNERS

def process_loan_application(request: LoanRequest) -> LoanResponse:
    if not validate_partner(request.channel_partner):
        return LoanResponse(
            status="failed",
            message=f"Unauthorized partner: {request.channel_partner}"
        )

    # Future logic: check BVN, credit history, KYC level, etc.
    loan_id = f"LOAN-{uuid.uuid4().hex[:10].upper()}"

    return LoanResponse(
        status="success",
        message="Loan application received and being processed.",
        loan_id=loan_id
    )
