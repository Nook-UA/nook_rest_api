from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
    MetaData,
)
from sqlalchemy.orm import declarative_base

metadata = MetaData()

id_ = Column("id", Integer, Identity(start=0, increment=1), primary_key=True)
name = Column("name", String)
phone = Column("phone", String)
email = Column("mail", String)

Base = declarative_base(metadata=metadata)