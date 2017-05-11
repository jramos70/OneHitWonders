import csv
from matplotlib import pyplot, dates

with open("one_hit_wonder.csv", 'r', encoding = 'latin1') as file_reader:
    reader = csv.reader(file_reader)
    next(reader, None)
    hits = {}
    all_songs = {}
    pre_vevo = {}
    vevo = {}
    isVevo = True
    for row in reader:

        if (row[2], row[3]) not in all_songs:
            all_songs[(row[2], row[3])] = [row[1]]
        else:
            all_songs[(row[2], row[3])].insert(0, row[1])

        if row[8].lower() == 'true':# or row[8].lower() == 'false':
        #if row[7].lower() == 'pop' and row[8].lower() == 'false':
            if (row[2], row[3]) not in hits:
                hits[(row[2], row[3])] = [row[1]]
            else:
                hits[(row[2], row[3])].insert(0, row[1])
            
            if (row[0] == '12/5/09'):
                isVevo = False

            if isVevo:
                if (row[2], row[3]) not in vevo:
                    vevo[(row[2], row[3])] = [row[1]]
                else:
                    vevo[(row[2], row[3])].insert(0, row[1])
            else:
                if (row[2], row[3]) not in pre_vevo:
                    pre_vevo[(row[2], row[3])] = [row[1]]
                else:
                    pre_vevo[(row[2], row[3])].insert(0, row[1])
    for song in hits:
        if song in vevo and song in pre_vevo:
            vevo.pop(song)

    print("vevo", len(vevo))
    print("pre_vevo", len(pre_vevo))
    print ("hits", len(hits))
    matrix = [0 for i in range(70)]
    for song in hits:
        x = 0
        for pos in hits[song]:
            if int(pos) <= 40:
                x += 1
        matrix[x] += 1
    matrix = [i/sum(matrix) for i in matrix]
    # matrix4 = [0 for i in range(100)]
    # for song in hits:
    #     x = 0
    #     for pos in hits[song]:
    #         if int(pos) <= 40:
    #             x += 1
    #         else:
    #             break
    #     matrix4[x] += 1

    matrix4 = [0 for i in range(70)]
    for song in all_songs:
        x = 0
        for pos in all_songs[song]:
            if int(pos) <= 40:
                x += 1
        if x > 0:
            matrix4[x] += 1

    matrix4 = [i/sum(matrix4) for i in matrix4]
    matrix2 = [0 for i in range(100)]
    for song in vevo:
        x = len(vevo[song])
        matrix2[x] += 1
    
    matrix3 = [0 for i in range(100)]
    for song in pre_vevo:
        x = len(pre_vevo[song])
        matrix3[x] += 1


for i in range(10):
    if i == 0:
        print (matrix[1:11])
    elif i == 9:
        print (matrix[91:101])
    else:
        print(matrix[i*10+1:i*10+11])
# print("\n vevo")

# for i in range(8):
#     if i == 0:
#         print (matrix2[1:11])
#     elif i == 7:
#         print (matrix2[71:80])
#     else:
#         print(matrix2[i*10+1:i*10+11])

# print("\n pre_vevo")

# for i in range(8):
#     if i == 0:
#         print (matrix3[1:11])
#     elif i == 7:
#         print (matrix3[71:80])
#     else:
#         print(matrix3[i*10+1:i*10+11])

val = 0
val2 = 0

for i in range(len(matrix2)):
    val += i * matrix2[i]

for i in range(len(matrix3)):
    val2 += i * matrix3[i]

# print("average post-vevo: ", val/len(vevo))
# print("average pre-vevo: ", val2/len(pre_vevo))


pyplot.plot(range(70), matrix, color = '#ffa500')
pyplot.plot(range(70), matrix4, color = '#808080')
# pyplot.fill_between(range(70), matrix, alpha = .8, color = 'b')
# pyplot.fill_between(range(70), matrix4, alpha = .8, color = 'g')

# pyplot.gca().invert_yaxis()
pyplot.xlabel('# of weeks')
pyplot.ylabel('% of songs')
# pyplot.yscale('log')
pyplot.legend(['one hit wonders', 'all wonders'], loc='upper right')
pyplot.suptitle('Lasting Time for One Hit Wonders vs All Wonders', fontsize=20)
pyplot.show()