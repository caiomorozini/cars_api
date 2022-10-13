import databases
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.core.config import settings
from sqlalchemy import Column, String, Table, CheckConstraint, Boolean


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)


users = Table(
    "users",
    metadata,
    Column(
        "id", String,
        server_default=text("gen_random_uuid()"),
        primary_key=True),
    Column("email",String, nullable=False, unique=True),
    Column("password",String, nullable=False),
    Column("Created at",TIMESTAMP(timezone=True),
        nullable=False,server_default=text('now()')),
)

owners = Table(
    "owners",
    metadata,
    Column(
        "id", String,
        server_default=text("gen_random_uuid()"),
        primary_key=True),
    Column("name", String, nullable=False),
    Column("email",String, nullable=False, unique=True),
    Column("sale_opportunity", Boolean, nullable=False, default=True),
    Column("Created at",TIMESTAMP(timezone=True), server_default=text('now()')),
)

cars = Table(
    "cars",
    metadata,
    Column(
        "id", String,
        server_default=text("gen_random_uuid()"),
        primary_key=True),
    Column("model",
           String,
            CheckConstraint("model in ('hatch', 'sedan', 'convertible')"),
            nullable=False),
    Column(
        "color",
        String,
        CheckConstraint("color in ('yellow', 'blue', 'gray')"),
        nullable=False),
    Column(
        "owner_email",
        String,
        ForeignKey("owners.email"),
        nullable=False),
    Column("Created at",TIMESTAMP(timezone=True), server_default=text('now()')),
    )


metadata.create_all(engine)
