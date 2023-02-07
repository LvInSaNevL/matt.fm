from ctypes import util
from http import HTTPStatus
import sys
from pydoc import cli
import datetime
import re
from urllib import response
from urllib.error import HTTPError
import requests
import json
from urllib.parse import urlparse
import os
import utils

import google_auth_oauthlib
import google.oauth2
import googleapiclient.discovery
import googleapiclient.errors
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly"]
playlist = "PLRDuNIkwpnsfJaOX5Bq3jrPtP2WfP_vBl"
lastAuth = datetime.datetime.min

def get_authenticated_service(lastAuth):
    utils.logPrint("Authenticating service access and refresh token", 0)
    nowAuth = datetime.datetime.now()
    authDiff = nowAuth - lastAuth
    if (authDiff.total_seconds() * 1000 < 250):
        datetime.time.sleep(0.150)
    
    lastAuth = datetime.datetime.now()

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "youtubeauth.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)

    if os.path.exists("refresh.token"):
        with open("refresh.token", 'r') as t:
            rawToken = t.read()
            with open(client_secrets_file, 'r') as j:
                youtubeAuth = json.loads(j.read())
            params = {
                "grant_type": "refresh_token",
                "client_id": youtubeAuth['installed']['client_id'],
                "client_secret": youtubeAuth['installed']['client_secret'],
                "refresh_token": rawToken
            }
            authorization_url = "https://www.googleapis.com/oauth2/v4/token"
            r = requests.post(authorization_url, data=params)
            credToken = google.oauth2.credentials.Credentials(
                                                    rawToken,
                                                    refresh_token = rawToken,
                                                    token_uri = 'https://accounts.google.com/o/oauth2/token',
                                                    client_id = youtubeAuth['installed']['client_id'],
                                                    client_secret = youtubeAuth['installed']['client_secret']
                                                    )
    else: 
        credFlow = flow.run_console()
        with open('refresh.token', 'w+') as f:
            credToken = credFlow
            f.write(credFlow._refresh_token)
            utils.logPrint('Saved Refresh Token to file: refresh.token', 0)
    
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credToken)

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
    except googleapiclient.errors.HttpError as err:
        if err.reason == "quotaExceeded":
            utils.logPrint("Quota limit exceded, terminating program.", 4)
            sys.exit()
        elif err.reason == "backendError":
            datetime.time.sleep(0.250)
            add_to_playlist(videoID)
        else:
            utils.logPrint("Unhandled exception while adding video: " + str(err), 4)

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
        except googleapiclient.errors.HttpError:
            utils.logPrint("Usually a 404 error that can(?) be ignored", 3)
        except:
            utils.logPrint(sys.exc_info()[0], 2)

### <summary>
# Simple helper function to verify that the youtube video is available on YT Music
# Also happens to provide the duration of the video which is handy
# <param name=videoID> The YouTube video ID, usually provided by URL
# <returns> Boolean value to tell if video is available
### </summary>
def check_video_exist(videoID):
    utils.logPrint("Checking if " + videoID + " exists", 0)
    try:
        headers = {'Accept-Encoding': 'identity'}
        url = "https://yt.lemnoslife.com/videos?part=status,contentDetails,music&id=" + videoID
        request = requests.get(url=url)
        data = json.loads(request.text)
        duration = int(data['items'][0]['contentDetails']['duration']) / 60
        if (data['items'][0]['music']['available']) and (duration < 10):
            return True
        else:
            return False
    except:
        return False
    