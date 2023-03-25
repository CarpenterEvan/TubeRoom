import pandas as pd
from GetTubeInfo import id_to_values, DB

doc = '''
Running this code makes two LaTeX tables summarizing the MSU tube shipment statistics by week 
(as well as UM construction statistics, currently by day).
The files are generated in the Weekly_Presentation folder. 
This code uses GetTubeInfo to access TUBEDB.txt. 
This means that the code expects TUBEDB.txt to be in the same directory as it, or linked to it through Google Drive Desktop.
I pull out the numerical values of interest for Bend, Tension, Leak, and DC tests, 
as well as if the tube is lost/broken, passed ALL tests, ready for chamber, or already in chamber. 

passed ALL tests = Ready for chamber + Already in chamber. 
'''

Date_series = pd.to_datetime(DB["Received"], format="%Y-%m-%d")

# These next 10 lines mask all of the data as either True or False, 
# I do this so I can sum all of these values grouped by week later.
Bend_series = DB["flagE"].map({"PASS":0, "Fail":1}, na_action=None).rename("Bent")
MSU = DB["Comment"].map(lambda x: "UM" not in x, na_action=None).rename("MSU")

T1_series = DB["flag"].map({"pass":1, "fail":0}, na_action=None).rename("T1$_\text{ok}$")
T2_series = DB["flag2"].map({"Pass2":1, "Pass2*":1, "Fail2":0, "Fail2*":0}, na_action=None).rename("T2$_\text{ok}$")
DC_series = DB["DCflag"].map({"OK":1, "WARN":0, "BAD":0, "TRIP":0}, na_action=None).rename("DC$_\text{ok}$")
Lost  = DB["ok"].map({"OK":0, "YES":0, "N/A":1, "NO":0}).rename("Lost")
All_Ok  = DB["ok"].map({"OK":1, "YES":1, "N/A":0, "NO":0}).rename("Passed All")
Ready = DB["ok"].map({"OK":0, "YES":1, "N/A":0, "NO":0}).rename("Ready")
Used  = DB["ok"].map({"OK":1, "YES":0, "N/A":0, "NO":0}).rename("In Chamber")


# By putting the series in this list it's easier to change the order of the columns without messing up the namning of things later
# this may not be neccessary, and only useful for the initial setup, so I may forget to remove it.
items_in_summary = [MSU, Lost, Bend_series, T1_series, T2_series, DC_series, All_Ok, Used, Ready] 

# This is used for naming the new "Total" column that I am about to make.  
column_names = [item.name for item in items_in_summary]
UM_column_names = ["Constructed", "UM"] + [column for column in column_names[1:]]

# Male dataframe out of the series above, in the order presented in items_in_summary
full_df = pd.concat(items_in_summary, axis=1)

full_df.index = Date_series

MSU_tubes = full_df[full_df["MSU"]==True]

# Group by week starting on friday, sum them, and represent as integers. 163 looks better than 163.0
MSU_summary = MSU_tubes.groupby([pd.Grouper(level="Received", freq="W-FRI")]).agg("sum").astype("int") 

# select values of MSU_summary where any value is != 0, take last 8 entries
MSU_summary = MSU_summary[(MSU_summary != 0).any(1)][-13:] 

# all bent tubes are lost, but not all lost tubes are bent
#MSU_summary["Lost"] = MSU_summary["Lost"] - MSU_summary["Bent"] 


# Doing this any later made it difficult to lable the "Total". 
MSU_summary = MSU_summary.reset_index(level="Received")

# Get totals for just the subset I chose above (last 8 values)
MSU_total = pd.DataFrame(MSU_summary.sum(numeric_only=True).tolist(), index=column_names).T

# Removing this line saves the date as "2022-11-25 00:00:00" instead of "2022-11-25"
MSU_summary["Received"] = MSU_summary["Received"].astype(str)


MSU_need_leak_test = 0#int(input("How many MSU tubes need Leak test?: "))
MSU_LT_row = pd.DataFrame(["-","-","-","-","-","-",f"-{MSU_need_leak_test}","-",f"-{MSU_need_leak_test}"], index=column_names).T

