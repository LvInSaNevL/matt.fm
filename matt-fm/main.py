# File Imports
import utils
import reddit
import datatypes
import youtube
import dbhook
# Dep imports
import time
from datetime import date
import json
from dataclasses import dataclass, asdict

todayDB = []

def main():
    # Getting reddit data
    utils.logPrint("Getting Reddit data", 0)
    reddit_data = reddit.get_posts(25)

    # Clearing yesterdays playlist
    utils.logPrint("Clearing YT playlist", 0)
    youtube.clear_playlist()

    # Getting YT data and (if possible) upload the video to the playlist
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

    # Write data out for debugging
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    filename = "data_export_{}.json".format(formatted_date)
    with open(filename, 'w') as f:
        json.dump([asdict(item) for item in todayDB], f, indent=4)

    
    print("Matt.FM execution is done")

# Actual program start
if __name__ == "__main__":
    start_time = time.time()
    main()
    utils.logPrint("Matt.FM execution took {} seconds".format(int((time.time() - start_time))), 0)