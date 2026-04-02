from pydantic import BaseModel, EmailStr


class LeadOut(BaseModel):
    name: str
    email: EmailStr
