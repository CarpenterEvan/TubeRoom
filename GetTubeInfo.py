                                                                        #
__author__ = "Evan Carpenter"
__version__ = "4.1"

import os
from re import match
import pandas as pd
from datetime import datetime, timedelta

home = os.path.expanduser("~")
home_to_google_drive_database = os.path.expanduser("~/Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt")
path_to_local = os.path.join(os.getcwd(), "TUBEDB.txt") # os.path.join(os.path.abspath(""), "Verifying", "TUBEDB.txt")


__doc__ = '''

This is a module designed to take in the ID of an sMDT barcode, 
and not only find it in the TUBEDB.txt file, which is stored in the 
Google Drive, but to format the values so that the result is easy to read. 
In case you are new to lab, the terms used: 
BT: Bend Test
DC: Dark Current test
T1: Frist tension test
T2: second tension test

'''



green_text  = lambda x: f'\x1b[32m{x}\x1b[0m' # It seems that this adds +9 to length of string
red_text    = lambda x: f'\x1b[31m{x}\x1b[0m'
white_text  = lambda x: f'\x1b[39m{x}\x1b[0m'
flashing_red= lambda x: f'\x1b[31;5m{x}\x1b[0m' # This adds +11 to length



def color_string(string, goal):
    '''Colors a string green or red using ANSI escape codes depending on if the string matches the goal. 
    ex: a pass for 2nd tension can look like 'Pass2' or 'Pass2*'
    ex: a pass for DC can look like 'OK' or 'BAD' '''
    passes = match(string, goal)
    if passes:
        return (green_text(string), True)
    elif not passes: 
        return (red_text(string), False)
        
def copy_DB_file_if_available():
    operating_system = os.uname().sysname # "Darwin"==Mac "Linux"==Linux "Windows"==Windows

    if operating_system != "Windows":
        copy_command = "cp"
    else: 
        copy_command = "copy"

    os.system(f"{copy_command} '{home_to_google_drive_database}' {path_to_local}")

def format_database():
    '''Opens Google Drive path to get to the .txt file in the shared drive, 
    hoping to change this in the future to reduce dependency on Google Drive Desktop...'''
    try:

        df = pd.read_csv(home_to_google_drive_database,
                        names = ["ID", "T1", "T2", "DC", "FV"],  
                        delimiter = "|",
                        memory_map = True,
                        dtype=str).dropna(axis=0)
        path_used = home_to_google_drive_database
        copy_DB_file_if_available()

    except FileNotFoundError:

        print(f'''
        
              1.) Hmm... Could not access {home_to_google_drive_database}
              2.) Trying local path {path_to_local}  

              ''')

        try: 

            df = pd.read_csv(path_to_local, 
                             names = ["ID", "T1", "T2", "DC", "FV"],  
                             delimiter = "|",
                             memory_map = True,
                             dtype=str).dropna(axis=0)

            path_used = path_to_local

        except FileNotFoundError:

            exit(f"\t3.) If you get this message, still could not find TUBEDB.txt, either install Google Drive Desktop or copy TUBEDB.txt from the Google Drive into: \n\t\t{os.path.dirname(path_to_local)}\n")

    if __name__ == "GetTubeInfo": # as opposed to "__main__" meaning this is running in a different file

        print(f"Database File is from: {path_used}")
        print(f"Last Updated:", datetime.fromtimestamp(os.path.getmtime(path_used)))

    df = df.applymap(lambda string: " ".join(string.split())) # "1   2 3     4  5"  -->  "1 2 3 4 5"
    df = df.applymap(lambda string: string.split(" ")) # "1 2 3 4 5"  -->  ["1", "2", "3", "4", "5"]

    ID = pd.DataFrame(df["ID"].tolist()[2:], columns=["tubeID",  "End",     "Received", "leakrate", "bend", "flagE"])
    T1 = pd.DataFrame(df["T1"].tolist()[2:], columns=["T1Date", "Length", "Frequency",  "Tension",  "flag", "L"])
    T2 = pd.DataFrame(df["T2"].tolist()[2:], columns=["dFrequency",  "dTension",   "dDays",    "flag2"])
    DC = pd.DataFrame(df["DC"].tolist()[2:], columns=["DCday",   "sys",     "DC",   "HVseconds",     "DCflag"])
    FV = pd.DataFrame(df["FV"].tolist()[2:], columns=["ENDday",  "done?",   "ok",       "Comment",   "None", "None"])

    newdf = pd.concat((ID, T1, T2, DC, FV), axis=1)

    return newdf

