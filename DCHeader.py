'''
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

from datetime import date, datetime
import pathlib
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

home = pathlib.Path.home()
GDrive_to_DB = pathlib.Path("Google Drive/Shared drives/sMDT Tube Testing Reports")
home_to_DB = pathlib.Path.joinpath(home, GDrive_to_DB) 
local_DC_folder = pathlib.Path("").absolute()


if home_to_DB.exists():
    path_to_Google_or_Local_file = pathlib.Path.joinpath(home_to_DB, "CAEN")
else:
    path_to_Google_or_Local_file = pathlib.Path.joinpath(local_DC_folder, "DC")
    print(f"\nCould not find Google Drive!") 

file_exists = pathlib.Path.joinpath(path_to_Google_or_Local_file, f"CAENPS_{year}{month}{day}_test.log").exists()

if (file_exists==False) and (home_to_DB.exists()):
    processed_file_exists = exists(pathlib.Path.joinpath(home_to_DB, f"Processed/CAENPS_{year}{month}{day}_test.log"))
    file_exists = processed_file_exists # True or False




path_to_template = pathlib.Path.joinpath(path_to_Google_or_Local_file, "_CAENPS_2022MMDD_template.log")

try: 
    test_number = int(input("Test Number?: ")) if file_exists else ""
except ValueError:
    print(" \n\n Test Number must be a number, it is the number at end of the .log file \n 'CAENPS_20220707_test\x1b[32m2\x1b[0m.log' for example \n\n ")
    exit() 


# "\x1b[32m;5m this text is green \x1b[0m"

new_file_name = f"CAENPS_{year}{month}{day}_test{test_number}.log"

file_path = pathlib.Path.joinpath(path_to_Google_or_Local_file, new_file_name)
print(f"Saving to: {file_path.parent}/\x1b[32m{new_file_name}\x1b[0m")

operator = input("Operator: ")
if operator == "stop":
    exit()

print(f"Time:     {time}")
print("--------Begin Scanning--------")   
print("(type \x1b[37;5mstop\x1b[0m to finish)".center(40, " "))
print("(type \x1b[37;5mped\x1b[0m for pedestal)".center(40, " "))

'''
3) ###########################################################################################
'''

counter = 0
DC_tube_IDs = []
ID_set = set()
def add_tube_to_list(this_tube):
    global counter
    if (this_tube not in ID_set):
        ID_set.add(this_tube)
        DC_tube_IDs.append(this_tube)
    elif (this_tube in ID_set):
        counter -= 1
    counter +=  1
while True:
    board_number = 4 if counter <= 23 else 1 
    this_tube = input(f"Board {board_number} Position {counter % 24: >2}: ")


    if this_tube == "ped":
        new_file_name = f"CAENPS_{year}{month}{day}_Pedestal.log"

        file_path = pathlib.Path.joinpath(path_to_Google_or_Local_file, new_file_name)
        
        for i in range(1,49):
            this_tube = f"MSU{i:0>5}"
            print(this_tube)
            add_tube_to_list(this_tube)
        this_tube = "stop"
        print(f"Now saving to: {file_path.parent}/\x1b[32m{new_file_name}\x1b[0m")

    if (this_tube == "stop") or (this_tube == "MSU07373"):
        break
    add_tube_to_list(this_tube)
num_of_tubes = len(DC_tube_IDs)

print(f"Number of tubes: {num_of_tubes}")
ID_string = " ".join(DC_tube_IDs)

'''
4) ###########################################################################################
'''

finish = input("Finish and Write File? [y/n]: ")

if finish == "y" or finish == "MSU07373":
    pass
elif finish != "y":
    print("OK, no file made")
    exit()

'''
4) ###########################################################################################
'''

def variable_length_mapping(string:str, number_of_spaces_between_values:int): 
    '''
    Sometimes you will only want to do DC runs in groups of 12, 24, or 36 tubes instead of 48, 
    If you do a run with 12 tubes for example, you will have to use:
    12 positions instead of 48 for MappingToBoards, HVpowerSupplyID, Pedestal(nA), HighVoltage(V), and DateTime

    Instead of manually changing it whenever the need arises, this function will automatically set the correct length of values. 

    string is the line (MappingToBoards, HVpowerSupplyID, etc..) and number_of_spaces_between_values is what it says, because the number of spaces between each HVpowerSupplyID is different from each Pedestal value. 
    I would rather account for the variabile spaces instead of change the spacing on the template to be uniform because the only thing better than perfection is standardization. 
    '''
    beginning_info = string[0:16]
    string_of_just_values = string[16:].strip(" \n") # strip out " " and "\n" with " \n"
    list_of_values = string_of_just_values.split(" " * number_of_spaces_between_values)
    correctly_sized_list = list_of_values[0:num_of_tubes] # num_of_tubes is defined later as the length of the list of IDs
    string_with_correct_number_of_values = str(" "* number_of_spaces_between_values).join(correctly_sized_list)
    return beginning_info + " " * number_of_spaces_between_values + string_with_correct_number_of_values + "\n"


with open(path_to_template, 'r') as Template:
    with open(file_path, 'a') as Output:
        lines = Template.readlines()
        Output.writelines(lines[0])
        Output.writelines(lines[1].replace("Name", f"{operator}"))
        Output.writelines(lines[2].replace("2022-XX-XX XX:XX:00", f"{year}-{month}-{day} {time}"))
        Output.writelines(lines[3:10])
        Output.writelines(variable_length_mapping(lines[10], 1)) # Excuse the boilerplate,
        Output.writelines(variable_length_mapping(lines[11], 4)) # but I will not change the spacing between the values in the template file. 
        Output.writelines(variable_length_mapping(lines[12], 6)) # Maybe there is still an even more clever solution to this though!
        Output.writelines(variable_length_mapping(lines[13], 5))
        Output.writelines(lines[14][0:17] + ID_string + "\n")
        Output.writelines(variable_length_mapping(lines[15], 1))

print("\n\n All Done! :) \n\n")