from sqlalchemy import select
from connection import get_session
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import Session, select, col
from schemas import *
from models import *

router = APIRouter()

@router.get("/list")
def profession_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@router.get("/{profession_id}")
def professions_get(profession_id: int,
                    session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@router.post("/")
def profession_create(prof: ProfessionDefault,
                      session=Depends(get_session)) -> ProfessionCreateResponse:
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return ProfessionCreateResponse(status=201, data=prof)


@router.delete("/delete/{profession_id}")
def professions_delete(profession_id: int, session=Depends(get_session)):
    profession = session.get(Profession, profession_id)
    if not profession:
        raise HTTPException(status_code=404, detail="profession not found")
    session.delete(profession)
    session.commit()
    return {"ok": True}


@router.patch("/{profession_id}")
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

