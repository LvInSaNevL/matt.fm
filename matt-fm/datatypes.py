from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

@dataclass
class Artist:
    name: str
    yt_id: str

@dataclass
class Song:
    yt_id: str
    # mfm_id: str (not implemented yet)
    published: str
    genre: str
    title: str
    description: str
    # artist: Artist (not implemented yet)
    thumbnail: str
    viewcount: int
    duration: int
  
@dataclass
class Post:
    subreddit: str
    published: str
    title: str
    permalink: str

@dataclass
class mattfm_item:
    song: Song
    post: Post