from pydantic import BaseModel, Field


class ProposalCreate(BaseModel):
    bid_amount: float = Field(gt=0)
    cover_letter: str = Field(min_length=10)
    delivery_time: int = Field(gt=0)