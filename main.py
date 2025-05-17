import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import (
    auth, account_balance, loans, onboarding, airtime, bills,
    qr, image_ocr, faq, transfers, admin, whatsapp
)
from routers.kyc import upgrade as kyc_upgrade
from middleware.request_logger import IPLoggingMiddleware
from services.redis_service import init_redis_pool

# Configure logger
logger = logging.getLogger("uvicorn.redis")

# 👇 Define lifespan handler BEFORE passing it to FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        redis_password = os.getenv("REDIS_PASSWORD", None)

        await init_redis_pool(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password
        )
        logger.info("✅ Redis initialized successfully")
        yield
    except Exception as e:
        logger.error(f"❌ Redis startup error: {e}")
        raise e

# 👇 Initialize FastAPI app AFTER defining lifespan
app = FastAPI(title="SmartBankBot API", lifespan=lifespan)

# Middleware
app.add_middleware(IPLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(onboarding.router, prefix="/api/v1/onboarding")
app.include_router(account_balance.router, prefix="/api/v1/account")
app.include_router(transfers.router, prefix="/api/v1/transfer")
app.include_router(airtime.router, prefix="/api/v1/airtime")
app.include_router(bills.router, prefix="/api/v1/bills")
app.include_router(loans.router, prefix="/api/v1/loan")
app.include_router(qr.router, prefix="/api/v1/qr")
app.include_router(image_ocr.router, prefix="/api/v1/ocr")
app.include_router(faq.router, prefix="/api/v1/faq")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(kyc_upgrade.router, prefix="/api/v1/kyc", tags=["KYC"])
app.include_router(whatsapp.router)

# Health check routes
@app.get("/")
def read_root():
    return {"message": "Welcome to SmartBankBot API"}

@app.get("/health")
def health():
    return {"status": "ok"}
