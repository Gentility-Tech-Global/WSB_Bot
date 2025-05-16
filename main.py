from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, account_balance, loans, onboarding, airtime, bills, qr, image_ocr, faq, transfers, admin
from routers.kyc import upgrade as kyc_upgrade
from middleware.request_logger import IPLoggingMiddleware

app = FastAPI(title="SmartBankBot API")

# Middleware
app.add_middleware(IPLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
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

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartBankBot API"}

@app.get("/health")
def health():
    return {"status": "ok"}
