from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = "whatsapp:+14155238886"  # Twilio sandbox

client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_whatsapp_otp(phone: str, otp: str):
    to = f"whatsapp:{phone}"
    body = f"🔐 Your verification code is: {otp}. It expires in 5 minutes."

    client.messages.create(
        body=body,
        from_=WHATSAPP_FROM,
        to=to
    )
