""" This script generates a graph of the database schema and saves it as a PNG file to be used in the README.md file.
"""
import json

from sqlalchemy import MetaData, JSON, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

from sqlalchemy_db_graphing import generate_graph_as_png, generate_graph_as_svg, PRESETS

SCHEMA_NAME = "my_app_schema"
metadata = MetaData(schema=SCHEMA_NAME)
Base = declarative_base(metadata=metadata)


class Quantity(Base):
    __tablename__ = "quantities"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String, ForeignKey("units.id"))
    api_of_origin = Column(String, ForeignKey("apis.id"))

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)

class Api(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    description = Column(String)

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True)
    from_unit = Column(String, ForeignKey("units.id"))
    to_unit = Column(String, ForeignKey("units.id"))
    factor = Column(Float)
    offset = Column(Float)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    model_definition = Column(JSON)

class MeasuredQuantity(Base):
    __tablename__ = "measured_quantities"

    quantity_id = Column(Integer, ForeignKey("quantities.id"), primary_key=True)
    date = Column(DateTime, primary_key=True)
    value = Column(Float)

class SimulationResults(Base):
    __tablename__ = "simulation_results"

    quantity_id = Column(Integer, ForeignKey("quantities.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), primary_key=True)
    value = Column(Float)
    simulation_date = Column(DateTime, primary_key=True)
    results = Column(JSON)
    success = Column(Boolean)
    message = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    role = Column(Integer, ForeignKey("roles.id"))

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class SimulationTask(Base):
    __tablename__ = "simulation_tasks"

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    date_target = Column(DateTime)
    date_created = Column(DateTime)
    attempts = Column(Integer)
    success = Column(Boolean)


if __name__ == "__main__":
    generate_graph_as_png(metadata=metadata, filename="diagrams/default.png")

    generate_graph_as_png(
        metadata=metadata,
        style_options="blue",
        display_legend=False,
        filename=f"diagrams/blue.png",
        rankdir="LR",
        splines = "ortho",
    )
    generate_graph_as_png(
        metadata=metadata,
        filename=f"diagrams/purple_rounded.png",
        style_options="purple_rounded",
        display_legend=False,
        rankdir="TD",  # Draw the graph from Left to Right instead of Top Down.
        splines="curved",
    )
    generate_graph_as_png(
        metadata=metadata,
        filename=f"diagrams/purple_blue.png",
        style_options="purple_blue",
        display_legend=False,
        rankdir="TD",  # Draw the graph from Left to Right instead of Top Down.
        splines="ortho",
    )
