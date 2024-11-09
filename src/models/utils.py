from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
)

id_ = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
name = Column("name", String)
phone = Column("phone", String)
email = Column("mail", String)