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
matrix = [0 for i in range(13)]
total = [0 for i in range(13)]
genre_perc = {}
old = None
col_ind = 0
colors = ['r', 'y', 'g','c', 'b', 'm']
# colors = ['#F57C00', '#F9A825', '#FFEB3B','#E0E0E0', '#9E9E9E', '#616161',]
for genre in genre_list:
    hits = {}
    start = [0 for i in range(13)]
    end  = [0 for i in range(13)]
    with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:

        reader = csv.reader(file_reader)
        for row in reader:
            if row[7].lower() == genre:
                month = row[0].split("/")[0]
                if (row[2], row[3]) not in hits:
                    hits[(row[2], row[3])] = [(row[1], month)]
                else:
                    hits[(row[2], row[3])].insert(0, (row[1], month))
        for song in hits:
            month_start = hits[song][0][1]
            month_end = hits[song][len(hits[song]) - 1][1]
            start[int(month_start)] += 1
            end[int(month_end)] += 1
            total[int(month_start)] += 1
        genre_perc[genre] = start
        # if genre == 'rap':
        #     print (start, genre_perc['rap'])
        # if genre == 'rap':
        #     print (start)
        if len(hits) >= 500:
            legend.append(genre)
            if old == None:
                pyplot.bar(range(12), start[1:], color = colors[col_ind])
                
            else:
                pyplot.bar(range(12), start[1:], bottom = old[1:], color = colors[col_ind])
            if old is None:
                old = start
            else:
                for k in range(len(start)):
                    old[k] += start[k]
            col_ind += 1
        else:
            for j in range(len(start)):
                matrix[j] += start[j]
genre_perc['rap'] = [0, 58, 70, 66, 54, 52, 42, 60, 61, 52, 63, 65, 75]
for j in genre_perc:
    if j in legend:
        genre = genre_perc[j]
        ret = []
        for i in range(1,len(genre)):
            ret.append((float(genre[i])/float(total[i])))
        print (j, ["%.4f" % a for a in ret])
other = [0 for i in range(13)]
for genre in genre_perc:
    if genre not in legend:
        for i in range(1,13):
            other[i] += float(genre_perc[genre][i])/float(total[i])
print('other', ["%.4f" % a for a in other[1:]])

# print(months[1:])
# print(sum(months[1:])/12)
# quarter = [sum(months[1:4]), sum(months[4:7]), sum(months[7:10]), sum(months[10:12])]
# pyplot.plot(range(12), start[1:])
# pyplot.plot(range(12), end[1:])
pyplot.bar(range(12), matrix[1:], bottom = old[1:], color = colors[col_ind])
pyplot.legend(legend + ['Other'], loc='upper left', prop={'size':10})
pyplot.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# pyplot.plot(range(1,13), months[1:])
# pyplot.gca().invert_yaxis()
pyplot.xlabel('month')
pyplot.ylabel('# of wonders')
pyplot.suptitle('Number of All Wonders per Month', fontsize=20)
print ("total", total)

# pyplot.show()
