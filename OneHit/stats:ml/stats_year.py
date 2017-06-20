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
matrix = [0 for i in range(18)]
old = None
col_ind = 0
colors = ['r', 'y', 'g','c', 'b', 'm']
colors = ['#F57C00', '#F9A825', '#FFEB3B','#E0E0E0', '#9E9E9E', '#616161',]
for genre in genre_list:
    hits = {}
    start = [0 for i in range(18)]
    end  = [0 for i in range(18)]
    with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:

        reader = csv.reader(file_reader)
        for row in reader:
            if row[8].lower() == 'true' and row[7].lower() == genre:
                year = row[0].split("/")[2]
                if year == '99':
                    break
                if year[0] == '0':
                    year = year[:-1]
                if (row[2], row[3]) not in hits:
                    hits[(row[2], row[3])] = [(row[1], year)]
                else:
                    hits[(row[2], row[3])].insert(0, (row[1], year))
        for song in hits:
            month_start = hits[song][0][1]
            month_end = hits[song][len(hits[song]) - 1][1]
            start[int(month_start)] += 1
            end[int(month_end)] += 1
        if len(hits) >= 30:
            legend.append(genre)
            if old == None:
                pyplot.bar(range(18), start[:], color = colors[col_ind])
                
            else:
                pyplot.bar(range(18), start[:], bottom = old[:], color = colors[col_ind])
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

pyplot.bar(range(18), matrix[:], bottom = old[:], color = colors[col_ind])
pyplot.legend(legend + ['Other'], loc='upper right')
# pyplot.xticks(range(18), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
pyplot.xlabel('month')
pyplot.ylabel('# of one hit wonders')
pyplot.suptitle('Number of One Hit Wonders per Month', fontsize=20)

pyplot.show()
