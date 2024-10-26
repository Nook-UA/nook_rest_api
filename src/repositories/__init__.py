__all__ = ["database"]

from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

class __Database:
    __engine = None
    __SessionLocal = None
    __Base = None

    def __init__(self):
        self.__save_connection_string(*self.__load_database_info())

        if not database_exists(self.conn_string):
            create_database(self.conn_string)

        self.__engine = create_engine(self.conn_string, echo=False)
        self.__Base = declarative_base(metadata=MetaData())
        self.__SessionLocal = sessionmaker(autoflush=False, bind=self.__engine)

    def __save_connection_string(self, user, password, host, port, database):
        print(user, password, host, port, database)
        self.conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def __load_database_info(self):
        load_dotenv(".env")
        fields = ["USER_NAME", "PASSWORD", "HOST", "PORT", "DATABASE_NAME"]
        return tuple(getenv(term) for term in fields)

    def init_database(self):
        self.__Base.metadata.create_all(bind=self.__engine)

    @property
    def session(self):
        return self.__SessionLocal()
    
    @property
    def Base(self):
        return self.__Base

    @property
    def conn(self):
        return self.__engine.connect()

database = __Database()
