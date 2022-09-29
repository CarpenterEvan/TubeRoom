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

from datetime import date, datetime
import os
in_file_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # ex. 2022-09-07 09:47:06
date_for_file_name = date.today().strftime("%Y%m%d")   # ex. 20220927

home = os.path.expanduser("~")
GDrive_to_DB = os.path.relpath("Google Drive/Shared drives/sMDT Tube Testing Reports")
home_to_DB = os.path.join(home, GDrive_to_DB) 
home_to_processed = os.path.join(home_to_DB, "Processed")

if os.path.exists(home_to_DB):
    path_to_Google_or_Local_file = os.path.join(home_to_DB, "CAEN")
else:
    print(f"\nCould not find Google Drive Desktop!") 
    path_to_Google_or_Local_file = os.path.join(os.getcwd(), "DC")

path_to_template = os.path.join(path_to_Google_or_Local_file, "_CAENPS_2022MMDD_template.log")




file_name = f"CAENPS_{date_for_file_name}_test.log"

def check_if_file_exists(file_name):
    
    file_exists = os.path.exists(os.path.join(path_to_Google_or_Local_file, file_name))

    if (file_exists==False) and (os.path.exists(home_to_DB)): # check if there is a file for today and it is just in the Processsed folder.
        processed_file = os.path.join(home_to_processed, file_name)
        processed_file_exists = os.path.exists(processed_file)
        file_exists = processed_file_exists

    return file_exists

def get_test_number(file_name):

    global test_number

    file_exists = check_if_file_exists(file_name)

    if file_exists:
        try: 
            test_number = int(input("Test Number?: "))
        except ValueError:
            exit(" \n\n Test Number must be a number, it is the number at end of the .log file \n 'CAENPS_20220707_test\x1b[32m2\x1b[0m.log' for example \n\n ")
            # "\x1b[32m;5m this text is green \x1b[0m"

        new_file_name = f"CAENPS_{date_for_file_name}_test{test_number}.log"
        new_file_exists = check_if_file_exists(new_file_name)

        if new_file_exists:
            print("That file exists! Try again")
            new_file_name = get_test_number(new_file_name) ###

    else: # so no file has been found
        test_number = ""
        new_file_name = file_name ###
        
    return new_file_name


if check_if_file_exists(file_name)==True:
    new_file_name = get_test_number(file_name)
    file_name = new_file_name
else: 
    file_name = file_name


file_path = os.path.join(path_to_Google_or_Local_file, file_name)

print(f"\nSaving to: {os.path.dirname(file_path)}/\x1b[32m{file_name}\x1b[0m")

operator = input("Operator: ")
if operator == "stop":
    exit()

print(f"Date/time: {in_file_date}\n")
print("--------Begin Scanning--------")   
print("(type \x1b[37;5mstop\x1b[0m to finish)".center(40, " "))
print("(type \x1b[37;5mped\x1b[0m for pedestal)".center(40, " "))



def add_tube_to_list(this_tube):
    '''After a tube is scanned, check if it ha already been scanned during this run. 
    If the tube has not been scanned (not in the set of TubeIDs), add it to the set of TubeIDs and append it to the ordered list of TubeIDs. 
    If the tube has been scanned, it is probably a duplicate of the one previously scanned, I decrease the counter because in the main loop the counter 
    determines the board position, I don't want the board position to keep going up if the tube is a duplicate'''
    global counter
    if (this_tube not in ID_set):
        ID_set.add(this_tube)
        DC_tube_IDs.append(this_tube)
    elif (this_tube in ID_set):
        counter -= 1
    counter +=  1


def final_confirm():

    finish = input("Finish and Write File? [y/n]: ")
    if finish == "y" or finish == "MSU07373":
        pass
    elif finish != "y":
        print("OK, no file made")
        exit()

def get_id_string():
    global counter, DC_tube_IDs, ID_set, num_of_tubes
    
    counter = 0
    DC_tube_IDs = []
    ID_set = set()
    
    while True:
        board_number = 4 if counter <= 23 else 1

        this_tube = input(f"Board {board_number} Position {counter % 24: >2}: ")

        if this_tube == "ped":
            global file_path
            new_file_name = f"CAENPS_{date_for_file_name}_Pedestal.log"

            file_path = os.path.join(path_to_Google_or_Local_file, new_file_name)

            for i in range(1,49):
                this_tube = f"MSU{i:0>5}"
                print(this_tube)
                add_tube_to_list(this_tube)
            this_tube = "stop"
            print(f"Now saving to: {os.path.dirname(file_path)}/\x1b[32m{new_file_name}\x1b[0m")

        if (this_tube == "stop") or (this_tube == "MSU07373"):
            num_of_tubes = len(DC_tube_IDs)
            print(f"Number of tubes: {num_of_tubes}")
            final_confirm()
            break
        add_tube_to_list(this_tube)

    ID_string = " ".join(DC_tube_IDs)
    return ID_string







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

def write_to_file(ID_string):
    with open(path_to_template, 'r') as Template:
        with open(file_path, 'a') as Output:
            lines = Template.readlines()
            Output.writelines(lines[0])
            Output.writelines(lines[1].replace("Name", f"{operator}"))
            Output.writelines(lines[2].replace("2022-XX-XX XX:XX:00", in_file_date))
            Output.writelines(lines[3:10])
            Output.writelines(variable_length_mapping(lines[10], 1)) # Excuse the boilerplate,
            Output.writelines(variable_length_mapping(lines[11], 4)) # but I will not change the spacing between the values in the template file. 
            Output.writelines(variable_length_mapping(lines[12], 6)) # Maybe there is still an even more clever solution to this though!
            Output.writelines(variable_length_mapping(lines[13], 5))
            Output.writelines(lines[14][0:17] + ID_string + "\n")
            Output.writelines(variable_length_mapping(lines[15], 1))

def main():
    ID_string = get_id_string()

    write_to_file(ID_string)
    
    print("\n\n All Done! :) \n\n")

if __name__=="__main__":
    main()