from fastapi import APIRouter, Request, status, BackgroundTasks
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from services.whatsapp_logic import handle_whatsapp_command
import logging

router = APIRouter(prefix="/webhook", tags=["WhatsApp Bot"])

logger = logging.getLogger("uvicorn.whatsapp")

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    WhatsApp webhook endpoint for Twilio Sandbox or Production.
    Receives incoming messages from users and routes to command handler.
    Returns a TwiML response with the bot's reply.
    """
    try:
        form = await request.form()
        sender = form.get("From")
        message = form.get("Body")
        media_url = form.get("MediaUrl0") if int(form.get("NumMedia", "0")) > 0 else None

        if not sender or not message:
            logger.warning("Missing sender or message body in request.")
            return PlainTextResponse("Missing required fields", status_code=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received WhatsApp message from {sender}: {message}")
        
        # Call handler (media or message)
        if media_url:
            reply = await handle_whatsapp_command("upload image", sender, media_url)
        else:
            reply = await handle_whatsapp_command(message.strip(), sender)

        # Respond with TwiML
        twiml_response = MessagingResponse()
        twiml_response.message(reply)

        return PlainTextResponse(str(twiml_response), status_code=200, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error handling WhatsApp webhook: {e}", exc_info=True)
        return PlainTextResponse("Internal server error", status_code=500)
