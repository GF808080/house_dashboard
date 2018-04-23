#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 11:46:01 2017
database models for our project
@author: sentinel
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Houses(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    

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


class Drivetimes(Base):
    __tablename__ = "drivetimes"
    id = Column(Integer, primary_key=True)
    start = Column(String)
    dest = Column(String)
    starttime = Column(DateTime)
    drivetime = Column(Integer)
    
class Offices(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    person = Column(String)
       
class Driveestimates(Base):
    __tablename__ = "Driveestimates"
    id = Column(Integer)
    address = Column(String, primary_key=True)
    AOffice_guess = Column(Integer)
    AOffice_traffic = Column(Integer)
    BOffice_guess = Column(Integer)
    BOffice_traffic = Column(Integer)
    date_time = Column(DateTime, primary_key=True)
    
class Laltongs(Base):
    __tablename__ = "latlongs"
    
    address = Column(String, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)

class Auth_users(Base):
    __tablename__= "auth_users"
    email = Column(String, primary_key=True)
    