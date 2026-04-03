import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from typing import TypedDict




class Trip(BaseModel):
    id: int
    start_date: datetime.date
    end_date: datetime.date
    route: str
    description: str


class TripMembers(BaseModel):
    id: int
    id_user: int
    id_trip: int

class Skill(BaseModel):
    id: int
    title: str
    description: Optional[str]

class Profession(BaseModel):
    id: int
    title: str
    description: Optional[str]


class User(BaseModel):
    id: int
    username: str
    birth_date: datetime.date
    experience: int
    profession: Profession
    skills: Optional[List[Skill]] = []

class ProfessionCreateResponse(TypedDict):
    status: int
    data: Profession


class UserCreateResponse(TypedDict):
    status: int
    data: User