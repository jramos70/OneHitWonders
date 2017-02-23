import csv, sqlite3, pandas as pd

#create connection to database
connex = sqlite3.connect('billboard.db')
cur = connex.cursor()

#read csv into Database by chunks
for chunk in pd.read_csv('billboard.csv', chunksize = 4, encoding = "ISO-8859-1"):
    chunk.to_sql(name = 'data', con = connex, if_exists = 'append', index = False)

#The table's name in billboard.db is data

 