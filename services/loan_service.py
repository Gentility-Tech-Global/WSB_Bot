from schemas.loan import LoanRequest, LoanResponse
import uuid
import re
from services.redis_service import get_data

ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

async def validate_partner(channel_partner: str) -> bool:
    return channel_partner in ALLOWED_PARTNERS

async def process_loan_application(request: LoanRequest) -> LoanResponse:
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


async def handle_loan_application(text: str, sender: str) -> str:
    amount_match = re.search(r'loan\s+(\d+)', text)
    if not amount_match:
        return "Please specify the loan amount like: Loan 5000"

    amount = int(amount_match.group(1))

    # Example business rule: check eligibility from user profile
    user_data = await get_data(f"user:{sender}")
    if not user_data:
        return "❌ You must be onboarded before applying for a loan. Use: Onboard John Doe, ..."

    # Mock eligibility
    if amount > 20000:
        return "❌ You are only eligible for a loan up to ₦20,000 currently."

    return f"✅ Loan request of ₦{amount:,} received. You’ll be notified once approved."