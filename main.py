import youtube
import utils
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
    utils.logPrint("Retreiving music", 0)

    with open("auth.json") as jsonfile:
            auth = json.load(jsonfile)

    redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                        client_secret=auth['reddit']['client_secret'],
                        user_agent=auth['reddit']['user_agent'],
                        username=auth['reddit']['username'],                     
                        password=auth['reddit']['password'])

    regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    for i in redditAuth.multireddit('lv_insane_vl', 'music').hot(limit=250):
        if len(contnentLinks) <= 10:
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


    # youtube.remove_from_playlist()

    for t in contnentLinks:
        youtube.add_to_playlist(t)


# Actual start
if __name__ == "__main__":
    main()