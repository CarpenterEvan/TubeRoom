import pandas as pd
from GetTubeInfo import id_to_values, DB

'''
EARLIEST WORKING VERSION 
'''

Date_series = DB["Received"]

Bend_series = DB["flagE"].map({"PASS":0, "Fail":1}, na_action=None).rename("Bent")
MSU = DB["Comment"].map(lambda x: "UM" not in x, na_action=None).rename("MSU")
UM = DB["Comment"].map(lambda x: "UM" in x, na_action=None).rename("UM")
T1_series = DB["flag"].map({"pass":1, "fail":0}, na_action=None).rename("T1$_\text{ok}$")
T2_series = DB["flag2"].map({"Pass2":1, "Pass2*":1, "Fail2":0, "Fail2*":0}, na_action=None).rename("T2$_\text{ok}$")
DC_series = DB["DCflag"].map({"OK":1, "WARN":0, "BAD":0, "TRIP":0}, na_action=None).rename("DC$_\text{ok}$")
Lost  = DB["ok"].map({"OK":0, "YES":0, "N/A":1, "NO":0}).rename("Lost")
All_Ok  = DB["ok"].map({"OK":1, "YES":1, "N/A":0, "NO":0}).rename("Passed All")
Ready = DB["ok"].map({"OK":0, "YES":1, "N/A":0, "NO":0}).rename("Ready")
Used  = DB["ok"].map({"OK":1, "YES":0, "N/A":0, "NO":0}).rename("In Chamber")


items_in_summary = [MSU, Lost, Bend_series, T1_series, T2_series, DC_series, All_Ok, Used, Ready] # standardizing order the values are in

values = pd.concat(items_in_summary, axis=1)
full_df = pd.concat([Date_series, values], axis=1) # I move the date series around a bit, it's easier to not add it in with items_in_series

MSU_tubes = full_df[full_df["MSU"]==True]
UM_tubes = full_df[full_df["MSU"]==False].rename(columns={"MSU":"UM", "Received":"Constructed"})
UM_tubes["UM"] = UM_tubes["UM"].map(lambda x: not x)


MSU_summary = MSU_tubes.groupby("Received").agg("sum").astype("int")[-8:] # group by date
MSU_summary["Lost"] = MSU_summary["Lost"] - MSU_summary["Bent"] # all bent tubes are lost, but not all lost tubes are bent
MSU_summary.index = pd.to_datetime(MSU_summary.index, format="%Y-%m-%d") # change the index to a datetime
MSU_summary = MSU_summary.groupby([pd.Grouper(level="Received", freq="W-FRI", origin="epoch")]).sum() # group by week

column_names = [item.name for item in items_in_summary]

MSU_summary = MSU_summary[(MSU_summary != 0).any(1)]


MSU_summary = MSU_summary.reset_index(level="Received")

MSU_total = pd.DataFrame(MSU_summary.sum(numeric_only=True).tolist(), index=column_names).T
MSU_summary["Received"] = MSU_summary["Received"].astype(str)

MSU_summary = pd.concat([MSU_summary, MSU_total])
MSU_summary["Received"][-1:] = "Total"
print(MSU_summary)


UM_summary = UM_tubes.groupby("Constructed").agg("sum").astype("int")[-31:]
UM_summary.loc["Total"] = UM_summary.sum(numeric_only=True, axis=0)
UM_summary = UM_summary.reset_index(level=0)


MSU_data_file = "Weekly_Presentation/MSU_Tube_Summary_Data.txt"
UM_data_file = "Weekly_Presentation/UM_Tube_Summary_Data.txt"

msu_string = MSU_summary.to_latex(buf=None, escape=False, column_format = "|c|c|c|c|c|c|c|c|c|c|", index=False).replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")
 
um_string= UM_summary.to_latex(buf=None, escape=False, column_format = "|c|c|c|c|c|c|c|c|c|c|", index=False).replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")


with open(MSU_data_file, "w") as msufile:
	msufile.write(msu_string)
with open(UM_data_file, "w") as umfile:
	umfile.write(um_string)
