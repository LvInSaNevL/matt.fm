# File imports
import utils
import youtube
# dep imports
import json
import time
import praw
import re

youtubeURLs = ["www.youtube.com",   
               "youtube.com",
               "youtu.be"]
credentials = None
last_call = 0
contnentLinks = []

def authenticate():
    global last_call
    global credentials
    
    now_time = time.time()

    if (now_time - last_call > 3):
        with open("auth.json") as jsonfile:
            auth = json.load(jsonfile)
        redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                            client_secret=auth['reddit']['client_secret'],
                            user_agent=auth['reddit']['user_agent'],
                            username=auth['reddit']['username'],                     
                            password=auth['reddit']['password'])
        credentials = redditAuth
        last_call = time.localtime()
    else:
        time.sleep(2)
        authenticate()

def getPosts(count):    
    utils.logPrint("Retreiving music", 0)

    regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    for i in credentials.multireddit('matt-fm', 'music').hot(limit=250):
        if len(contnentLinks) < count:
            result = re.search(regex, i.url)
            checks = (i.url not in youtubeURLs,
                        result.group() not in contnentLinks,
                        youtube.check_video_exist(result.group())                       
                    )
            
            if all(checks):
                contnentLinks.append(result.group())
            else:
                continue
            
    return contnentLinks