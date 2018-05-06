#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 16:07:52 2017

@author: sentinel
"""
from os.path import dirname, join
import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import math
from bokeh.transform import factor_cmap
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Legend, LabelSet
from bokeh.palettes import Category20
from bokeh.io import show
sys.path.append("..")
import models, config



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

offices = [BaseConfig.AOFFICE, BaseConfig.BOFFICE]
## Pick colors for people
colormapPerson ={BaseConfig.PERSONA:'darkorchid', BaseConfig.PERSONB:'darkolivegreen'}
colormapCommute ={'evening':'orange', 'morning':'blue'}

## Sort offices and people by destination
def personify(x):
    if x.start == BaseConfig.AOFFICE:
        return BaseConfig.PERSONA
    elif x.dest == BaseConfig.AOFFICE:
        return BaseConfig.PERSONA
    elif x.start == BaseConfig.BOFFICE:
        return BaseConfig.PERSONB
    elif x.dest ==BaseConfig.BOFFICE:
        return BaseConfig.PERSONB
    else:
        pass

def id_drive(time):
    if (time.hour >= 6) & (time.hour < 9):
        return 'morning'
    elif (time.hour >= 16) & (time.hour < 19):
        return 'evening'
    else:
        return None

def pricevdrives(frame, time):
    MPSFT = list(frame.Mean_List_Price_psqft.values)
    drive = 'combined_guess_'+time
    CBDT = list(frame[drive].values)
    zipcs = list(frame.ZIP.values)
    source = ColumnDataSource(data=dict(PriceSQFT=MPSFT, Combined_Drive=CBDT,
                                        ZIP = zipcs))
    title = "Price per sqft VS  {} Combined Commute".format(time)
    p = figure(plot_height=350, toolbar_location=None, title=title)
    p.scatter(x='Combined_Drive', y='PriceSQFT', source=source,              fill_color=factor_cmap('ZIP', palette=list(Category20[len(zipcs)]), factors=zipcs),              size=15)
    p.y_range.end = 600
    p.x_range.end = 70
    labels = LabelSet(x='Combined_Drive', y='PriceSQFT', text='ZIP', level='glyph',
                  x_offset=5, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)
    return p


engine = create_engine(dbloc, echo=True)
connection = engine.connect()
data= pd.read_sql("SELECT * FROM driveestimates", con=connection)
data.drop_duplicates(inplace=True)

data.columns = ['address', BaseConfig.PERSONA+'_guess', 
                BaseConfig.PERSONA+'_traffic', BaseConfig.PERSONB+'_guess',\
           BaseConfig.PERSONB+'_traffic', 'date_time']


data.columns = ['address', BaseConfig.PERSONA+'_guess', 
                BaseConfig.PERSONA+'_traffic', BaseConfig.PERSONB+'_guess',\
           BaseConfig.PERSONB+'_traffic', 'date_time']
data['cleandate']=data.date_time.apply(lambda x: pd.to_datetime(x))
data['hour'] = data.cleandate.apply(lambda x: int(x.hour))
data['commute'] =data.cleandate.apply(lambda x: id_drive(x))
data['ZIP']=data.address.apply(lambda x: x[-5:])

colors = Category20[len(data.ZIP.unique())]
colormap = {}
for i, j in enumerate(data.ZIP.unique()):
    colormap[j]=colors[i]
    
data['color']= data.ZIP.apply(lambda x: colormap[x])   
data.sort_values(by='ZIP', inplace=True)
houses =list(data.address.unique())

## Sub-divide data
amdata = data[data['hour']<=12]
pmdata = data[data['hour']>=12]
sourceAM = ColumnDataSource(amdata)
sourcePM= ColumnDataSource(pmdata)

hover = HoverTool(tooltips=[("address","@address")])
## Make Tooltipsconfig
##establish amplot
p1 = figure(title="Morning Drive Estimates From Google", 
            x_range=houses, y_range=(0, 90), plot_width=1700)


ama = p1.scatter("address", BaseConfig.PERSONA+'_traffic', color='color',
                 marker='inverted_triangle', source=sourceAM, size=10)

amb = p1.scatter("address", BaseConfig.PERSONB+'_guess', color='color',
                 marker='x', source=sourceAM, size=10)

## add the pretties
legend = Legend(items=[
            (BaseConfig.PERSONA, [ama]),\
            (BaseConfig.PERSONB, [amb]),
             ], location=(0, -30))

p1.xaxis.major_label_text_font_size="10pt"
p1.xaxis.major_label_orientation = math.pi/2
p1.add_layout(legend, 'right')
p1.add_tools(hover)

##establish amplot
p2 = figure(title="Evening Drive Estimates From Google",
            x_range=houses, y_range=(0, 90), plot_width=1700)
pma = p2.scatter("address", BaseConfig.PERSONA+'_traffic', color='color',
                 marker='inverted_triangle', source=sourcePM, size=10)

pmb = p2.scatter("address", BaseConfig.PERSONB+'_guess', color='color',
                 marker='x', source=sourcePM, size=10)    

## add the pretties
legend2 = Legend(items=[
            (BaseConfig.PERSONA, [pma]),\
            (BaseConfig.PERSONB, [pmb]),
             ], location=(0, -30))

p2.xaxis.major_label_text_font_size="12pt"
p2.xaxis.major_label_orientation = math.pi/2
p2.add_layout(legend2, 'right')
p2.add_tools(hover)




from bokeh.io import output_file, save
filename1 = 'morning_drives.html'
output_file(filename1)
save(p1)


filename2 = 'evening_drives.html'
output_file(filename2)
save(p2)

