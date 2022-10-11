from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
import os
save_file = os.getcwd()
print("\n" + save_file)
today = datetime.datetime.today()
week_ago = today - datetime.timedelta(days = 7)
print(week_ago.strftime("%Y%m%d"))
home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
TubeTension = Path.joinpath(home, GDrive_path, "TubeTension")
processed_folder = Path.joinpath(TubeTension, "Processed")


df = pd.DataFrame(columns = ["Operator", "Date", "tubeID", "Length", 
                             "Density", "Frequency", "Tension", "TensionError"])
for file in TubeTension.glob("*.log"):
    file_name = file.name[8:16]
    date_of_file = datetime.datetime.strptime(file_name, "%Y%m%d")
    within_last_week = date_of_file > week_ago
    if within_last_week:
        try: 
            this_file = pd.read_csv(file, sep="\t")
            df = pd.concat([df, this_file], ignore_index=True)
        except pd.errors.ParserError: 
            print(file)
for file in processed_folder.glob("*.log"):
    file_name = file.name[8:16]
    date_of_file = datetime.datetime.strptime(file_name, "%Y%m%d")
    within_last_week = date_of_file > week_ago
    if within_last_week:
        try: 
            this_file = pd.read_csv(file, sep="\t")
            df = pd.concat([df, this_file], ignore_index=True)
        except pd.errors.ParserError: 
            print(file)

fig = plt.figure(figsize=(8,5), tight_layout=True)
ax = fig.add_subplot(111,
                     title=f"Tension Tests Performed Between {week_ago:%m/%d}-{today:%m/%d}", 
                     xlabel="Tension (g)",
                     ylabel="Number of Tubes",
                     aspect="auto")

n, bins, patches = ax.hist(df["Tension"], bins=range(320,410,10))# so bins= [325,335,345,355,365,375,385,395]
bin_centers = [(patch.xy[0]+patch._width*0.5)for patch in patches]

number_under = len(df[(df["Tension"]<325)])
number_over =  len(df[(df["Tension"]>380)])

print(df[(df["Tension"]<325) | (df["Tension"]>380)][["Operator", "Date", "tubeID","Tension"]])
total_tested = int(sum(n[1:]))
total_number = len(df["Tension"])
for index, value in enumerate(n):
    num_tubes = int(value)
    if num_tubes == 0:
        continue
    percent_of_total = 100 * num_tubes / total_number
    a = ax.text(bin_centers[index], value,
            f"{num_tubes} ({percent_of_total:.1f}%)",
            size=10,
            color="red", 
            horizontalalignment="center", 
            verticalalignment="bottom")

            
ax.text(0.25, 0.7, f"Total tested: {total_number}", 
        horizontalalignment="center",
        transform=ax.transAxes)
ax.text(0.25, 0.6, f"Under 325g: {number_under} tube(s)",
        horizontalalignment="center",
        transform=ax.transAxes)
ax.text(0.25, 0.55, f"  Over 380g: {number_over} tube(s)",
        horizontalalignment="center", 
        transform=ax.transAxes)

ax.set_xticks(bins)
plt.savefig(f"{save_file}/last_week_tt.png", dpi=1000)
plt.show()