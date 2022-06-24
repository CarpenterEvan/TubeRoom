import pandas as pd
from datetime import datetime, timedelta
global df, path

path = "./Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt"
df = pd.read_csv(path, 
                 names = ["ID", "T1", "T2", "DC", "Fin"],  
                 delimiter = "|")
df = df.applymap(lambda string: " ".join(string.split()))
df = df.applymap(lambda string: string.split(" "))
df["justID"] = df["ID"].map(lambda ID_as_list: ID_as_list[0])
print(df)