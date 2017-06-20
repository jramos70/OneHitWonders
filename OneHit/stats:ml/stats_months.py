import csv
from matplotlib import pyplot, dates

with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:
    reader = csv.reader(file_reader)
    hits = {}
    start = [0 for i in range(13)]
    end  = [0 for i in range(13)]
    for row in reader:
        if row[8].lower() == 'true':# or row[8].lower() == 'false':
            month = row[0].split("/")[0]
            if (row[2], row[3]) not in hits:
                hits[(row[2], row[3])] = [(row[1], month)]
            else:
                hits[(row[2], row[3])].insert(0, (row[1], month))
    x = 0
    for song in hits:
        month_start = hits[song][0][1]
        month_end = hits[song][len(hits[song]) - 1][1]
        start[int(month_start)] += 1
        end[int(month_end)] += 1


# print(months[1:])
# print(sum(months[1:])/12)
# quarter = [sum(months[1:4]), sum(months[4:7]), sum(months[7:10]), sum(months[10:12])]
pyplot.plot(range(12), start[1:])
pyplot.plot(range(12), end[1:])
pyplot.legend(['starting month', 'ending month'], loc='upper left')
pyplot.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# pyplot.plot(range(1,13), months[1:])
# pyplot.gca().invert_yaxis()
pyplot.xlabel('month')
pyplot.ylabel('# of one hit wonders')
pyplot.suptitle('Number of One Hit Wonders per Month', fontsize=20)

pyplot.show()
