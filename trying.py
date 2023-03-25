import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("SwagedTubes.csv")
#exit(print(df["ID"][df["Swage Depth Before"].idxmin()]))
swageDelta = df["Swage Depth Before"] - df["Swage Depth After"]
lengthDelta = df["Length Before"] - df["Length After"]
tensionBins = range(320,385,5)
lengthBins = [1623.75+(0.10*i) for i in range(0,16,1)]

fig, ((tension_ax, tens_delt_ax), (length_ax, length_delt_ax)) = plt.subplots(ncols=2, nrows=2, figsize=(12,8), layout="tight")
def stats(before, after="", rounding=1, unit="g", othertext="Before:"):
	before_average = round(before.mean(),rounding)
	before_stdev = round(before.std(),rounding)
	before_stats = r"{} ($\mu$={}±{}{})".format(othertext, before_average, before_stdev, unit)
	stats_return = [before_stats]
	if type(after)==str:
		return stats_return	
	else:
		after_average = round(after.mean(),rounding)
		after_stdev = round(after.std(),rounding)
		after_stats = r"After ($\mu$={}±{}{})".format(after_average, after_stdev, unit)
		stats_return.append(after_stats)
		return stats_return

tension_stats = stats(df['Tension Before'], df['Tension After'])


tension_ax.hist(df["Tension Before"], bins=tensionBins, alpha=0.75, edgecolor="black", linewidth=1.25)
tension_ax.hist(df["Tension After"], bins=tensionBins, alpha=0.75, edgecolor="black", linewidth=1.25)
tension_ax.legend(tension_stats, loc="upper left")
tension_ax.set_title("Tension of Faulty Tubes Before and After Swaging (grams)")
tension_ax.set_ylabel(f"Entries/{tensionBins.step}g")
tension_ax.set_xlabel("Tension (g)")
tension_ax.vlines(x=[325,380], ymin=0,ymax=80, colors="red", linestyles="dashed")

tensionDelta = df["Tension After"]-df["Tension Before"]
tens_delt_stats = stats(tensionDelta, othertext="")
tens_delt_ax.hist(tensionDelta, bins=range(10,30,2),edgecolor="black", linewidth=1.25)

tens_delt_ax.set_title("Difference in Tension (grams)")
tens_delt_ax.set_ylabel(f"Entries/{2}g")
tens_delt_ax.set_xlabel("Tension (g)")
tens_delt_ax.legend(tens_delt_stats, loc="upper left")

length_stats = stats(df['Length Before'], df['Length After'], rounding=2, unit="mm")
length_ax.set_xticks([1623.75+(0.10*i) for i in range(0,16,3)])
length_ax.hist(df["Length Before"], bins=lengthBins, alpha=0.75, edgecolor="black", linewidth=1.25)
length_ax.hist(df["Length After"], bins=lengthBins, alpha=0.75, edgecolor="black", linewidth=1.25)
length_ax.legend(length_stats, loc="upper left")
length_ax.set_title("Length of Faulty Tubes Before and After Swaging (mm)")
length_ax.set_ylabel(f"Entries/{0.10}g")
length_ax.set_xlabel("Length (mm)")

length_ax.vlines(x=[1623.75,1625.25], ymin=0,ymax=80, colors="red", linestyles="dashed")

lengthDelta = df["Length After"]-df["Length Before"]
length_delt_ax.hist(lengthDelta, bins=20, edgecolor="black", linewidth=1.25)
length_delt_stats = stats(lengthDelta, rounding=2, unit="mm", othertext="")
length_delt_ax.legend(length_delt_stats, loc="upper left")

length_delt_ax.set_title("Difference in Length (mm)")
length_delt_ax.set_ylabel(f"Entries/{2}mm")
length_delt_ax.set_xlabel("Length Difference (mm)")

plt.savefig("Weekly_Presentation/TensionLengthAfterSwaging.png")
plt.show()
#exit()
df['Swage Depth Before'] = (df['Swage Depth Before']+5)*25.4
df['Swage Depth After'] = (df['Swage Depth After']+5)*25.4



fig , ((swage_ax, swage_delt_ax)) = plt.subplots(ncols=2, nrows=1, figsize=(12,5), layout="tight")
swage_stats = stats(df['Swage Depth Before'], after=df['Swage Depth After'], rounding=3, unit="mm")

swageBins = [140.08+(0.05*i) for i in range(0,35,1)]

swage_ax.hist(df["Swage Depth Before"], bins=swageBins, edgecolor="black", linewidth=1.25)
swage_ax.hist(df["Swage Depth After"], bins=swageBins, edgecolor="black", linewidth=1.25)

swage_ax.set_title("Swage Depth Before and After Swaging (mm)")
swage_ax.set_ylabel(f"Entries /0.05mm")
swage_ax.set_xlabel("Swage Depth (mm)")
swage_ax.legend(swage_stats, loc="upper right")
swage_ax.vlines(x=[140.72], ymin=0,ymax=130, colors="red", linestyles="dashed")
swageDelta = abs(df["Swage Depth After"]-df["Swage Depth Before"])
swage_delt_bins = [0+0.05*i for i in range(0,15,1)]
swage_delt_ax.hist(swageDelta, bins=swage_delt_bins, edgecolor="black", linewidth=1.25)
swage_delt_stats = stats(swageDelta, rounding=3, unit="mm", othertext="")
swage_depth_average = round(swageDelta.mean(),3)
swage_depth_stdev = round(swageDelta.std(),3)
swage_depth_stats = r"($\mu$={}±{}mm)".format(swage_depth_average, swage_depth_stdev)
swage_delt_ax.legend(swage_delt_stats, loc="upper right")

