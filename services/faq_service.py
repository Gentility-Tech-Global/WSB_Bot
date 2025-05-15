from schemas.faq_ import FAQ, FAQResponse, PartnerRequest

#Mock FAQ data(to be replaced with DB or CMS integration)
faqs = [ 
    FAQ(id=1, question="How do I fund my wallet?", answer="You can fund your wallet through your bank, USSD, or agents."),
    FAQ(id=2, question="How do I buy airtime?", answer="Use the Airtime option from the main menu and follow the prompts."),
    FAQ(id=3, question="What is the loan interest rate?", answer="Our loan interest starts at 3% monthly depending on the product."),
]

ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

def validate_partner(partner: str) -> bool:
    return partner in ALLOWED_PARTNERS

def get_faqs(request: PartnerRequest) -> FAQResponse:
    if not validate_partner(request.channel_partner):
        return FAQResponse(
            status="failed",
            message=f"Unauthorized access from: {request.channel_partner}"
        )
    
    return FAQResponse(
        status="success",
        data=faqs,
        message="FAQs retrived successfully"
    )
