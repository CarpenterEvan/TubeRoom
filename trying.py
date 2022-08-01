import os,sys
from pathlib import Path

import argparse
parser = argparse.ArgumentParser(prog= __file__, description='Process some integers.')

home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022 = Path.joinpath(DC_path, "2022")
Processed_2022_06 = Path.joinpath(DC_path, "2022", "2022_06")

processed = []
for i in Processed_2022.glob("*"):
    subfolder = Path.joinpath(Processed_2022, i)
    for j in subfolder.glob("*"):
        processed.append(j)
        DC_File = open(j, "r")
    ID_Line = DC_File
print(processed)

