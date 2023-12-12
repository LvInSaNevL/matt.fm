import requests
import json

videoID = "A_XFk05rrqQ"
# Request to check if it is available on YT Music since there is no official way
# Free API access that doesn't effect our quota so this is nice to use
try:
    headers = {'Accept-Encoding': 'identity'}
    url = "https://yt.lemnoslife.com/videos?part=music&id=" + videoID
    request = requests.get(url=url)
    isMusic = json.loads(request.text)        
    if isMusic['items'][0]['music']['available']:
        print("True")
    else:
        print("False")
except Exception as e:
    print(e)
    pass  