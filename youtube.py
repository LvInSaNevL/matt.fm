from http import HTTPStatus
from pydoc import cli
import datetime
import re
from urllib import response
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
    if (authDiff.total_seconds() * 1000 < 100):
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
        credFlow = flow.run_local_server(port=0)
        with open('refresh.token', 'w+') as f:
            credToken = credFlow
            f.write(credFlow._refresh_token)
            utils.logPrint('Saved Refresh Token to file: refresh.token', 0)
    
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credToken)

def add_to_playlist(videoID):
    utils.logPrint("Adding {0} to playlist".format(videoID), 0)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service(lastAuth)

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

    utils.logPrint(add_video_response, 0)

def remove_from_playlist():
    utils.logPrint("Clearing out yesterdays music", 0)
    toRemove = []

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service(lastAuth)

    request = youtube.playlistItems().list(
        part = "snippet,contentDetails",
        playlistId = playlist,
        maxResults = 50
    )
    response = request.execute()
    utils.logPrint(response, 0)

    playlist_items = []
    while request is not None:
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)
    
    for t in playlist_items:
        youtube.playlistItems().delete(
            id = t["id"]
        ).execute()

def check_video_exist(videoID):
    try:
        request = requests.head("https://music.youtube.com/watch?v=".join(videoID))
        return request.status_code == HTTPStatus.OK
    except:
        return False