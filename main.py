# File imports
import youtube
import reddit
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
    youtube.remove_from_playlist()
    newContent = reddit.getPosts()
    # print(len(newContent))
    
    # # You need this sleep for YouTube to catch up, it could probably be reduced but this is safe
    # time.sleep(5)
    
    # # for c in newContent:
    # #     youtube.add_to_playlist(c)


# Actual start
if __name__ == "__main__":
    main()