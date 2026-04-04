import datetime
from typing import Optional, List

from pydantic import BaseModel
from typing_extensions import TypedDict
from sqlmodel import SQLModel, Field, Relationship


class TripUserLink(SQLModel, table=True):
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


class SkillUserLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


class TripDefault(SQLModel):
    start_date: datetime.date
    end_date: datetime.date
    departure_place: str
    arrival_place: str
    description: str


class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    users: Optional[List["User"]] = Relationship(back_populates="trips", link_model=TripUserLink)


class ProfessionDefault(SQLModel):
    title: str
    description: Optional[str]


class Profession(ProfessionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    users_prof: List["User"] = Relationship(back_populates="profession")


class SkillDefault(SQLModel):
    title: str
    description: Optional[str]


class Skill(SkillDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    users: Optional[List["User"]] = Relationship(back_populates="skills", link_model=SkillUserLink)


class UserDefault(SQLModel):
    username: str
    birth_date: datetime.date
    description: Optional[str]
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="users_prof")
    skills: Optional[List[Skill]] = Relationship(
        back_populates="users",
        link_model=SkillUserLink)
    trips: Optional[List[Trip]] = Relationship(
        back_populates="users", link_model=TripUserLink)


class UserFull(UserDefault):
    profession: Optional[Profession] = None
    skills: Optional[List[Skill]] = None
    trips: Optional[List[Trip]] = None


class UserSkills(UserDefault):
    skills: Optional[List[Skill]] = None


class AddSkillsRequest(BaseModel):
    skill_ids: List[int]


class AddTripRequest(BaseModel):
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
