# File imports
import utils
import youtube
import reddit
import db_hook
# dep imports
import time
from ast import And
from pydoc import cli
from urllib.parse import urlparse

def main():    
    reddit.authenticate()
    newContent = reddit.getPosts(25)
    youtube.remove_from_playlist()
    
    # You need this sleep for YouTube to catch up, it could probably be reduced but this is safe
    data = db_hook.todaySongs
    time.sleep(5)
    
    for c in newContent:
        youtube.add_to_playlist(c)


# Actual start
if __name__ == "__main__":
    main()