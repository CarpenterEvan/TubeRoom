import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import  Path
import time

#humidity = input("Humidity")
start = time.time()
stripstring = lambda x: x.strip(" [ ]; ]: ")
date = "20220801"#input('Date:')
path = Path.joinpath(Path.home(), f"Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/Processed/CAENPS_{date}_test.log")

df = pd.read_csv(path,
                 skiprows=16,
                 delimiter=" ",
                 usecols=[0, 3, 5, 7, 9],
                 names=["Datetime", "bd", "ch", "par", "val"],
                 parse_dates=["Datetime"],
                 infer_datetime_format=True,
                 na_values = ["false", "true"],
                 false_values=["false", "true"],
                 converters={0: stripstring,
                             3: stripstring, 
                             5: stripstring,
                             7: stripstring,
                             9: stripstring}
                ).set_index("Datetime")
print(df[df["val"]=="false"].index) # maybe dont index by datetime yet?
df.drop(df[df["val"]=="false"].index)
print(df[df["val"]=="false"].index)
print(df["val"].astype(float)); exit()
df4 = df[df["bd"]=="4"].drop("bd", axis=1)
df1 = df[df["bd"]=="1"].drop("bd", axis=1)

ch_n = 1

bd4_ch_n = df4[df4["ch"]==str(ch_n)].drop("ch", axis=1)
bd4_ch_n_V = bd4_ch_n[bd4_ch_n["par"]=="VMon"]
print(bd4_ch_n_V["val"]); exit(f"time taken: {time.time()-start:.2f} s")

df.dropna()
dfnp = df.to_numpy()
innp = df.index.to_numpy()

print(dfnp)

#df = df.set_index("Datetime")
#df_time = df.resample("1S", label="left")
#print(df_time)
bd = "1-05"
for i in range(48):
    print(i)
exit()
print(df)
df_VMon = df[(df["par"]=="VMon") & (df["Location"]==f"{bd}")].reset_index(drop=True)
df_VMon = df_VMon.reset_index(drop=True)
df_VMon = df_VMon.set_index("Datetime")
df_VMon.resample('1s').mean().bfill()
df_IMon = df[(df["par"]=="IMon") & (df["Location"]==f"{bd}")]
df_IMon = df_IMon.reset_index(drop=True)
df_IMon = df_IMon.set_index("Datetime")
df_IMon = df_IMon["val"]
df_IMon.resample('1s').mean().bfill()
#df = df.drop(labels=["par", "Location"], axis="columns")
#df = df.resample("1S", label="right").mean().fillna(method="ffill")
print(df_IMon)
print(df_VMon)

plt.plot(df_IMon)
plt.show()



#npdf = df.to_numpy()
#print(npdf)

#plt.plot(df)
#plt.tick_params(axis='x',labelsize=15,rotation=45)
#plt.tight_layout()
#plt.show()