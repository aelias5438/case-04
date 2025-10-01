from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
from typing_extensions import Literal



class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = Field(..., description="Must be true to accept")
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)
    user_agent: Optional[str] = None     
    submission_id: Optional[str] = None
    source: Optional[str] = "other"
  
    @validator("rating", pre=True)
    def parse_rating(cls, v):
        if isinstance(v, str) and v.strip():
            return int(v.split()[0])  # "2 - Poor" -> 2
        return v
    @validator("comments")
    def _strip_comments(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("consent")
    def _must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v
        
#Good example of inheritance
class StoredSurveyRecord(BaseModel):
    name: str
    consent: bool
    rating: int
    comments: Optional[str] = None
    source: Literal["homepage","email","qr","other"] = "other"
    user_agent: Optional[str] = None

    hash_email: str
    hash_age:str
    submission_id: str

    received_at: datetime
    ip: str
