from GetTubeInfo import *
import pandas as pd
from pathlib import Path
import numpy as np
import time

home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022 = Path.joinpath(DC_path, "2022")

processed = []

for i in Processed_2022.glob("*"):
    subfolder = Path.joinpath(Processed_2022, i)
    for j in subfolder.glob("*test*.log"):
        processed.append(j)

DC_Files = sorted(DC_path.glob("*test*.log") ) 

All_Files = DC_Files + processed

path_to_local = Path.joinpath(Path("").absolute(), "DC")

ID_list = []

start = time.time()

for file in All_Files:
    DC_File = open(file, "r")
    ID_Line = DC_File.readlines()[14][16:].strip("\n").strip(" ")
    ID_line_listed = ID_Line.split(" ")
    ID_list += ID_line_listed
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