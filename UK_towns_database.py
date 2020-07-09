import csv # give python csv superpowers


from sqlalchemy import Integer, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Country is currently the "parent" of everything. It is the "root".
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    country = Column(String)


# County is a child of Country
class Town(Base):
    __tablename__ = 'town'
    id = Column(Integer, primary_key=True)
    county = Column(String)
    country_name = Column(String)
    name = Column(String)
    grid_reference = Column(String)
    easting = Column(Integer)
    northing = Column(Integer)
    latitude = Column(String)
    longitude = Column(String)
    elevation = Column(Integer)
    postcode_sector = Column(String)
    local_government_area = Column(String)
    nuts_region = Column(String)
    town_type = Column(String)
    # We define the relationship between Country and County here.
    country = relation("Country", backref="town")
    country_id = Column(Integer, ForeignKey('country.id'))


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine('sqlite:///UK_towns.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


''' Above here defines the DB'''
''' Below here adds data to the DB '''

def addTown(session, town_input):
    # Try and get the Country from the database. If error (Except) add to the database.
    town = Town()
    # Add attributes
    town.county = town_input["county"]
    town.name = town_input["name"]
    town.grid_reference = town_input["grid_reference"]
    town.easting = town_input["easting"]
    town.northing = town_input["northing"]
    town.latitude = town_input["latitude"]
    town.longitude = town_input["longitude"]
    town.elevation = town_input["elevation"]
    town.postcode_sector = town_input["postcode_sector"]
    town.local_government_area = town_input["local_government_area"]
    town.nuts_region = town_input["nuts_region"]
    town.town_type = town_input["town_type"]
    # add the country (parent) to the county (child)
    session.add(town)
    session.commit()


session = dbconnect()

with open(r"uk-towns-sample.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for town in reader:
        addTown(session, town)