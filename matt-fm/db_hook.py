# File imports
from urllib.parse import SplitResult
import db_queries
import utils
# dep imports
import psycopg2
import re
import uuid
from datetime import datetime

todaySongs = []

def connection():
    auth = utils.readAuth('db')
    connector = psycopg2.connect(
        database="mattfm",
        user=auth["username"],
        password=auth["password"],
        host="172.19.0.4",
        port="5432"
    )
    return connector

def dbInsert(query, values):
    dbAuth = connection()
    with dbAuth:
        with dbAuth.cursor() as dbAuth_cursor:
            try: 
                dbAuth_cursor.execute(query, values)
                dbAuth.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error) 
        dbAuth_cursor.close()
                
def addArtist(data):
    values = {
        'name': data.name,
        'youtube_id': data.yt_id
    }
    dbInsert(db_queries.addArtist, values)

# This gets its own db query because we need return values
def addSong(data):
    query = "SELECT EXISTS(SELECT 1 FROM youtube.song WHERE yt_id = '%s');"
    value = data.yt_id
    dbAuth = connection()
    with dbAuth:
        with dbAuth.cursor() as dbAuth_cursor:
            try:
                dbAuth_cursor.execute(query, value)
                doesExist = dbAuth_cursor.fetchone()
                if doesExist:
                    updateSong(data)
                else:
                    addNewSong(data)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error) 

def updateSong(data):
    values = (
        datetime.today().strftime('%Y-%m-%d'),
        data.yt_id
    )
    dbInsert(db_queries.updateSong, values)

def addNewSong(data):    
    print("adding song " + data.title)
    # Formatting the Wikipedia URLs
    regex = re.findall(r'^https?\:\/\/([\w\.]+)wikipedia.org\/wiki\/([\w]+\_?)', data.genre)
    clean_genre = regex[-1]

    values = {
        'mattfm_id': utils.genUUID(),
        'yt_id': data.yt_id,
        'published': data.published,
        'dates_posted': (datetime.today().strftime('%Y-%m-%d'),),
        'genre': clean_genre,
        'title': data.title,
        'artist': data.artist.yt_id,
        'description': data.description,
        'viewcount': data.viewcount,
        'duration': data.duration,
        'thumbnail': data.thumbnail
    }
    dbInsert(db_queries.addSong, values)
 
def addRedditPost(data):
    values = {
                'subreddit': data.subreddit,
                'date_posted': datetime.utcfromtimestamp(data.published).strftime('%Y-%m-%d'),
                'title': data.title,
                'permalink': data.permalink,
                'upvotes': data.ups,
                'downvotes': data.downs
            }
    dbInsert(db_queries.addPost, values)

def createMattFMItem(data):
    values = {
                'date': datetime.today().strftime('%Y-%m-%d'),
                'yt_id': data.song.yt_id,
                'playlist_id': utils.genUUID(),
                'r_post': data.post.permalink
            }
    dbInsert(db_queries.mattfmItem, values)

def updateDB():
    for i in todaySongs:
        print("Adding {0} to the database".format(i.song.title))
        addArtist(i.song.artist)
        addSong(i.song)
        addRedditPost(i.post)
        # createMattFMItem(i)