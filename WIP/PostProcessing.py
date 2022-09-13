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


with open(path, "r") as file: 
    header = [next(file) for x in range(16)]
nominal_voltage = int(header[9][17:].strip())
mapping_to_boards = header[10][16:].strip(" \n").split(" ")
HVpowerSupplyID = header[11][16:].strip(" \n").split("   ")
Pedestal = " ".join(header[12][15:].split()).split(" ")
ID_Mapping = header[14][16:].strip(" \n").split(" ")
print(len(Pedestal))
P4 = Pedestal[0:24]
P1 = Pedestal[24:49]

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
df.drop(df[df["val"].str.contains("true|false")].index, inplace=True)
df["val"] = df["val"].astype(float)
df4 = df[df["bd"]=="4"].drop("bd", axis=1)
df1 = df[df["bd"]=="1"].drop("bd", axis=1)
#ch_n = 4

def bd4_ch_I(ch_n):
    df4_n = df4[df4["ch"] == str(ch_n)]
    df4_n.drop("ch", axis=1, inplace=True)
    
    df4_V = df4_n[df4_n["par"] == "VMon"].drop("par", axis=1, inplace=False)
    
    df4_V = df4_V[df4_V["val"].between(left=2897, right=2902)]
    df4_V_first = df4_V.index[0]
    print(df4_V_first)
    df4_I = df4_n[df4_n["par"] == "IMon"].drop("par", axis=1, inplace=False).loc[df4_V_first:]

    df4_I = df4_I.applymap(lambda x: float(x)-float(Pedestal[ch_n])/100)

    return df4_I

bd4 = []
for chh in range(3):
    print(bd4_ch_I(chh))

exit(f"Time taken ≈ {time.time()-start:.4f}s")



#df_time = df.resample("1S", label="left")





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