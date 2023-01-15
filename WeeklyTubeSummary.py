import pandas as pd
from GetTubeInfo import id_to_values, DB


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




values = pd.concat([ MSU, Lost, Bend_series, T1_series, T2_series, DC_series, All_Ok, Used, Ready], axis=1)
full_df = pd.concat([Date_series, values], axis=1)

MSU_tubes = full_df[full_df["MSU"]==True]
UM_tubes = full_df[full_df["MSU"]==False].rename(columns={"MSU":"UM", "Received":"Constructed"})
UM_tubes["UM"] = UM_tubes["UM"].map(lambda x: not x)


MSU_summary = MSU_tubes.groupby("Received").agg("sum").astype("int")[-8:]
MSU_summary["Lost"] = MSU_summary["Lost"] - MSU_summary["Bent"]
MSU_summary.index = pd.to_datetime(MSU_summary.index, format="%Y-%m-%d")
MSU_summary = MSU_summary.groupby([pd.Grouper(level=0, freq='W', origin="2020-01-20")]).sum()


print(MSU_summary)
column_names = [Bend_series.name, MSU.name, T1_series.name, T2_series.name, DC_series.name, Lost.name, All_Ok.name, Ready.name, Used.name]

MSU_summary = MSU_summary[(MSU_summary != 0).any(1)]
MSU_summary = MSU_summary.reset_index(level=0)
totals = MSU_summary.sum(numeric_only=True).tolist()
total_df = pd.DataFrame(totals, index=0, columns=column_names)#.transpose().columns(column_names)

print(total_df)
exit()
MSU_summary = pd.concat([MSU_summary, totals], columns=[Bend_series.name, MSU.name, T1_series.name, T2_series.name, DC_series.name, Lost.name, All_Ok.name, Ready.name, Used.name])

print(MSU_summary)

exit()
UM_summary = UM_tubes.groupby("Constructed").agg("sum").astype("int")[-31:]
UM_summary.loc["Total"]= UM_summary.sum(numeric_only=True, axis=0)
UM_summary = UM_summary.reset_index(level=0)


MSU_data_file = "Weekly_Presentation/MSU_Tube_Summary_Data.txt"
UM_data_file = "Weekly_Presentation/UM_Tube_Summary_Data.txt"

msu_string = MSU_summary.to_latex(buf=None, escape=False, column_format = "|c|c|c|c|c|c|c|c|c|c|", index=False).replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")
 
um_string= UM_summary.to_latex(buf=None, escape=False, column_format = "|c|c|c|c|c|c|c|c|c|c|", index=False).replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")


with open(MSU_data_file, "w") as msufile:
	msufile.write(msu_string)
with open(UM_data_file, "w") as umfile:
	umfile.write(um_string)
