#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:59:16 2017

@author: sentinel
"""

from os.path import dirname, join
import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc
from bokeh.palettes import Category20
sys.path.append("..")
import models, config


###############################################################################
### I ken haz data?
###############################################################################
Housedetails= models.Housedetails
Driveestimates = models.Driveestimates
BaseConfig = config.BaseConfig
dbloc = BaseConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(dbloc,  echo=True)
connection = engine.connect()
Base = declarative_base()
meta = MetaData()
session = sessionmaker(bind=engine)
session.configure(bind=engine)
s = session()

#housedetails data
query1 = s.query(Housedetails)
data1 = pd.read_sql(query1.statement, s.bind)
data1['lowad']=data1.ADDRESS.str.lower()

#driveestimates data
query2 = s.query(Driveestimates)
data2 = pd.read_sql(query2.statement, s.bind)
data2['lowad']=data2.address.apply(lambda x: x.split(',')[0].lower())
data2['zip']= data2.address.str[-5:]


## Get clean office guesses
def id_drive(time):
    if (time.hour >= 6) & (time.hour < 9):
        return 'morning'
    elif (time.hour >= 16) & (time.hour < 19):
        return 'evening'
    else:
        return None

def to_float(x):
    try:
        return(float(x))
    except:
        return None

def mean_replace_aguess(row, meandict):
    try:
        return float(row.AOffice_guess)
    except:
        return meandict[row.zip]
    
def mean_replace_bguess(row, meandict):
    try:
        return float(row.BOffice_guess)
    except:
        return meandict[row.zip]
    
data2['BOffice_guess']=data2['BOffice_guess'].apply(lambda x: to_float(x))
data2['AOffice_guess']=data2['AOffice_guess'].apply(lambda x: to_float(x))
#return a dictionary of average drive per zip code
data2['drivetime']= data2.date_time.apply(lambda x: id_drive(x))
data2.dropna(axis=0, subset=['AOffice_guess', 'AOffice_traffic', 'BOffice_guess', 'BOffice_traffic', 'zip'],\
             inplace=True)
toclean = data2[['AOffice_guess', 'AOffice_traffic', 'BOffice_guess', 'BOffice_traffic', 'zip']]
am = data2[data2.drivetime == 'morning']
pm = data2[data2.drivetime == 'evening']

##make our mean dicts
a_mean_estimateAM = am['AOffice_guess'].groupby(am['zip']).mean()
b_mean_estimateAM = am['BOffice_guess'].groupby(am['zip']).mean()
a_mean_estimatePM =pm['AOffice_guess'].groupby(pm['zip']).mean()
b_mean_estimatePM =pm['BOffice_guess'].groupby(pm['zip']).mean()
##
am['cleana'] = am.apply(lambda row: mean_replace_aguess(row, a_mean_estimateAM), axis=1)
pm['cleana'] = pm.apply(lambda row: mean_replace_aguess(row, a_mean_estimatePM), axis=1)
am['cleanb'] = am.apply(lambda row: mean_replace_bguess(row, b_mean_estimateAM), axis=1)
pm['cleanb'] = pm.apply(lambda row: mean_replace_bguess(row, b_mean_estimatePM), axis=1)

am['combined_guess'] = am['cleana']+am['cleanb']
pm['combined_guess'] = pm['cleana']+pm['cleanb']

driveframe = pd.merge(am, pm, on ='lowad', suffixes = ('_am', '_pm'))


data = pd.merge(data1, driveframe, on = 'lowad')

#drivetimes data
###############################################################################
### Set up some colors
###############################################################################

##use brewer for quick coloring as long as that allows
#colors = brewer['Spectral'][len(data.CITY.unique())]
#colormap = {}
#for i, j in enumerate(data.CITY.unique()):
#    colormap[j]=colors[i]
#data['color']= data.CITY.apply(lambda x: colormap[x])
colors = Category20[len(data.ZIP.unique())]
colormap = {}
for i, j in enumerate(data.ZIP.unique()):
    colormap[j]=colors[i]
data['color']= data.ZIP.apply(lambda x: colormap[x])

###############################################################################
### clean up some numbers
###############################################################################
def to_int(x):
    try:
        myint = int(x.replace('.0',''))
    except:
        myint=x
    if x == '0':
        x = 2018
    return myint

def owned_length(cleanyear):
    l = 2018-cleanyear
    if l>1000:
        l=0
    return l

def priceSQFT(row):
    try:
        return float(row['LIST_PRICE'])/float(row['SQFT'])
    except:
        return None

data.fillna(0, inplace=True)  # just replace missing values with zero
data['cleanprice']= data.LIST_PRICE.apply(lambda x: float(x))
data['cleanyear']= data.YEAR_BUILT.apply(lambda x: to_int(x))
data['length_owned']= data.cleanyear.apply(lambda x: owned_length(x))
data['cleanbeds']= data.BEDS.apply(lambda x: to_int(x))
data['cleanbaths']= data.BATHS.apply(lambda x: float(x))
data['cleanpark']= data.PARKING_SPOTS.apply(lambda x: to_int(x))
data['price_sqft']=data.apply(priceSQFT, axis=1)
data['zipc']= data['ZIP'].apply(lambda x: int(x))
data['cleanSQFT']=data['SQFT'].apply(lambda x: to_int(x))

###
#get a list of all the cities fro grins
cities = list(data.CITY.unique())
cities.append('All')

##take care of my alpha here
data['alpha']=1.2
#uncomment if you want alpha to highlight only where something's been owned a long time
#data["alpha"] = np.where(data["length_owned"] >21, 0.9, 0.25) #alpha based on ownership

data.drop_duplicates(subset=['ADDRESS'],  inplace=True)
###############################################################################
## skipping some mapping stuff, let's look at this later
###############################################################################
axis_map= {
        "List Price": "cleanprice",
        "sqft":"cleanSQFT",
        "Year Built": "cleanyear",
        "Length_Owned": "length_owned",
        "Bedrooms": "cleanbeds",
        "Bathrooms": "cleanbaths",
        "Price Sqft": "price_sqft",
        "ZIP": "zipc", 
        "Combined AM Drives": "combined_guess_am",
        "Combined PM Drives": "combined_guess_pm"}
###############################################################################
## Pointing to html base
###############################################################################

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)


###############################################################################
## Make some sliders
###############################################################################

min_year = Slider(title="Year Built", start=1940, end=2018, value=1940, step=1)
max_year = Slider(title="End Year Built", start=1940, end=2018, value=2018, step=1)
length_owned = Slider(title="Length Owned By Seller", start=2, end=70, value=10, step=1)
baths = Slider(title="Number of Bathrooms", start=2, end=5, value=2, step=.5)
beds = Slider(title="Number of Bedrooms", start=3, end=6, value=3, step=1)
price = Slider(title="Listed Price", start=0, end=1100000, value=400000, step=10000)
city = Select(title="City", value="All", options=cities)
sqft =Slider(title="sqft", start=1000, end=7000, value=1200, step=10)
#ptype = Select(title="Parking Type", value="All", options=data.PARKING_TYPE.unique())
#pspace = Select(title="Parking Spaces", value="All", options=data.PARKING_SPOTS.unique())

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Year Built")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="List Price")

###############################################################################
## create column data source
###############################################################################
# Create Column Data Source that will be used by the plot

source = ColumnDataSource(data=dict(x=[], y=[], color=[], address=[], cleanyear=[],\
                                    price =[], alpha=[], pspots=[], city=[],\
                                    psqft=[], zipc=[], combined_guess_pm=[],\
                                    combined_guess_am=[])) 
###############################################################################
## create tooltips
###############################################################################
hover = HoverTool(tooltips=[
    ("Address", "@address"),
    ("Year Built", "@cleanyear"),
    ("$", "@price"),
    ("Parking Spots","@pspots"),
    ("City","@city"),
    ("Zip","@zipc"),
    ("AM Drives","@combined_guess_am"),
    ("PM Drives", "@combined_guess_pm")
    
])

###############################################################################
## make the plot
###############################################################################

#is it possible this can go un-changed?
p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tools=[hover])
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None,\
         fill_alpha="alpha", legend='zipc')
p.legend.location = "top_left"
#p.legend.location = "top_center"
###############################################################################
## make our functions to select houses and update data
###############################################################################


def select_house():
    #select_switches
    city_val = city.value
#    ptype_val = ptype.value                                   #saved for later
#    pspace_val = pspace.value
    ##get dots we want to show from sliders
    selected = data[
        (data.cleanprice >= price.value) &
        (data.cleanbeds >= beds.value) &
        (data.cleanyear >= min_year.value) &
        (data.cleanyear <= max_year.value) &
        (data.cleanbaths >= baths.value) &
        (data.cleanSQFT >= sqft.value)
    ]
    if (city_val != "All"):
        selected = selected[selected.CITY.str.contains(city_val)==True]
    return selected

 
def update():
    df = select_house()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d houses selected" % len(df)
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        address=df["ADDRESS"],
        cleanyear=df['cleanyear'],
        sqft=df['cleanSQFT'],
        year=df["cleanyear"],
        price=df["cleanprice"],
        alpha=df["alpha"],
        pspots=df["cleanpark"],
        city=df['CITY'],
        psqft=df['price_sqft'],
        zipc=df['zipc'],
        combined_guess_pm=df['combined_guess_pm'],
        combined_guess_am=df['combined_guess_am']
    )

controls = [min_year ,max_year, sqft, baths, beds, price, city, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'scale_width'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Houses"