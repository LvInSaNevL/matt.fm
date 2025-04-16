# File imports
import utils
# dep imports
import psycopg2
from datetime import datetime

def connection():
    auth = utils.readAuth('db')
    connector = psycopg2.connect(
        database="mattfm",
        user="admin",
        password="password1234",
        host="172.18.0.2",
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

def updateArtist():
    query = """
              INSERT INTO youtube.artists (name, youtube_id)
              VALUES (%(name)s, %(youtube_id)s);
            """
    values = {
        'name': "Test Name3",
        'youtube_id': "kjdu8jSJ2"
    }
    dbInsert(query, values)

def updateSong():
    query = """
              INSERT INTO youtube.song (
                  yt_id, published, genre, title, description, viewcount, duration, artist, thumbnail
              )
              VALUES (
                  %(yt_id)s, %(published)s, %(genre)s, %(title)s, %(description)s, %(viewcount)s, %(duration)s, %(artist)s, %(thumbnail)s
              );
            """ 
    values = {
        "yt_id": "a9ifihas",
        "published": "2025-03-10",
        "genre": "Pop",
        "title": "Never Gonna Let You Go",
        "description": "This is a test description",
        "viewcount": 200,
        "duration": 312,
        "artist": "Test Name2",
        "thumbnail": "https://img.youtube.com/vi/LGbRpdCRwt0/default.jpg"
    }
    dbInsert(query, values)

def addRedditPost():
    query = """
              INSERT INTO social.reddit (
                  post_id, title, subreddit, upvotes, downvotes
              )
              VALUES (
                  %(post_id)s, %(title)s, %(subreddit)s, %(upvotes)s, %(downvotes)s
              )
            """
    values = {
        "post_id": "1j8anhz",
        "title": "Nox Obscura - Through the Dark and in Secret",
        "subreddit": "newmusic",
        "upvotes": 21,
        "downvotes": 9
    }
    dbInsert(query, values)

def updatePost():
    addRedditPost()
    query = """
              INSERT INTO social.post(
                post_id, platform, date_posted, author
              )
              VALUES (
                %(post_id)s, %(platform)s, %(date_posted)s, %(author)s
              )
            """
    values = {
        "post_id": "1j8anhz",
        "platform": "reddit",
        "date_posted": "2025-03-10",
        "author": "HenryRuz16"
    }
    dbInsert(query, values)

def updateDB(dbEntries):
    updatePost()
    # for item in dbEntries:
    #     updateSong()