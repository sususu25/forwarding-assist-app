from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    hscode: str
    packaging: str
    qty: int
    weight: float

class CheckRequest(BaseModel):
    destination: str
    items: List[Item]
