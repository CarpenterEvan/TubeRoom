import os
import re
import GetTubeInfo
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
__author__ = "Evan Carpenter"
__version__ = "1"

home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
path_to_local = Path.joinpath(Path(__file__).absolute().parent, "outputs")
home_to_GDrive = Path.joinpath(home, GDrive_path)
DC_path = Path.joinpath(home_to_GDrive, "CAEN")
Tens_path = Path.joinpath(home_to_GDrive, "TubeTension")
CAEN_processed = Path.joinpath(DC_path, "Processed")

DC_Files = sorted(CAEN_processed.glob("*test*.log"))

ID_list = []
for file in DC_Files:
    DC_File = open(file, "r")
    ID_Line = DC_File.readlines()[14][16:].strip("\n")
    ID_line_listed = ID_Line.split(" ")
    ID_list += ID_line_listed
    DC_File.close()

for oneID in ID_list:
    print(oneID)
    full_tuberow = GetTubeInfo.locate_tube_row(oneID)
    row = GetTubeInfo.filter_columns(full_tuberow)
    print(row["Shipment_date"])