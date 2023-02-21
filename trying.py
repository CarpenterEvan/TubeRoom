import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("SwagedTubes.csv")
swageDelta = df["Swage Depth Before"] - df["Swage Depth After"]
lengthDelta = df["Length Before"] - df["Length After"]
myBins = range(320,385,5)
fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(16,5))

ax[0].hist([df["Tension Before"], df["Tension After"]], bins=myBins)
ax[0].legend(["Before", "After"], loc="upper left")
ax[0].set_title("Tension of Faulty Tubes Before and After Swaging (grams )")
ax[0].set_ylabel(f"Entries/{myBins.step}g")
ax[0].set_xlabel("Tension (g)")
ax[0].vlines(x=[325,380], ymin=0,ymax=40, colors="red", linestyles="dashed")

tensionDelta = df["Tension After"]-df["Tension Before"]
n, bins, patches = ax[1].hist(tensionDelta, bins=range(10,30,2))

ax[1].set_title("Difference in Tension (grams)")
ax[1].set_ylabel(f"Entries/{2}g")
ax[1].set_xlabel("Tension (g)")

plt.savefig("TensionAfterSwaging.png")
plt.show()

