import csv # give python csv superpowers

with open(r"uk-towns-sample.csv") as csvfile:
    reader = csv.DictReader(csvfile)

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
class County(Base):
    __tablename__ = 'county'
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
    country = relation("Country", backref="county")
    country_id = Column(Integer, ForeignKey('country.id'))


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine('sqlite:///UK_towns.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


''' Above here defines the DB'''
''' Below here adds data to the DB '''

def addCounty(session, county_input):
    # Try and get the Country from the database. If error (Except) add to the database.
    try: 
        country = session.query(Country).filter(Country.country == county_input["country"]).one()
    except:
        country = Country()
        country.country = county_input["country"]
        session.add(country)
    county = County()
    # Add attributes
    county.county = county_input["county"]
    county.name = county_input["name"]
    county.grid_reference = county_input["grid_reference"]
    county.easting = county_input["easting"]
    county.northing = county_input["northing"]
    county.latitude = county_input["latitude"]
    county.longitude = county_input["longitude"]
    county.elevation = county_input["elevation"]
    county.postcode_sector = county_input["postcode_sector"]
    county.local_government_area = county_input["local_government_area"]
    county.nuts_region = county_input["nuts_region"]
    county.town_type = county_input["town_type"]
    # add the country (parent) to the county (child)
    county.country = country
    session.add(county)
    session.commit()
