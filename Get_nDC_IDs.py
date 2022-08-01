import GetTubeInfo
import pandas as pd
from pathlib import Path


home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022 = Path.joinpath(DC_path, "2022")
Processed_2022_06 = Path.joinpath(DC_path, "2022", "2022_06")
processed = []

for i in Processed_2022.glob("*"):
    subfolder = Path.joinpath(Processed_2022, i)
    for j in subfolder.glob("*test*.log"):
        processed.append(j)

start_date = "2022-06-28"

DC_Files = sorted(DC_path.glob("*test*.log") ) 
Processed_2022_06_Files = sorted(Processed_2022_06.glob("*test*.log"))


All_Files = DC_Files + processed

path_to_local = Path.joinpath(Path(__file__).absolute().parent, "DC")

ID_list = []

for file in All_Files:
    print(file.name)
    DC_File = open(file, "r")
    ID_Line = DC_File.readlines()[14][16:].strip("\n").strip(" ")
    ID_line_listed = ID_Line.split(" ")
    ID_list += ID_line_listed
    DC_File.close()

d,s = dict(), set()
print("done with stripping IDs")
for line in ID_list: 
    thisID = line.strip("\n")
    if thisID in s and thisID in d.keys():
        d[thisID] += 1
    elif thisID not in s:
        s.add(thisID)
        d[thisID] = 1
print("done with filling dictionary")
full_list = [(GetTubeInfo.get_formatted_tuple(id)[0][11:21], id, d[id]) for id in d.keys()]
'''IDFile = open(Path.joinpath(path_to_local, "IDOutput.txt"), "w")'''

'''for id in d.keys():
    verify_string, good_tube = GetTubeInfo.get_formatted_tuple(id)
    date = verify_string[11:21]
    full_list.append((date, id, d[id]))'''

df = pd.DataFrame(data=full_list, columns=["Date", "ID", "ndc"]).sort_values("Date")
df.to_csv(Path.joinpath(path_to_local, "IDOutput.txt"), sep=",")


'''IDFile.write(f"{date}\t{id}\t{d[id]}\n")
IDFile.close()'''