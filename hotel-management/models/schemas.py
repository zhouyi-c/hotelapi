from pydantic import BaseModel, conint
from datetime import date
from typing import Optional

class HotelQuery(BaseModel):
    min_price: conint(ge=0) = 0
    max_price: conint(le=10000) = 1000
    date: Optional[date] = None

class ComplaintRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = "default"

class ComplexQuery(BaseModel):
    query: str

class AttractionRequest(BaseModel):
    radius: int