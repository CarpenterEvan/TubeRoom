import Verification
from Verification import ID
import datetime
d = {}
s = set()
while True:
    tubeid = input("Scan: ")
    if tubeid=="stop":
        for i in d:
            print(i, d[i])
        break
    tuberow, = ID.index[ID["tubeID"].str.contains(tubeid)]
    string = ID["Received"].iloc[tuberow]
    #print(datetime.datetime.strptime(string, "%Y-%m-%d"))
    if string not in d and tubeid not in s:
        d[string] = 1
        s.add(tubeid)
    elif string in d:
        d[string] +=1 