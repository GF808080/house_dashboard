#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 11:23:21 2018
simple script to ensure every db exists locally

@author: sentinel
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import BaseConfig

dbloc = BaseConfig.SQLALCHEMY_DATABASE_URI

engine = create_engine(dbloc,  echo=True)
connection = engine.connect()
Base = declarative_base()
meta = MetaData()
session = sessionmaker(bind=engine)
session.configure(bind=engine)
s = session()

class houses(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True)
    address = Column(String)  
    def __init__(self, name):

        self.name = name    

class drivetimes(Base):
    __tablename__ = "drivetimes"
    id = Column(Integer, primary_key=True)
    start = Column(String)
    dest = Column(String)
    starttime = Column(String)
    drivetime = Column(Integer)
    
    def __init__(self, name):

        self.name = name  

class offices(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    person = Column(String)

    def __init__(self, name):
        
        self.name = name
        
class Driveestimates(Base):
    __tablename__ = "Driveestimates"
    id = Column(Integer)
    address = Column(String, primary_key=True, unique=True)
    AOffice_guess = Column(Integer)
    AOffice_traffic = Column(Integer)
    BOffice_guess = Column(Integer)
    BOffice_traffic = Column(Integer)
    date_time = Column(String)
    
    def __init__(self, name):

        self.name = name
class Housedetails(Base):
    __tablename__ = "Housedetails"
    id = Column(Integer)
    URL = Column(String, primary_key=True)
    SALE_TYPE = Column(String)
    HOME_TYPE = Column(String)
    ADDRESS = Column(String)
    CITY = Column(String)
    STATE = Column(String)
    ZIP = Column(String)
    LIST_PRICE = Column(Integer) 
    BEDS = Column(Integer) 
    BATHS = Column(Float)
    LOCATION= Column(String)
    SQFT = Column(Integer) 
    LOT_SIZE = Column(Integer) 
    YEAR_BUILT =Column(String)
    PARKING_SPOTS = Column(Integer) 
    PARKING_TYPE = Column(String)
    DAYS_ON_MARKET = Column(Integer) 
    STATUS = Column(String)
    RECENT_REDUCTION_DATE = Column(String)
    ORIGINAL_LIST_PRICE = Column(Integer) 
    LAST_SALE_DATE = Column(String)
    LAST_SALE_PRICE = Column(Integer) 
    SOURCE = Column(String)
    LISTING_ID = Column(String)
    ORIGINAL_SOURCE = Column(String)
    LATITUDE = Column(String)
    LONGITUDE = Column(String)
    IS_SHORT_SALE = Column(Boolean)
    
##### CREATE STEP---only need to do this once
Base.metadata.create_all(engine)
### 
Houses = Table('houses', meta, autoload=True, autoload_with = engine)
Offices = Table('offices', meta, autoload=True, autoload_with = engine)
DriveTimes = Table('drivetimes', meta, autoload=True, autoload_with=engine)
DriveEstimates = Table('Driveestimates', meta, autoload=True, autoload_with=engine)
