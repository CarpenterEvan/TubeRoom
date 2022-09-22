
import pathlib
import sys
import os.path
from datetime import date, datetime
from pathlib import Path
from re import match

from GetTubeInfo import get_formatted_tuple



__author__ = "Evan Carpenter"

counter = 0

WriteFile = ("save" in sys.argv) or ("record" in sys.argv) # This is just to record the tubes scanned to a file
OrderedFile = ("ordered" in sys.argv and not WriteFile) # For recording the order of tubes before they get glued into module
CheckFile = ("check" in sys.argv) # going through a file of tubes and putting them through the main function
SearchFor = ("search" in sys.argv) # searching for certain tubes, pritns a bell return when it's found

def write_tube_to_file_or_append_to_ordered_list(tubeid):
    '''This adds a line to the written file or adds a tube to the ordered file. 
    I keep the ordered version as a list so it can be reversed in order at the end. 
    This can also be done with a file, but if there is an error in the scanning during a write file, I want to save the intermediate output, 
    wheras the ordered file should be made all at once with no interruption--> 
    an error should not result in a partially complete file, it should result in no file.'''
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

    folder_path = Path.joinpath(Path.home(), f"Google Drive/Shared drives/sMDT Tube Testing Reports/OrderOfTubesInMod/Mod{module}")
    if not Path.exists(folder_path):
        Path.mkdir(folder_path)
    else: pass

    file_path = Path.joinpath(folder_path, file_name)

    if Path.exists(file_path):
        exit(f"That file already exists at {file_path}! Do not overwrite!")

    OrderedIDs = open(file_path, "w")
    print(f"\x1b[32;5mMaking Ordered File\x1b[0m at: {file_path}")
else: 
    file_path = Path("")
    print("\x1b[31;5mNOT RECORDING\x1b[0m") # Blinking red text "NOT RECORDING"


tests_summary_dictionary = {"Bend":0,  
                            "T1":0, 
                            "T2":0, 
                            "DC":0,
					        "total":0}


def add_to_summary_dictionaries(date_string, good_tube_dict):
    global dates_summary_dictionary, tests_summary_dictionary

    if date_string not in dates_summary_dictionary.keys():
        dates_summary_dictionary[date_string] = 0
    else: pass
    

    for i in good_tube_dict.keys():
        if good_tube_dict[i] == True:
            tests_summary_dictionary[i] += 1
        else: pass
    dates_summary_dictionary[date_string] += 1
    tests_summary_dictionary["total"] += 1
    
    
    


dates_summary_dictionary, tubeID_set = dict(), set()

def main(inputs):
    global dates_summary_dictionary, tubeID_set, counter # I use this dictionary and set to filter out duplicates
    tubeid = inputs

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT", "sal"]:
        spacer  = "--------------"
        finish_writing_files()

        print("\n" + spacer)

        for i in sorted(dates_summary_dictionary):
            print(i, dates_summary_dictionary[i])
        print("Total: ", sum(dates_summary_dictionary.values()))

        print(spacer)
        #total = tests_summary_dictionary['total']
        #for i in sorted(tests_summary_dictionary)[:-1]:
        #    print(f"Passed {i: ^4} test: {tests_summary_dictionary[i]}  |  Failed/Need {i: ^4} test: {total - tests_summary_dictionary[i]}")
        #print(f"Total Scanned: {total} «")
        #print(spacer)
        exit("\n All done! :) \n")
    else: pass

    counter = counter + 1  if counter<=9 else 1
    counter = counter if len(tubeid)!=0 else 0 # this is so you can hit enter (which is input as "") to reset the counter

    verify_string, good_tube_dict = get_formatted_tuple(tubeid)
    if len(good_tube_dict) == 1:
        counter = 0
        
    good_tube = all(good_tube_dict.values())

    date_string = verify_string[11:21]
    not_dashes = match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_string) != None 


    #This should be self consistent looking for duplicates in the good/bad dictionary because a tube that is bad on first scan won't update to good while the program is running

    if not_dashes and tubeid not in tubeID_set:
        tubeID_set.add(tubeid)
        add_to_summary_dictionaries(date_string, good_tube_dict)
        write_tube_to_file_or_append_to_ordered_list(tubeid)

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

