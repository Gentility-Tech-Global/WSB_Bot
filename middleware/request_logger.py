from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

logger =logging.getLogger("uvicorn.access")

class IPLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        user_agent = request.headers.get("user-agent")
        logger.info(f"Request from IP: {ip}, User-Agent: {user_agent}")
        response = await call_next(request)
        return response