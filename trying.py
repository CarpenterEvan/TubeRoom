import os
import re
import matplotlib.pyplot as plt
from GetTubeInfo import id_to_values
lengths = []
with open("Verifying/Verified_2022102812.txt", "r") as file:
	for i in file.readlines():
		tubeid = i.strip("\n")
		value, good = id_to_values(tubeid)
		lengths.append(float(re.sub("\\x1b\[[0-9]*m", "", value["T1_Length"])))
lengths.append(1625.45)
bins = [1625.25, 1625.35, 1625.45, 1625.55, 1625.65, 1625.75, 1625.85, 1625.95]
n, bins, patches = plt.hist(lengths, bins=bins)


bin_centers = [patch._x0 + patch._width/2 for patch in patches]

for index, value in enumerate(n):
    print(int(value))
    num_tubes = int(value)
    plt.text(bin_centers[index], value,
            f"{num_tubes}",
            color="r", 
            horizontalalignment='center', 
            verticalalignment="bottom")

plt.xticks(ticks=bins, labels=list(map(str, bins)))
plt.title("Distribution of tubes that are too long (but pass all other tests)")
plt.xlabel("Length (mm)")
plt.ylabel("# Tubes")
plt.show()

'''
╔═══════════════════╗  ╔═════════════════════╗
║ 2020-01-20:     1 ║ 
'''