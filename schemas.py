from typing import Optional
from pydantic import BaseModel

class Customer(BaseModel):
    Gender: Optional[str] = None
    Age: Optional[int] = None
    AnnualIncome: Optional[float] = None
    SpendingScore: Optional[int] = None

    class Config():
        schema_extra = {
            "example": {
                "Gender": "Female",
                "Age": 25,
                "AnnualIncome": 18000.0,
                "SpendingScore": 50
            }
        }

class ShowCustomer(BaseModel):
    Gender: Optional[str] = None
    Age: Optional[str] = None
    SpendingScore: Optional[int] = None
    # If we want to use this as response model
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class Showuser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True