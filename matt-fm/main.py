# File imports
import reddit
import db_hook
import youtube
# dep imports
from ast import And
import time
from pydoc import cli
from urllib.parse import urlparse

def main():    
    reddit.authenticate()
    reddit.getPosts(10)

    youtube.remove_from_playlist()
    
    # You need this sleep for YouTube to catch up, it could probably be reduced but this is safe
    data = db_hook.todaySongs
    time.sleep(5)
    
    for c in data:
        print(c)
        youtube.add_to_playlist(c.song.yt_id)

    db_hook.updateDB()


# Actual start
if __name__ == "__main__":
    main()