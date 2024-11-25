""" Module for pytest fixtures. """

import pytest
from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

metadata_1 = MetaData()
TestBase1 = declarative_base(metadata=metadata_1)


class User(TestBase1):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    age = Column(Integer)
    height = Column(Float)
    active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    roles = Column(Integer, ForeignKey(column=f"roles.id"))


class Role(TestBase1):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


SCHEMA = "test_schema"
metadata_2 = MetaData(schema=SCHEMA)
TestBase2 = declarative_base(metadata=metadata_2)


class User(TestBase2):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    age = Column(Integer)
    height = Column(Float)
    active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    roles = Column(Integer, ForeignKey(column=f"{SCHEMA}.roles.id"))


class Role(TestBase2):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


metadata_3 = MetaData()
TestBase3 = declarative_base(metadata=metadata_3)


class User(TestBase3):
    __tablename__ = "users"
    __table_args__ = {"schema": "test_schema"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    age = Column(Integer)
    height = Column(Float)
    active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    roles = Column(Integer, ForeignKey(column=f"test_schema_2.roles.id"))


class Role(TestBase3):
    __tablename__ = "roles"
    __table_args__ = {"schema": "test_schema_2"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


@pytest.fixture
def test_databases():
    return {
        "test_base_default_schema": TestBase1,
        "test_base_custom_schema": TestBase2,
        "test_base_multiple_schemas": TestBase3,
    }
