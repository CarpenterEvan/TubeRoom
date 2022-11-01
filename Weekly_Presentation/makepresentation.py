import os
import glob
import datetime

pdf_date = datetime.datetime.strftime(datetime.datetime.today(), "%Y%m%d")


os.system("python tubepop.py")
os.system("python Get_LastWeek_TT.py")
os.system("latex present.tex")
os.rename("present.pdf", f"{pdf_date}_TubeRoomUpdate.pdf")

the_glob = glob.glob(os.path.abspath("")+"/present.*")
the_glob.remove(os.path.abspath("")+"/present.tex")
for file in the_glob:
	print(f"deleting {file[-11:]}")
	os.remove(file)
os.remove(os.path.abspath("")+"/../present.log")