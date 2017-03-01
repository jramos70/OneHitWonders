from bs4 import BeautifulSoup
import urllib.request as url
import sqlite3, re, requests, csv, arrow
import datetime

#Scrapes billboard for song name, artist, last week's position, peak position, and weeks on chart
#Input: date: YYYY-MM-DD
#Output list of list of info stated above
def top100_scraper(date):
    #extract song name
    r = url.urlopen('http://www.billboard.com/charts/hot-100/' + date).read()
    soup = BeautifulSoup(r, "html.parser")
    soup.get_text()
    html_list = []
    for song in soup.find_all('div', {'class': re.compile(r'chart-row__title')}):
        html_list.append(song)
    song_name_list = []
    artist_list = []
    for song in html_list:
        #get the song names
        extract_title1 = str(song)[59:]
        extract_title2 = extract_title1.split('</h2>')
        song_name_list.append(extract_title2[0])
    
        #get the artist names
        extract_artist1 = str(song)[59:]
        extract_title2 = extract_title1.split('\n')
        artist_list.append(extract_title2[2].lstrip().rstrip())

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
         top100_list.append([song_name_list[i], artist_list[i], last_week_list[i], peak_position_list[i],time_on_chart_list[i]])
    return top100_list

#create csv file
with open ('top100_billboard.csv','w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    #pick the date here. I selected March 4, 2017 as the first on
    d = datetime.datetime.strptime("2017-03-04", "%Y-%m-%d")
    date = d.strftime("%Y-%m-%d")
    writer.writerow(['date', 'position', 'songname', 'artist', 'last week', 'peak position', 'weeks on chart'])
    for weeks in range (62):   #number of weeks go here
        data = top100_scraper(str(date))
        #puts in songs from 1 - 100
        for i in range(100):
                writer.writerow([date, i+1, data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]])
        #update the date
        d = d - datetime.timedelta(days=7)
        date = d.strftime("%Y-%m-%d")
