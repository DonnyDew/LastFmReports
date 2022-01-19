import requests
import time 
import streamlit as st
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import os
import pandas as pd
import numpy as np


def monthConvert(monthStr,year):
    if monthStr.lower() == 'january' or monthStr.lower() == 'jan':
        month = 1
        daysInMonth = 31
                
    elif monthStr.lower() == 'february' or monthStr.lower() == 'feb':
        month = 2
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    daysInMonth = 29
                else: 
                    daysInMonth = 28
            else:
                daysInMonth = 29
        else:
            daysInMonth = 28
    elif monthStr.lower() == 'march' or monthStr.lower() == 'mar':
        month = 3
        daysInMonth = 31
    elif monthStr.lower() == 'april' or monthStr.lower() == 'apr':
        month = 4
        daysInMonth = 30
    elif monthStr.lower() == 'may' or monthStr.lower() == 'may':
        month = 5
        daysInMonth = 31
    elif monthStr.lower() == 'june' or monthStr.lower() == 'jun':
        month = 6
        daysInMonth = 30
    elif monthStr.lower() == 'july' or monthStr.lower() == 'jul':
        month = 7
        daysInMonth = 31
    elif monthStr.lower() == 'august' or monthStr.lower() == 'aug':
        month = 8
        daysInMonth = 31
    elif monthStr.lower() == 'september' or monthStr.lower() == 'sep':
        month = 9
        daysInMonth = 30
    elif monthStr.lower() == 'october' or monthStr.lower() == 'oct':
        month = 10
        daysInMonth = 31
    elif monthStr.lower() == 'november' or monthStr.lower() == 'nov':
        month = 11
        daysInMonth = 30
    elif monthStr.lower() == 'december' or monthStr.lower() == 'dec':
        month = 12
        daysInMonth = 31
    else:
        month = 0
        daysInMonth = 0
    return [month,daysInMonth]
def getUniTime(yearList,mode,regiTime):
    if mode == "1a":
        today = dt.today()
        dateM = str(dt(today.year, today.month, 1))
        month = int(dateM[5:7])
        year = int(dateM[0:4])
        timeStart = time.mktime(datetime.datetime(year,month,1,0,0,0).timetuple())
        timeEnd = time.time()
    elif mode == "1b":
        year = int(st.selectbox("Enter year ",yearList))
        monthStr = st.selectbox("Enter month",["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
        monthDayList = monthConvert(monthStr,year)
        timeStart = time.mktime(datetime.datetime(year,monthDayList[0],1,0,0,0).timetuple())
        timeEnd = time.mktime(datetime.datetime(year,monthDayList[0],monthDayList[1],23,59,59).timetuple())
    elif mode == "2a":
        today = dt.today()
        dateM = str(dt(today.year, today.month, 1))
        year = int(dateM[0:4])
        timeStart = time.mktime(datetime.datetime(year,1,1,0,0,0).timetuple())
        timeEnd = time.time()
    elif mode == "2b":
        if len(yearList) == 0:
            st.write("No data from previous years... displaying current year")
            mode = "2a"
        else:
            year = st.selectbox("Enter year",yearList)
            timeStart = time.mktime(datetime.datetime(year,1,1,0,0,0).timetuple())
            timeEnd = time.mktime(datetime.datetime(year,12,31,23,59,59).timetuple())
    elif mode == "3":
        timeStart = time.mktime(regiTime.timetuple())
        timeEnd = time.time()
    elif mode == "4":
        timeStart = time.mktime(st.date_input("Start Date").timetuple())
        timeEnd = time.mktime(st.date_input("End Date").timetuple())
    
    timeStart = format(timeStart, ".0f")
    timeEnd = format(timeEnd, ".0f")
    floatTime = [timeStart,timeEnd]
    return [str(floatTime) for floatTime in floatTime]
API_KEY = str(os.environ.get('LASTFM_API_KEY'))
USER_AGENT = st.text_input("Enter Last Fm User Name")
def getUserData(pictureOrSTime):
    headers = {"user-agent": USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'
    payload = {'method':'user.getInfo'}
    payload['user'] = USER_AGENT
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    response = requests.get(url,headers=headers, params=payload)
    data = response.json()
        
    if pictureOrSTime == 'picture':
        return data['user']['image'][2]['#text']
    else:
        timestamp = data['user']['registered']['#text']
        datetime = dt.fromtimestamp(timestamp)
        return datetime
def lastfm_weeklyChart(timeList,method):
    headers = {"user-agent": USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'
    payload = {'method' : method}
    payload['user'] = USER_AGENT
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['from'] = 	timeList[0]
    payload['to'] = timeList[1]
    response = requests.get(url,headers=headers, params=payload)
    return response.json()
def getArtistDiscovery(artist):
    #Tracks
    trackData = lastfm_weeklyChart(timeList,'user.getWeeklyTrackChart')
    totalSongs = len(trackData['weeklytrackchart']['track'])    
    SongList = []
    
    SongFreqList = []
    for i in range(0,totalSongs):
        if trackData['weeklytrackchart']['track'][i]['artist']['#text'] == artist:
            SongList.append(trackData['weeklytrackchart']['track'][i]['name'])
            SongFreqList.append(int(trackData['weeklytrackchart']['track'][i]['playcount']))
    TData = {'Song Name' : SongList,'PlayCount':SongFreqList}
    td = pd.DataFrame(data=TData)
    td.index = np.arange(1,len(td)+1)
    return td
def getArtList():
    artistData = lastfm_weeklyChart(timeList,'user.getWeeklyArtistChart')
    totalArtists = len(artistData['weeklyartistchart']['artist'])
    artistList = []
    
    count = 0
    for i in range(0,totalArtists):
        if count < 51:
            artistList.append(artistData['weeklyartistchart']['artist'][i]['name'])
        else:
            break
    return artistList  


if USER_AGENT != "":
    regiDT = getUserData('STime')
    yearRegistered = int(str(regiDT)[:4])
    countYear = yearRegistered
    today = dt.today()
    dateM = str(dt(today.year, today.month, 1))
    year = int(dateM[0:4])
    yearList = []
    while year >= countYear:
        yearList.append(countYear)
        countYear += 1
    st.write("Mode 1: Monthly Report")
    st.write("Mode 2: Yearly Report")
    st.write("Mode 3: All Time")
    st.write("Mode 4: Custom")    
    mode = st.selectbox("Choose mode 1-4",["1","2","3","4"])
    if mode == "1":
        st.write("Mode 1a: Current Month")
        st.write("Mode 1b: Previous Month")
        mode = st.selectbox("Choose mode 1a-1b",["1a","1b"])
    if mode == "2":
        st.write("Mode 2a: Current Year")
        st.write("Mode 2b: Previous Year")
        mode = st.selectbox("Choose mode 2a-2b",["2a","2b"])
    timeList = getUniTime(yearList,mode,regiDT)
    
    artistList = getArtList()
    artist = st.selectbox("Choose an artist",artistList)
st.write("wait for mode option before clicking")
continue_button = st.button("Press when ready")
if continue_button == True:
    st.write("Loading . . .")
    header = st.beta_container()
    with header:
        st.header(f"{artist} Discovery")
        st.dataframe(getArtistDiscovery(artist))
