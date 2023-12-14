# Creates a new entry in the youtube.artists table
addArtist = """
              INSERT INTO youtube.artists (name, youtube_id)
              VALUES (%(name)s, %(youtube_id)s);
            """

# Updates the date[] for existing songs
updateSong = """
               UPDATE youtube.song 
               SET dates_posted = ARRAY_APPEND(dates_posted, %(yt_id)s);
             """

# Adds a new song item to the youtube.song table
addSong = """
            INSERT INTO youtube.song (
                mattfm_id, yt_id, published, dates_posted, genre, title, artist, description, viewcount, duration, thumbnail
            )
            VALUES (
                %(mattfm_id)s, %(yt_id)s, %(published)s, ARRAY[%(dates_posted)s]::date, %(genre)s, %(title)s, %(artist)s, %(description)s, %(viewcount)s, %(duration)s, %(thumbnail)s
            );
          """ 

# Adds a new post item to the reddit.post table
addPost = """
            INSERT INTO reddit.post (
                subreddit, date_posted, title, permalink, upvotes, downvotes
            )
            VALUES (%(subreddit)s, %(date_posted)s, %(title)s, %(permalink)s, %(upvotes)s, %(downvotes)s);
          """

# Creates the parent Matt.FM item
mattfmItem = """
              INSERT INTO mattfm.playlist_item(
                  date, yt_id, playlist_id, r_post
              )
              VALUES (%(date)s, %(yt_id)s, %(playlist_id)s, %(r_post)s);
            """