from typing import Optional, List
import datetime
from sqlmodel import SQLModel, Field, Relationship


class TripUserLink(SQLModel, table=True):
    trip_id: int = Field(default=None, foreign_key="trip.id", primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role: str = Field(default="passenger")


class SkillUserLink(SQLModel, table=True):
    skill_id: int = Field(default=None, foreign_key="skill.id", primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)


class TripDefault(SQLModel):
    start_date: datetime.date
    end_date: datetime.date
    departure_place: str
    arrival_place: str
    description: str


class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    creator_id: int = Field(foreign_key="user.id")
    creator: "User" = Relationship(back_populates="created_trips")
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
    experience: int | None
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")
    project_preferences: Optional[str] | None


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    profession: Optional[Profession] = Relationship(back_populates="users_prof")
    skills: Optional[List[Skill]] = Relationship(
        back_populates="users",
        link_model=SkillUserLink)
    trips: Optional[List[Trip]] = Relationship(
        back_populates="users", link_model=TripUserLink)
    created_trips: List["Trip"] = Relationship(back_populates="creator")


class UserFull(UserDefault):
    profession: Optional[Profession] = None
    skills: Optional[List[Skill]] = None
    trips: Optional[List[Trip]] = None


class UserSkills(UserDefault):
    skills: Optional[List[Skill]] = None




