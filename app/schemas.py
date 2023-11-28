from uuid import UUID
from typing import Optional, Annotated
from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    username : Optional[str] = Field(None, description="user name")
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    emergency_contact1 : Optional[int] = Field(None, description="emergency contact 1")
    emergency_contact2 : Optional[int] = Field(None, description="emergency contact 2")
    emergency_contact3 : Optional[int] = Field(None, description="emergency contact 3")

    class Config:
        schema_extra = {
            "example": {
                "username" : "jeetb",
                "email": "jeetBarot@x.com",
                "password": "NewPass@02"
            }
        }

class UserOut(BaseModel):
    username: str
    email: str
    emergency_contact1 : Optional[int]
    emergency_contact2 : Optional[int]
    emergency_contact3 : Optional[int]



class SystemUser(UserOut):
    id: int
    password: str

class UserLocationData(BaseModel):
    first_attempt : Optional[bool] = False
    latitude : Optional[float]
    longitude : Optional[float]