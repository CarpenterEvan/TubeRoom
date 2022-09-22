from GetTubeInfo import *
import pandas as pd
from pathlib import Path
import numpy as np
import time
import pickle

home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022 = Path.joinpath(DC_path, "2022")


processed = []


path_to_local = Path.joinpath(Path("").absolute(), "DC")
start = time.time()

ID_list = []
for path in Processed_2022.glob("**/*test*.log"): 
    with open(path, "r") as file: 
        ID_list += [next(file) for _ in range(16)][14][16:].strip(" \n").split(" ")
    print(path)


d,s = dict(), set()
print("Done with stripping IDs")

for line in ID_list: 
    thisID = line.strip("\n")
    print(thisID)
    if thisID in s and thisID in d.keys():
        d[thisID] += 1
    elif thisID not in s:
        s.add(thisID)
        d[thisID] = 1
print("Done with filling dictionary")
#GetTubeInfo.get_formatted_tuple(id)[0][11:21] 74.11 s
# filter_columns(locate_tube_row(id))["Shipment_date"] 38.59 s
def transform(id):
    return (filter_columns(locate_tube_row(id))["Shipment_date"], id, d[id])
value = map(transform, d.keys())

with open("IDOutput.pickle", "wb") as handle:
    pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)

#full_list = [(filter_columns(locate_tube_row(id))["Shipment_date"], id, d[id]) for id in d.keys()]
#print(full_list)
#with Path.joinpath(path_to_local, "IDOutput.txt").open("w") as output:
#    for i in value:
#        output.write(f"{i[0]}{i[1]}{i[2]}")
exit(time.time()-start)

df = pd.DataFrame(data=full_list, columns=["Date", "ID", "ndc"]).sort_values("Date").reset_index(drop=True)
df.to_csv(Path.joinpath(path_to_local, "IDOutput.txt"), sep=",")