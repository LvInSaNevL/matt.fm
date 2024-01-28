from ctypes import util
from http import HTTPStatus
import sys
from pydoc import cli
import datetime
import isodate
import re
from urllib import response
from urllib.error import HTTPError
import requests
import json
from urllib.parse import urlparse
import os
import utils

import google.auth.exceptions
import google_auth_oauthlib
import google.oauth2
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.errors
import datatypes

# Variables and such
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly"]
playlist = "PL4QDB2QvOpDmz4YHkJcPqdMBs51cSnEdo"
lastAuth = datetime.datetime.min       

# Authenticates to the Google API
def get_authenticated_service(lastAuth):
    utils.logPrint("Authenticating YouTube service access and refresh token", 0)
    nowAuth = datetime.datetime.now()
    authDiff = nowAuth - lastAuth
    if (authDiff.total_seconds() * 1000 < 250):
        datetime.time.sleep(0.150)
    
    lastAuth = datetime.datetime.now()

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "youtubeauth.json"
    redirect_uri = "http://localhost:5656"
    cred_token = None

    # Try to use the refresh token first
    if os.path.exists("refresh.token"):
        try:
            cred_token = Credentials.from_authorized_user_file('refresh.token')
            cred_token.refresh(Request())
        except google.auth.exceptions.RefreshError as e:
            print(e)
    # Manually authenticate with the user if no token is available  
    else:
        credFlow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        cred = credFlow.run_local_server(
            host='localhost',
            port=5656,
            authorization_prompt_message='Please visit this URL: {url}',
            success_message='The auth flow is complete; you may close this window.',
            open_browser=False
        )
        with open('refresh.token', 'w') as token:
            token.write(cred.to_json())
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=cred_token)

### <summary>
# Adds a new video to the playlist
# <param name=videoID> The YouTube video ID, usually provided by URL
### </summary
def add_to_playlist(videoID):
    utils.logPrint("Adding {0} to playlist".format(videoID), 0)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service(lastAuth)

    try:
        add_video_response = youtube.playlistItems().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    playlistId=playlist,
                    resourceId=dict(
                        kind="youtube#video",
                        videoId=videoID
                    )
                )
            )
        ).execute()
        utils.logPrint(add_video_response['snippet']['title'], 0)
    except googleapiclient.errors.HttpError as e:
            print(e)
    except:
        utils.logPrint(sys.exc_info()[0], 2)

### <summary>
# Recursively removes all videos from the current playlist
### </summary>
def remove_from_playlist():
    utils.logPrint("Clearing out yesterdays music", 0)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service(lastAuth)

    # Makes the first round of API calls
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist
    )

    response = request.execute()
    utils.logPrint(response, 0)

    currentLen = response["pageInfo"]["totalResults"]
    playlist_items = []    
    for p in response['items']:
        playlist_items.append(p)
        
    utils.logPrint("Getting previous days content", 0)
    while len(playlist_items) < response["pageInfo"]['totalResults']:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlist,
            pageToken=response["nextPageToken"]
        )        
        response = request.execute()
        for p in response['items']:
            playlist_items.append(p)
    utils.logPrint(playlist_items, 0)
    
    for t in playlist_items:
        try:
            utils.logPrint("Removing " + t["id"], 0)
            youtube.playlistItems().delete(
                id = t["id"]
            ).execute()
        except googleapiclient.errors.HttpError as e:
            print(e)
            # utils.logPrint("Usually a 404 error that can(?) be ignored " + e, 3)
        except:
            utils.logPrint(sys.exc_info()[0], 2)

def check_video_exist(videoID):
    """A simple helper function to verify that the YT video is available on YT Music, because the
    YT API doesn't have that information handy

    Parameters
    ----------
    videoID : str
        The ID of the video to check

    Returns
    -------
    A boolean value telling if the video is available
        True = video is available
        False = video is not available

    Raises
    ------
    Honestly I'm not sure, but I am catching something
    """
    utils.logPrint("Checking if " + videoID + " exists", 0)
    # Request to check if it is available on YT Music since there is no official way
    # Free API access that doesn't effect our quota so this is nice to use
    try:
        headers = {'Accept-Encoding': 'identity'}
        url = "https://yt.lemnoslife.com/videos?part=music&id=" + videoID
        request = requests.get(url=url)
        isMusic = json.loads(request.text)      
        if isMusic['items'][0]['music']['available']:
            return True
        else:
            return False
    except Exception as e:
        print(e)

def get_video_info(videoID):
    """Gets all the info available for the song, so we can document it

    Parameters
    ----------
    videoID : str
        The YouTube video ID, usually provided by URL

    Returns
    -------
    datatypes.Song()
    """
    utils.logPrint("Getting data for " + videoID, 0)

    # Making sure the song is actually available before hitting the YT API
    isAvailable = check_video_exist(videoID)
    if not isAvailable:
        return None

    # Getting the data from the YT API
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service(lastAuth)

    # Makes the first round of API calls
    request = youtube.videos().list(
        part="snippet,topicDetails,contentDetails,statistics",
        id=videoID
    )
    response = request.execute()
    
    rawData = response["items"][0]

    # Final round of checks to make sure song meets criteria
    checks = (
            60 < isodate.parse_duration(rawData["contentDetails"]["duration"]).seconds < 600,
            "[free]" not in rawData["snippet"]["title"].lower(),
            "type beat" not in rawData["snippet"]["title"].lower(),
            "ost" not in rawData["snippet"]["title"].lower(),
            int(rawData["statistics"]["viewCount"]) <= 75000
        )
    if not all(checks):
        return None    

    data = datatypes.Song(
        yt_id=rawData["id"],
        mfm_id=utils.genUUID(),
        published=rawData["snippet"]["publishedAt"],
        genre=rawData["topicDetails"]["topicCategories"][0],
        title=rawData["snippet"]["title"],
        description=rawData["snippet"]["description"],
        artist=datatypes.Artist(
            name=rawData["snippet"]["channelTitle"],
            yt_id=rawData["snippet"]["channelId"]
        ),
        thumbnail=rawData["snippet"]["thumbnails"]["default"]["url"],
        viewcount=rawData["statistics"]["viewCount"],
        duration= isodate.parse_duration(rawData["contentDetails"]["duration"]).seconds
    )
    return data