DB = format_database()

def locate_tube_row(input_tubeID:str):
    '''Takes in a tube's ID and finds the ID in the tubeID column of the dataframe. 
    There are three default letters that I use for quick testing which translate to IDs: d, f, b.
    If something not of the form MSU[0-9]{5} (MSU followed by 5 numbers) is entered, the defaults are checked
    If the ID is not found, the row returned is -1 '''

    global DB

    defaults = {"d": "MSU05122", # default (good)
                "f": "MSU01341", # fails multiple tests
                "b": "MSU00229"} # bad, multiple tests missing, good for testing "-----"

    tubeID = input_tubeID
    try:
        looks_like_tube_ID = match("MSU[0-9]{5}", tubeID) != None

        if looks_like_tube_ID:
            pass 

        elif tubeID in defaults.keys():
                tubeID = defaults[tubeID] # Default
        else: 
            return -1


        tuberow_index, = DB["tubeID"].index[ DB["tubeID"].str.contains(tubeID) ] # index of the row with True, which is the only row with the ID
        # "tuberow_index, " unpacks just the first value of the tuple into the variable tuberow
        return tuberow_index     

    except ValueError: # This means the ID is valid but not in the DB
        return -2 
        
def filter_columns(tuberow_index):
    '''Given a specific row, filter out the values of interest (*). 
        A tyical 'row' object for a given ID looks like:
       -------------------------------
       || tubeID          MSU05123 ||  0
       || End                 IHEP ||  1   Endplug type
       || Received      2021-06-23 ||  2   Shipment date
       || leakrate        3.04E-06 ||  3 
       || bend                0.00 ||  4 
       || flagE               PASS ||  5 * Bend Flag
       || T1Date          21-07-07 ||  6 * Measured on 1st UM Tension
       || Length           1624.72 ||  7 * Measured on 1st UM Tension
       || Frequency           95.0 ||  8 
       || Tension          362.971 ||  9 * Date of 1st UM Tension
       || flag                pass || 10 * 1st Tension flag
       || L                      B || 11   Length Category
       || dFrequency          0.50 || 12 
       || dTension          -3.831 || 13 *
       || dDays                13D || 14 *
       || flag2              Pass2 || 15 * 2nd Tension flag
       || DCday           21-06-23 || 16
       || sys                 CAEN || 17   DC on CAEN or UM
       || DC                  0.32 || 18 * Value of DC
       || HVseconds          54820 || 19 * TOTAL time at 2900 V
       || DCflag                OK || 20 *
       || ENDday          21/07/07 || 21 
       || done?                  3 || 22 
       || ok                   YES || 23 * Final Pass
       || Comment               UM || 24 
       || None             BIS1A12 || 25   Extra comment
       || None                None || 26   Extra comment
       || Name: 4407, dtype: object|| 
       -------------------------------''' 
    fullrow = DB.iloc[tuberow_index]
    row = {"tubeID"           :    fullrow.tubeID,

           "Shipment_date"    :  fullrow.Received,

           "Bend_flag"        :     fullrow.flagE,
           "T1_date"          :    fullrow.T1Date,
           "T1_length"        :    fullrow.Length,

           "T1_tension"       :   fullrow.Tension,
           "T1_flag"          :      fullrow.flag,


           "T2_tension_delta" :  fullrow.dTension,
           "T2_time_delta"    :     fullrow.dDays,
           "T2_flag"          :     fullrow.flag2,

           "DC_date"          :     fullrow.DCday,

           "DC_DC"            :        fullrow.DC,
           "DC_seconds"       : fullrow.HVseconds,
           "DC_flag"          :    fullrow.DCflag,


           "Final_flag"       :        fullrow.ok}
    return row