swage_delt_ax.set_title("Difference in Swage Depth (mm)")
swage_delt_ax.set_ylabel(f"Entries/0.05mm")
swage_delt_ax.set_xlabel("Swage Depth Difference (mm)")
plt.savefig("SwageDepth_METRIC.png")
plt.show()


fig , ((day_1_swage_ax, day_1_swage_delt_ax), (day_2_swage_ax, day_2_swage_delt_ax), (day_3_swage_ax, day_3_swage_delt_ax)) = plt.subplots(ncols=2, nrows=3, figsize=(12,8), layout="tight")

first_day = df[:141]
second_day = df[141:294]
third_day = df[294:]


day_1_swage_ax.hist(first_day["Swage Depth Before"], bins=swageBins, edgecolor="black", linewidth=1.25)
day_2_swage_ax.hist(second_day["Swage Depth Before"], bins=swageBins, edgecolor="black", linewidth=1.25)
day_3_swage_ax.hist(third_day["Swage Depth Before"], bins=swageBins, edgecolor="black", linewidth=1.25)

day_1_swage_ax.hist(first_day["Swage Depth After"], bins=swageBins, edgecolor="black", linewidth=1.25)
day_2_swage_ax.hist(second_day["Swage Depth After"], bins=swageBins, edgecolor="black", linewidth=1.25)
day_3_swage_ax.hist(third_day["Swage Depth After"], bins=swageBins, edgecolor="black", linewidth=1.25)

day_1_swage_stats = stats(first_day['Swage Depth Before'], after=first_day['Swage Depth After'], rounding=3, unit="mm")
day_2_swage_stats = stats(second_day['Swage Depth Before'], after=second_day['Swage Depth After'], rounding=3, unit="mm")
day_3_swage_stats = stats(third_day['Swage Depth Before'], after=third_day['Swage Depth After'], rounding=3, unit="mm")

day_1_swage_ax.set_title("Swage Depth Before and After Day 1")
day_1_swage_ax.set_ylabel("Entries/0.05mm")
day_1_swage_ax.set_xlabel("Swage Depth (mm)")
day_1_swage_ax.legend(day_1_swage_stats)

day_2_swage_ax.set_title("Swage Depth Before and After Day 2")
day_2_swage_ax.set_ylabel("Entries/0.05mm")
day_2_swage_ax.set_xlabel("Swage Depth (mm)")
day_2_swage_ax.legend(day_2_swage_stats)

day_3_swage_ax.set_title("Swage Depth Before and After Day 3")
day_3_swage_ax.set_ylabel("Entries/0.05mm")
day_3_swage_ax.set_xlabel("Swage Depth (mm)")
day_3_swage_ax.legend(day_3_swage_stats)


day_swage_depth_bins = [0.006+0.001*i for i in range(20)]
Day_one_swageDelta = abs(first_day["Swage Depth After"]-first_day["Swage Depth Before"])
Day_two_swageDelta = abs(second_day["Swage Depth After"]-second_day["Swage Depth Before"])
Day_three_swageDelta = abs(third_day["Swage Depth After"]-third_day["Swage Depth Before"])

day_1_swage_delt_ax.hist(Day_one_swageDelta, bins=swage_delt_bins, edgecolor="black", linewidth=1.25)
day_2_swage_delt_ax.hist(Day_two_swageDelta, bins=swage_delt_bins, edgecolor="black", linewidth=1.25)
day_3_swage_delt_ax.hist(Day_three_swageDelta, bins=swage_delt_bins, edgecolor="black", linewidth=1.25)

day_1_swage_delt_stats = stats(first_day['Swage Depth Before'], rounding=3, unit="mm", othertext="")
day_2_swage_delt_stats = stats(second_day['Swage Depth Before'], rounding=3, unit="mm", othertext="")
day_3_swage_delt_stats = stats(third_day['Swage Depth Before'], rounding=3, unit="mm", othertext="")

day_1_swage_delt_ax.set_title("Swage Depth Before and After Day 1")
day_1_swage_delt_ax.set_ylabel('Entries/0.05mm')
day_1_swage_delt_ax.set_xlabel("Swage Depth Difference (mm)")
day_1_swage_delt_ax.legend(day_1_swage_delt_stats)

day_2_swage_delt_ax.set_title("Swage Depth Before and After Day 2")
day_2_swage_delt_ax.set_ylabel('Entries/0.05mm')
day_2_swage_delt_ax.set_xlabel("Swage Depth Difference (mm)")
day_2_swage_delt_ax.legend(day_2_swage_delt_stats)

day_3_swage_delt_ax.set_title("Swage Depth Before and After Day 3")
day_3_swage_delt_ax.set_ylabel('Entries/0.05mm')
day_3_swage_delt_ax.set_xlabel("Swage Depth Difference (mm)")
day_3_swage_delt_ax.legend(day_3_swage_delt_stats)


plt.savefig("SwageDepth_ByDay.png")
plt.show()