import os
import time
import asyncio
from celery import Celery
import httpx


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")


celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)


celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_expires = 3600 

celery_app.conf.beat_schedule = {
    'parse-every-hour': {
        'task': 'parse_urls_task', 
        'schedule': 10.0, 
        'args': (['https://python.org', 'https://fastapi.tiangolo.com'],)
    },
}

celery_app.conf.timezone = 'UTC'

@celery_app.task(name="parse_urls_task")
def parse_urls_task(urls: list):
    PARSER_URL = "http://parser_service:8001/parse"
    
    with httpx.Client(timeout=60.0) as client:
        response = client.post(PARSER_URL, json={"urls": urls})
        return response.json()