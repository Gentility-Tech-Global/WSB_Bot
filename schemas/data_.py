from pydantic import BaseModel, constr, conint
from typing import Optional, Literal, Annotated

PhoneNumberStr = Annotated[str, constr(min_length=10, max_length=15)]
DataPlanType = Literal["daily", "weekly", "monthly"]
PositiveInt = Annotated[int, conint(gt=0)]
NetworkName = Literal["mtn", "glo", "airtel", "9mobile"]

class DataTopUpRequest(BaseModel):
    phone_number: PhoneNumberStr
    amount: PositiveInt
    network: NetworkName
    Plan_type: DataPlanType
    user_id: str

class DataTopUpResponse(BaseModel):
    status: str
    transaction_id: Optional[str]
    message: Optional[str] = None