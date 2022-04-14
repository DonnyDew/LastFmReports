# Last FM Reports
This project takes user music data from Last Fm to generate different kinds of reports

## Purpose of Project
I wanted to see my music data in a Monthly/Yearly breakdown in a way that Last Fm didn't. I took some inspiration from Spotify Wrapped in how you have all your music recapped. However I am displeased in how Spotify is often inaccurate with tracking
user statistics so I rely on Last Fm. With my own program I can customize the stats to my liking. I hope people can use my project for their own curiosity about their music stats and/or creating their
own music stat projects.

## Last FM
Last FM is a site that can link with any platform you use to listen to music like spotify,apple, and youtube.
It accurately keeps track of all the songs you listen to and gives you the data.
Last FM has an API that I used to get the data

## Set Up
To track your own music you need to create a Last FM account and link it to whatever platform you listen to music.
To access the project click this link: https://share.streamlit.io/donnydew/lastfmreports/LastFMReports.py
From there you enter your Last Fm username(if you don't have one you can use mine "DonnyDew"). 

## Different Modes
The 4 modes are monthly, yearly, all time, and custom. The modes represent what time range of music you would like to look at and are self explanatory.For monthly and yearly you can choose the current month/year or any one you want.

## Monthly Report Features
* Pictures of two most played songs
* 3 data tables showing songs, artists, and albums listened to for the month and how many times listned to. 
* Genre Pie Chart which is shows the genres of music you listen to.
* Another data table ranking your top 50 played songs by how popular they are by Last Fm users.
* Song reccomendations which uses a built in Last Fm features
* Artist Discovery which breaks downs all the songs you listned to by your most played artist for the month.

## Yearly Report Features
* Everything from the monthly report
* Bar chart showing tracks played per month
* Table of top song and artist of each month and frequency
* Bar Chart of how many plays your top song of the month had
* The 3 data tables from the monthly report for every single month

## All Time and Custom Features
* Same as the Monthly Report

## API Keys and Secrets
In order to keep my info safe, I hide my API keys in an environmental variable. In order to use this yourself, you need to make your own api account. Last FM is really easy to get and you can simply replace `API_KEY` with your own.
For Spotify api you need to a client id, client secret, and redirect url in order for your token to refresh. The library I used for this is Spotipy and I would recommend researching more about that

# What is this artistStats file?
It is a work in progress program that focuses on an artist and is easy to change from artist to artist. It was from that program I added the artist discovery to the LastFm Reports. To run this program you would have to do it locally as of now (4/14/22).

