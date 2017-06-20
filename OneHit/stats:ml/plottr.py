from matplotlib import pyplot, dates
import csv

with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:
    reader = csv.reader(file_reader)
    hits = {}
    for row in reader:
        if row[8].lower() == 'true':
            if (row[2], row[3]) not in hits:
                hits[(row[2], row[3])] = [row[1]]
            else:
                hits[(row[2], row[3])].insert(0, row[1])
    x = 0
    for song in hits:
        end = 0
        inside = False
        for i in range(len(hits[song])):
            if int(hits[song][i]) <= 40:
                inside = True
            if int(hits[song][i]) > 40 and inside == True:
                end = i
                break

        artist_song = song[0] + " - " + song[1]
        pyplot.plot(hits[song][:end], label = artist_song)
        x += 1
    # pyplot.legend(loc='lower right', prop={'size':8})
    pyplot.gca().invert_yaxis()
    pyplot.show()