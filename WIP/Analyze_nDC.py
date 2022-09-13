import GetTubeInfo
from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt
home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
path_to_local = Path.joinpath(Path("").parent, "DC")




#date_list = ['2022-06-21']#, '2022-06-28', '2022-07-07', '2022-07-14']
'''
Run Get_nDC_IDs.py before this to get the list of Tube IDs from DC tests
2022-07-14
2022-07-07
2022-06-28
2022-06-21
2022-06-16
2022-06-09
2022-05-31
2022-05-03
2022-04-26
'''

date = '2022-07-28'
#print(df)
#df["Date"] = pd.to_datetime(df["Date"])
#printdf = df["Date"].map(lambda x: x.strptime('%Y-%m-%d'))
#print(printdf)
df_one_date = df[df["Date"]==date].reset_index()

ndc_one_date = df_one_date["ndc"]
max_num_treatments = df_one_date["ndc"].max()
total_number = len(ndc_one_date)
left_list = [0, 3, 105, 206]
#num_graphs = len(date_list)
runs_list = range(1,max_num_treatments+2, 1)
print(df_one_date[df_one_date["ndc"]>1].sort_values("ndc"))
# I want to scale the width of the figure to be wider when there are many many tests, 
if max_num_treatments < 5:
        figure_size = (5,5)
elif max_num_treatments <= 10:
        figure_size = (8,5)
elif max_num_treatments >10:
        figure_size = (max_num_treatments,5)
#figure_size = (max_num_treatments, 5) if max_num_treatments > 5 else (5,5) 
# but when there are only 2-3 tests, I don't want the figure to be only 2-3 wide!!
fig = plt.figure(figsize=figure_size, tight_layout=True)
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

# Select the rows in df_one_date where ndc (in df_one_date) is >1, choose only columns ["ID", "ndc"], sort valus by ndc
saving_df = df_one_date[df_one_date["ndc"]>1][["ID","ndc"]].sort_values("ndc") 

formatted_date = date.replace("-","_",1).replace("-","")
plt.savefig(Path.joinpath(path_to_local,f"nDC_{formatted_date}.png"), dpi=200, format="png")
saving_df.to_csv(Path.joinpath(path_to_local, f"BadDC_{formatted_date}.txt"), sep=",", header=False, index=False)
plt.show()