def format_tension(row):
    '''
    Given a certain row, extract the values related to tension. 
    Check if both tension tests have been done. 
    
    If both have been done, figure out what the previous tension was, 
        assign it to T1, assign the current tension to T2

    If only the first test has been done, 
        see how many days until the second test can be done. 
        return dashes for T2.
    
    If neither test has been done, return dashes ("---") 
    '''
    try:
        
        T1_date = row["T1_date"] 
        T1_tension  = float(row["T1_tension"])
        T1_length   = float(row["T1_length"])
        valid_T1_string = True
    except ValueError:
        
        T1_date = "01-01-01"
        T1_tension  = 0.
        T1_length   = 0.
        valid_T1_string = False
        
    try:

        T2_tension_delta = float(row["T2_tension_delta"])
        T2_time_delta = int(row["T2_time_delta"][:-1]) # 13D --> 13
        valid_T2_string = True

    except ValueError: 

        T2_tension_delta =  0.
        T2_time_delta = 0
        valid_T2_string = False

    T1_datetime = datetime.strptime(T1_date, "%y-%m-%d")
    T2_datetime_delta = timedelta(days = T2_time_delta)

    if valid_T1_string and valid_T2_string: 
        # Both measurements are done, 
        # this means the most recent tension test is in the T1 spot, 
        # and it's difference in time and tension are in the T2 spot. 
        # We need to subtract this difference to see the "true" T1, the test before the most recent one. 

        T2_date = datetime.strftime(T1_datetime, "%y-%m-%d")
        T2_tension = str(round(T1_tension,3))

        T1_date = datetime.strftime(T1_datetime - T2_datetime_delta, "%y-%m-%d")
        T1_tension = round(T1_tension - T2_tension_delta, 3)
    
        

    elif valid_T1_string and not valid_T2_string:
        # Only first measurement is taken, 
        # we don't have any deltas, so no subtraction for T1, and T2 is null

        T1_date = datetime.strftime(T1_datetime, "%y-%m-%d")
        T1_tension = T1_tension

        T2_date = "--------"
        T2_tension = "-------"
        T2_datetime_delta = datetime.today()-T1_datetime # If no T2 delta, then see how long it has been waiting

    else: 
        T1_date = "--------"
        T1_tension = "-------"
        T2_date = "--------"
        T2_tension = "-------"

    T2_days_delta = T2_datetime_delta.days

    # Remember, if there is no test for T2, T2_tension = "-------" 
    # then T2_days_delta is the calculated as the difference from T1 to today, 
    # I want that to display with different colors. 
    # If it has been less than 14 days, regardless of if there is a test, make T2_days_delta red.
    # If it has been at least 14 days, check if it has been tested, if there is a T2 test, make it white, if no test, make it green
    # If somehow a tube is none of these conditions, make it "---" as a safeguard 

    if (T2_days_delta < 14): 

        T2_days_delta = red_text(T2_days_delta)
 
    elif (T2_days_delta >= 14):

        if ("-" in T2_tension):

            T2_days_delta = green_text(T2_days_delta)

        else: 

            T2_days_delta = white_text(T2_days_delta)

    else: 
        T2_days_delta = white_text("---")

    return T1_date, T1_tension, T1_length, T2_date, T2_tension, T2_days_delta

