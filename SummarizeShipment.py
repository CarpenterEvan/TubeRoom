from GetTubeInfo import id_to_values, DB
import GetTubeInfo
import pandas as pd

DB["IS_UM"] = DB["Comment"].apply(lambda row: "UM" in row)
print(DB["IS_UM"])
print(DB.groupby("Received").any()["tubeID"])
exit()
for shipment_date in DB.groupby("Received").any()["tubeID"].index:
	that_date_df = DB[DB["Received"]==shipment_date]
	that_date_df["tubeID"].to_csv(f"Summary/Tubes_From_{shipment_date.replace('-','')}.txt", index=False)
    