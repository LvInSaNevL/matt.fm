# File imports
import utils
import youtube
import db_hook
import datatypes
# dep imports
import time
import praw
import re

last_call = 0
contnentLinks = []

### <summary>
# As of July 2023 Reddit started to rate limit their API, so we needed a helper function in order
# to keep them from shutting off our API. Only allows MFM to hit the API every 3 seconds 
# <returns> A PRAW Reddit authentication object, `redditAuth`
### </summary>
def authenticate():
    # Makes sure its been at least 3sec since we last used the API
    global last_call
    while time.time() - last_call < 3:
      time.sleep(1)
    last_call = time.time()

    # Reads credentials from `auth.json`
    utils.logPrint("Authenticating Reddit service access and refresh token", 0)
    auth = utils.readAuth('reddit')
    redditAuth = praw.Reddit(client_id=auth['client_id'],
                        client_secret=auth['client_secret'],
                        user_agent=auth['user_agent'],
                        username=auth['username'],                     
                        password=auth['password'])
    
    return redditAuth

### <summary>
# This is honestly the main loop of MFM. Its primary role is to crawl the multireddit for music
# but it also needs to hit the YT API to make sure it's a real song, so I just get all the song
# data at that point as well. 
# <param name=count> (int) The number of songs we want in the playlist
# <returns> `contentLinks`, which is a list of IDs, we probably don't actually need to do this
### </summary>
def getPosts(count):    
    utils.logPrint("Retreiving music", 0)

    # This matches against the various YT URLs, so we can get the video ID
    regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    creds = authenticate()
    for i in creds.multireddit('matt-fm', 'music').hot(limit=250):
        if len(db_hook.todaySongs) < count:
            # This entire code block is in a try/except loop is because sometimes when the regex
            # matches against a non-YT URL the program will crash
            try: 
                # Checks to see if song is has been seen already
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