#MSU_total[All_Ok.name] -= MSU_need_leak_test
#MSU_total[Ready.name] -= MSU_need_leak_test



UM = DB["Comment"].map(lambda x: "UM" in x, na_action=None).rename("UM")
# Select the parts of full_df that are UM tubes, rename the relevant columns for presentation
UM_tubes = full_df[full_df["MSU"]==False].rename(columns={"MSU":"UM"})
# In full_df, UM is a column of False, if I want to do sums, I need to flip all values to True
UM_tubes["UM"] = UM_tubes["UM"].map(lambda x: not x)
UM_summary = UM_tubes.groupby([pd.Grouper(level="Received", freq="W-FRI")]).agg("sum").astype("int")
#UM_summary["Lost"] = UM_summary["Lost"] - UM_summary["Bent"] 
# setting the index as column_names re-labels what was "UM" as "MSU"
UM_total = pd.DataFrame(UM_summary[-8:].sum(numeric_only=True).tolist(), index=column_names).T

MSU_total = MSU_total + UM_total

UM_total["Received"] = "(UM tubes this row)"
print(UM_total)
MSU_summary = pd.concat([UM_total, MSU_summary, MSU_total])

#MSU_summary["Received"][-2:-1] = "Need Leak"
MSU_summary["Received"][-1:] = "Total"

MSU_summary["LT$_\text{ok}$"] = MSU_summary["MSU"]

MSU_summary = MSU_summary[["Received"] + column_names[0:3] + ["LT$_\text{ok}$"] + column_names[3:]]

MSU_data_file = "Weekly_Presentation/MSU_Tube_Summary_Data.tex"

# This will generate a warning about using a Styler, in my opinion it was too complicated to be worth time looking into. 
# If the code breaks because keywords are switched around, I am sorry. - Past Evan
# Currently, it writes the MSU_summary to a LaTeX table, ignoring the index. 
# I remove the date as the index earlier because when I include it, the index lable "Received" is offset from the rest of the headers. 
# This was much easier to do for automatic table generation. 


msu_string = MSU_summary.to_latex(buf=None, escape=False, column_format = "r|" + "r|"*(len(list(MSU_summary.axes[1]))-2) + "r", index=False)

# Getting rid ot top/mid/bottom rule and adding in an \hline after every line break. This is stylistic. 
#msu_string = msu_string.replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")
 
with open(MSU_data_file, "w") as msufile:
	msufile.write(msu_string)

#print(msu_string); exit()

exit()
print(UM_total); exit()

UM_summary = UM_summary[(UM_summary != 0).any(1)]





UM_summary["Constructed"] = UM_summary.index.astype(str)

UM_summary = pd.concat([UM_summary, UM_total])

UM_summary["Constructed"][-1:] = "Total"

# Re-ordering the columns 
UM_summary = UM_summary[UM_column_names]


# Get totals for just the subset I chose above (last 8 values)



UM_data_file = "Weekly_Presentation/UM_Tube_Summary_Data.tex"

um_string= UM_summary.to_latex(buf=None, escape=False, column_format = "|c|" + "c|"*len(items_in_summary), index=False).replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")

UM_summary = UM_summary.reset_index(level=0)
with open(UM_data_file, "w") as umfile:
	umfile.write(um_string)


both_totals = UM_total.rename(columns={"UM":"MSU"}) + MSU_total
both_totals = both_totals.rename(columns={"MSU":"Total \# of Tubes"})
both_totals["Total Number in Tube Room"] = both_totals["Total \# of Tubes"] - both_totals["In Chamber"]# - both_totals["Bent"]- both_totals["Lost"]

both_totals_string = both_totals.to_latex(buf=None, escape=False, column_format = "|c|" + "c|"*(len(items_in_summary)-1) + "p{2.5cm}|", index=False).replace(r"\\", r"\\\hline").replace(r"\toprule", "\hline").replace(r"\midrule", "").replace(r"\bottomrule", "")

totals_data_file = "Weekly_Presentation/Totals_Summary_Data.tex"

with open(totals_data_file, "w") as totalsfile:
	totalsfile.write(both_totals_string)
