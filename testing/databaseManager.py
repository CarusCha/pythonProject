import sqlite3
#
#
#
# con = sqlite3.connect("./db/kospi.db")
# sqlite3.Connection
#
# cursor = con.cursor()
# # cursor.execute("CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volumn int)")
# # cursor.execute("INSERT INTO kakao VALUES('16.06.03', 97000, 98600, 96900, 98000, 321405)")
# print(cursor.execute("SELECT * FROM kakao"))
#
# for data in cursor.fetchall()[0]:
#     print(data)
#
# # con.commit()
# con.close()




import pandas as pd
# import pandas_datareader.data as web
from pandas import Series, DataFrame
import datetime

con = sqlite3.connect("./db/kospi.db")

# for x in range(0,1):
#     raw_data = {'col0': [1, 2, 3, 4], 'col1': [10, 20, 30, 40], 'col2': [100, 200, 300, 400]}


# raw_data = [{'1':[{'name':'samsung', 'price':100}, {'name':'LG', 'price':50}]}, {'2':[{'name':'samsung', 'price':100}, {'name':'LG', 'price':50}]}]
# raw_data = {'1':[{'name':'samsung', 'price':100}, {'name':'LG', 'price':50}]}
raw_data = [{'name':'samsung', 'price':100}, {'name':'LG', 'price':50}]

df = DataFrame(raw_data)
df.to_sql('test', con, if_exists='replace')

test = pd.read_sql('SELECT * FROM test', con, index_col='index')
print(test)

# start = datetime.datetime(2010, 1, 1)
# end = datetime.datetime(2016, 6, 12)
print(datetime.date.today())
# df = web.DataReader("078930.KS", "yahoo", start, end)

# print(df.head())