from sqlalchemy import select
from sqlalchemy.orm import selectinload
from connection import init_db, create_database, get_session
from security import hash_password, verify_password, create_access_token, get_current_user
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select, col
from fastapi import APIRouter

from models import *
from schemas import *


router = APIRouter()

@router.post("/")
def users_create(user: UserDefault,
                 session=Depends(get_session)) -> UserCreateResponse:
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserCreateResponse(status=200, data=user)


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/list")
def users_list(session=Depends(get_session)) -> List[UserFull]:
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserFull)
def users_get(user_id: int, session=Depends(get_session)) -> UserFull:
    return session.get(User, user_id)


@router.delete("/delete/{user_id}")
def users_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@router.patch("/{user_id}")
def users_update(user_id: int,
                 user: UserUpdate,
                 session=Depends(get_session)) -> UserDefault:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/{user_id}/skills", response_model=UserFull)
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


@router.post("/{user_id}/trips", response_model=UserFull)
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
        raise HTTPException(status_code=404, detail="trip not found")
    for trip in db_trips:
        if trip not in db_user.trips:
            db_user.trips.append(trip)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user



@router.patch("/me/change-password")
def change_password(
    data: ChangePasswordRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный текущий пароль"
        )
    
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Новые пароли не совпадают"
        )

    if data.old_password == data.new_password:
        raise HTTPException(
            status_code=400,
            detail="Новый пароль не может совпадать со старым"
        )


    current_user.hashed_password = hash_password(data.new_password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return {"message": "Пароль успешно изменен"}