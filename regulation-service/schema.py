from pydantic import BaseModel
from typing import List, Optional

class RegulationResponse(BaseModel):
    country: str
    cargo_type: str
    required_documents: List[str]
    packaging_requirement: Optional[str]
    co_required: Optional[bool]
    notes: Optional[str]