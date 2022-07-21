import os,sys
import re
import pandas as pd
import pathlib
import GetTubeInfo

home = pathlib.Path.home()
GDrive_to_DB = pathlib.Path("Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN")
final = pathlib.Path.joinpath(home, GDrive_to_DB, f"CAENPS_{1}{2}{3}_test.log")
print(home)
print(GDrive_to_DB.parents[0])
print(final)
