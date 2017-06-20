import csv
from matplotlib import pyplot, dates

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
Emo
Crunk
Hollywood
Disco
'''
genre_list = list(map(lambda x: x.strip().lower(), genre_list_raw.split()))
genre_list.sort(key=len)
# genre_list.reverse()
legend = []
matrix = [0 for i in range(16)]
old = None
col_ind = 0
colors = ['r', 'y', 'g','c', 'b', 'm']
# colors = ['#F57C00', '#F9A825', '#FFEB3B','#E0E0E0', '#9E9E9E', '#616161',]
for genre in genre_list:
    hits = {}
    start = [0 for i in range(16)]
    end  = [0 for i in range(16)]
    with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:

        reader = csv.reader(file_reader)
        for row in reader:
            if row[7].lower() == genre:
                year = row[0].split("/")[2]
                if year == '99' or year == '98' or year == '97' or year == '16' or year == '17':
                    continue
                if year[0] == '0':
                    year = year[-1]
                if (row[2], row[3]) not in hits:
                    hits[(row[2], row[3])] = [(row[1], year)]
                else:
                    hits[(row[2], row[3])].insert(0, (row[1], year))
        for song in hits:
            dates = hits[song]
            begin = hits[song][0][1]
            for i in dates:
                if int(i[0]) > 40:
                    continue
            start[int(begin)] += 1

        if len(hits) >= 500:
            legend.append(genre)
            print (genre, len(hits), start)
            if old == None:
                pyplot.bar(range(16), start[:], color = colors[col_ind])
                
            else:
                pyplot.bar(range(16), start[:], bottom = old[:], color = colors[col_ind])
            if old is None:
                old = start
            else:
                for k in range(len(start)):
                    old[k] += start[k]
            col_ind += 1
        else:
            for j in range(len(start)):
                # print (j)
                matrix[j] += start[j]

pyplot.bar(range(16), matrix[:], bottom = old[:], color = colors[col_ind])
print ("other, ", matrix)
pyplot.legend(legend + ['Other'], loc='upper right')
pyplot.xticks(range(16), [str(i) for i in range (2000, 2016)])
pyplot.xlabel('year')
pyplot.ylabel('# of wonders')
pyplot.suptitle('Number of All Wonders per Year', fontsize=20)

pyplot.show()
