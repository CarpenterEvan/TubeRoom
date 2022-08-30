from GetTubeInfo import *
import pandas as pd
from pathlib import Path
import numpy as np
import time
import gzip

home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022 = Path.joinpath(DC_path, "2022")


processed = []




path_to_local = Path.joinpath(Path("").absolute(), "DC")

#ID_List = [open(file).readlines()[14][16:].strip("\n").strip(" ").split(" ") for file in All_Files] #46s
start = time.time()
ID_list = []
for file in DC_path.glob("**/*test*.log"): 
    print(file)
    DC_File = open(file)
    ID_list += DC_File.readlines()[14][16:].strip(" \n").split(" ")
    DC_File.close()

d,s = dict(), set()
print("Done with stripping IDs")

for line in ID_list: 
    thisID = line.strip("\n")
    if thisID in s and thisID in d.keys():
        d[thisID] += 1
    elif thisID not in s:
        s.add(thisID)
        d[thisID] = 1
print("Done with filling dictionary")
#GetTubeInfo.get_formatted_tuple(id)[0][11:21] 74.11 s
# filter_columns(locate_tube_row(id))["Shipment_date"] 38.59 s

full_list = [(filter_columns(locate_tube_row(id))["Shipment_date"], id, d[id]) for id in d.keys()]

print(time.time()-start)

df = pd.DataFrame(data=full_list, columns=["Date", "ID", "ndc"]).sort_values("Date").reset_index(drop=True)
df.to_csv(Path.joinpath(path_to_local, "IDOutput.txt"), sep=",")