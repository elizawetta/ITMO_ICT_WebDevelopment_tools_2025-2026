from sqlalchemy import select
from connection import get_session
from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from fastapi import APIRouter, Query
from security import get_current_user
from schemas import *
from models import *

router = APIRouter()


@router.get("/list")
def trips_list(session=Depends(get_session)) -> List[Trip]:
    return session.exec(select(Trip)).all()

@router.get("/search", response_model=List[Trip])
def search_trips(departure: Optional[str] = Query(None),
                 arrival: Optional[str] = Query(None),
                 start_date: Optional[datetime.date] = Query(None),
                 end_date: Optional[datetime.date] = Query(None),
                 db: Session = Depends(get_session)) -> List[Trip]:
    statement = select(Trip)
    if departure:
        statement = statement.where(Trip.departure_place == departure)
    if arrival:
        statement = statement.where(Trip.arrival_place == arrival)
    if start_date:
        statement = statement.where(Trip.start_date == start_date)
    if end_date:
        statement = statement.where(Trip.end_date == end_date)

    results = db.exec(statement).all()
    return results

@router.get("/{trip_id}")
def trip_get(trip_id: int,
             session=Depends(get_session)) -> Trip:
    return session.get(Trip, trip_id)


@router.post("/")
def trip_create(trip_in: TripDefault,
                session=Depends(get_session),
                current_user: User = Depends(get_current_user)) -> TripCreateResponse:
    trip_data = trip_in.model_dump()
    trip_data["creator_id"] = current_user.id
    db_trip = Trip.model_validate(trip_data)
    session.add(db_trip)
    session.commit()
    session.refresh(db_trip)
    return TripCreateResponse(status=201, data=db_trip)


@router.delete("/delete/{trip_id}")
def trip_delete(trip_id: int,
                session=Depends(get_session),
                current_user: User = Depends(get_current_user)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="trip not found")
    if trip.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden")
    session.delete(trip)
    session.commit()
    return {"ok": True}


@router.patch("/{trip_id}")
def trip_update(trip_id: int,
                session=Depends(get_session),
                current_user: User = Depends(get_current_user)) -> Trip:
    db_trip = session.get(Trip, trip_id)
    if not db_trip:
        raise HTTPException(status_code=404, detail="trip not found")
    if db_trip.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden")
    data = db_trip.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(data, key, value)
    session.add(data)
    session.commit()
    session.refresh(db_trip)
    return db_trip





@router.delete("/{trip_id}/leave")
def leave_trip(
        trip_id: int,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    statement = select(TripUserLink).where(
        TripUserLink.trip_id == trip_id,
        TripUserLink.user_id == current_user.id
    )
    link = db.exec(statement).first()

    if not link:
        raise HTTPException(status_code=404, detail="Вы не являетесь участником этой поездки")

    db.delete(link)
    db.commit()

    return {"message": "Вы успешно покинули поездку"}
