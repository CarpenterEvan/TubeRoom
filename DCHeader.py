'''
The following text describes the code, use it as a reference, not a book!!
    1)  Get the date and time for today, I use the time and date in the file, and the date for the file name
            For example, CAENPS_20220512_test.log for 2022-05-12

    2)  However, if CAENPS_20220512_test.log already exists and the date has not changed, then the name should be 
            CAENPS_20220512_test2.log, so I check if a file of the same date already exists. 
            Just as an extra precaution, I have the code print what the name and time will be just to double check.
            The code then asks for the operator name. If the file name printed before it does not look good for some reason, 
            put the operator name as "stop" and it will exit the program. 

    3)  The code prompts for the tube IDs, after scanning all of them, it prints the IDs scanned for a double check.

    4)  Final yes/no verification before writing to the file. 

    5)  Writing to the file, I take the lines from the example file and replace the strings with the variables defined in the code
            I write with "a" to append, to further minimize the possibility of overwriting data
'''

from os.path import exists
from sys import exit
from datetime import date, datetime
'''
1) ###########################################################################################
'''
year = date.today().strftime("%Y")
month = date.today().strftime("%m")
day = date.today().strftime("%d")
time = datetime.now().strftime("%H:%M:%S")
in_file_date = f"{year}-{month}-{day}" # I use separate variable here because I also need to name the file.

'''
2) ###########################################################################################
'''

file_exists = exists(f"./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/CAENPS_{year}{month}{day}_test.log")
if file_exists==False:
    processed_file_exists = exists(f"./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/CAENPS_{year}{month}{day}_test.log")
    file_exists = processed_file_exists # True or False

try: 
    test_number = int(input("Test Number?: ")) if file_exists else ""
except ValueError:
    print(" \n\n Test Number must be a number, it is the number at end of the .log file \n '..._test\x1b[32m2\x1b[0m.log' for example \n\n ")
    exit() 

# \x1b[32m;5m this text is green \x1b[0m
file_name = f"./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/CAENPS_{year}{month}{day}_test{test_number}.log"
print(f"\nFile Name: \x1b[32mCAENPS_{year}{month}{day}_test{test_number}.log\x1b[0m")

operator = input("Operator: ")
if operator == "stop":
    exit()

print(f"Time:     {time}")
'''
3) ###########################################################################################
'''
counter = 0
DC_tube_IDs = []
ID_set = set()
while True:
    board_number = 4 if counter <= 23 else 1 
    this_tube = input(f"Board {board_number} Position {counter % 24: >2}: ")

    if this_tube == "stop":
        break
    if this_tube not in ID_set:
        ID_set.add(this_tube)
        DC_tube_IDs.append(this_tube)
    counter +=  1

print(DC_tube_IDs)
print(len(DC_tube_IDs))
ID_string = " ".join(DC_tube_IDs)
'''
4) ###########################################################################################
'''

finish = input("Finish? [y/n]: ")

if finish == "y":
    pass
elif finish != "y":
    exit()

'''
4) ###########################################################################################
'''

with open("./Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN/_CAENPS_2022MMDD_template.log", 'r') as Template:
    with open(file_name, 'a') as Output:
        lines = Template.readlines()
        Output.write(lines[0])
        Output.write(lines[1].replace("Evan", f"{operator}"))
        Output.write(lines[2].replace("2022-XX-XX XX:XX:00", f"{year}-{month}-{day} {time}"))
        Output.writelines(lines[3:14])
        Output.write(lines[14][0:16]+ ID_string + "\n")
        Output.write(lines[15])

print("\n\n All Done! :) \n\n")