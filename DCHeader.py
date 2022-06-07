from os.path import exists
from sys import exit
import datetime

year = datetime.date.today().strftime("%Y")
month = datetime.date.today().strftime("%m")
day = datetime.date.today().strftime("%d")
time = datetime.datetime.now().strftime("%H:%M:%S")
in_file_date = f"{year}-{month}-{day}" # I use separate variable here because I also need to name the file.

file_exists = exists(f"./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/CAENPS_{year}{month}{day}_test.log")
if file_exists==False:
    processed_file_exists = exists(f"./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/CAENPS_{year}{month}{day}_test.log")
    file_exists = True if processed_file_exists == True else False

test_number = "2" if file_exists == True else ""
file_name = f"./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/CAENPS_{year}{month}{day}_test{test_number}.log"
print(file_name)
print(time) 
operator = input("Operator: ")
if operator == "stop":
    exit()
DC_tube_IDs = " "
while True:
    this_tube = input("Tube ID: ")
    if this_tube != "stop":
        DC_tube_IDs += (this_tube) + " "  
    if this_tube == "stop":
        break
print(DC_tube_IDs)
print(len(DC_tube_IDs)//8)

with open("./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/_CAENPS_2022MMDD_template.log", 'r') as Template:
    with open(file_name, 'a') as Output:
        lines = Template.readlines()
        Output.write(lines[0])
        Output.write(lines[1].replace("Evan", f"{operator}"))
        Output.write(lines[2].replace("2022-XX-XX XX:XX:00", f"{year}-{month}-{day} {time}"))
        Output.writelines(lines[3:13])
        Output.write(lines[14][0:15]+ DC_tube_IDs + "\n")
        Output.write(lines[15])

