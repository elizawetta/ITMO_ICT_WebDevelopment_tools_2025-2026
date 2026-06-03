from connection import init_db, create_database
from fastapi import FastAPI, HTTPException
from routers import auth, skills, professions, trips, users
from schemas import ParseRequest
import os
import httpx
from celery_app import parse_urls_task, celery_app
from celery.result import AsyncResult

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_database()
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"

PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://parser_service:8001/parse")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(professions.router, prefix="/api/professions", tags=["Professions"])


@app.post("/call-parser")
async def call_parser_endpoint(data: ParseRequest):
    """
    Эндпоинт, который принимает список URL и пересылает их микросервису-парсеру
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                PARSER_SERVICE_URL,
                json={"urls": data.urls},
                timeout=10.0
            )
            
            response.raise_for_status()
            
            return response.json()
            
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Parser service is unavailable")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        


@app.post("/call-parser-async")
async def call_parser_async(data: ParseRequest):
    task = parse_urls_task.delay(data.urls)
    
    return {
        "status": "Task dispatched",
        "task_id": task.id,
        "message": "Parsing has started in the background"
    }


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    result = {
        "task_id": task_id,
        "status": task_result.status,
    }
    
    if task_result.status == 'SUCCESS':
        result["result"] = task_result.result # То, что вернула функция parse_urls_task
    elif task_result.status == 'FAILURE':
        result["error"] = str(task_result.info)
        
    return result