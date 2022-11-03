import datetime
import os
import glob
import re



home_to_DB = os.path.expanduser("~/Google Drive/Shared drives/sMDT Tube Testing Reports") 
CAEN = os.path.join(home_to_DB, "CAEN")
Tension = os.path.join(home_to_DB, "TubeTension")
CAEN_glob = glob.glob(CAEN+"/Processed/*test*.log")
Tension_glob = glob.glob(Tension+"/Processed/*.log")
print("\n".join(Tension_glob))
exit(print("\n".join(CAEN_glob)))
save_file = os.path.abspath("")
print("\n" + save_file)
today = datetime.datetime.today()
week_ago = today - datetime.timedelta(days = 7)
print(week_ago.strftime("%Y%m%d"))
home = Path.home()
GDrive_path = Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
TubeTension = Path.joinpath(home, GDrive_path, "TubeTension")
processed_folder = Path.joinpath(TubeTension, "Processed")


for the_file in TubeTension.glob("*.log"):
	re.findall("MSU[0-9]{5}", the_file.read())