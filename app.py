#Import necessary packages
import streamlit as st
import datetime
from datetime import date, datetime, timedelta
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import sqlite3
import base64
import time
from userdefined import *


#Set page width to wide
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')


#Css for graph div and image div
pagecss = '''    
<style>
    [data-testid="stVerticalBlock"] {
        stArrowVegaLiteChart: -2px 5px 17px 11px grey;
    }
</style>
'''

#DB path on webserver
dbPath = "/var/www/aspendb/probesearch/SensorsData/Data-Store.db"


#local_css() to read css file and apply on the entire page
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


#buildChart() takes dataframe, xAxis, yAxis and title of the graph to plot images
def buildChart(df,xAxis,yAxis,title):
    
    xAxis = xAxis+":O"
    #initialize chart object and add data
    chart = alt.Chart(df).mark_circle().encode(
        alt.X('utchoursminutes(xAxis):O', title='time of day'),
        alt.Y(yAxis, title='Value'),
        tooltip=[
            alt.X(xAxis, title='time of day'),
            alt.Y(yAxis, title='Value')
        
        ]
    ).interactive()
        
    #set chart properties
    chart = chart.properties(
        title={
            'text': title,
            'fontSize': 16,
            'font': 'Courier',
            'anchor': 'middle'
            },
            width=550,
            height=200

        ).configure_axis(
            labelFontSize=12,
            titleFontSize=12
        )
        
    return chart
    
    
#make_grid() uses encoded image and plot it based on the initialized time range for each tabs on the UI
def make_grid(itemList,df,section):
    width = 80
    height = 65
    cols = section.columns(6)
    filteredDF = df.loc[df['time'].isin(itemList)]
    imageList = list(filteredDF["image"])
    timeList = list(filteredDF["time"])
    for i in range(len(imageList)):
        try:
            imgRaw = imageList[i]
            img_decoded = base64.b64decode(imgRaw)
            imgInMem = Image.open(BytesIO(img_decoded))   
            imgInMem = imgInMem.resize((width,height))
            cols[i].image(imgInMem,caption=timeList[i])
        except:
            pass

    

#readSqlite() reads data based on the query provided and returns a dataframe
def readSqlite(query,dbPath):
    conn = sqlite3.connect(dbPath)
    df = pd.read_sql_query(query, conn)
    return df


#LOad required file
local_css("/var/www/aspendb/probesearch/Reporting-Project/static/css/style.css")
config = readJson("/var/www/aspendb/probesearch/Reporting-Project/config.json")

#Load queries
QueryDict = config["Query"]


#Main container
main = st.container()


#Inside main container
with main:
    
    #create header
    header = st.container()
    
    with header:
        
        header.subheader("Sensor - Report")
        
        headerCol1, headerCol2 = header.columns([1,1])
        today = date.today()
        date = headerCol1.date_input('Select Date', today,key="1")
        date = date.strftime("%Y-%m-%d 00:00:00")
        
        #read current day data of all RPIs
        df = pd.DataFrame()
        for k,v in QueryDict.items():
            temp = readSqlite(v.format(date),dbPath)
            if temp.shape[0] !=0:
                df = pd.concat([df, temp])
                
        
        df['xAxis'] = pd.to_datetime(df['xAxis'])
        df['xAxis_temp'] = pd.to_datetime(df['xAxis']).dt.date
        df['time'] = pd.to_datetime(df['xAxis']).dt.time
        
        #Based on our entire data get unique Rooms
        options = list(df["room"].unique())
        selected_option = headerCol2.selectbox('Select Room', options)
        
        #Filter data based on room selected
        df = df.loc[df['room'] == selected_option]
        

    #create body
    body = st.container()
    
    if(df.shape[0]>0):
        # Create two columns with relative widths of 2 and 2
        left_column, right_column = body.columns([2, 2])
        
        with left_column:
            #Create three tabs
            Temperature, Humidity, Brightness = left_column.tabs(["Temperature", "Humidity", "Brightness"])
            
            #Temperature
            data = df[["xAxis","yAxisTemp"]]
            #call buildChart function to create a graph
            chart = buildChart(data,"xAxis","yAxisTemp","Temperature")
            Temperature.altair_chart(chart)
            Temperature.markdown(pagecss,unsafe_allow_html=True)

            #Humidity
            if(df["yAxisHumid"].dropna().shape[0]):
                data = df[["xAxis","yAxisHumid"]]
                #call buildChart function to create a graph
                chart = buildChart(data,"xAxis","yAxisHumid","Humidity")
                Humidity.altair_chart(chart)

            #Brightness
            data = df[["xAxis","yAxisBrightness"]]
            #call buildChart function to create a graph
            chart = buildChart(data,"xAxis","yAxisBrightness","Brightness")
            Brightness.altair_chart(chart)

        
        with right_column:
            #create 4 tabs
            tab1, tab2, tab3,tab4 = right_column.tabs(["12AM-6AM", "6AM-12PM", "12PM-6PM","6PM-12AM"])
            
            TwelveToSix = []
            SixToTwelve = []
            TwelveToSixEve = []
            SixEveToTwelve = []
            
            for i in list(df['time']):
                #create reference time for comparison
                twelveAM = datetime(1991, 1, 1, 0, 0, 0).time()
                twelvePM = datetime(1991, 1, 1, 12, 0, 0).time()
                sixAM = datetime(1991, 1, 1, 6, 0, 0).time()
                sixPM = datetime(1991, 1, 1, 18, 0, 0).time()
                
                #Append data based on reference time
                if i>=twelveAM and i<sixAM:
                    TwelveToSix.append(i)
                elif i>=sixAM and i<twelvePM:
                    SixToTwelve.append(i)
                elif i>=twelvePM and i<sixPM:
                    TwelveToSixEve.append(i)
                else:
                    SixEveToTwelve.append(i)
            
            #Call make_grid function to create a grid of images
            if len(TwelveToSix[:6])!=0: make_grid(TwelveToSix[:6],df,tab1)
            if len(TwelveToSix[6:12])!=0: make_grid(TwelveToSix[6:12],df,tab1)
            if len(SixToTwelve[:6])!=0: make_grid(SixToTwelve[:6],df,tab2)
            if len(SixToTwelve[6:12])!=0: make_grid(SixToTwelve[6:12],df,tab2)
            if len(TwelveToSixEve[:6])!=0: make_grid(TwelveToSixEve[:6],df,tab3)
            if len(TwelveToSixEve[6:12])!=0: make_grid(TwelveToSixEve[6:12],df,tab3)
            if len(SixEveToTwelve[:6])!=0: make_grid(SixEveToTwelve[:6],df,tab4)
            if len(SixEveToTwelve[6:12])!=0: make_grid(SixEveToTwelve[6:12],df,tab4)
            
    else:
        body.markdown("<center><h3>No data to show...</h3></center>",unsafe_allow_html=True)
    