from pydantic import BaseModel

class TravelRequest(BaseModel):
    name: str
    destination: str
    days: int
    budget: int