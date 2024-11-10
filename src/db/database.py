from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..settings import settingObj

POSTGRES_DATABASE_URL = f"postgresql://{settingObj.db_user}:{settingObj.db_password}@{settingObj.db_host}:{settingObj.db_port}/{settingObj.db_name}"

engine = create_engine(POSTGRES_DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
