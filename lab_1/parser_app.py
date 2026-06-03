import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Skill
from schemas import ParseRequest
from dotenv import load_dotenv
import os


load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:5432/{DB_NAME}"
)



engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

app = FastAPI(title="Parser Microservice")

semaphore = asyncio.Semaphore(5)

async def parse_and_save(client, url: str):
    async with semaphore:
        try:
            async with client.get(url) as response:
                html = await response.text()

            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string.strip() if soup.title else "No title"
            skill = Skill(
                title=title + " [async]",
                description=f"Parsed from {url}"
            )

            async with AsyncSessionLocal() as session:
                session.add(skill)
                await session.commit()

            return { "url": url, "title": title, "status": "saved"}

        except Exception as e:
            return {"url": url, "status": "error", "error": str(e)}



@app.post("/parse")
async def parse_urls(data: ParseRequest):
    start_time = time.time()
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as client:
        tasks = [asyncio.create_task(parse_and_save(client, url)) for url in data.urls]
        results = await asyncio.gather(*tasks)
    execution_time = round(time.time() - start_time, 2)
    return {
        "status": "success",
        "parsed": len(results),
        "execution_time": execution_time,
        "results": results
        }


@app.on_event("startup")
async def on_startup():
    pass
