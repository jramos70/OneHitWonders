import requests
import time

def genre(artist,song):
    api_key = 'b45db8136c5b56cfa6aa2b77fe6c3a61'
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist='
    artstr = '+'.join(artist.lower().split())
    songstr = '+'.join(song.lower().split())
    url += artstr + '&track=' + songstr + '&api_key=' + api_key + '&format=json'
    j = requests.get(url).json()
    time.sleep(0.3)
    return j['toptags']['tag'][0]['name']

print genre('Ed Sheeran','Shape Of You')
