# File imports
import utils
import youtube
import db_hook
import datatypes
# dep imports
import time
import praw
import re

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
    auth = utils.readAuth('reddit')
    redditAuth = praw.Reddit(client_id=auth['client_id'],
                        client_secret=auth['client_secret'],
                        user_agent=auth['user_agent'],
                        username=auth['username'],                     
                        password=auth['password'])
    
    return redditAuth

def getPosts(count):    
    global totalSongs
    utils.logPrint("Retreiving music", 0)

    regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    creds = authenticate()
    for i in creds.multireddit('matt-fm', 'music').hot(limit=250):
        if len(db_hook.todaySongs) < count:
            try: 
                result = re.search(regex, i.url)
                if result.group() in contnentLinks:
                    continue
                             
                # You need to do this to get the subreddit I guess
                submission = authenticate().submission(id=i.id)

                # Just an extra check to get rid of anything not available on YT Music
                ytData = youtube.get_video_info(result.group())
                if ytData is None: continue

                # Creating the dataset for this song
                data = datatypes.mattfm_item(
                    song=ytData,
                    post=datatypes.Post(
                        subreddit=str(submission.subreddit),
                        published=i.created_utc,
                        title=i.title,
                        permalink=i.id,
                        ups=i.ups,
                        downs=i.downs
                    )
                )
                db_hook.todaySongs.append(data)
                contnentLinks.append(data.song.yt_id)
                print("We have {} songs now", len(db_hook.todaySongs))
                
            except Exception as e:
                print(e)
                pass            
                    
    return contnentLinks