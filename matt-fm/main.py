# File imports
import reddit
import db_hook
import youtube
# dep imports
import time

def main():    
    # Getting reddit data
    reddit.authenticate()
    reddit.getPosts(10)

    # Cleaning out the existing playlists
    youtube.remove_from_playlist()
    
    # You need this sleep for YouTube to catch up, it could probably be reduced but this is safe
    data = db_hook.todaySongs
    time.sleep(5)
    
    # Adding songs to the YT playlist
    for c in data:
        print(c)
        youtube.add_to_playlist(c.song.yt_id)

    # Adding songs to the YT database
    db_hook.updateDB()


# Actual start
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Matt.FM execution took {} seconds".format(int((time.time() - start_time))))