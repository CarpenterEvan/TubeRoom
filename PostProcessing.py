import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import  Path

#humidity = input("Humidity")

stripstring = lambda x: x.strip("[];]:")
date = "20220801"#input('Date:')
path = Path.joinpath(Path.home(), f"Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/Processed/CAENPS_{date}_test.log")
df = pd.read_csv(path,
                 skiprows=16,
                 delimiter=" ",
                 usecols=[0, 3, 5, 7, 9],
                 names=["Datetime", "bd", "ch", "par", "val"],
                 parse_dates=["Datetime"],
                 infer_datetime_format=True,
                 converters={0: stripstring,
                             3: stripstring, 
                             5: stripstring,
                             7: stripstring,
                             9: stripstring}
                 )
df["Location"] = df["bd"] + "-" + df["ch"].str.pad(width=2,fillchar="0")
df = df.drop(labels=["bd","ch"], axis="columns") 
df["val"] = df["val"][(df["val"] != "true") & (df["val"] != "false") ].astype(np.float64)
df = df.dropna()
#df = df.set_index("Datetime")
#df_time = df.resample("1S", label="left")
#print(df_time)
bd = "1-06"

df_VMon = df[(df["par"]=="VMon") & (df["Location"]==f"{bd}")].reset_index(drop=True)
df_VMon = df_VMon.reset_index(drop=True)
df_VMon = df_VMon.set_index("Datetime")
df_VMon = df_VMon["val"]
df_VMon.resample('1s').mean().bfill()
df_IMon = df[(df["par"]=="IMon") & (df["Location"]==f"{bd}")]
df_IMon = df_IMon.reset_index(drop=True)
df_IMon = df_IMon.set_index("Datetime")
df_IMon = df_IMon["val"]
df_IMon.resample('1s').mean().bfill()
#df = df.drop(labels=["par", "Location"], axis="columns")
#df = df.resample("1S", label="right").mean().fillna(method="ffill")
print(df_IMon)
print("")


#npdf = df.to_numpy()
#print(npdf)

#plt.plot(df)
#plt.tick_params(axis='x',labelsize=15,rotation=45)
#plt.tight_layout()
#plt.show()