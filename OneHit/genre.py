import requests
import time

def genre(artist,song):
    api_key = 'b45db8136c5b56cfa6aa2b77fe6c3a61'
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist='
    artstr = '+'.join(artist.lower().split())
    songstr = '+'.join(song.lower().split())
    url += artstr + '&track=' + songstr + '&autocorrect=1' \
        + '&api_key=' + api_key + '&format=json'
    j = requests.get(url).json()
    time.sleep(0.3)
    if ('toptags' not in j) or (len(j['toptags']['tag']) == 0):
        return spotify_genre(artstr)
    return j['toptags']['tag'][0]['name']

def spotify_genre(artist):
    url = 'https://api.spotify.com/v1/search?q=' + artist + '&type=artist'
    j = requests.get(url).json()
    if len(j['artists']['items']) == 0:
        return 'NULL'
    if len(j['artists']['items'][0]['genres']) == 0:
        return 'NULL'
    return j['artists']['items'][0]['genres'][0]

print genre('zayn','I Don\'t Wanna Live Forever (Fifty Shades Darker)')
