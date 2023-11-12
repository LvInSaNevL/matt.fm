# File imports
import utils
import youtube
import db_hook
import datatypes
# dep imports
import json
import time
import praw
import re
import inspect

youtubeURLs = ["www.youtube.com",   
               "youtube.com",
               "youtu.be"]
last_call = 0
contnentLinks = []

def authenticate():
    global last_call
    while time.time() - last_call < 3:
      time.sleep(1)
    last_call = time.time()

    utils.logPrint("Authenticating Reddit service access and refresh token", 0)
    with open("auth.json") as jsonfile:
        auth = json.load(jsonfile)

    redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                        client_secret=auth['reddit']['client_secret'],
                        user_agent=auth['reddit']['user_agent'],
                        username=auth['reddit']['username'],                     
                        password=auth['reddit']['password'])
    
    return redditAuth

totalSongs = 0
def getPosts(count):    
    global totalSongs
    utils.logPrint("Retreiving music", 0)

    regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    creds = authenticate()
    for i in creds.multireddit('matt-fm', 'music').hot(limit=250):
        if len(db_hook.todaySongs) < count:
            try: 
                result = re.search(regex, i.url)
                yt_data = youtube.check_video_exist(result.group())
                checks = (i.url not in youtubeURLs,
                            result.group() not in contnentLinks,
                            youtube.check_video_exist(result.group())                       
                        )
                
                if all(checks):
                    # You need to do this to get the subreddit I guess
                    submission = authenticate().submission(id=i.id)
                    # Creating the dataset for this song
                    data = datatypes.mattfm_item(
                        song=yt_data,
                        post=datatypes.Post(
                            subreddit=str(submission.subreddit),
                            published=i.created_utc,
                            title=i.title,
                            permalink=i.url
                        )
                    )
                    db_hook.todaySongs.append(data)
                    contnentLinks.append(data.song.yt_id)
                    totalSongs = totalSongs + 1
                    print("We have {} songs now", totalSongs)
                else:
                    continue
            except Exception:
                pass            
                    
    return contnentLinks