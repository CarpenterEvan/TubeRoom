import os 
import sys
from datetime import datetime
import time
from GetTubeInfo import get_formatted_tuple
import GetTubeInfo

__author__ = "Evan Carpenter"



################################## Pre-defined values ##################################
global counter, dates_summary_dictionary, tests_summary_dictionary, tubeID_set
counter = 0
tests_summary_dictionary = {"BT_pass_TT_pass_DC_pass":0,

                            "BT_fail_TT_pass_DC_pass":0,
                            "BT_pass_TT_fail_DC_pass":0,
                            "BT_pass_TT_pass_DC_fail":0,

                            "BT_fail_TT_fail_DC_pass":0,
                            "BT_fail_TT_pass_DC_fail":0,
                            "BT_pass_TT_fail_DC_fail":0,

                            "BT_fail_TT_fail_DC_fail":0}
dates_summary_dictionary = dict()
tubeID_set = set()

############################## Process command line args ###############################
command_line_arguments = sys.argv
if len(command_line_arguments)>2:
    err_string = '''Only one option at a time:
        'write' to write to a file named
        'ordered' to make the ordered file for a mod chamber
        'check' to check the contents of a file that is just a list of IDs '''
    exit(err_string)

WriteFile = command_line_arguments[-1] == "write"  # This is just to record the tubes scanned to a file
OrderedFile = command_line_arguments[-1] == "ordered" # This saves the tubes in reverse order to a file, 
# I call it ordered because the order is very important,  the last tube scanned will be the first tube glued in. 

CheckFile = command_line_arguments[-1] == "check" # going through a file of tubes and putting them through the main function
SearchFor =  command_line_arguments[-1] == "search" # Still in progress.

if WriteFile:

    OrderedFile = False
    CheckFile = False

    file_name = f"Verified_{datetime.now().strftime('%Y%m%d%H')}.txt"
    file_path = os.path.join(os.path.abspath(""), "Verifying", file_name)
    VerifiedIDs = open(file_path, "a+") # Writes to a file with yyyymmdd format in name
    print(f"\x1b[32;5mRecording\x1b[0m: {file_path}") # Blinking green text "Recording"

elif OrderedFile:

    CheckFile = False

    module =     input("       Mod?: ")
    multilayer = input("MultiLayer?: ")
    layer =      input("     Layer?: ")
    if "stop" in [module, multilayer, layer]:
        exit()
    ordered_list = []

    file_name = f"Mod{module}_Multilayer{multilayer}_Layer{layer}.txt"

    folder_path = os.path.expanduser(f"~/Google Drive/Shared drives/sMDT Tube Testing Reports/OrderOfTubesInMod/Mod{module}")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else: pass

    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        exit(f"That file already exists at {file_path}!\nDo not overwrite!")

    OrderedIDs = open(file_path, "w")
    print(f"\x1b[32;5mMaking Ordered File\x1b[0m at: {file_path}")

else: 
    file_path = os.path # empty path (?)
    print("\x1b[31;5mNOT RECORDING\x1b[0m") # Blinking red text "NOT RECORDING"

###################################### Functions ######################################
def write_tube_to_file_or_append_to_ordered_list(tubeid):
    '''This adds a line to the written file or adds a tube to the ordered file. 
    I keep the ordered version as a list so it can be reversed in order at the end.'''
    if WriteFile:
        VerifiedIDs.writelines(tubeid)
    elif OrderedFile:
        ordered_list.append(tubeid + "\n")
    else: pass
def update_counter(tubeid, verify_string, good_tube_dict): 
    global counter
    counter = counter + 1  if counter<=9 else 1 # reset counter after counter = 10
    counter = counter if len(tubeid)!=0 else 0 # this is so you can hit enter (which is input as "") to reset the counter
    
    if len(good_tube_dict) == 1: # this is only true when the "filler" dictionary is passed for an error tube ID
        counter = 0

    # "\x1b[31m" is the beginning of a red colored text (see GetTubeInfo.red_text) 
    
    if "\x1b[31m" in verify_string:
        colored_counter = GetTubeInfo.red_text(counter) # coloring the counter helps find which index of the row is bad
    else: 
        colored_counter = GetTubeInfo.white_text(counter)

    if counter == 0:
        colored_counter =  GetTubeInfo.white_text("") # removing GetTubeInfo.white_text messes with padding

    return colored_counter
