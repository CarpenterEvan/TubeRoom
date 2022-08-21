import os,sys
import re
from pathlib import Path
from GetTubeInfo import DB
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(prog= __file__, description='Process some integers.')

home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
DC_path = Path.joinpath(home, GDrive_path, "CAEN", "Processed")
Processed_2022 = Path.joinpath(DC_path, "2022")
Processed_2022_06 = Path.joinpath(DC_path, "2022", "2022_06")

dicts={"A":1, "B":2}
green_text  = lambda x: f"\x1b[32m{x}\x1b[0m" # I don't know how this affects string length
red_text    = lambda x: f"\x1b[31m{x}\x1b[0m"
print(green_text("a"), len(green_text("a")))
print(red_text("b"), len(red_text("a")))

