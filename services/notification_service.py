import requests
from core.config import settings
from datetime import datetime

def send_whatsapp_message(to_number: str, message: str):
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message}
        }
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            settings.WHATSAPP_API_URL,
            json=payload,
            headers=headers
        )
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to send WhatsApp message: {response.text}")
    except Exception as e:
        raise RuntimeError(f"WhatsApp notification failed: {str(e)}")
    

def send_webhook_fallback(payload: dict) -> None:
    """
    Trigger fallback webhook notification if WhatsApp fails.
    """
    try:
        data = {
            "user_id": payload["user_id"],
            "merchant_id": payload["merchant_id"],
            "amount": payload["amount"],
            "merchant_name": payload.get("merchant_name"),
            "timestamp": datetime.utcnow().isoformat()
        }
        response = requests.post(settings.webhook_url, json=data, timeout=10)
        response.raise_for_status()
    except Exception as e:
        # Log this error in future via a logger
        print(f"[WebhookFallback] Failed to notify webhook: {str(e)}")
