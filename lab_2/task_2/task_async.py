import asyncio
import time
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

from sqlmodel import SQLModel, Field

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)

from sqlalchemy.orm import sessionmaker


class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]


DB_USER = "postgres"
DB_PASS = "db"
DB_HOST = "localhost"
DB_NAME = "trips"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


URLS = [
    "https://example.com",
    "https://python.org",
    "https://github.com",
    "https://stackoverflow.com",
    "https://wikipedia.org",
    "https://openai.com",
    "https://reddit.com",
    "https://news.ycombinator.com",
    "https://docs.python.org",
    "https://pypi.org",
    "https://fastapi.tiangolo.com",
    "https://sqlmodel.tiangolo.com",
    "https://realpython.com",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.nytimes.com",
    "https://www.mozilla.org",
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.amazon.com",
]


async def parse_and_save(client, url):
    try:
        async with client.get(url) as response:
            html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip()
        skill = Skill(
            title=title + " [async]",
            description=f"Parsed from {url}"
        )
        async with AsyncSessionLocal() as session:
            session.add(skill)
            await session.commit()


    except Exception as e:
        print(f"[ERROR] {url}: {e}")


async def main():
    async with aiohttp.ClientSession() as client:
        tasks = []
        for url in URLS:
            tasks.append(
                asyncio.create_task(
                    parse_and_save(client, url)
                )
            )
        await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main())
end_time = time.time()
print("Async finished")
print(f"Execution time: {end_time - start_time:.2f} sec")