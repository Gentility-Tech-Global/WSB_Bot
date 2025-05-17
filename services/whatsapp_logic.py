import re
from typing import Optional

from services.transaction_service import process_transfer, process_balance
from services.onboarding_service import onboard_user
from services.airtime_services import airtime_topup
from services.data_service import data_topup
from services.loan_service import handle_loan_application
from services.bills_service import handle_bill_payment
from services.state_manager import get_session_state, set_session_state

# Constants for session states
SESSION_AWAITING_QR_IMAGE = "awaiting_qr_image"
SESSION_AWAITING_SLIP_IMAGE = "awaiting_slip_image"

# Predefined user messages
MSG_MISSING_PIN = "Please provide your 4-digit PIN. Example: BAL 1234"
MSG_SUPPORT_CONTACT = (
    "Need help? Our support team will contact you shortly, "
    "or call us on +234 81 601 88661"
)
MSG_UNKNOWN_COMMAND = (
    "Sorry, I couldn't understand your request. Try commands like:\n"
    "• BAL 1234\n"
    "• Transfer 1000 to GTBank 0123456789\n"
    "• Airtime 500 to 0803xxxxxxx\n"
    "• Onboard John Doe, 08012345678, 2233445566, 1995-06-01\n"
    "\nAfter onboarding, you'll receive your account number automatically."
)

async def handle_whatsapp_command(message: str, sender: str, media_url: Optional[str] = None) -> str:
    """
    Main handler for incoming WhatsApp messages.

    Args:
        message (str): Incoming message text from user.
        sender (str): User's WhatsApp number/identifier.
        media_url (Optional[str]): URL to media if sent, otherwise None.

    Returns:
        str: Response message to send back to user.
    """

    # Prioritize media upload handling if media URL is provided
    if media_url:
        # Depending on your app logic, you can route media to a dedicated handler here
        # For now, just acknowledge receipt
        return f"Image received from {sender} — URL: {media_url}"

    text = message.strip().lower()
    session = await get_session_state(sender)

    # Handle session states first (multi-step interactions)
    if session == SESSION_AWAITING_QR_IMAGE:
        return "Please upload the QR code image to proceed."
    if session == SESSION_AWAITING_SLIP_IMAGE:
        return "Please upload the account slip image to proceed."

    # Command dispatch mapping for easier management and extensibility
    if text.startswith("bal") or "balance" in text:
        return await _handle_balance_check(text, sender)

    if text.startswith("transfer"):
        return await process_transfer(text, sender)

    if "airtime" in text:
        return await airtime_topup(text, sender)

    if "data" in text:
        return await data_topup(text, sender)

    if "loan" in text:
        return await handle_loan_application(text, sender)

    if "signup" in text or "onboard" in text:
        return await onboard_user(text, sender)

    if "pay bill" in text or "bill payment" in text:
        return await handle_bill_payment(text, sender)

    if "support" in text or "help" in text:
        return MSG_SUPPORT_CONTACT

    if "qr" in text or "scan" in text:
        await set_session_state(sender, SESSION_AWAITING_QR_IMAGE)
        return "Please send the QR code image now."

    if "image" in text or "upload" in text:
        await set_session_state(sender, SESSION_AWAITING_SLIP_IMAGE)
        return "Please upload the account slip image now."

    return MSG_UNKNOWN_COMMAND


async def _handle_balance_check(text: str, sender: str) -> str:
    """
    Handle the balance check command, validating PIN presence.

    Args:
        text (str): User message text.
        sender (str): User identifier.

    Returns:
        str: Response message.
    """
    pin_match = re.findall(r"\b\d{4,6}\b", text)
    if not pin_match:
        return MSG_MISSING_PIN

    pin = pin_match[0]
    return await process_balance(sender, pin)
