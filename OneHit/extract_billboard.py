import urllib.request as url
import sqlite3, re, requests, csv, datetime
from bs4 import BeautifulSoup

#Scrapes billboard for song name, artist, last week's position, peak position, and weeks on chart
#Input: date: YYYY-MM-DD
#Output list of list of info stated above
def top100_scraper(date):
    #extract song name
    req = url.urlopen('http://www.billboard.com/charts/hot-100/' + date).read()
    soup = BeautifulSoup(req, "html.parser")
    soup.get_text()
    html_list = []
    for song in soup.find_all('div', {'class': re.compile(r'chart-row__title')}):
        html_list.append(song)
    song_name_list = []
    artist_list = []
    clean_list = []
    for song in html_list:
        #get the song names
        extract_title1 = str(song)[59:]
        extract_title2 = extract_title1.split('</h2>')
        song_name_list.append(extract_title2[0])

        #get the artist names
        extract_title2 = extract_title1.split('\n')
        artist_list.append(extract_title2[2].lstrip().rstrip())

        #check if there is an anchor tag or not for artist name
        if 'href' in extract_title1:
            clean_list.append(True)
        else:
            clean_list.append(False)

    #extract last week rankings
    html_list = []
    for song in soup.find_all('div', {'class': re.compile(r'chart-row__last-week')}):
        html_list.append(song)
    last_week_list = []
    for song in html_list:
        extract_title1 = str(song)[114:]
        extract_title2 = extract_title1[:-14]
        last_week_list.append(extract_title2)

    #extract peak position
    html_list = []
    for song in soup.find_all('div', {'class': re.compile(r'chart-row__top-spot')}):
        html_list.append(song)
    peak_position_list = []
    for song in html_list:
        extract_title1 = str(song)[117:]
        extract_title2 = extract_title1[:-14]
        peak_position_list.append(extract_title2)

    #weeks on charts
    html_list = []
    for song in soup.find_all('div', {'class': re.compile(r'chart-row__weeks-on-chart')}):
        html_list.append(song)
    time_on_chart_list = []
    for song in html_list:
        extract_title1 = str(song)[122:]
        extract_title2 = extract_title1[:-14]
        time_on_chart_list.append(extract_title2)

    #combine final results
    top100_list = []
    for i in range(100):
        top100_list.append([song_name_list[i], artist_list[i], last_week_list[i],
        peak_position_list[i], time_on_chart_list[i], clean_list[i]])
    return top100_list

#extract anchor artist names
def extract_anchor_name(date):
    req = url.urlopen('http://www.billboard.com/charts/hot-100/' + date).read()
    soup = BeautifulSoup(req, "html.parser")
    soup.get_text()
    html_list = []
    for song in soup.find_all('div', {'class': re.compile(r'chart-row__title')}):
        html_list.append(song)
    artist_list = []
    for song in html_list:
        if 'href="http://www.billboard.com/artist/' in str(song):
            extract_song = str(song).split('href="http://www.billboard.com/artist/')
            extract_song = extract_song[1][:-40]
            extract_song = extract_song.split('">')[0]
            artist_list.append(extract_song.split('/')[1].replace("-", " "))
    return artist_list


#create csv file for total, clean, and dirty 
with open ('top100_billboard.csv','w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    with open ('top100_clean.csv', 'w', encoding = 'utf-8') as clean_file:
        clean = csv.writer(clean_file)
        with open ('top100_dirty.csv', 'w', encoding = 'utf-8') as dirty_file:
            dirty = csv.writer(dirty_file)
            
            #pick the date here. I selected March 4, 2017 as the first on
            d = datetime.datetime.strptime("2017-03-04", "%Y-%m-%d")
            date = d.strftime("%Y-%m-%d")
            
            #create row headers for each file
            writer.writerow(['date', 'position', 'songname', 'artist', 'last week', 'peak position', 'weeks on chart'])
            clean.writerow(['date', 'position', 'songname', 'artist', 'last week', 'peak position', 'weeks on chart', 'clean name'])
            dirty.writerow(['date', 'position', 'songname', 'artist', 'last week', 'peak position', 'weeks on chart'])
            duplicates = set()

            for weeks in range (1000):   #number of weeks go here
                data = top100_scraper(str(date))
                clean_data = extract_anchor_name(date)
                #puts in songs from 1 - 100
                j = 0
                for i in range(100):
                    writer.writerow([date, i+1, data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]])

                    #also put it into clean or dirty csv file, depending on what is needed
                    if data[i][5] == True:
                        clean.writerow([date, i+1, data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], clean_data[j]])
                        j = j+1
                    else:
                        if data[i][5] == 'DJ Suede The Remix God':
                            print("WTF")
                        if data[i][1] not in duplicates:
                            dirty.writerow([date, i+1, data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]])
                            duplicates.add(data[i][1])
                            print ('adding', data[i][1])
                        
                #update the date
                d = d - datetime.timedelta(days=7)
                date = d.strftime("%Y-%m-%d")
