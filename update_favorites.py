#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from utils import estimate_commutes
from models import Driveestimates
from datetime import datetime
from config import BaseConfig

dbloc = BaseConfig.SQLALCHEMY_DATABASE_URI 
print(dbloc)
import time
time.sleep(10)
engine = create_engine(dbloc,  echo=True)
connection = engine.connect()
Base = declarative_base()
meta = MetaData()

Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
session.configure(bind=engine)
s = session()


def morning_night(address):
        morning_commute = datetime(2018, 9,25, 7)
        evening_commute = datetime(2018, 9,25, 17)
        commutes = [morning_commute, evening_commute]
        for commute in commutes:
#            print("Doing {address}, for {commute}".format(address = address, commute = commute))
            ne=estimate_commutes(address, commute) #ne, new DriveEstimate
            toinsert = Driveestimates(address=address,\
                                      AOffice_guess=ne['AOffice_guess'],\
                                      AOffice_traffic=ne['AOffice_traffic'],\
                                      BOffice_guess=ne['BOffice_guess'],\
                                      BOffice_traffic=ne['BOffice_traffic'],\
                                      date_time=ne['date_time'])
#            print(toinsert)
            s.add(toinsert)
            s.commit()


#use my table class for easy data-insertion
HouseDetails = Table('Housedetails', meta, autoload=True, autoload_with=engine)

### Delete old favorites to put new ones in
d = HouseDetails.delete()
s.execute(d)

addresses = pd.read_sql('SELECT ADDRESS from Housedetails', con = connection).ADDRESS.values
###############
## read in lastest export from favorites and clean the column names
###############
favorite_file = 'redfin_exports/redfin_2018-04-14-18-17-43_results.csv'
fav = pd.read_csv(favorite_file)
clean_names = [n.replace(' ', '_') for n in fav.columns]
fav.columns = clean_names
addresses = []
for i, row in fav.iterrows():
    if row['ADDRESS'] not in addresses:
        add = row['ADDRESS']+', '+str(row['ZIP'])
#        print('doing {}'.format(add))
        morning_night(add)
#        print('done')
        try:
            ins = HouseDetails.insert().values(URL = row['URL_(SEE_http://www.redfin.com/buy-a-home/comparative-market-analysis_FOR_INFO_ON_PRICING)'],
                                                            SALE_TYPE = row['SALE_TYPE'],
                                                            HOME_TYPE = row['HOME_TYPE'],
                                                            ADDRESS = row['ADDRESS'],
                                                            CITY = row['CITY'],
                                                            STATE = row['STATE'],
                                                            ZIP = row['ZIP'],
                                                            LIST_PRICE = row['LIST_PRICE'],
                                                            BEDS = row['BEDS'],
                                                            BATHS = row['BATHS'],
                                                            LOCATION = row['LOCATION'],
                                                            SQFT = row['SQFT'],
                                                            LOT_SIZE = row['LOT_SIZE'],
                                                            YEAR_BUILT = row['YEAR_BUILT'],
                                                            PARKING_SPOTS = row['PARKING_SPOTS'],
                                                            PARKING_TYPE = row['PARKING_TYPE'],
                                                            DAYS_ON_MARKET = row['DAYS_ON_MARKET'],
                                                            STATUS = row['PARKING_SPOTS'],
                                                            RECENT_REDUCTION_DATE = row['RECENT_REDUCTION_DATE'],
                                                            ORIGINAL_LIST_PRICE = row['ORIGINAL_LIST_PRICE'],
                                                            LAST_SALE_DATE = row['LAST_SALE_DATE'],
                                                            LAST_SALE_PRICE = row['LAST_SALE_PRICE'],
                                                             LISTING_ID = row['LISTING_ID'],
                                                            SOURCE = row['SOURCE'],
                                                           ORIGINAL_SOURCE = row['ORIGINAL_SOURCE'],
                                                            LATITUDE = row['LATITUDE'],
                                                            LONGITUDE = row['LONGITUDE'],
                                                            IS_SHORT_SALE = row['IS_SHORT_SALE'])
            
        except:
            print('failed on {}'.format(row['ADDRESS']))
        try:
            connection.execute(ins)
        except:
            print("Bad execute on inserting {}".format(row['ADDRESS']))