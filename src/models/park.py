from sqlalchemy import Table, Column, Integer, String, LargeBinary, ForeignKey
from .utils import *

park = Table(
    "park",
    metadata,
    id_,
    name,
    Column("picture", LargeBinary),
    Column("location", String),
    Column("total_spots", Integer),
    Column("owner", Integer, ForeignKey("client.id")),
)
