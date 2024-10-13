from sqlalchemy import Table, Column, LargeBinary
from .utils import *

client_table = Table(
    "client",
    metadata,
    id_,
    name,
    phone,
    email,
    Column("picture", LargeBinary),
)
