from fastapi import FastAPI
from routers import auth, account_balance, onboarding, transactions, airtime, bills, loan, qr, image_ocr, faq
from routers import admin
from routers.kyc import upgrade as kyc_upgrade

app = FastAPI(title="SmartBankBot API")

# Include Routers
app.include_router(onboarding.router, prefix="/api/v1/onboarding")
app.include_router(account_balance.router, prefix="/api/v1/account")
app.include_router(transactions.router, prefix="/api/v1/transfer")
app.include_router(airtime.router, prefix="/api/v1/airtime")
app.include_router(bills.router, prefix="/api/v1/bills")
app.include_router(loan.router, prefix="/api/v1/loan")
app.include_router(qr.router, prefix="/api/v1/qr")
app.include_router(image_ocr.router, prefix="/api/v1/ocr")
app.include_router(faq.router, prefix="/api/v1/faq")
app.include_router(auth.router, prefix="/app/v1", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(kyc_upgrade.router, prefix="/kyc", tags=["KYC"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartBankBot API"}
