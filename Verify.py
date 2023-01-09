import re
import os 
import sys
from datetime import datetime
from GetTubeInfo import get_formatted_tuple
import GetTubeInfo

__author__ = "Evan Carpenter"
__verison__ = "6.2"
__doc__ = ''' 
Verify is meant to handle the logistics of multiple scans.
counter counts up to 10 and resets, printing a line of '-' when it does. 
There are options to save the tubes scanned into a file, or to read tubeids from a file. 
During a run the data from each tube is saved and summarized at the end in a fancy unicode box. 

run 'python verify.py test' to make sure this runs properly,

Since this uses GetTubeInfo all of the depencencies related to the Google Drive apply here as well: 
if Google Drive desktop cannot be found, the code will look for TUBEDB.txt in the same folder as Verify.py
'''

### Potential Updates: 
#    Warning: Currently, allowing for updating the DB live, during a run of this code
#             is something I have considered, but it could also break the current method 
#             of making the summary of the tubes. 
#
#
#

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
table_dictionary = {"BT":0, "TT":0, "DC":0}

dates_summary_dictionary = dict()
table_summary_dictionary = dict()
tubeID_set = set()
terminal_width = GetTubeInfo.terminal_width
############################## Process command line args ###############################
Nexargs = len(sys.argv)-1 # Number of extra arguments 
first_argument = sys.argv[-Nexargs]


OrderedFile = (first_argument == "ordered") # This saves the tubes in reverse order to a file, 
# I call it ordered because the order is very important,  the last tube scanned will be the first tube glued in. 
WriteFile   = (first_argument == "write") # This is just to record the tubes scanned to a file
CheckFile   = (first_argument == "check") # going through a file of tubes and putting them through the main function
SearchFor   = (first_argument == "search") # Still in progress.

dont_use_seperator = "-smush" in sys.argv
no_color_bool = "-bland" in sys.argv


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
elif SearchFor:
    with open(input("Input file with IDs to search for: "), "r") as the_file:
        target_list = re.findall("MSU[0-9]{5}", the_file.read())
else: 
    file_path = os.path # empty path (?)
    print("\x1b[31;5mNOT RECORDING\x1b[0m") # Blinking red text "NOT RECORDING"

###################################### Functions ######################################
def write_tube_to_file_or_append_to_ordered_list(tubeid):
    '''This adds a line to the written file or adds a tube to the ordered file. 
    I keep the ordered version as a list so it can be reversed in order at the end.'''
    if WriteFile:
        VerifiedIDs.write(tubeid + "\n")
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
    if "filler" in good_tube_dict.keys():
        return 0
    if date_string not in dates_summary_dictionary.keys():
        dates_summary_dictionary[date_string] = 0
    else: pass
    
    boolean_to_pass_fail = lambda boolean: "pass" if boolean else "fail"
    try:
        Bend = boolean_to_pass_fail(good_tube_dict["Bend"])
        Tens = boolean_to_pass_fail(good_tube_dict["T1"] and good_tube_dict["T2"])
        DC =  boolean_to_pass_fail(good_tube_dict["DC"])
    except KeyError:
        print(good_tube_dict)
        exit("Uh oh, a key error was found.\nI'm expecting the keys to be 'Bend', 'T1', 'T2', 'DC'")

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

def compile_summary_dictionaries():
    # find the max value, find how many characters it is, pick the bigger one
    if len(dates_summary_dictionary) == 0:
        dates_summary_dictionary["xxxx-xx-xx"] = 0
        longest_number = 1
    else:
        longest_number = len(str(sum(dates_summary_dictionary.values())))
    

    gc = GetTubeInfo.green_text(chr(10003)) # green check ✓
    rx = GetTubeInfo.red_text(chr(10005)) # red X ✕
    
    # get green check or red x from pass fail. 
    get_gc_or_rx_from_pass_fail = lambda string: string.replace("pass",gc).replace("fail",rx).replace("_"," ") 
    # "BT_pass_TT_pass_DC_fail" -> "BT ✓ TT ✓ DC ✕ "
    # len(string) is 38
    # but apparent length is 15

    tests_found_during_scanning = [test for test in tests_summary_dictionary.keys() if tests_summary_dictionary[test] !=0]
    tests_list = [ f" {get_gc_or_rx_from_pass_fail(test)} {tests_summary_dictionary[test]: >{longest_number}} " for test in tests_found_during_scanning]
    dates_list = [f" {date}: {dates_summary_dictionary[date]: >{longest_number}} " for date in sorted(dates_summary_dictionary)]
    dates_total = f" {'Total:': ^11} {sum(dates_summary_dictionary.values()): >{longest_number}} "

    filler_list = lambda width: [" " * width for _ in range(abs(    len(tests_list) - len(dates_list)    ))]

    width_of_dates_list = 14 + longest_number # len(" 2022-09-20:  N ") = 14, len(N) <= longest_number 
    width_of_tests_list = 17 + longest_number # len(" BT ✓ TT ✓ DC ✓ N ") = 17, len(N) <= longest_number

    if len(dates_list) < len(tests_list): # tests box is longer than dates box
        dates_list += filler_list(width_of_dates_list)
    elif len(dates_list) > len(tests_list): # dates box is longer than tests box
        tests_list += filler_list(width_of_tests_list)
    return dates_list, dates_total, width_of_dates_list, tests_list, width_of_tests_list

