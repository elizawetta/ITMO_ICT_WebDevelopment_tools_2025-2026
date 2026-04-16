from sqlalchemy import select
from connection import init_db, create_database, get_session
from fastapi import HTTPException, Depends
from sqlmodel import Session, select, col
from fastapi import APIRouter
from schemas import *
from models import *

router = APIRouter()


@router.get("/list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@router.get("/{skill_id}")
def skill_get(skill_id: int,
              session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)


@router.post("/")
def skill_create(skill: SkillDefault,
                 session=Depends(get_session)) -> SkillCreateResponse:
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return SkillCreateResponse(status=201, data=skill)


@router.delete("/delete/{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}


@router.patch("/{skill_id}")
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

