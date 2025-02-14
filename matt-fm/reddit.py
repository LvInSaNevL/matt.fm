# File Imports
import utils
import datatypes
import youtube
# Dep Imports
import time
import datetime
import praw
import re

'''
<summary>
Generates an OAuth token to access Reddit. 
<returns> A PRAW Reddit authentication object, `redditAuth`
'''
last_call = 0
def _authenticate():
    '''
    <summary>

    Generates an OAuth token to access Reddit. Reddit has a pretty strict timeout policy
    though so we have to rate limit outselves. 

    <returns> 

    A PRAW Reddit authentication object, `redditAuth`
    '''
    global last_call
    while time.time() - last_call < 3:
      time.sleep(1)
    last_call = time.time()

    # Reads credentials from `auth.json`
    utils.logPrint("Authenticating Reddit service access and refresh token", 0)
    auth = utils.readAuth('reddit')
    redditAuth = praw.Reddit(client_id=auth['client_id'],
                        client_secret=auth['client_secret'],
                        user_agent=auth['user_agent'],
                        username=auth['username'],                     
                        password=auth['password'])
    print(redditAuth.user.me())
    return redditAuth

def get_posts(number=1):
    '''
    <summary>

    Gets the top posts from the reddit Multireddit that we have set up. 

    <parameters>
    number: int
        How many posts you want returned. Default is 1. 
    '''
    posts = []
    auth = _authenticate()
    # Matches against all YT URLs, including shortened ones or ones with tracking
    yt_regex = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"

    all_posts = auth.multireddit('matt-fm', 'music').hot(limit=250)
    post_iterator = 0
    while (len(posts) < number):
        current_post = next(all_posts)
        '''
        This entire code block is in a try/catch because sometimes when the regex
        matches against a non-YT URL the program crashes. 
        No idea why, but I think it has to do with my regex matching
        '''
        try: 
            result = re.search(yt_regex, current_post.url)
            if (not youtube.playability(result.group())):
                utils.logPrint(f"Video {result.group()} is not available on YouTube Music", 2)
                continue
            if (result.group() in posts):
                continue
            else:
                utils.logPrint(f"Adding post {current_post.id} to the return list", 1)
                newPost = datatypes.Post(
                        subreddit = current_post.subreddit_name_prefixed,
                        published = datetime.datetime.fromtimestamp(current_post.created).strftime('%Y-%m-%d'),
                        title = current_post.title,
                        permalink = current_post.id,
                        ups = current_post.ups,
                        downs = int(current_post.ups * current_post.upvote_ratio),
                        yt_id = result.group()
                )
                posts.append(newPost)
        except AttributeError:
            utils.logPrint(f"Post {current_post.id} is not a youtube post", 2)
            continue
        except Exception as e:
            utils.logPrint(f"Fatal Error: {e}", 4)

        post_iterator += 1

    return posts