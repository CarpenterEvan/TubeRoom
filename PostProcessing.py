import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#humidity = input("Humidity")

stripstring = lambda x: x.strip("[];]:")

df = pd.read_csv("~/Desktop/CAENPS_20220518_test2.log",
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
df_IMon = df[(df["par"]=="IMon") & (df["Location"]==f"{bd}")].reset_index()
df_VMon = df[(df["par"]=="VMon") & (df["Location"]==f"{bd}")].reset_index()
#df = df.drop(labels=["par", "Location"], axis="columns")
#df = df.resample("1S", label="right").mean().fillna(method="ffill")
print(df_IMon)
print(df_VMon)
first_2900 = df_VMon[df_VMon["val"]>=2796.].index
last_2900 = df_VMon[df_VMon["val"]>=2796.].index[-1]
print(first_2900)
print(last_2900)
#npdf = df.to_numpy()
#print(npdf)

#plt.plot(df)
#plt.tick_params(axis='x',labelsize=15,rotation=45)
#plt.tight_layout()
#plt.show()