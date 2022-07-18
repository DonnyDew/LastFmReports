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
import plotly.graph_objects as go

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
    if mode == "Current Month":
        today = dt.today()
        dateM = str(dt(today.year, today.month, 1))
        month = int(dateM[5:7])
        year = int(dateM[0:4])
        timeStart = time.mktime(datetime.datetime(year,month,1,0,0,0).timetuple())
        timeEnd = time.time()
    elif mode == "Previous Month":
        year = int(st.selectbox("Enter year ",yearList))
        monthStr = st.selectbox("Enter month",["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
        monthDayList = monthConvert(monthStr,year)
        timeStart = time.mktime(datetime.datetime(year,monthDayList[0],1,0,0,0).timetuple())
        timeEnd = time.mktime(datetime.datetime(year,monthDayList[0],monthDayList[1],23,59,59).timetuple())
    elif mode == "Current Year":
        today = dt.today()
        dateM = str(dt(today.year, today.month, 1))
        year = int(dateM[0:4])
        timeStart = time.mktime(datetime.datetime(year,1,1,0,0,0).timetuple())
        timeEnd = time.time()
    elif mode == "Previous Year":
        if len(yearList) == 0:
            st.write("No data from previous years... displaying current year")
            mode = "Current Year"
        else:
            year = st.selectbox("Enter year",yearList[1:])
            timeStart = time.mktime(datetime.datetime(year,1,1,0,0,0).timetuple())
            timeEnd = time.mktime(datetime.datetime(year,12,31,23,59,59).timetuple())
    elif mode == "All Time":
        timeStart = time.mktime(regiTime.timetuple())
        timeEnd = time.time()
    elif mode == "Custom":
        timeStart = time.mktime(st.date_input("Start Date").timetuple())
        timeEnd = time.mktime(st.date_input("End Date").timetuple())
    
    timeStart = format(timeStart, ".0f")
    timeEnd = format(timeEnd, ".0f")
    floatTime = [timeStart,timeEnd]
    return [str(floatTime) for floatTime in floatTime]
API_KEY = str(os.environ.get('LASTFM_API_KEY'))
USER_AGENT = st.text_input("Enter Last Fm User Name")
def getUserData():
    headers = {"user-agent": USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'
    payload = {'method':'user.getInfo'}
    payload['user'] = USER_AGENT
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    response = requests.get(url,headers=headers, params=payload)
    data = response.json()
    timestamp = data['user']['registered']['#text']
    datetime = dt.fromtimestamp(timestamp)
    return datetime
if USER_AGENT != "":
    regiDT = getUserData()
    yearRegistered = int(str(regiDT)[:4])
    countYear = yearRegistered
    today = dt.today()
    dateM = str(dt(today.year, today.month, 1))
    year = int(dateM[0:4])
    yearList = []
    while year >= countYear:
        yearList.append(countYear)
        countYear += 1
    yearList.reverse()
    st.write("Modes:")
    st.write("Monthly Report")
    st.write("Yearly Report")
    st.write("All Time")
    st.write("Custom")    
    mode = st.selectbox("Choose mode: ",["Monthly Report","Yearly Report","All Time","Custom"])
    if mode == "Monthly Report":
        st.write("Current Month or Previous Month?")
        mode = st.selectbox("Choose mode: ",["Current Month","Previous Month"])
    if mode == "Yearly Report":
        st.write("Current Year or Previous Year")
        mode = st.selectbox("Choose mode: ",["Current Year","Previous Year"])
    timeList = getUniTime(yearList,mode,regiDT)
st.write("wait for mode option before clicking")
continue_button = st.button("Press when ready")
def getUserPic():
        headers = {"user-agent": USER_AGENT}
        url = 'http://ws.audioscrobbler.com/2.0/'
        payload = {'method':'user.getInfo'}
        payload['user'] = USER_AGENT
        payload['api_key'] = API_KEY
        payload['format'] = 'json'
        response = requests.get(url,headers=headers, params=payload)
        data = response.json()
        return data['user']['image'][2]['#text']

if continue_button == True:
    st.write("Loading . . .")
    header = st.beta_container()
    with header:
        st.title(f"Welcome {USER_AGENT} to your Song Report")
        try:
            userImage = getUserPic()
            st.image(userImage)
            st.write(f"Profile picture of {USER_AGENT}")
        except FileNotFoundError:
            st.write("User has no profile picture")
        st.subheader("Created by Donny Dew")
        st.write("Powered by AudioScrobbler from Last.FM")
        st.write("Last.FM URL: https://www.last.fm/")
#############################################################################################################
    def lastfm_trackGetInfo(artist,track):
        headers = {"user-agent": USER_AGENT}
        url = 'http://ws.audioscrobbler.com/2.0/'
        payload = {'method' : 'track.getInfo'}
        payload['user'] = USER_AGENT
        payload['api_key'] = API_KEY
        payload['format'] = 'json'
        payload["autocorrect"] = 1
        payload["artist"] = artist
        payload["track"] = track
        payload["username"] = USER_AGENT
        response = requests.get(url,headers=headers, params=payload)
        return response.json()
    
    openingData = st.beta_container()
    with openingData:
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
        def getMonthlyTables():
            #Tracks
            trackData = lastfm_weeklyChart(timeList,'user.getWeeklyTrackChart')
            totalSongs = len(trackData['weeklytrackchart']['track'])    
            SongList = []
            ArtistList = []
            SongFreqList = []
            totalTracks = 0
            for i in range(0,totalSongs):
                SongList.append(trackData['weeklytrackchart']['track'][i]['name'])
                ArtistList.append(trackData['weeklytrackchart']['track'][i]['artist']['#text'])
                SongFreqList.append(int(trackData['weeklytrackchart']['track'][i]['playcount']))
                totalTracks += int(trackData['weeklytrackchart']['track'][i]['playcount'])
            TData = {'Song Name' : SongList,'Artist':ArtistList,'PlayCount':SongFreqList}
            td = pd.DataFrame(data=TData)
            td.index = np.arange(1,len(td)+1)
            #Artists
            artistData = lastfm_weeklyChart(timeList,'user.getWeeklyArtistChart')
                
            totalArtists = len(artistData['weeklyartistchart']['artist'])
            artArtistList = []
            artistFreqList = []
            arPercentOfTracks = []
            for i in range(0,totalArtists):
                artArtistList.append(artistData['weeklyartistchart']['artist'][i]['name'])
                artistFreqList.append(artistData['weeklyartistchart']['artist'][i]['playcount'])
                arPercentOfTracks.append(format(float(artistFreqList[i])/totalTracks,'.2%'))
            arData = {"Artist Name":artArtistList,"Freq":artistFreqList,"% Of Total Tracks":arPercentOfTracks}
            ar = pd.DataFrame(data=arData)
            ar.index = np.arange(1,len(ar)+1)
            #Albums
            albumData = lastfm_weeklyChart(timeList,'user.getWeeklyAlbumChart')
            totalAlbums = len(albumData['weeklyalbumchart']['album'])
            alAlbumList = []
            albumFreqList = []
            alPercentOfTracks = []
            for i in range(0,totalAlbums):
                alAlbumList.append(albumData['weeklyalbumchart']['album'][i]['name'])
                albumFreqList.append(albumData['weeklyalbumchart']['album'][i]['playcount'])
                alPercentOfTracks.append(format(float(albumFreqList[i])/totalTracks,'.2%'))
            alData = {"Album Name":alAlbumList,"Freq":albumFreqList,"% Of Total Tracks":alPercentOfTracks}
            al = pd.DataFrame(data=alData)
            al.index = np.arange(1,len(al)+1)
            #Return 3 tables
            return [td,ar,al,SongList,totalSongs]
        dataTables = getMonthlyTables()
        trackTable = dataTables[0]
        artistTable = dataTables[1]
        albumTable = dataTables[2]
        songList = dataTables[3]
        totalSongs = dataTables[4]
        def getpicUrl(num):
            data = lastfm_trackGetInfo(trackTable["Artist"][num],trackTable["Song Name"][num])
            picUrl = data["track"]['album']['image'][3]["#text"]
            return picUrl
    
        def getImages():
            picCount = 0 #this variable will stop program from infintely searching for picture
            image1 = ""
            count = 1
            while len(image1) < 1 and picCount < 10 :
                try:
                    image1 = getpicUrl(count)
                    count += 1
                except KeyError:
                    image1 = ""
                    count += 1
                picCount += 1
            picCount = 0
            image2 = ""
            while len(image2) < 1 and picCount < 10:
                try:
                    image2 = getpicUrl(count)
                except KeyError:
                    image2 = ""
                    count += 1
                picCount += 1
            return [image1,image2]
        st.header("Song, Artist, & Album Data Tables")
        picol1,picol2 = st.beta_columns(2)
        try:
            images = getImages()
            picol1.image(images[0])
            picol2.image(images[1])
        except KeyError:
            st.write("Pictures Not Found")
        st.dataframe(trackTable)
        st.dataframe(artistTable)
        st.dataframe(albumTable)
#########################################################################################################        
    genreCont = st.beta_container()
    with genreCont:
        def lastfm_artistGetTag(artist):
            headers = {"user-agent": USER_AGENT}
            url = 'http://ws.audioscrobbler.com/2.0/'
            payload = {'method' : 'artist.getTopTags'}
            payload['user'] = USER_AGENT
            payload['api_key'] = API_KEY
            payload['format'] = 'json'
            payload["autocorrect"] = 1
            payload["artist"] = artist
            response = requests.get(url,headers=headers, params=payload)
            return response.json()
        genreDic = {}
        for i in range(1,21):
            artistGData = lastfm_artistGetTag(trackTable["Artist"][i])
            for e in range(0,5):
                try:
                    count = artistGData['toptags']['tag'][e]['count']
                    tag = artistGData['toptags']['tag'][e]['name']
                    if tag not in genreDic:
                        genreDic[tag] = count
                    else:
                        genreDic[tag] += count
                except IndexError:
                    break
        def sortDictbyValue(dictionary):
            sorted_keys = sorted(dictionary,reverse = True,key=lambda x: (dictionary[x]))
            tempDict = {}
            for i in sorted_keys:
                tempDict[i] = ""
            tempDict2 = {}
            for (k,v),(k2,v2) in zip(dictionary.items(),tempDict.items()):
                tempDict2[k2] = dictionary[k2]
            return tempDict2
        genreDic = sortDictbyValue(genreDic)
        genreTagList = []
        genreCountList = []
        count = 0
        for k,v in genreDic.items():
            genreTagList.append(k)
            genreCountList.append(v)
            count += 1
            if count > 4:
                break
        genrePie = go.Figure(data=[go.Pie(labels=genreTagList,values=genreCountList)])
        st.header("Genre Pie Chart")
        st.write(genrePie)
####################################################################################################################        
    popCont = st.beta_container()
    def getTrackInfo(track,artist):
        headers = {"user-agent": USER_AGENT}
        url = 'http://ws.audioscrobbler.com/2.0/'
        payload = {'method':'track.getInfo'}
        payload['user'] = USER_AGENT
        payload['api_key'] = API_KEY
        payload['format'] = 'json'
        payload['track'] = track
        payload['artist'] = artist
        payload['autocorrect'] = 1
        response = requests.get(url,headers=headers, params=payload)
        data = response.json()
        return data['track']['playcount']
    def sortDictbyValue2(dictionary,value): #nested dictionary sort
        sorted_keys = sorted(dictionary,reverse = True,key=lambda x: (dictionary[x][value]))
        tempDict = {}
        for i in sorted_keys:
            tempDict[str(i) + "A"] = ""
        dictionary2 = {}
        for k,v in dictionary.items():
            dictionary2[str(k)+"A"] = v    
        tempDict2 = {}
        for (k,v),(k2,v2) in zip(dictionary2.items(),tempDict.items()):
            tempDict2[k2] = dictionary2[k2]
        numberDict = {}
        for i in range(0,len(sorted_keys)):
            numberDict[i] = ""
        tempDict3 = {}
        for (k,v),(k2,v2) in zip(numberDict.items(),tempDict2.items()):
            tempDict3[int(k)] = v2
        return tempDict3
    popDic = {}
    for i in range(1,52):
        popDic[i] = {"Track":trackTable["Song Name"][i],"Artist":trackTable["Artist"][i],
                     "Popularity":int(getTrackInfo(trackTable["Song Name"][i],trackTable["Artist"][i]))}
    popDic = sortDictbyValue2(popDic,"Popularity")
    popTrackList = []
    popArtistList = []
    popPopList = []
    for i in range(1,51):
        popTrackList.append(popDic[i]["Track"])
        popArtistList.append(popDic[i]["Artist"])
        popPopList.append(format(popDic[i]["Popularity"],",.0f"))
    popData = {"Track":popTrackList,"Artist":popArtistList,"Popularity":popPopList}
    popDataFrame = pd.DataFrame(popData)
    popDataFrame.index = np.arange(1,len(popDataFrame)+1)
        
    with popCont:
        st.header("The popularity of your top 50 songs")
        st.dataframe(popDataFrame)
####################################################################################################
    def flattenList(thelist):
        flattenedList = []
        for sublist in thelist:
            for item in sublist:
                flattenedList.append(item)
        return flattenedList
    def getSimilarTrack(track,artist,limit):
        headers = {"user-agent": USER_AGENT}
        url = 'http://ws.audioscrobbler.com/2.0/'
        payload = {'method':'track.getSimilar'}
        payload['user'] = USER_AGENT
        payload['api_key'] = API_KEY
        payload['format'] = 'json'
        payload['track'] = track
        payload['artist'] = artist
        payload['autocorrect'] = 1
        payload['limit'] = limit
        response = requests.get(url,headers=headers, params=payload)
        data = response.json()
        trackList = []
        artistList = []
        matchList = []
        for i in range(0,limit):
            trackList.append(data['similartracks']['track'][i]['name'])  
            artistList.append(data['similartracks']['track'][i]['artist']['name'])
            matchList.append(data['similartracks']['track'][i]['match'])     
        return trackList,artistList,matchList
    
    recTrack = []
    recArtist = []
    recMatch = []
    
    for i in range(1,16):
        try:
            recTrack.append(getSimilarTrack(trackTable["Song Name"][i],trackTable['Artist'][i],3)[0])
            recArtist.append(getSimilarTrack(trackTable["Song Name"][i],trackTable['Artist'][i],3)[1])
            recMatch.append(getSimilarTrack(trackTable["Song Name"][i],trackTable['Artist'][i],3)[2])
        except IndexError:
            pass
    recTrack = flattenList(recTrack)
    recArtist = flattenList(recArtist)
    recMatch = flattenList(recMatch)
    recDic = {}
    for i in range(0,len(recTrack)):
        if recTrack[i] not in songList and recMatch[i] > .25:
            recDic[recTrack[i] + " " + recArtist[i]] = {"Track":recTrack[i],"Artist":recArtist[i],"Match":recMatch[i]}
    recDic = sortDictbyValue2(recDic,"Match")
    recTrack2 = []
    recArtist2 = []
    recMatch2 = []
    for k,v in recDic.items():
        recTrack2.append(recDic[k]["Track"])
        recArtist2.append(recDic[k]["Artist"])
        recMatch2.append(format(recDic[k]["Match"],".0%"))
    recData = {"Track":recTrack2,"Artist":recArtist2,"Match %":recMatch2}
    rec = pd.DataFrame(recData)
    recCont = st.beta_container()
    with recCont:
        st.subheader("Song reccomendations:")
        st.dataframe(rec)
        
#####################################################################################################################
    def getArtistDiscovery():
        artist = artistTable["Artist Name"][1]
        trackList = []
        countList = []
        for i in range(1,totalSongs):
            if (trackTable["Artist"][i] == artist):
                trackList.append(trackTable["Song Name"][i])
                countList.append(trackTable["PlayCount"][i])
        artDiscData = {"Song Name":trackList,"Play Count":countList}
        ad = pd.DataFrame(artDiscData)
        ad.index = np.arange(1,len(ad)+1)
        return ad
    artDiscCont = st.beta_container()
    with artDiscCont:
        bestArtist = artistTable["Artist Name"][1]
        st.header(f"{bestArtist} Discovery")
        st.write(getArtistDiscovery())
########################################################################################################################
    def getMonthUniTime(year,month):
        monthDayList = monthConvert(month,year)
        timeStart = float(time.mktime(datetime.datetime(year,monthDayList[0],1,0,0,0).timetuple())) + 28800  #For CT + 21600
        timeEnd = float(time.mktime(datetime.datetime(year,monthDayList[0],monthDayList[1],23,59,59).timetuple())) + 28800
            
        timeStart = format(timeStart, ".0f")
        timeEnd = format(timeEnd, ".0f")
        floatTime = [timeStart,timeEnd]
        return [str(floatTime) for floatTime in floatTime] 
    def getMonthlyTables(year,month):
        timeList = getMonthUniTime(year,month)
        #Tracks
        trackData = lastfm_weeklyChart(timeList,'user.getWeeklyTrackChart')
            
        totalSongs = len(trackData['weeklytrackchart']['track'])
        songDict = {}
        for i in range(0,totalSongs):
            songDict[i] = {"Track":trackData['weeklytrackchart']['track'][i]['name'],"PlayCount":int(trackData['weeklytrackchart']['track'][i]['playcount'])
            ,"Artist":trackData['weeklytrackchart']['track'][i]['artist']['#text']}
        totalTracks = 0
        for i in range(0,totalSongs):
            totalTracks += songDict[i]["PlayCount"]
            
        SongList = []
        ArtistList = []
        SongFreqList = []
        for i in range(0,totalSongs):
            SongList.append(songDict[i]["Track"])
            ArtistList.append(songDict[i]["Artist"])
            SongFreqList.append(songDict[i]["PlayCount"])
        tData = {'Song Name' : SongList,'Artist':ArtistList,'PlayCount':SongFreqList}
        td = pd.DataFrame(data=tData)
        td.index = np.arange(1,len(td)+1)
        #Artists
        artistData = lastfm_weeklyChart(timeList,'user.getWeeklyArtistChart')
            
        totalArtists = len(artistData['weeklyartistchart']['artist'])
        artArtistList = []
        artistFreqList = []
        for i in range(0,totalArtists):
            artArtistList.append(artistData['weeklyartistchart']['artist'][i]['name'])
            artistFreqList.append(artistData['weeklyartistchart']['artist'][i]['playcount'])
        arData = {"Artist Name":artArtistList,"PlayCount":artistFreqList}
        ar = pd.DataFrame(data=arData)
        ar.index = np.arange(1,len(ar)+1)
        #Albums
        albumData = lastfm_weeklyChart(timeList,'user.getWeeklyAlbumChart')
        totalAlbums = len(albumData['weeklyalbumchart']['album'])

        alAlbumList = []
        albumFreqList = []
        for i in range(0,totalAlbums):
            alAlbumList.append(albumData['weeklyalbumchart']['album'][i]['name'])
            albumFreqList.append(albumData['weeklyalbumchart']['album'][i]['playcount'])
        alData = {"Album Name":alAlbumList,"Freq":albumFreqList}
        al = pd.DataFrame(data=alData)
        al.index = np.arange(1,len(al)+1)
        #Return 3 tables
        return [td,ar,al,tData,arData]               
    def getTotalSongs(year,month):
        timeList = getMonthUniTime(year,month)
        #Tracks
        trackData = lastfm_weeklyChart(timeList,'user.getWeeklyTrackChart')
            
        totalSongs = len(trackData['weeklytrackchart']['track'])
        totalTracks = 0
        for i in range(0,totalSongs):
            totalTracks += int(trackData['weeklytrackchart']['track'][i]['playcount'])
        return totalTracks
    
    if mode == "Current Year" or mode == "Previous Year":
        almost_year = time.ctime(int(timeList[0]))
        year = int(almost_year[-4:])
        theMonths = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        monthTables = []
        totalSongsList = []
        for month in theMonths:
            monthTables.append(getMonthlyTables(year,month))
            totalSongsList.append(getTotalSongs(year,month))
        ts = pd.DataFrame(data=totalSongsList,index=[1,2,3,4,5,6,7,8,9,10,11,12])
        
        janTables = monthTables[0]
        febTables = monthTables[1]
        marTables = monthTables[2]
        aprTables = monthTables[3]
        mayTables = monthTables[4]
        junTables = monthTables[5]
        julTables = monthTables[6]
        augTables = monthTables[7]
        sepTables = monthTables[8]
        octTables = monthTables[9]
        novTables = monthTables[10]
        decTables = monthTables[11]
        
        def getTopSong():
            Song = []
            Artist = []
            Plays = []
            for i in range(0,12):
                try:
                    Song.append(monthTables[i][3]['Song Name'][0])
                    Artist.append(monthTables[i][3]['Artist'][0])
                    Plays.append(monthTables[i][3]['PlayCount'][0])
                except IndexError:
                    Song.append("-")
                    Artist.append("-")
                    Plays.append(0)
            return [Song,Artist,Plays]
        def getTopArtist():
            Artist = []
            Plays = []
            for i in range(0,12):
                try:
                    Artist.append(monthTables[i][4]['Artist Name'][0])
                    Plays.append(monthTables[i][4]['PlayCount'][0])
                except IndexError:
                    Artist.append("-")
                    Plays.append(0)
            return [Artist,Plays]
        TopSongData = getTopSong()
        topData = {"Track":TopSongData[0],"Artist":TopSongData[1],"Freq":TopSongData[2]}
        tps = pd.DataFrame(data=topData,index=[1,2,3,4,5,6,7,8,9,10,11,12])
        
        tps2 = pd.DataFrame(data=TopSongData[2],index=[1,2,3,4,5,6,7,8,9,10,11,12])
        TopArtistData = getTopArtist()
        topAData = {"Artist":TopArtistData[0],"Freq":TopArtistData[1]}
        ta = pd.DataFrame(data=topAData,index=[1,2,3,4,5,6,7,8,9,10,11,12])
        topStuffCont = st.beta_container()
        with topStuffCont:
            st.subheader("Tracks played per month")
            st.bar_chart(ts)
            st.subheader("Top Songs from each Month")
            st.dataframe(tps)
            st.subheader("Top Artists from each Month")
            st.dataframe(ta)
            st.subheader("Top Songs Freq per month")
            st.bar_chart(tps2)
        JanuaryData = st.beta_container()
        FebruaryData = st.beta_container()
        MarchData = st.beta_container()
        AprilData = st.beta_container()
        MayData = st.beta_container()
        JuneData = st.beta_container()
        JulyData = st.beta_container()
        AugustData = st.beta_container()
        SeptemberData = st.beta_container()
        OctoberData = st.beta_container()
        NovemberData = st.beta_container()
        DecemberData = st.beta_container()
        with JanuaryData:
            st.header("January Data")
            st.dataframe(janTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(janTables[1])
            tabcol2.dataframe(janTables[2])
            st.write(f"Total songs played in month: {totalSongsList[0]}")
        
        with FebruaryData:
            st.header("February Data")
            st.dataframe(febTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(febTables[1])
            tabcol2.dataframe(febTables[2])
            st.write(f"Total songs played in month: {totalSongsList[1]}")
            
        with MarchData:
            st.header("March Data")
            st.dataframe(marTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(marTables[1])
            tabcol2.dataframe(marTables[2])
            st.write(f"Total songs played in month: {totalSongsList[2]}")
            
        with AprilData:
            st.header("April Data")
            st.dataframe(aprTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(aprTables[1])
            tabcol2.dataframe(aprTables[2])
            st.write(f"Total songs played in month: {totalSongsList[3]}")
        
        with MayData:
            st.header("May Data")
            st.dataframe(mayTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(mayTables[1])
            tabcol2.dataframe(mayTables[2])
            st.write(f"Total songs played in month: {totalSongsList[4]}")
            
        with JuneData:
            st.header("June Data")
            st.dataframe(junTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(junTables[1])
            tabcol2.dataframe(junTables[2])
            st.write(f"Total songs played in month: {totalSongsList[5]}")
            
        with JulyData:
            st.header("July Data")
            st.dataframe(julTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(julTables[1])
            tabcol2.dataframe(julTables[2])
            st.write(f"Total songs played in month: {totalSongsList[6]}")
            
        with AugustData:
            st.header("August Data")
            st.dataframe(augTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(augTables[1])
            tabcol2.dataframe(augTables[2])
            st.write(f"Total songs played in month: {totalSongsList[7]}")
            
        with SeptemberData:
            st.header("September Data")
            st.dataframe(sepTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(sepTables[1])
            tabcol2.dataframe(sepTables[2])
            st.write(f"Total songs played in month: {totalSongsList[8]}")
            
        with OctoberData:
            st.header("October Data")
            st.dataframe(octTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(octTables[1])
            tabcol2.dataframe(octTables[2])
            st.write(f"Total songs played in month: {totalSongsList[9]}")
            
        with NovemberData:
            st.header("November Data")
            st.dataframe(novTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(novTables[1])
            tabcol2.dataframe(novTables[2])
            st.write(f"Total songs played in month: {totalSongsList[10]}")
            
        with DecemberData:
            st.header("December Data")
            st.dataframe(decTables[0])
            tabcol1,tabcol2 = st.beta_columns(2)
            tabcol1.dataframe(decTables[1])
            tabcol2.dataframe(decTables[2])
            st.write(f"Total songs played in month: {totalSongsList[11]}")
                    
        
        
        
