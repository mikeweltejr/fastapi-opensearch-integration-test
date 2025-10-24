from pydantic import BaseModel, Field
from .filters import Filters

class RetrieveRequest(BaseModel):
    query: str = Field(min_length=1)
    filters: Filters = Field(default_factory=Filters)
    size: int = Field(10, ge=1, le=20)
    from_: int = Field(0, ge=0, alias="from")
    num_candidates: int = Field(1000, ge=1, le=1000)
