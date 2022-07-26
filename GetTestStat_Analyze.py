import GetTubeInfo
from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt
home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
path_to_local = Path.joinpath(Path(__file__).absolute().parent, "outputs")

d,s = dict(), set()

with open(Path.joinpath(path_to_local, "IDOutput.txt"), "r") as IDFile:
    for line in IDFile: 
        thisID = line.strip("\n")
        if thisID not in s:
            s.add(thisID)
            d[thisID] = 1
        elif thisID in s and thisID in d.keys():
            d[thisID] +=1

s_date = set()
d_date = dict()
full_list = []
for id in d.keys():
    full_tuberow = GetTubeInfo.locate_tube_row(id)
    date = GetTubeInfo.filter_columns(full_tuberow)["Shipment_date"]
    full_list.append((date, id, d[id]))
#print(full_list)
df = pd.DataFrame(data = full_list, columns=["Date", "ID", "ndc"])
the_date = "2022-07-14"
df_one_date = df[df["Date"]==the_date].reset_index()
print(df_one_date)
ndc_one_date = df_one_date["ndc"]
plt.hist(ndc_one_date, bins=[1,2,3,4,5], align="left", rwidth=0.5)


plt.title(the_date)
plt.xticks([1,2,3,4,5])
plt.show()