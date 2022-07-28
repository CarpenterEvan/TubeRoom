import GetTubeInfo
import pandas as pd
from pathlib import Path


home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022_06 = Path.joinpath(DC_path, "2022", "2022_06")
start_date = "2022-06-28"

DC_Files = sorted(DC_path.glob("*test*.log") ) 
Processed_2022_06_Files = sorted(Processed_2022_06.glob("*test*.log"))


All_Files = DC_Files + Processed_2022_06_Files

path_to_local = Path.joinpath(Path(__file__).absolute().parent, "outputs")



ID_list = []

for file in All_Files:
    DC_File = open(file, "r")
    ID_Line = DC_File.readlines()[14][16:].strip("\n").strip(" ")
    ID_line_listed = ID_Line.split(" ")
    ID_list += ID_line_listed
    DC_File.close()

d,s = dict(), set()
for line in ID_list: 
    thisID = line.strip("\n")
    if thisID not in s:
        s.add(thisID)
        d[thisID] = 1
    elif thisID in s and thisID in d.keys():
        d[thisID] +=1
full_list = []
IDFile = open(Path.joinpath(path_to_local, "IDOutput.txt"), "w")
for id in d.keys():
    full_tuberow = GetTubeInfo.locate_tube_row(id)
    date = GetTubeInfo.filter_columns(full_tuberow)["Shipment_date"]
    full_list.append((date, id, d[id]))
    IDFile.write(f"{date}\t{id}\t{d[id]}\n")

IDFile.close()