from sqlmodel import SQLModel, Session, create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_USER = "postgres"
DB_PASS = "db"
DB_HOST = "localhost"
DB_NAME = "trips"

db_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
engine = create_engine(db_url, echo=True)

def create_database():
    conn = psycopg2.connect(
        dbname='postgres',
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"База данных {DB_NAME} успешно создана!")
    except psycopg2.errors.DuplicateDatabase:
        print(f"База данных {DB_NAME} уже существует.")
    finally:
        cursor.close()
        conn.close()

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
