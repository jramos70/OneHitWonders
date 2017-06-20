import csv
import editdistance
import re

hits = {}
one_hit_checker = {}
month_dict= {'Jan': 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
with open ('oneWiki.csv', 'r', encoding = 'latin1') as r:
    reader = csv.reader(r)
    next(reader, None)
    for row in reader:
        song = row[1]
        song = song.replace("(Remix)", "")
        song = song[1:-1]
        peak = row[2]
        date = row[3].split("-")
        month = str(month_dict[date[1]])
        day = date[0]
        year = row[4][2:]
        hits[(peak, month, day, year)] = song

with open('top100_billboard.csv', 'r', encoding = 'utf-8') as r:
    reader = csv.reader(r)
    next(reader, None)
    for row in reader:
        peak = row[5]
        song = row[2]
        date = row[0].split("/")
        month = date[0]
        day = date[1]
        year = date[2]
        check = (peak, month, day, year)
        if check in hits:
            edit_distance = editdistance.eval(song, hits[check])
            if edit_distance <= 5:
                one_hit_checker[(song, row[3])] = "True"

with open ('one_hit_wonder.csv','w', encoding = 'utf-8') as f:
    with open('top100_billboard.csv', 'r', encoding = 'utf-8') as r:
        writer = csv.writer(f)
        reader = csv.reader(r)
        next(reader, None)
        writer.writerow(['date', 'position', 'songname', 'artist', 'last week', 'peak position', 'weeks on chart', 'genre', 'isOneHit'])
        for row in reader:
            isOneHit = "False"
            peak = row[5]
            date = row[0].split("/")
            month = date[0]
            day = date[1]
            year = date[2]
            check = (peak, month, day, year)
            
            if ((row[2], row[3]) in one_hit_checker):
                isOneHit = "True"
                
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], isOneHit])

        



        
