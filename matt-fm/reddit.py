# File imports
import utils
import youtube
# dep imports
import json
import praw
import re

youtubeURLs = ["www.youtube.com",   
               "youtube.com",
               "youtu.be"]

contnentLinks = []

def getPosts():    
    utils.logPrint("Retreiving music", 0)

    with open("auth.json") as jsonfile:
            auth = json.load(jsonfile)

    redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                        client_secret=auth['reddit']['client_secret'],
                        user_agent=auth['reddit']['user_agent'],
                        username=auth['reddit']['username'],                     
                        password=auth['reddit']['password'])

    regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    for i in redditAuth.multireddit('matt-fm', 'music').hot(limit=250):
        if len(contnentLinks) < 100:
            try:
                result = re.search(regex, i.url)
                checks = (i.url not in youtubeURLs,
                        result.group() not in contnentLinks,
                        youtube.check_video_exist(result.group())
                        )
                
                if all(checks):
                    contnentLinks.append(result.group())
            finally:
                continue
            
    return contnentLinks