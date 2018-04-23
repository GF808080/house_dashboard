#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 15:23:56 2017

@author: sentinel
"""

import os
#import bcrypt as bc

# default config
class BaseConfig(object):
    DEBUG = True #not sure I'll ever have this out of debug
    # shortened for readability
    SECRET_KEY = 'ThisIsPretty?H8rdtoGuess?'
    JSAPIKEY="AIzaSyC6IATymJ0wOWpkRL4qFcws6LmyKg7qxHk"
    DBLOC="sqlite:////home/sentinel/explore/project/drivebase.db"
    MAPS_KEY= "AIzaSyA3p9TNsfVEyIJ72XDyxyyon2gUfcaPv-c"
    BOFFICE= "14390 Chantilly Crossing Ln, Chantilly, VA 20151"
    AOFFICE= "3800 Reservoir Rd NW Washington, DC 20007"
    PERSONA="Stacy"
    PERSONB="Karl"
    LOGFILE="/home/sentinel/drivetimes/drivelog.txt"
    GEOCODE_KEY="AIzaSyCU-Xv1SCQZtsFAaywXLor7JIspj4W-4cU"
    ZWSID="X1-ZWz1g5bk1ex43v_3tnpx"
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/sentinel/explore/project/drivebase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  ## process in the example, probably for deployment
    #SECURITY_PASSWORD_SALT =bc.gensalt()

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False