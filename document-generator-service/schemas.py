from pydantic import BaseModel, Field
from typing import Literal, List

class Item(BaseModel):
    name: str
    qty: int = Field(gt=0)
    unit: str = "PCS"
    amount: float = 0

class PdfRequest(BaseModel):
    doc_type: Literal["CI", "PL"]
    exporter: str
    consignee: str
    destination: str
    invoice_no: str
    lc_no: str | None = None
    port_of_loading: str | None = None
    items: List[Item]