def print_summary_dictionary_and_exit():
        finish_writing_files()

        dates_list, dates_total, width_of_dates_list,\
            tests_list, width_of_tests_list = compile_summary_dictionaries()
        
        
        final_message = f"All done! {chr(9835)} :)".center(width_of_tests_list+2, " ")

        top_left, top_right = chr(9556), chr(9559)
        wall = chr(9553)
        horizontal = chr(9552)
        T_left, T_right = chr(9568), chr(9571) # T rotated left or T rotated right
        bot_left, bot_right = chr(9562), chr(9565) # bottom left and right corners
        
        spacer  = lambda left, length, right:   left + horizontal*length + right
        box_entry = lambda item:                wall +       item        + wall

        cap_of_box = lambda length: spacer(top_left, length, top_right)
        seperator_of_box = lambda length: spacer(T_left, length, T_right)
        U_of_box = lambda length: spacer(bot_left, length, bot_right)

        print("\n")
        longer_list = range(max(len(dates_list) , len(tests_list)))

        dates_title = "Dates Summary".center(width_of_dates_list+2, " ")
        tests_title = "Tests Summary".center(width_of_tests_list+2," ")

        print(                          dates_title + " "*2 + tests_title)
        print(      cap_of_box(width_of_dates_list) + " "*2 + cap_of_box(width_of_tests_list))
        [print(        box_entry(dates_list[index]) + " "*2 + box_entry(tests_list[index]) ) for index in longer_list]
        print(seperator_of_box(width_of_dates_list) + " "*2 + U_of_box(width_of_tests_list))
        print(               box_entry(dates_total) + " "*2 + final_message)
        print(        U_of_box(width_of_dates_list))
        #print("   date     total  BT  TT  DC")
        #for date in sorted(table_summary_dictionary):
        #    print(f"{date}:  {dates_summary_dictionary[date]}   {table_summary_dictionary[date]['BT']}  {table_summary_dictionary#[date]['TT']}  {table_summary_dictionary[date]['DC']}")
        exit("\n")

def main(inputs):
    tubeid = inputs

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT", "sal"]:
        print_summary_dictionary_and_exit()
    elif SearchFor and tubeid in target_list: 
        print("\a", end="\033[1A")
    else: pass

    print_list, good_tube_dict = get_formatted_tuple(tubeid, suppress_colors=no_color_bool)
    if "filler" not in good_tube_dict.keys() and "error" not in good_tube_dict.keys():
        verify_string = f" | ".join(print_list)
    else:
        verify_string = print_list

    colored_counter = update_counter(tubeid, verify_string, good_tube_dict)

    date_string = print_list[2]
    not_dashes = "---" not in date_string

    #This should be self consistent while looking for duplicates in the good/bad dictionary because a tube that is bad on first scan won't update to good while the program is running
    if not_dashes and tubeid not in tubeID_set:
        tubeID_set.add(tubeid)
        write_tube_to_file_or_append_to_ordered_list(tubeid)
        add_to_summary_dictionaries(date_string, good_tube_dict)

    print("", end="\033[1A")
    print(f"{verify_string} {colored_counter: >11}")

    if counter == 10 and not dont_use_seperator:
        print("-" * terminal_width)

    return tubeid

def test_case():
    intro_string = "ID       |UM/MSU| Ship. date | Bend test  | 1st-TT  Date        Tension  Length    | 2nd-TT  Date   (days)        Tension  | DC      Date      DC    Time on DC      | Final pass?"
    
    print(intro_string)
    print("-"*len(intro_string))
    print(" ")
    
    main("d"); print(" ")
    main("f"); print(" ")
    main("b"); print(" ")
    main("t1"); print(" ")
    main("t4"); print(" ")
    main("t2"); print(" ")
    main("t3"); print(" ")
    main("t4"); print(" ")
    main("d"); print(" ")
    main("f"); print(" ")

    main("d"); print(" ")
    main("f"); print(" ")
    main("b"); print(" ")
    main("t1"); print(" ")
    main("t4"); print(" ")
    main(""); print(" ")
    main("t2"); print(" ")
    main("t3"); print(" ")
    main("t4"); print(" ")
    main("d"); print(" ")
    main("f"); print(" ")
    
    main("stop")
    return 0

######################################## Main ########################################

if __name__ == "__main__":

    if first_argument=="test":
            test_case()

    if not CheckFile:
        while True:
            main(input("Tube ID: "))

    if CheckFile:
        
        file_name = input("File Name [ModXX]: ")
        
        print(" ")
        newlist = []
        if "Mod" in file_name:
            mod_dir = os.path.expanduser(f"~/Google Drive/Shared drives/sMDT Tube Testing Reports/OrderOfTubesInMod/Mod{file_name[3:]}")
            try:
                for file in os.scandir(mod_dir):
                    a_file = os.path.join(mod_dir, file.name)
                    tube_list = open(a_file, "r").readlines()
                    newlist += [id.strip() for id in tube_list]
            except FileNotFoundError:
                exit("Sorry, but either that file doesn't exist, or I can't see it from here!")
        else: 
            try:
                with open(file_name, 'r') as the_file:
                    newlist = re.findall("MSU[0-9]{5}", the_file.read())
            except FileNotFoundError:
                exit("Sorry, but either that file doesn't exist, or I can't see it from here!")

        newlist.append("stop")
        for tube in newlist: 
            main(tube)
            print(" ")
