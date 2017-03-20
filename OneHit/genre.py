import requests
import time

genre_list_raw = '''
Jazz
Hip-hop
Rap
Blues
R&B
Rock
Folk
Pop
Electronic
Classical
Punk
Country
Alternative
Metal
Dubstep
Techno
Reggae
Instrumental
K-pop
Emo
Crunk
Raggaeton
'''

genre_list = list(map(lambda x: x.strip().lower(), genre_list_raw.split()))

def genre(artist, song, genre_list):
    api_key = 'b45db8136c5b56cfa6aa2b77fe6c3a61'
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist='
    artstr = '+'.join(artist.lower().split())
    songstr = '+'.join(song.lower().split())
    url += artstr + '&track=' + songstr + '&autocorrect=1' \
        + '&api_key=' + api_key + '&format=json'
    j = requests.get(url).json()
    time.sleep(0.3)
    if ('toptags' not in j) or (len(j['toptags']['tag']) == 0):
        return spotify_genre(artstr, genre_list)
    for tag in map(lambda x: x['name'].lower(), j['toptags']['tag']):
        for genre in genre_list:
            if genre in tag:
                return genre
    return spotify_genre(artstr, genre_list)

def spotify_genre(artist, genre_list):
    url = 'https://api.spotify.com/v1/search?q=' + artist + '&type=artist'
    j = requests.get(url).json()
    if len(j['artists']['items']) == 0:
        return 'NULL'
    if len(j['artists']['items'][0]['genres']) == 0:
        return 'NULL'
    for tag in map(lambda x: x.lower(), j['artists']['items'][0]['genres']):
        for genre in genre_list:
            if genre in tag:
                return genre
    return 'NULL'

print(genre('Ed Sheeran','Shape Of You', genre_list)) #pop
print(genre('Migos','Bad and Boujee', genre_list)) #rap
print(genre('Marian Hill','Down', genre_list)) #electronic
print(genre('Keith Urban','The Fighter', genre_list)) #country
