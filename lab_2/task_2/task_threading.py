import threading
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional



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
            title=title + ' [threading]',
            description=f"Parsed from {url}"
        )

        with Session(engine) as session:
            session.add(skill)
            session.commit()

        # print(f"[SUCCESS] {url} -> {title}")

    except Exception as e:
        print(f"[ERROR] {url}: {e}")


threads = []
start_time = time.time()


for url in URLS:
    thread = threading.Thread(target=parse_and_save, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()

print("Threading finished")
print(f"Execution time: {end_time - start_time:.2f} sec")