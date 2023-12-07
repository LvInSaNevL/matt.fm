# File imports
from urllib.parse import SplitResult
import datatypes
# dep imports
import psycopg2
import random
import re
from datetime import datetime

todaySongs = []

def connection():
    connector = psycopg2.connect(
        database="mattfm",
        user="postgres",
        password="postgres",
        host="172.19.0.4",
        port="5432"
    )
    return connector

def addArtist(data):
    dbAuth = connection()
    with dbAuth:
        with dbAuth.cursor() as dbAuth_cursor:
            try:
                dbAuth_cursor.execute("""
                    INSERT INTO youtube.artists (name, youtube_id) 
                    VALUES ('{0}', '{1}');
                """.format(data.name, data.yt_id))
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

def addSong(data):
    dbAuth = connection()
    with dbAuth:
        with dbAuth.cursor() as dbAuth_cursor:
            try:
                insert_query = """
                    WITH ins_artist AS (
                        SELECT * FROM youtube.artists WHERE youtube_id = %s
                    )
                    INSERT INTO youtube.song (
                        yt_id, published, genre, title, artist, description, viewcount, duration, thumbnail
                    )
                    SELECT %s, %s, %s, %s, ins_artist.youtube_id, %s, %s, %s, %s FROM ins_artist;
                """
                # Formatting the Wikipedia URLs
                regex = re.findall(r'^https?\:\/\/([\w\.]+)wikipedia.org\/wiki\/([\w]+\_?)', data.genre)
                clean_genre = regex[-1]

                # Using the execute method with a tuple of values
                values = (
                    data.artist.yt_id, 
                    data.yt_id, 
                    data.published, 
                    clean_genre, 
                    data.title, 
                    data.description, 
                    data.viewcount, 
                    data.duration, 
                    data.thumbnail
                )

                dbAuth_cursor.execute(insert_query, values)
                dbAuth.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)  

def addRedditPost(data):
    dbAuth = connection()
    with dbAuth:
        with dbAuth.cursor() as dbAuth_cursor:
            try:
                insert_query = """
                    INSERT INTO reddit.post (
                        subreddit, date_posted, title, permalink, upvotes, downvotes
                    )
                    SELECT %s, %s, %s, %s, %s, %s;
                """

                values = (
                    data.subreddit,
                    datetime.fromtimestamp(data.published).strftime('%Y-%m-%d'),
                    data.title,
                    data.permalink,
                    data.upvotes,
                    data.downvotes
                )
                dbAuth_cursor.execute(insert_query, values)
                dbAuth.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

def createMattFMItem(data):
    dbAuth = connection()
    with dbAuth:
        with dbAuth.cursor() as dbAuth_cursor:
            try:
                insert_query = """
                    INSERT INTO mattfm.playlist_item(
                        date, yt_id, playlist_id, r_post
                    )
                    SELECT %s, %s, %s, %s;
                """

                values = (
                    datetime.today().strftime('%Y-%m-%d'),
                    data.song.yt_id,
                    data.playlist_id,
                    data.post.permalink
                )

                dbAuth_cursor.execute(insert_query, values)
                dbAuth.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)      

def updateDB():
    dbAuth = connection()
    for i in todaySongs:
        print("Adding {0} to the database".format(i.song.title))
        addArtist(i.song.artist)
        addSong(i.song)
        addRedditPost(i.post)
        createMattFMItem(i)