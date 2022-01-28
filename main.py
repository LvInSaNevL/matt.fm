from ast import And
from pydoc import cli
import requests
import praw
import json
from urllib.parse import urlparse
import re
import os

import google_auth_oauthlib
import google.oauth2
import googleapiclient.discovery
import googleapiclient.errors
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

youtubeURLs = ["www.youtube.com",   
               "youtube.com",
               "youtu.be"]

contnentLinks = []

def get_authenticated_service():
    print("Authenticating service access and refresh token")

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
        print(credFlow)
        with open('refresh.token', 'w+') as f:
            credToken = credFlow
            f.write(credFlow._refresh_token)
            print('Saved Refresh Token to file: refresh.token')
    
    print('Refresh Token:', credToken)
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credToken)

def add_to_playlist(videoID):
    print("Adding {0} to playlist".format(videoID))

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service()

    add_video_response = youtube.playlistItems().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                playlistId="PLRDuNIkwpnsfJaOX5Bq3jrPtP2WfP_vBl",
                resourceId=dict(
                    kind="youtube#video",
                    videoId=videoID
                )
            )
        )
    ).execute()

    print(add_video_response)


def main():
    print("Retreiving music")

    with open("auth.json") as jsonfile:
            auth = json.load(jsonfile)

    redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                        client_secret=auth['reddit']['client_secret'],
                        user_agent=auth['reddit']['user_agent'],
                        username=auth['reddit']['username'],                     
                        password=auth['reddit']['password'])

    for i in redditAuth.multireddit('lv_insane_vl', 'music').hot(limit=250):
        if any(x in i.url for x in youtubeURLs) and len(contnentLinks) < 100:
            regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
            result = re.search(regex, i.url)
            try:
                contnentLinks.append(result.group())
            except:
                pass

    for t in contnentLinks:
        add_to_playlist(t)


# Actual start
if __name__ == "__main__":
    main()