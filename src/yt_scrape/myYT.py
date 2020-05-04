import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import pickle
import urllib
import requests
import os
import json
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Converts youtube's PT time to a default colon seperated form
def _js_parseInt(string):
    return str(''.join([x for x in string if x.isdigit()]))
def formatTime(duration):
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
    hours = _js_parseInt(match[0]) if match[0] else str(0)
    minutes = _js_parseInt(match[1]) if match[1] else str(0)
    seconds = _js_parseInt(match[2]) if match[2] else str(0)
    if hours == str(0):
        return minutes + ":" + seconds
    else:
        return hours + ":" + minutes + ":" + seconds


# Gets the views, duration, likes, and dislikes from a video.
# Performs a YT api call which uses about 5 units per request
# Called onto every video
def get_video_stats(youtube, vidId, key):
    # Two different requests
    req1 = youtube.videos().list(part='snippet,contentDetails', id=vidId)
    res1 = req1.execute()
    # https://www.googleapis.com/youtube/v3/videos?part=statistics&id=IDIDID&key=KEYKEYKEY&part=contentDetails
    req2 = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" + vidId + "&key=" + key + "&part=contentDetails")
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
def process_dataframe(df,current_finished_count,total_records,progress_callback):
    try:
        # Sets up youtube API portion here
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=get_credentials())
        index=0

        # Get key
        f = open("api_keys/yt_apikey", "r")
        apikey = f.read()
        f.close()

        for i in df.index:
            # Get video ID of top result
            #print(df)
            query = df['title'][i] + " " + df['artist'][i]
            request = youtube.search().list(part="snippet", maxResults=3, q=query)
            response = request.execute()
            print(query)
            # Get top 3 results
            vidId1 = response['items'][0]['id']['videoId']
            stats1 = get_video_stats(youtube, vidId1, apikey)

            df.at[i,'Title 1'] = response['items'][0]['snippet']['title']
            df.at[i,'videoID 1'] = response['items'][0]['id']['videoId']
            df.at[i,'Views 1'] = stats1[0]
            df.at[i,'Duration 1'] = formatTime(stats1[1])
            df.at[i,'Thumbs Up 1'] = stats1[2]
            df.at[i,'Thumbs Down 1'] = stats1[3]

            vidId2 = response['items'][1]['id']['videoId']
            stats2 = get_video_stats(youtube, vidId2, apikey)
            df.at[i,'Title 2'] = response['items'][1]['snippet']['title']
            df.at[i,'videoID 2'] = response['items'][1]['id']['videoId']
            df.at[i,'Views 2'] = stats2[0]
            df.at[i,'Duration 2'] = formatTime(stats2[1])
            df.at[i,'Thumbs Up 2'] = stats2[2]
            df.at[i,'Thumbs Down 2'] = stats2[3]

            vidId3 = response['items'][2]['id']['videoId']
            stats3 = get_video_stats(youtube, vidId3, apikey)
            df.at[i,'Title 3'] = response['items'][2]['snippet']['title']
            df.at[i,'videoID 3'] = response['items'][2]['id']['videoId']
            df.at[i,'Views 3'] = stats3[0]
            df.at[i,'Duration 3'] = formatTime(stats3[1])
            df.at[i,'Thumbs Up 3'] = stats3[2]
            df.at[i,'Thumbs Down 3'] = stats3[3]
            index+=1
            progress_callback.emit(int(100 * (index+current_finished_count) / total_records))
    except Exception as e: print(e)
    
    return df

# Takes a dictionary where keys are sheet names (Excel file)
# Values are pandas dataframes
def get_youtube_data(sheets,output_path, progress_callback):
    i=0
    total_records=0
    for sheet_name in sheets:
        total_records+=sheets[sheet_name].shape[0]
    writer = pd.ExcelWriter(os.path.join(output_path, 'youtube_output.xlsx'), engine='xlsxwriter')
    current_finished_count=0
    for key, value in sheets.items():
        #sheets[key] = process_dataframe(value)
        process_dataframe(value,current_finished_count,total_records,progress_callback).to_excel(writer, sheet_name=key)
        current_finished_count+=value.shape[0]
        progress_callback.emit(int((i+1)*100/len(sheets)))
        i+=1
    writer.save()
    progress_callback.emit(100)
    return sheets
