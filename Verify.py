import pathlib
import sys
from datetime import date
from pathlib import Path
from re import match

import GetTubeInfo
from GetTubeInfo import get_formatted_tuple

__author__ = "Evan Carpenter"

counter = 0

good_dict, bad_dict = dict(), dict()
good_set, bad_set = set(), set()

WriteFile = ("save" in sys.argv) or ("record" in sys.argv) # This is just to record the tubes scanned to a file
OrderedFile = ("ordered" in sys.argv and not WriteFile) # For recording the order of tubes before they get glued into module
CheckFile = ("check" in sys.argv) # going through a file of tubes and putting them through the main function
SearchFor = ("search" in sys.argv) # searching for certain tubes, pritns a bell return when it's found

def write_tube_to_file_or_append_to_ordered_list(tubeid):
    if WriteFile:
        VerifiedIDs.writelines(tubeid)
    elif OrderedFile:
        ordered_list.append(tubeid + "\n")
    else: pass

def finish_writing_files():
    if WriteFile:
        VerifiedIDs.close()
    elif OrderedFile:
        ordered_list.reverse()
        OrderedIDs.writelines(ordered_list)
        OrderedIDs.close()
    else: pass

if WriteFile:

    file_name = f"Verified_{date.today().strftime('%Y%m%d')}.txt"
    file_path = Path.joinpath(Path(__file__).absolute().parent, "Verifying", file_name)

    VerifiedIDs = open(file_path, "a") # Writes to a file with yyyymmdd format in name
    print(f"\x1b[32;5mMaking Verified File\x1b[0m: {file_path}") # Blinking green text "Making Verified File"

elif OrderedFile:
    module = input("       Mod?: ")
    multilayer = input("MultiLayer?: ")
    layer = input("     Layer?: ")
    if "stop" in [module, multilayer, layer]:
        exit()
    ordered_list = []

    file_name = f"Mod{module}_Multilayer{multilayer}_Layer{layer}.txt"

    file_path = Path.joinpath(Path.home(), f"Google Drive/Shared drives/sMDT Tube Testing Reports/OrderOfTubesInMod/Mod{module}", file_name)
    print(file_path)

    if Path.exists(file_path):
        exit(f"That file already exists at {file_path}! Do not overwrite!")

    OrderedIDs = open(file_path, "w")
    print(f"\x1b[32;5mMaking Ordered File\x1b[0m at: {file_path}")
else: 
    file_path = Path("")
    print("\x1b[31;5mNOT RECORDING\x1b[0m") # Blinking red text "NOT RECORDING"




def main(inputs):
    global good_dict, good_set, bad_dict, bad_set, counter # I use this dictionary and set to filter out duplicates
    tubeid = inputs

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT", "SAL"]:
        spacer  = "--------------"
        finish_writing_files()

        print("\n" + spacer)

        for i in sorted(good_dict):
            print(i, good_dict[i])
        print("Total OK: ", sum(good_dict.values()))

        print(spacer)

        for i in sorted(bad_dict):
            print(i, bad_dict[i])
        print("Total Bad:", sum(bad_dict.values()))

        print(spacer*2)

        total_dict = {**good_dict, **bad_dict}
        for i in sorted(total_dict):
            print(f"{i} {total_dict[i]}")
        print(f"Total All: {sum(total_dict.values())} «")
        print(spacer)
        exit("\n All done! :) \n")
    else: pass

    counter = counter + 1  if counter<=9 else 1
    counter = counter if len(tubeid)!=0 else 0 # this is so you can hit enter (which is input as "") to reset the counter

    verify_string, good_tube = get_formatted_tuple(tubeid)

    date_string = verify_string[11:21]
    not_dashes = match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_string) != None 
    good_tube = True
    if (good_tube) and (not_dashes):
        d = good_dict
        s = good_set
    elif (not good_tube) and (not_dashes):
        d = bad_dict
        s = bad_set
    else: 
        dashes_dict = dict()
        dashes_set = set()
        d, s = dashes_dict, dashes_set
    #This should be self consistent looking for duplicates in the good/bad dictionary because a tube that is bad on first scan won't update to good while the program is running
    if (date_string not in d.keys()): 
        s.add(tubeid) 
        write_tube_to_file_or_append_to_ordered_list(tubeid)
        d[date_string] = 1
    elif (tubeid not in s):
        s.add(tubeid)
        write_tube_to_file_or_append_to_ordered_list(tubeid)
        d[date_string] += 1

    print("", end="\033[1A")
    print(verify_string, 
          counter if counter!=0 else "")

    if counter == 10:
        print("-"*166)
    return tubeid


if not CheckFile:
    while True:
        main(input("Tube ID: "))

if CheckFile:
    file_name = input("File Name: ")
    newlist = []

    if "Mod" in file_name:
        for file in Path.joinpath(Path.home(), f"Google Drive/Shared drives/sMDT Tube Testing Reports/OrderOfTubesInMod/Mod{file_name[3:]}").glob(f"Mod{file_name[3:]}*.txt"):
            tube_list = open(file, "r").readlines()
            newlist += [id.strip() for id in tube_list]
    else: 
        with open(file_name, 'r') as the_file:
            for tubeid in the_file.readlines():
                newlist.append(tubeid)

    newlist.append("stop")

    for tube in newlist: 
        main(tube)
        print(" ")

