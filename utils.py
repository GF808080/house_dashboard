#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 10:18:09 2018

@author: sentinel
"""

from config import BaseConfig
import googlemaps

dbloc = BaseConfig.SQLALCHEMY_DATABASE_URI
maps_key = BaseConfig.GDM_KEY
logfile = BaseConfig.LOGFILE


#set google key
gmaps = googlemaps.Client(key=maps_key)

#estimate a morning commute on a Tuesday during a school-year

# Set offices
AOffice = BaseConfig.AOFFICE
BOffice = BaseConfig.BOFFICE
offices = [AOffice, BOffice]

def estimate_commutes(new_address, time):
        commuteA = gmaps.distance_matrix(new_address, AOffice, mode="driving",
                                            language="en-US",
                                            units="imperial",
                                            departure_time=time,
                                            avoid='highways',
                                            traffic_model="best_guess")
        #extract the duration and insert into db
        try:
            estimate = commuteA['rows'][0]['elements'][0]['duration']['text']
            AOffice_guess = int(estimate.replace(' mins', ''))
            ### Traffic
            estimate = commuteA['rows'][0]['elements'][0]['duration_in_traffic']['text']
            AOffice_traffic = int(estimate.replace(' mins', ''))
        except:
            AOffice_guess=None
            AOffice_traffic=None
            print('failed commuteA')
            
        commuteB = gmaps.distance_matrix(new_address, BOffice, mode="driving",
                                            language="en-US",
                                            units="imperial",
                                            departure_time=time,
                                            traffic_model="best_guess")
        #extract the duration and insert into db
        try:
            estimate = commuteB['rows'][0]['elements'][0]['duration']['text']
            BOffice_guess = int(estimate.replace(' mins', ''))
            ### Traffic
            estimate = commuteB['rows'][0]['elements'][0]['duration_in_traffic']['text']
            BOffice_traffic = int(estimate.replace(' mins', ''))
        except:
            BOffice_traffic = None
            BOffice_guess = None
            print('failed commute b')
            
        
        DE= {'address':new_address,\
                                         'AOffice_guess':AOffice_guess,\
                                         'AOffice_traffic':AOffice_traffic,\
                                         'BOffice_guess':BOffice_guess,\
                                         'BOffice_traffic':BOffice_traffic,\
                                         'date_time':time}
        return DE

