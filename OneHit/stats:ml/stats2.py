import csv
from matplotlib import pyplot, dates
import numpy as np

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
genre_list.reverse()
y_pos = [0 for i in range(len(genre_list))]
iterator = 0
for genre in genre_list:
    with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:
        reader = csv.reader(file_reader)
        hits = {}
        for row in reader:
            if row[8].lower() == 'true' and row[7].lower() == genre:
                if (row[2], row[3]) not in hits:
                    hits[(row[2], row[3])] = [row[1]]
                else:
                    hits[(row[2], row[3])].insert(0, row[1])
        if len(hits) == 0:
            genre_list.remove(genre)
            y_pos = y_pos[:-1]
            continue
        matrix = [0 for i in range(100)]
        for song in hits:
            print (song[0], song[1])
            x = len(hits[song])
            matrix[x] += 1
            y_pos[iterator] += 1
    
    print(genre)
    for i in range(10):
        if i == 0:
            print (matrix[1:11])
        elif i == 9:
            print (matrix[91:101])
        else:
            print(matrix[i*10+1:i*10+11])
    print()
    # pyplot.plot(range(100), matrix)
    # pyplot.plot()
    # pyplot.gca().invert_yaxis()
    # pyplot.xticks(y_pos, tuple(genre_list))
    iterator += 1
#pyplot.rcdefaults()
genre_list2 = np.arange(len(genre_list))
# print(genre_list2)
# genre_list2 = np.array(genre_list)
# genre_list2 = genre_list2[::-1]
pyplot.bar(genre_list2, y_pos, align='center', alpha=0.5)
#pyplot.bar(genre_list, y, width, color="blue")
pyplot.ylabel('# of one-hit wonders')
pyplot.title('genre') 
pyplot.xticks(genre_list2, genre_list, rotation='vertical')
print(y_pos)
pyplot.show()

