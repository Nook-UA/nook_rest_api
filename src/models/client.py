from sqlalchemy import Table, Column, LargeBinary
from .utils import *

park = Table(
    "client",
    metadata,
    id_,
    name,
    phone,
    email,
    Column("picture", LargeBinary),
)
