from connection import get_session
from security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from models import *
from schemas import *

router = APIRouter()


@router.post("/register")
def register(user_data: UserCreateRequest, db: Session = Depends(get_session)):
    h_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=h_password,
        birth_date=user_data.birth_date,
        description=user_data.description,
        experience=user_data.experience,
        profession_id=user_data.profession_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "ok", "user_id": new_user.id}


@router.post("/login")
def login(form_data: LoginRequest, db: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    user = db.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
