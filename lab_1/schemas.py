from typing import Optional, List
import datetime
import pydantic
from typing_extensions import TypedDict
from sqlmodel import Field
from models import * 

class AddSkillsRequest(pydantic.BaseModel):
    skill_ids: List[int]


class AddTripRequest(pydantic.BaseModel):
    trip_ids: List[int]


class ProfessionCreateResponse(TypedDict):
    status: int
    data: Profession


class UserCreateResponse(TypedDict):
    status: int
    data: User


class SkillCreateResponse(TypedDict):
    status: int
    data: Skill


class TripCreateResponse(TypedDict):
    status: int
    data: Trip


class UserCreateRequest(pydantic.BaseModel):
    username: str = pydantic.Field(..., min_length=3, max_length=50)
    password: str = pydantic.Field(..., min_length=8)
    birth_date: datetime.date
    description: Optional[str] = None
    experience: Optional[int] = None
    profession_id: Optional[int] = None
    project_preferences: Optional[str] = None


class LoginRequest(pydantic.BaseModel):
    username: str
    password: str



class ChangePasswordRequest(pydantic.BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str


class UserUpdate(SQLModel):
    username: Optional[str] = None
    birth_date: Optional[datetime.date] = None
    description: Optional[str] = None
    experience: Optional[int] = None
    profession_id: Optional[int] = None
    project_preferences: Optional[str] = None