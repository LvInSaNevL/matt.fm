import youtube
from ast import And
from pydoc import cli
import praw
import json
from urllib.parse import urlparse
import re

youtubeURLs = ["www.youtube.com",   
               "youtube.com",
               "youtu.be"]

contnentLinks = []

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
                if youtube.check_video_exist and not (i.url in contnentLinks):
                    contnentLinks.append(result.group())
            except:
                pass

    youtube.remove_from_playlist()

    for t in contnentLinks:
        youtube.add_to_playlist(t)


# Actual start
if __name__ == "__main__":
    main()