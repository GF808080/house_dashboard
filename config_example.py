#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 15:23:56 2017

@author: sentinel
"""

# default config
class BaseConfig(object):
    DEBUG = True #not sure I'll ever have this out of debug
    SECRET_KEY = 'changeme'
    JSAPIKEY="changeme" #for google point mapping
    GDM_KEY= "changeme"
    BOFFICE= "changeme"
    AOFFICE= "changeme"
    PERSONA="changeme"
    PERSONB="changeme"
    LOGFILE="changeme"
    GEOCODE_KEY="changeme"
    SQLALCHEMY_DATABASE_URI = "changeme"
    SQLALCHEMY_TRACK_MODIFICATIONS=False #quiets down sqlalchemy

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False