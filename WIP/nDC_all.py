from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime
home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
path_to_local = Path.joinpath(Path("").parent, "DC")
IDOutput = Path.joinpath(path_to_local, "IDOutput.txt")

ID_df = pd.read_csv(IDOutput, sep=",")

df = pd.DataFrame(columns=["Date", "untreated", "treated"])



df[["Date", "untreated"]] = ID_df.groupby("Date")["ndc"].apply(lambda x: (x<2).sum()).reset_index(name='untreated')

df["treated"]  = ID_df.groupby("Date")["ndc"].apply(lambda x: (x>=2).sum()).reset_index(name='treated')["treated"]
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
#df.index = df["Date"]
#df.index = pd.to_datetime(df.index)
#df = df.drop(columns=["Date"])
df = df[2:]
main = df[["Date", "treated"]].reset_index(drop=True)
print(main)
fig = plt.figure(figsize=(10,5), tight_layout=True)
ax = fig.add_subplot(111,
                     title=f"Number of DC runs for tubes", 
                     xlabel="Shipment Date",
                     ylabel="Number of tubes")


#n, bins, patches = 
#ax.bar(main["Date"].map(datetime.strftime("%Y-%m-%d")), main["treated"], width=1)#, bins=len(main))#, histtype='bar')#stacked',align="left", rwidth=1)
print(main["treated"])
plt.xticks(rotation="vertical")

#bin_centers = [(patch._x0 + patch._x1)/2 for patch in patches]
#for index, value in enumerate(n):
#    num_tubes = int(value)
#    ax.text(bin_centers[index], value,
#            f"{num_tubes}",
#            color="r", 
#            horizontalalignment='center', 
#            verticalalignment="bottom")
ax.bar([0,1,2,3,4,5,6,7], [10,7,14,3,2,0,1,6], width=0.9)
plt.xticks([0,1,2,3,4,5,6,7], ["1", "2", "3", "4", "5", "6", "7", "8"])
plt.show()
exit()