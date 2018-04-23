#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 15:23:56 2017

@author: sentinel
"""

# default config
class BaseConfig(object):
    DEBUG = True #not sure I'll ever have this out of debug
    SECRET_KEY = 'changeme?'
    JSAPIKEY="AIzaSyC6IATymJ0wOWpkRL4qFcws6LmyKg7qxHk" #for google maps
    GDM_KEY= "AIzaSyA3p9TNsfVEyIJ72XDyxyyon2gUfcaPv-c" #for google distance matrix
    BOFFICE= "14390 Chantilly Crossing Ln, Chantilly, VA 20151"
    AOFFICE= "3800 Reservoir Rd NW Washington, DC 20007"
    PERSONA="Stacy"
    PERSONB="Karl"
    LOGFILE="drivelog.txt"
    GEOCODE_KEY="AIzaSyCU-Xv1SCQZtsFAaywXLor7JIspj4W-4cU"
    SQLALCHEMY_DATABASE_URI = "sqlite:///drivebase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False