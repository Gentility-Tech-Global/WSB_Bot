from schemas.account_balance_ import BalanceCheckRequest, BalanceCheckResponse

# In-memory mock balance store (replace with DB in production)
mock_user_balances = {
    "user123": {"balance": 3500.75, "currency": "NGN"},
    "user456": {"balance": 0.0, "currency": "NGN"},
}

ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

def validate_partner(partner: str) -> bool:
    return partner in ALLOWED_PARTNERS

def fetch_account_balance(request: BalanceCheckRequest) -> BalanceCheckResponse:
    if not validate_partner(request.channel_partner):
        return BalanceCheckResponse(
            status="failed",
            message=f"Unauthorized partner: {request.channel_partner}"
        )

    user_data = mock_user_balances.get(request.user_id)
    if not user_data:
        return BalanceCheckResponse(
            status="failed",
            message="User not found or has no wallet."
        )

    return BalanceCheckResponse(
        status="success",
        balance=user_data["balance"],
        currency=user_data["currency"],
        message="Balance fetched successfully."
    )
