import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import pickle
import urllib
import requests
import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Gets the views, duration, likes, and dislikes from a video.
# Performs a YT api call which uses about 5 units per request
# Called onto every video
def get_video_stats(youtube, vidId):
    # Two different requests
    req1 = youtube.videos().list(part='snippet,contentDetails', id=vidId)
    res1 = req1.execute()
    # https://www.googleapis.com/youtube/v3/videos?part=statistics&id=IDIDID&key=KEYKEYKEY&part=contentDetails
    req2 = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" + vidId + "&key=AIzaSyAfxOHwTyZWlHoGTvCd0M3dpo_4oqlKHAA" + "&part=contentDetails")
    res2 = json.load(req2)

    # Set values
    duration = res1['items'][0]['contentDetails']['duration']
    views = res2['items'][0]['statistics']['viewCount']
    dislikes = None; likes = None 
    try:
        if res2['items'][0]['statistics']['dislikeCount']:
            dislikes = res2['items'][0]['statistics']['dislikeCount']
    except KeyError:
        dislikes = None 

    try:
        if res2['items'][0]['statistics']['likeCount']:
            likes = res2['items'][0]['statistics']['likeCount']
    except KeyError:
        likes = None  

    return (views, duration, likes, dislikes)

# Grabs/gets the credentials in order to use the YT api
# There should be a pickle file which does this automatically
def get_credentials():
    if os.path.exists("api_keys/yt_picklefile"):
        with open("api_keys/yt_picklefile", 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("api_keys/yt_secret.json", ["https://www.googleapis.com/auth/youtube.force-ssl"])
        credentials = flow.run_console()
        with open("api_keys/yt_picklefile", 'wb') as f:
            pickle.dump(credentials, f)
    return credentials

# Fill the dataframe here after querying YT results
# There's a good chance you'll hit the quota right now
# If there's a error, save whatever has been scraped
def process_dataframe(df):
    try:
        # Sets up youtube API portion here
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=get_credentials())
        for i in df.index:
            # Get video ID of top result
            #print(df)
            query = df['title'][i] + " " + df['artist'][i]
            request = youtube.search().list(part="snippet", maxResults=3, q=query)
            response = request.execute()
            print(query)
            # Get top 3 results
            vidId1 = response['items'][0]['id']['videoId']
            stats1 = get_video_stats(youtube, vidId1)

            df.at[i,'Title 1'] = response['items'][0]['snippet']['title']
            df.at[i,'videoID 1'] = response['items'][0]['id']['videoId']
            df.at[i,'Views 1'] = stats1[0]
            df.at[i,'Duration 1'] = stats1[1]
            df.at[i,'Thumbs Up 1'] = stats1[2]
            df.at[i,'Thumbs Down 1'] = stats1[3]

            vidId2 = response['items'][1]['id']['videoId']
            stats2 = get_video_stats(youtube, vidId2)
            df.at[i,'Title 2'] = response['items'][1]['snippet']['title']
            df.at[i,'videoID 2'] = response['items'][1]['id']['videoId']
            df.at[i,'Views 2'] = stats2[0]
            df.at[i,'Duration 2'] = stats2[1]
            df.at[i,'Thumbs Up 2'] = stats2[2]
            df.at[i,'Thumbs Down 2'] = stats2[3]

            vidId3 = response['items'][2]['id']['videoId']
            stats3 = get_video_stats(youtube, vidId3)
            df.at[i,'Title 3'] = response['items'][2]['snippet']['title']
            df.at[i,'videoID 3'] = response['items'][2]['id']['videoId']
            df.at[i,'Views 3'] = stats3[0]
            df.at[i,'Duration 3'] = stats3[1]
            df.at[i,'Thumbs Up 3'] = stats3[2]
            df.at[i,'Thumbs Down 3'] = stats3[3]
    except Exception as e:
        print(e)
        print("An exception occured. High likely quota limit. Saving whatever has been read")
    
    
    return df

# Takes a dictionary where keys are sheet names (Excel file)
# Values are pandas dataframes
def get_youtube_data(sheets,progress_callback):
    i=0
    for key, value in sheets.items():
        sheets[key] = process_dataframe(value)
        progress_callback.emit(int(i*100/len(sheets)))
    progress_callback.emit(100)
    return sheets
