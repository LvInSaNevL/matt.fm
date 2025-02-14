# File imports
import utils
import datatypes
# Dep imports
import datetime
import requests
import isodate
import os
# YouTube specific imports
import google.auth.exceptions
import google_auth_oauthlib
import google.oauth2
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.errors

# Variables and such
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly"]
# playlist = "PL4QDB2QvOpDmz4YHkJcPqdMBs51cSnEdo" # Prod
playlist = "PL4QDB2QvOpDkw9d28o9uAZmOcmm2C1O2O" # Testing
lastAuth = datetime.datetime.min       

###############
# ERROR TYPES #
###############
'''
Returned if a video is not available on youtube, usually because of a 404 response
'''
class VideoNotAvailable(Exception):
    pass

# Authenticates to the Google API
def get_authenticated_service(lastAuth):
    utils.logPrint("Authenticating YouTube service access and refresh token", 0)

    # YouTube has strict rate limits, so we have to throttle ourselves
    nowAuth = datetime.datetime.now()
    authDiff = nowAuth - lastAuth
    if (authDiff.total_seconds() * 1000 < 250):
        utils.logPrint("Refresh cycle not reached, waiting", 0)
        datetime.time.sleep(0.150)
    
    lastAuth = datetime.datetime.now()

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "youtubeauth.json"
    redirect_uri = "http://localhost:5656"
    cred_token = None

    # Try to use the refresh token first
    if os.path.exists("refresh.token"):
        utils.logPrint("Attempting to read refresh.token", 0)
        try:
            cred_token = Credentials.from_authorized_user_file('refresh.token')
            cred_token.refresh(Request())
        except google.auth.exceptions.RefreshError as e:
            print(e)
    # Manually authenticate with the user if no token is available  
    else:
        utils.logPrint("Unable to read token, falling back to auth flow")
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
# Recursively removes all videos from the current playlist
### </summary>
def clear_playlist():
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

def playability(VIDEO_ID):    
    '''
    Returns the playability status of a song on YouTube Music
        True = Playable
        False = Not Playable

    Usage Examples:
    Give me a second - Annie = NOT PLAYABLE
    >>> playability("MgNDY2qKZGo")
    False
    
    Never gonna give you up - Rick Astley = PLAYABLE
    >>> playability("dQw4w9WgXcQ")
    True

    Invalid Song - Made Up Artist = NOT PLAYABLE
    >> playability("cumfuck")
    VideoNotAvailable
    '''
    URL = "https://music.youtube.com/youtubei/v1/player"
    API_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

    headers = {
        "Content-Type": "application/json",
        "Accept-Language": "en",
        "Referer": "https://music.youtube.com"
    }

    payload = {
        "videoId": VIDEO_ID,
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "1.9999099"
            }
        }
    }

    response = requests.post(f"{URL}?key={API_KEY}", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        playable = data["playabilityStatus"]["status"]
        if (playable == "OK"):
            return True
        elif (playable == "UNPLAYABLE"):
            return False
        elif (playable == "ERROR"):
            if (data["playabilityStatus"]['reason'] == "This video is unavailable"):
                return VideoNotAvailable({"id": VIDEO_ID, "message": "Video is no longer available on youtube"})
        else:
            return False
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

# contentDetails,status
def get_video(videoID):
    utils.logPrint("Gettting info about {0}".format(videoID), 0)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_authenticated_service(lastAuth)
    request = youtube.videos().list(
        part="snippet,topicDetails,contentDetails,statistics,status",
        id=videoID
    )
    response = request.execute()
    rawData = response["items"][0]
    print(rawData)

    # Final round of checks to make sure song meets criteria
    songLength = isodate.parse_duration(rawData["contentDetails"]["duration"]).seconds
    checks = (
            60 < songLength < 600,
            "[free]" not in rawData["snippet"]["title"].lower(),
            "type beat" not in rawData["snippet"]["title"].lower(),
            "ost" not in rawData["snippet"]["title"].lower(),
            "#ai" not in rawData["snippet"]["title"].lower(),
            "ai cover" not in rawData["snippet"]["title"].lower(),
            int(rawData["statistics"]["viewCount"]) <= 50000
        )
    if not all(checks):
        return None  
    else:
        _thumbs = rawData['snippet']['thumbnails'].popitem()
        return datatypes.Song(
                yt_id = rawData['id'],
                # mfm_id: str
                published = rawData['snippet']['publishedAt'],
                genre = rawData['topicDetails']['topicCategories'][-1], 
                title = rawData['snippet']['title'],
                description = rawData['snippet']['description'],
                artist = datatypes.Artist(
                        name = rawData['snippet']['channelTitle'],
                        yt_id = rawData['snippet']['channelId']
                ),
                thumbnail = _thumbs[1],
                viewcount = rawData['statistics']['viewCount'],
                duration = songLength
            )


def add_video(videoID):
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
        print(add_video_response)
        utils.logPrint(add_video_response['snippet']['title'], 0)
        return True
    except googleapiclient.errors.HttpError as e:
            print(e)
    except Exception as e:
        utils.logPrint(f"Fatal Error: {e}", 4)