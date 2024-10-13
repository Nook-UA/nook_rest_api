# __all__ = ["connection"]

# from dotenv import load_dotenv
# from os import getenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# class __Database:
#     __engine = None
#     __SessionLocal = None
#     Base = None

#     def __init__(self):
#         self.__save_connection_string(*self.__load_database_info())
#         self.__engine = create_engine(self.conn_string)
#         self.__SessionLocal = sessionmaker(autoflush=False, bind=self.__engine)
#         self.Base = declarative_base()

#     def __save_connection_string(self, user, password, host, port, database):
#         self.conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

#     def __load_database_info(self):
#         load_dotenv(".env")
#         fields = ["USER", "PASSWORD", "HOST", "PORT", "DATABASE"]
#         return tuple(getenv(term) for term in fields)

#     def session(self):
#         db = self.__SessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()

#     def conn(self):
#         return self.__engine.connect()


# database = __Database()
# connection = database.conn()
