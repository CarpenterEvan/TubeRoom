import pandas as pd
df = pd.read_csv("./Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt", 
                 names = ["ID", "T1", "T2", "DC", "Fin"],  
                 delimiter = "|")