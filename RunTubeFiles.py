from GetTubeInfo import get_formatted_tuple
import re
import datetime 
import sys
import pathlib
counter = 0
global d,s # I use this dictionary and set to filter out duplicates
d = dict()
s = set()

WriteFile = ("clean" in sys.argv)
CheckFile = ("check" in sys.argv)
OrderedFile = ("ordered" in sys.argv)

def write_tube_to_file_or_append_to_ordered_list():
    if WriteFile:
        VerifiedIDs.write(tubeid)
        VerifiedIDs.write("\n")
    elif OrderedFile:
        ordered_list.append(tubeid)
        ordered_list.append("\n")
    else: pass
def finish_writing_files():
    if WriteFile:
        VerifiedIDs.close()
    elif OrderedFile:
        ordered_list.reverse()
        OrderedIDs.writelines(ordered_list[1:])
        OrderedIDs.close
    else: pass

if WriteFile:
    file_name = f"Verified_{datetime.date.today().strftime('%Y%m%d')}.txt"
    file_path = pathlib.Path.joinpath(pathlib.Path(__file__).absolute().parent,"outputs", file_name)
    VerifiedIDs = open(file_path, "a") # Writes to a file with yyyymmdd format in name
    print(f"\x1b[32;5mMaking Verified File\x1b[0m: {file_path}") # Blinking green text "CLEANING"
elif OrderedFile:
    multilayer = input("MultiLayer?: ")
    layer = input("     Layer?: ")
    ordered_list = []
    file_name = f"Multilayer{multilayer}_Layer{layer}_{datetime.date.today().strftime('%Y%m%d')}.txt"
    file_path = pathlib.Path.joinpath(pathlib.Path(__file__).absolute().parent,"outputs", file_name)
    OrderedIDs = open(file_path, "w")
    print(f"\x1b[32;5mMaking Ordered File\x1b[0m at: {file_path}")
else: 
    file_path = pathlib.Path("")
    print("\x1b[31;5mNOT RECORDING\x1b[0m") # Blinking red text "NOT RECORDING"

'''
if CheckFile:
    file_name = input("Name: ")
    tube_list = open(f"outputs/{file_name}", "r").readlines()
    newlist = [i.strip() for i in tube_list]
    newlist.append("stop")
#for tube in newlist: #tubeid = tube
# #if tubeid in match_list:
    #    print("\a")
'''
while True:
    tubeid = input("Tube ID: ")

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT", "SAL"]:
        finish_writing_files()
        for i in sorted(d):
            print(i, d[i])
        print("Total: ", sum(d.values()))
        print("\n All done! :) \n")
        exit()
    else: pass

    counter = counter + 1  if counter<=9 else 1
    counter = counter if len(tubeid)!=0 else 0 # this is so you can hit enter (which is input as "") to reset the counter

    verify_string, good_tube = get_formatted_tuple(tubeid)

    # good_tube is checked before adding the tubeid into the counting dictionary.
    # it is important only good tubes are counted when writing to a file, but
    # when not writing the file, I want to count every tube no matter what. 
    good_tube = good_tube if WriteFile=="True" else True 


    date_string = verify_string[11:21]
    not_dashes = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_string) != None 

    if (good_tube) and (not_dashes):
        if (date_string not in d.keys()):
            s.add(tubeid) 
            write_tube_to_file_or_append_to_ordered_list()
            d[date_string] = 1
        elif (tubeid not in s):
            s.add(tubeid)
            write_tube_to_file_or_append_to_ordered_list()
            d[date_string] += 1
        else: pass
    else: pass

    print("", end="\033[1A")
    print(verify_string, 
          counter if counter!=0 else "" )  