def format_values(row:dict):
    '''

    Take in the filtered values from the row. 
    If they are measurement values attempt to convert them to a float. 
    If it is a flag indicating pass/fail, color it green/red accordingly

    return two dictionaries: one of the colored value and flag strings, and one of True/False for all 4 tests

    '''
    tubeID = row["tubeID"]
    shipment_date_string = row["Shipment_date"].strip()
    shipment_date = datetime.strptime(shipment_date_string, "%Y-%m-%d")

    Bend_flag, Bend_passed = color_string(row["Bend_flag"], "PASS")
    T1_flag, T1_passed = color_string(row["T1_flag"], "pass")
    T2_flag, T2_passed = color_string(row["T2_flag"], "Pass2")
    DC_flag, DC_passed = color_string(row["DC_flag"], "OK")


    T1_date, T1_tension, T1_length, T2_date, T2_tension, T2_days_delta = format_tension(row)


    DC_DC = row["DC_DC"]
    DC_date = row["DC_date"]

    try: 

        DC_seconds = int(row["DC_seconds"])
        DC_hours = DC_seconds // 3600
        DC_pass:bool = (DC_hours>=4) and DC_passed
        DC_minutes = (DC_seconds - DC_hours * 3600) // 60
        DC_seconds = DC_seconds - DC_minutes * 60 - DC_hours * 3600
        DC_total_time = f"{DC_hours:0>2}:{DC_minutes:0>2}:{DC_seconds:0>2}" 

    except ValueError:
        
        DC_total_time = "00:00:00"
        DC_pass = False

    good_tube_dict = {"Bend":Bend_passed, "T1":T1_passed, "T2":T2_passed, "DC":DC_pass}
    #good_tube = all([Bend_passed, T1_passed, T2_passed, DC_pass])
    value_dict = {"ID": tubeID,
                  "Ship_Date": shipment_date_string, "Bend_Flag":Bend_flag,
                  "T1_Date": T1_date, "T1_Flag": T1_flag, "T1_Tension": T1_tension, "T1_Length": T1_length,
                  "T2_Date": T2_date, "T2_Flag": T2_flag, "T2_Tension": T2_tension, "T2_time_delta": T2_days_delta, 
                  "DC_Date": DC_date, "DC_DC": DC_DC, "DC_Time": DC_total_time, "DC_Flag": DC_flag}

    return value_dict, good_tube_dict

def get_formatted_tuple(input_tubeID:str):
    '''
    Using the prompted input tube ID, attempt to use locate_tube_row to find the row. 
    Handle any errors thrown by locate_tube_row. 
    Use filter_columns to get out the values of the row
    Use format_values with the row to get the formatted dictionaries. 
    Use the formatted string dictionary to make a list of printable strings, 
        join them around a common separator and return the string. 
    return the boolean dictionary that sumarizes each test. 

    '''
    tuberow = locate_tube_row(input_tubeID)

    
    
    error_string = " | ".join([f"{input_tubeID: <8}", 
                                "----------", 
                                "Bend: ----", 
                                "T1 on -------- ---- ---.---g ----.--mm", 
                                "T2 on -------- (∆---) -----  ---.---g", 
                                "DC on -------- ---.--nA  --:--:--   ---", 
                                "Final: --- "])

    filler_string = "-"*len(error_string)
    
    if tuberow == -1:
        return filler_string, {"filler": False}
    elif tuberow == -2:
        return error_string, {"error": False}
    else: 
        pass


    row = filter_columns(tuberow)

    value, good_tube_dict = format_values(row)
    good_tube = all(good_tube_dict.values())

    print_list = [f"{value['ID']}",
                  f"{value['Ship_Date']: <10}", 
                  f"Bend: {value['Bend_Flag']: <12}",
                  f"T1 on {value['T1_Date']} {value['T1_Flag']: <12} {value['T1_Tension']:0<7}g {value['T1_Length']:0<7}mm",
                  f"T2 on {value['T2_Date']: <9}(∆{value['T2_time_delta']: >12}) {value['T2_Flag']: <15} {value['T2_Tension']:0<7}g",
                  f"DC on {value['DC_Date']} {value['DC_DC']: >6}nA {value['DC_Time']: ^10} {value['DC_Flag']: >13}"]
    if row["Final_flag"] == "YES" and good_tube:
        Final_flag = green_text(row["Final_flag"])
    else: 
        Final_flag = red_text(row["Final_flag"])

    print_list.append(f"Final: {Final_flag: <12}")
    final_string = f" | ".join(print_list)
    return final_string, good_tube_dict

def id_to_values(input_tubeID:str):
    '''Quick and easy use of functions to return the dictionaries of values. 
    This function does not handle errors from locate_tube_row'''
    tuberow_index = locate_tube_row(input_tubeID)
    row = filter_columns(tuberow_index)
    value_dict, good_tube_dict = format_values(row)
    return value_dict, good_tube_dict