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