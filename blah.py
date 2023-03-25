import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("IDTD.tsv", delimiter="\t", names=["ID","Date", "Swage"])
df["Date"] = pd.to_datetime(df["Date"])
plt.title("Swage Depth vs Swage Date of MSU Tubes Reswaged")
plt.scatter(df["Date"], df["Swage"]+5)
plt.ylabel("Count")
plt.xlabel("First Tension Date (Closest recorded date to swage)")
plt.tick_params(axis="x", rotation = 45) # Rotates X-Axis Ticks by 45-degrees
plt.savefig("SwageTimeline.png")
plt.show()
exit()
fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(12,5))

ax[0].bar()
ax[1].scatter(df["Date"], df["Swage"]+5)
ax[1].tick_params(axis="x", rotation = 45) # Rotates X-Axis Ticks by 45-degrees
ax[0].tick_params(axis="x", rotation = 45) # Rotates X-Axis Ticks by 45-degrees
plt.title("Swage Depth vs Swage Date of MSU Tubes Reswaged")
ax[0].set_xlabel("Swage date")
ax[0].set_ylabel("Count")
ax[1].set_xlabel("First Tension Date (Closest recorded date to swage)")
ax[1].set_ylabel("Swage Depth (in)")

