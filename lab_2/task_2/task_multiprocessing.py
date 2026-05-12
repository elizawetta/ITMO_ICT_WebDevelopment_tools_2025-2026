import multiprocessing
import time
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from sqlmodel import SQLModel, Field, Session, create_engine

class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]

DB_USER = "postgres"
DB_PASS = "db"
DB_HOST = "localhost"
DB_NAME = "trips"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)



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



def parse_and_save(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip()
        skill = Skill(
            title=title + ' [multiprocessing]',
            description=f"Parsed from {url}"
        )
        with Session(engine) as session:
            session.add(skill)
            session.commit()

    except Exception as e:
        print(f"[ERROR] {url}: {e}")



if __name__ == "__main__":
    start_time = time.time()

    with multiprocessing.Pool(4) as pool:
        pool.map(parse_and_save, URLS)

    end_time = time.time()

    print("Multiprocessing finished")
    print(f"Execution time: {end_time - start_time:.2f} sec")