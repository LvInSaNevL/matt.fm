# File Imports
import utils
import reddit
import datatypes
import youtube
# Dep imports
import time

todayDB = []

def main():
    # Getting reddit data
    utils.logPrint("Getting Reddit data", 0)
    reddit_data = reddit.get_posts(5)

    utils.logPrint("Clearing YT playlist", 0)
    youtube.clear_playlist()

    utils.logPrint("Getting YouTube data", 0)
    for r in reddit_data:
        yt_data = youtube.get_video(r.yt_id)
        if (yt_data is not None):
            youtube.add_video(r.yt_id)
            todayDB.append(datatypes.mattfm_item(
                mfm_id = utils.genUUID(),
                song = yt_data,
                post = r
            ))

# Actual program start
if __name__ == "__main__":
    start_time = time.time()
    main()
    utils.logPrint("Matt.FM execution took {} seconds".format(int((time.time() - start_time))), 0)