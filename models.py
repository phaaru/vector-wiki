from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# notes = sqlalchemy.Table(
#     "notes",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("text", sqlalchemy.String),
#     sqlalchemy.Column("completed", sqlalchemy.Boolean),
# )

# continents = Table(
#     "continent",
#     metadata,
#     Column("id")
# )

class Continent(Base):
    __tablename__ = "continent"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    population = Column(Integer)
    area_in_sqm = Column(Integer)
    countries = relationship(
        "Country", back_populates="continent",
        cascade="all, delete",
        passive_deletes=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    population = Column(Integer)
    area_in_sqm = Column(Integer)
    quantity_national_parks = Column(Integer)
    quantity_hospitals = Column(Integer)
    continent_id = Column(Integer, ForeignKey('continent.id', ondelete="CASCADE"))
    continent = relationship("Continent", back_populates="countries")
    cities = relationship(
        "City", back_populates="country",
        cascade="all, delete",
        passive_deletes=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    population = Column(Integer)
    area_in_sqm = Column(Integer)
    quantity_roads = Column(Integer)
    quantity_trees = Column(Integer)
    country_id = Column(Integer, ForeignKey('country.id', ondelete="CASCADE"))
    country = relationship("Country", back_populates="cities")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Cascade Delete does not work on SQLite
# https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys
# When SQLite foreign keys are enabled, it is not possible to emit CREATE or DROP statements for tables that contain mutually-dependent foreign key constraints; to emit the DDL for these tables requires that ALTER TABLE be used to create or drop these constraints separately, for which SQLite has no support.
