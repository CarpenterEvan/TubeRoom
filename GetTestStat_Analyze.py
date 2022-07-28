import GetTubeInfo
from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt
home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
path_to_local = Path.joinpath(Path(__file__).absolute().parent, "outputs")


df = pd.read_csv(Path.joinpath(path_to_local, "IDOutput.txt"), sep="\t", names=["Date", "ID", "ndc"])



date_list = ['2022-06-21']#, '2022-06-28', '2022-07-07', '2022-07-14']
date = '2022-06-28'
left_list = [0, 3, 105, 206]
#num_graphs = len(date_list)
runs_list = [1,2,3,4,5]
fig = plt.figure(figsize=(5, 5), tight_layout=True)


#for i, date in enumerate(date_list):

df_one_date = df[df["Date"]==date].reset_index()
ndc_one_date = df_one_date["ndc"]
total_number = len(ndc_one_date)

ax = fig.add_subplot(111,
                     title=f"Number of DC runs for tubes from {date}", 
                     xlabel="Number of DC runs (on CAEN)",
                     ylabel="Number of tubes",
                     xticks=runs_list,
                     aspect="auto")

n, bins, patches = ax.hist(ndc_one_date, bins=runs_list, align="left", rwidth=0.8)
total_treated = int(sum(n[1:]))

bin_centers = [(patch._x0 + patch._x1)/2 for patch in patches]

for index, value in enumerate(n):
    num_tubes = int(value)
    percent_of_total = 100 * num_tubes / total_number
    ax.text(bin_centers[index], value,
            f"{num_tubes} ({percent_of_total:.2f}%)",
            color="r", 
            horizontalalignment='center', 
            verticalalignment="bottom")

ax.text(0.725, 0.8, f"Total # tubes: {total_number}", 
        horizontalalignment="center",
        transform=ax.transAxes)
ax.text(0.725, 0.7, f"Total treated: {total_treated} ({100 * total_treated / total_number:.2f}%)", 
        horizontalalignment="center",
        transform=ax.transAxes)
need_to_treat = f"Need to treat (not shown): {0}"
#ax.text(0.725, 0.6, need_to_treat, 
#        horizontalalignment="center",
#        transform=ax.transAxes)
plt.savefig(Path.joinpath(path_to_local,f"nDC_{date.replace('-','')}"), dpi=200, format="png")
plt.show()