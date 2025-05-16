from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

logger = logging.getLogger("uvicorn.access")

class IPLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            ip = request.client.host
            user_agent = request.headers.get("user-agent", "unknown")
            logger.info(f"[Request Log] IP: {ip}, User-Agent: {user_agent}")
        except Exception as e:
            logger.warning(f"Failed to log request details: {str(e)}")

        response = await call_next(request)
        return response
