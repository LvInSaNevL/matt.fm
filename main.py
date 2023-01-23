# File imports
# import youtube
import reddit
# dep imports
import utils
from ast import And
from pydoc import cli
import platform
import praw
import json
from urllib.parse import urlparse

def main():
    content = reddit.getPosts()
    print(len(content))
    # # youtube.remove_from_playlist()

    # for t in contnentLinks:
    #     youtube.add_to_playlist(t)


# Actual start
if __name__ == "__main__":
    main()