def add_to_summary_dictionaries(date_string, good_tube_dict):
    if date_string not in dates_summary_dictionary.keys():
        dates_summary_dictionary[date_string] = 0
    else: pass

    boolean_to_pass_fail = lambda boolean: "pass" if boolean else "fail"
    Bend = boolean_to_pass_fail(good_tube_dict["Bend"])
    Tens = boolean_to_pass_fail(good_tube_dict["T1"] and good_tube_dict["T2"])
    DC =  boolean_to_pass_fail(good_tube_dict["DC"])

    tests_summary_dictionary[f"BT_{Bend}_TT_{Tens}_DC_{DC}"] += 1
    dates_summary_dictionary[date_string] += 1


def finish_writing_files():
    '''closes the files if WriteFile, or reverses the order of the Ordered list and saves it all to a file. '''
    if WriteFile:
        VerifiedIDs.close()
    elif OrderedFile:
        ordered_list.reverse()
        OrderedIDs.writelines(ordered_list)
        OrderedIDs.close()
    else: pass
def print_summary_dictionary_and_exit():
        finish_writing_files()

        spacer  = chr(9552)*17 
        top_left, top_right = chr(9556), chr(9559)
        wall = chr(9553)
        separator_left, separator_right = chr(9568), chr(9571)
        bot_left, bot_right = chr(9562), chr(9565)


        cap_of_box =          top_left + spacer + top_right
        box_entry = lambda item:  wall +  item  + wall
        box_seperator = separator_left + spacer + separator_right
        U_of_box =            bot_left + spacer + bot_right
        

        print(f"{'Dates Summary': ^20} {'Tests Summary': ^20}")
        print(cap_of_box + " "*2 + cap_of_box)


        dates_list = [f" {item}: {dates_summary_dictionary[item]: >3} " for item in sorted(dates_summary_dictionary)]
        gc = GetTubeInfo.green_text(chr(10003)) # green check
        rx = GetTubeInfo.red_text(chr(10005)) # red X
        get_gc_or_rx_from_pass_fail = lambda string: string.replace("pass",gc).replace("fail",rx).replace("_"," ")

        tests_list = [ f"{get_gc_or_rx_from_pass_fail(item)} {tests_summary_dictionary[item]} " for item in tests_summary_dictionary.keys()]
        if len(dates_list) <8:
            for _ in range(10-len(dates_list)):
                dates_list.append(" "*len(dates_list[0]))

        for index, test in enumerate(tests_list):
            print(box_entry(dates_list[index]) + " "*2 +  box_entry(test))

        
        print(box_seperator + " "*2 + U_of_box)
        print(wall + f" {'Total:': ^11} {sum(dates_summary_dictionary.values()): >3} " + wall + f"    All done! {chr(2384)}  :)")

        print(U_of_box)
  
        exit("\n")



def main(inputs):

    tubeid = inputs

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT", "sal"]:
        print_summary_dictionary_and_exit()
    else: pass
    
    verify_string, good_tube_dict = get_formatted_tuple(tubeid)

    colored_counter = update_counter(tubeid, verify_string, good_tube_dict)

    date_string = verify_string[11:21]
    not_dashes = "---" not in date_string

    #This should be self consistent while looking for duplicates in the good/bad dictionary because a tube that is bad on first scan won't update to good while the program is running
    if not_dashes and tubeid not in tubeID_set:
        tubeID_set.add(tubeid)
        add_to_summary_dictionaries(date_string, good_tube_dict)
        write_tube_to_file_or_append_to_ordered_list(tubeid)

    print("", end="\033[1A")
    print(f"{verify_string} {colored_counter: >11}")

    if counter == 10:
        print("-"*170)

    return tubeid
def test_case():
    intro_string = "ID       | Ship. date | Bend test  | 1st-TT  Date        Tension  Length    | 2nd-TT  Date   (days)        Tension  | DC      Date      DC    Time on DC      | Final pass?"
    
    print(intro_string)
    print("-"*len(intro_string))
    print(" ")
    for _ in range(10):
        main("d"); print(" ")
        main("f"); print(" ")
        main("b"); print(" ")
    main("stop")
    return 0
if __name__ == "__main__":
    if sys.argv[-1]=="test":
            test_case()

    if not CheckFile:
        
        while True:
            main(input("Tube ID: "))

    if CheckFile:
        file_name = input("File Name [ModXX]: ")
        newlist = []
        if "Mod" in file_name:
            mod_dir = os.path.expanduser(f"~/Google Drive/Shared drives/sMDT Tube Testing Reports/OrderOfTubesInMod/Mod{file_name[3:]}")
            for file in os.scandir(mod_dir):
                a_file = os.path.join(mod_dir, file.name)
                tube_list = open(a_file, "r").readlines()
                newlist += [id.strip() for id in tube_list]
        else: 
            with open(file_name, 'r') as the_file:
                for tubeid in the_file.readlines():
                    newlist.append(tubeid)

        newlist.append("stop")

        for tube in newlist: 
            main(tube)
            print(" ")
    