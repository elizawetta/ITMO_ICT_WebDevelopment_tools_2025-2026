from connection import init_db, create_database
from fastapi import FastAPI
from routers import auth, skills, professions, trips, users

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_database()
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"


app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(professions.router, prefix="/api/professions", tags=["Professions"])
