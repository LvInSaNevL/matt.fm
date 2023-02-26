# File imports
import youtube
import reddit
import database
# dep imports
import utils
import time
from ast import And
from pydoc import cli
import platform
import praw
import json
from urllib.parse import urlparse

def main():    
    newContent = reddit.getPosts()
    youtube.remove_from_playlist()
    
    # You need this sleep for YouTube to catch up, it could probably be reduced but this is safe
    data = database.todaySongs
    time.sleep(5)
    
    for c in newContent:
        youtube.add_to_playlist(c)


# Actual start
if __name__ == "__main__":
    main()