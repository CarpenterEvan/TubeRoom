import GetTubeInfo
import pandas as pd
from pathlib import Path


home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")

path_to_local = Path.joinpath(Path(__file__).absolute().parent, "outputs")
DC_Files = sorted(DC_path.glob("*test*.log"))

ID_list = []
for file in DC_Files:
    DC_File = open(file, "r")
    ID_Line = DC_File.readlines()[14][16:].strip("\n")
    print(ID_Line)
    ID_line_listed = ID_Line.split(" ")
    ID_list += ID_line_listed
    DC_File.close()
IDFile = open(Path.joinpath(path_to_local, "IDOutput.txt"), "w")
print(ID_list)
IDFile.write('\n'.join(ID_list))
IDFile.close()