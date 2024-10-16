import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv

def get_session() -> Session:
    load_dotenv()
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    database = os.getenv('POSTGRES_DB')
    engine = None
    try:
        engine = create_engine(f'postgresql://{user}:{password}@db:5432/{database}')
    except Exception as e:
        print('Unable to access postgresql database', repr(e))
    session = Session(engine)
    return session
