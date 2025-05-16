import re
from services.transaction_service import process_transfer, process_balance
from services.onboarding_service import onboard_user
from services.airtime_services import airtime_topup, data_topup
from services.loan_service import handle_loan_application
from services.bills_service import handle_bill_payment
from services.state_manager import get_session_state, set_session_state


async def handle_whatsapp_command(message: str, sender: str) -> str:
    text = message.strip().lower()

    # Session-based triggers for multi-step commands
    session = await get_session_state(sender)
    if session == "awaiting_qr_image":
        return "Please upload the QR code image to proceed."
    elif session == "awaiting_slip_image":
        return "Please upload the account slip image to proceed."

    # Balance check
    if text.startswith("bal") or "balance" in text:
        pin_match = re.findall(r"\d{4,6}", text)
        if not pin_match:
            return "Please provide your 4-digit PIN. Example: BAL 1234"
        return await process_balance(sender, pin_match[0])

    # Transfer
    if text.startswith("transfer"):
        return await process_transfer(text, sender)

    # Airtime/Data top-up
    if "airtime" in text:
        return await airtime_topup(text, sender)
    if "data" in text:
        return await data_topup(text, sender)

    # Loan request
    if "loan" in text:
        return await handle_loan_application(text, sender)

    # User onboarding
    if "signup" in text or "onboard" in text:
        return await onboard_user(text, sender)

    # Bill payment
    if "pay bill" in text or "bill payment" in text:
        return await handle_bill_payment(text, sender)

    # Support/help
    if "support" in text or "help" in text:
        return ("Need help? Our support team will contact you shortly, or call us on +234 81 601 88661")

    # QR scan trigger
    if "qr" in text or "scan" in text:
        await set_session_state(sender, "awaiting_qr_image")
        return "Please send the QR code image now."

    # Image/receipt upload
    if "image" in text or "upload" in text:
        await set_session_state(sender, "awaiting_slip_image")
        return "Please upload the account slip image now."

    return ("Sorry, I couldn't understand your request. Try commands like:\n"
            "• BAL 1234\n"
            "• Transfer 1000 to GTBank 0123456789\n"
            "• Airtime 500 to 0803xxxxxxx\n"
            "• Onboard John Doe, 08012345678, 2233445566, 1995-06-01\n"
            "\nAfter onboarding, you'll receive your account number automatically.")
