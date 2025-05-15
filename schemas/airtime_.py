from pydantic import BaseModel, constr, conint
from typing import Optional, Annotated


PhoneNumberStr = Annotated[str, constr(min_length=10, max_length=15)]
PositiveInt = Annotated[int, conint(gt=0)]

class AirtimeTopUpRequest(BaseModel):
    phone_number: PhoneNumberStr
    amount: PositiveInt
    network: str
    user_id: str

class AirtimeTopUpResponse(BaseModel):
    status: str
    transaction_id: str
    message: Optional[str]