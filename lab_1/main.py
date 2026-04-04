from sqlalchemy import select
from sqlalchemy.orm import selectinload
from connection import init_db, create_database, get_session
from models import *
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select, col

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_database()
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.post("/users")
def users_create(user: UserDefault,
                 session=Depends(get_session)) -> UserCreateResponse:
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserCreateResponse(status=200, data=user)


@app.get("/users_list")
def users_list(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()


@app.get("/users/{user_id}", response_model=UserFull)
def users_get(user_id: int, session=Depends(get_session)) -> User:
    return session.get(User, user_id)


@app.delete("/users/delete/{user_id}")
def users_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@app.patch("/users/{user_id}")
def users_update(user_id: int,
                 user: UserDefault,
                 session=Depends(get_session)) -> UserDefault:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_data, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user







@app.post("/users/{user_id}/skills", response_model=UserFull)
def add_skills_to_user(
        user_id: int,
        request: AddSkillsRequest,
        session: Session = Depends(get_session)
):
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.skills))
    )
    results = session.exec(statement)
    db_user = results.first()

    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    skills_statement = select(Skill).where(col(Skill.id).in_(request.skill_ids))
    db_skills = session.exec(skills_statement).all()

    if not db_skills:
        raise HTTPException(status_code=404, detail="skills not found")
    for skill in db_skills:
        if skill not in db_user.skills:
            db_user.skills.append(skill)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.post("/users/{user_id}/trips", response_model=UserFull)
def add_trips_to_user(
        user_id: int,
        request: AddTripRequest,
        session: Session = Depends(get_session)
):
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.trips))
    )
    results = session.exec(statement)
    db_user = results.first()

    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    trips_statement = select(Trip).where(col(Trip.id).in_(request.trip_ids))
    db_trips = session.exec(trips_statement).all()

    if not db_trips:
        raise HTTPException(status_code=404, detail="skills not found")
    for trip in db_trips:
        if trip not in db_user.trips:
            db_user.trips.append(trip)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.get("/professions_list")
def profession_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/professions/{profession_id}")
def professions_get(profession_id: int,
                    session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/professions")
def profession_create(prof: ProfessionDefault,
                      session=Depends(get_session)) -> ProfessionCreateResponse:
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return ProfessionCreateResponse(status=201, data=prof)


@app.delete("/professions/delete/{profession_id}")
def professions_delete(profession_id: int, session=Depends(get_session)):
    profession = session.get(Profession, profession_id)
    if not profession:
        raise HTTPException(status_code=404, detail="profession not found")
    session.delete(profession)
    session.commit()
    return {"ok": True}


@app.patch("/professions/{profession_id}")
def professions_update(profession_id: int,
                       profession: Profession,
                       session=Depends(get_session)) -> Profession:
    db_profession = session.get(Profession, profession_id)
    if not db_profession:
        raise HTTPException(status_code=404, detail="profession not found")

    profession_data = profession.dict(exclude_unset=True)
    for key, value in profession_data.items():
        setattr(profession_data, key, value)
    session.add(profession_data)
    session.commit()
    session.refresh(db_profession)
    return db_profession


@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skills/{skill_id}")
def skill_get(skill_id: int,
              session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)


@app.post("/skills")
def skill_create(skill: SkillDefault,
                 session=Depends(get_session)) -> SkillCreateResponse:
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return SkillCreateResponse(status=201, data=skill)


@app.delete("/skills/delete/{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}


@app.patch("/skills/{skill_id}")
def skill_update(skill_id: int,
                 skill: Skill,
                 session=Depends(get_session)) -> Skill:
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="skill not found")

    data = skill.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(data, key, value)
    session.add(data)
    session.commit()
    session.refresh(db_skill)
    return db_skill
# LOL

@app.get("/trips_list")
def trips_list(session=Depends(get_session)) -> List[Trip]:
    return session.exec(select(Trip)).all()


@app.get("/trips/{trip_id}")
def trip_get(trip_id: int,
              session=Depends(get_session)) -> Trip:
    return session.get(Trip, trip_id)


@app.post("/trips")
def trip_create(trip: TripDefault,
                 session=Depends(get_session)) -> TripCreateResponse:
    trip = Trip.model_validate(trip)
    session.add(trip)
    session.commit()
    session.refresh(trip)
    return TripCreateResponse(status=201, data=trip)


@app.delete("/trips/delete/{trip_id}")
def trip_delete(trip_id: int, session=Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="trip not found")
    session.delete(trip)
    session.commit()
    return {"ok": True}


@app.patch("/trips/{trip_id}")
def trip_update(trip_id: int,
                 trip: Trip,
                 session=Depends(get_session)) -> Trip:
    db_trip = session.get(Trip, trip_id)
    if not db_trip:
        raise HTTPException(status_code=404, detail="trip not found")

    data = trip.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(data, key, value)
    session.add(data)
    session.commit()
    session.refresh(db_trip)
    return db_trip
