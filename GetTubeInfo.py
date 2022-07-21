import os
import re
import pandas as pd
from datetime import datetime, timedelta
import pathlib

home = pathlib.Path.home()
GDrive_to_DB = pathlib.Path("Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt")
final = pathlib.Path.joinpath(home, GDrive_to_DB)
__author__ = "Evan Carpenter"
__version__ = "3"


green_text  = lambda x: f"\x1b[32m{x}\x1b[0m" # I don't know how this affects string length
red_text    = lambda x: f"\x1b[31m{x}\x1b[0m"
flashing_red= lambda x: f"\x1b[31;5m{x}\x1b[0m"

def color_string(string, goal):
    '''Colors a string green or red using ANSI escape codes depending on iff the string matches the goal'''
    
    passes = re.match(string, goal)
    if passes:
        return (green_text(string), True)
    elif not passes: 
        return (red_text(string), False)

def Format_Database():
    '''Opens Google Drive path to get to the .txt file in the shared drive, hoping to change this in the future to reduce dependency on Google Drive Desktop...'''
    path = final
    try:
        df = pd.read_csv(path, 
                        names = ["ID", "T1", "T2", "DC", "FV"],  
                        delimiter = "|",
                        memory_map = True)
    except FileNotFoundError:
        print("FileNotFoundError: Couldn't reach TUBEDB.txt, maybe Google Drive is not reachable from here?")
        print("                   Check where your Google Drive Desktop is installed")
        print("                   You want to access ./Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt")
        print(f"                   This file is in {__file__}")
        exit()
    print("Last Updated:", datetime.fromtimestamp(os.path.getctime(path)))
    df = df.applymap(lambda string: " ".join(string.split()))
    df = df.applymap(lambda string: string.split(" "))
    ID = pd.DataFrame(df["ID"].tolist()[2:], columns=["tubeID",  "End",     "Received", "leakrate", "bend", "flagE"])
    T1 = pd.DataFrame(df["T1"].tolist()[2:], columns=["T1Date", "Length", "Frequency",  "Tension",  "flag", "L"])
    T2 = pd.DataFrame(df["T2"].tolist()[2:], columns=["dFrequency",  "dTension",   "dDays",    "flag2"])
    DC = pd.DataFrame(df["DC"].tolist()[2:], columns=["DCday",   "sys",     "DC",   "HVseconds",     "DCflag"])
    FV = pd.DataFrame(df["FV"].tolist()[2:], columns=["ENDday",  "done?",   "ok",       "Comment",   "None", "None"])
    newdf = pd.concat((ID, T1, T2, DC, FV), axis=1)
    return newdf

global DB # Declare global variables so I can access them inside functions
DB = Format_Database()

def Locate_Tube_Row(input_tubeID:str):
    '''Takes in a tube's ID and finds the ID in the tubeID column of the dataframe. 
    There are three default letters that I use for quick testing which translate to IDs: d, f, b.
    If something not of the form MSU[0-9]{5} (MSU followed by 5 numbers) is entered, the defaults are checked
    If the ID is not found, the row returned is -1 '''

    defaults = {"d": "MSU05123", # default (good)
                "f": "MSU01341", # fails multiple tests
                "b": "MSU00229"} # multiple tests missing "-----"
    tubeID = input_tubeID
    try:
        istube = re.match("MSU[0-9]{5}", tubeID) 
        assert istube # this will raise an AssertionError if the ID does not look like "MSU" followed by 5 numbers
        # "tuberow, " unpacks just the first value of the tuple into the variable tuberow
        tuberow, = DB["tubeID"].index[ DB["tubeID"].str.contains(tubeID) ] # index of the row with True, which is row with ID
        return tuberow     
    except AssertionError: # This means ID was not valid, possibly a default key
        if len(tubeID) == 1 and tubeID in defaults.keys():
                tubeID = defaults[tubeID] # Default
                tuberow, = DB["tubeID"].index[ DB["tubeID"].str.contains(tubeID) ] # index of the row with True, which is row with ID
                return tuberow
        else: 
            return -1
    except ValueError: # This means the ID is valid but not in the DB
        return -2 
        
def Filter_Columns(tuberow):
    '''A tyical 'row' object for a given ID looks like:
       -------------------------------
       || tubeID          MSU05123 || 0
       || End                 IHEP || 1  Endplug type
       || Received      2021-06-23 || 2  
       || leakrate        3.04E-06 || 3  
       || bend                0.00 || 4  
       || flagE               PASS || 5  Bend Flag
       || T1Date          21-07-07 || 6  Measured on 1st UM Tension
       || Length           1624.72 || 7  Measured on 1st UM Tension
       || Frequency           95.0 || 8  
       || Tension          362.971 || 9  Date of 1st UM Tension
       || flag                pass || 10 1st Tension flag
       || L                      B || 11 Length Category
       || dFrequency          0.50 || 12 
       || dTension          -3.831 || 13
       || dDays                13D || 14
       || flag2              Pass2 || 15 2nd Tension flag
       || DCday           21-06-23 || 16
       || sys                 CAEN || 17 DC on CAEN or UM
       || DC                  0.32 || 18 
       || HVseconds          54820 || 19 TOTAL time at 2900 V
       || DCflag                OK || 20 
       || ENDday          21/07/07 || 21
       || done?                  3 || 22
       || ok                   YES || 23
       || Comment               UM || 24
       || None             BIS1A12 || 25
       || None                None || 26
       || Name: 4407, dtype: object|| 
       -------------------------------''' 
    fullrow = DB.iloc[tuberow]
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

def Format_Values(row:dict):
    tubeID = row["tubeID"]
    shipment_date = row["Shipment_date"]
    Bend_flag, Bend_passed = color_string(row["Bend_flag"], "PASS")
    T1_flag, T1_passed = color_string(row["T1_flag"], "pass")
    T2_flag, T2_passed = color_string(row["T2_flag"], "Pass2")
    DC_flag, DC_passed = color_string(row["DC_flag"], "OK")
    try:
        T1_date:str = row["T1_date"]
        T1_tension  = float(row["T1_tension"])
        T1_length   = float(row["T1_length"])
    except ValueError:
        T1_date = "11-11-11"
        T1_tension  = 0.
        T1_length   = 0.
    T1_datetime = datetime.strptime(T1_date, "%y-%m-%d")
    # I keep these seperate because it has been the case where there is no T1 and there is a T2
    # putting the two try/except blocks together would drop an error on no T1 and ignore the T2
    try: 
        T2_tension_delta = float(row["T2_tension_delta"])
        T2_time_delta_string = int(row["T2_time_delta"][:-1])
    except ValueError: 
        T2_tension_delta =  -T1_tension
        T2_time_delta_string = int(0)
    T2_time_delta = timedelta(days = T2_time_delta_string)
    T2_date = datetime.strftime(T1_datetime + T2_time_delta, "%y-%m-%d") if T2_time_delta > timedelta(days=0) else 0
    T2_tension = round(T1_tension + T2_tension_delta , 3)

    DC_DC = row["DC_DC"]
    DC_date = row["DC_date"]
    try: 
        DC_seconds = int(row["DC_seconds"])
        DC_hours = DC_seconds // 3600
        DC_passed:bool = (DC_hours>=4)
        DC_minutes = (DC_seconds - DC_hours * 3600) // 60
        DC_seconds = DC_seconds - DC_minutes * 60 - DC_hours * 3600
        DC_total_time = f"{DC_hours:0>2}:{DC_minutes:0>2}:{DC_seconds:0>2}" 
    except ValueError:
        DC_total_time = "00:00:00"
    good_tube = all([Bend_passed, T1_passed, T2_passed, DC_passed])
    print_list = [f"{tubeID}",
                  f"{shipment_date: <10}", f"Bend: {Bend_flag: <12}",
                  f"T1 on {T1_date} {T1_flag: <12} {T1_tension:0<7}g {T1_length :0<7}mm",
                  f"T2 on {T2_date: <9} {T2_flag: <15} {T2_tension:0<7}g",
                  f"DC on {DC_date} {DC_DC: >6}nA {DC_total_time: ^10} {DC_flag: >13}"]
    return print_list, good_tube

def Create_Final_Tuple(input_tubeID:str):
    tuberow = Locate_Tube_Row(input_tubeID)

    filler_string = "-"*166
    error_string = f"The ID '{input_tubeID}' either does not exist or is not in the database yet :("
    if tuberow == -1:
        return filler_string, False
    elif tuberow == -2:
        return error_string, False
    else: 
        pass

    full_tuberow = Locate_Tube_Row(input_tubeID)

    row = Filter_Columns(full_tuberow)

    print_list, good_tube = Format_Values(row)
    
    if row["Final_flag"] == "YES" and good_tube:
        Final_flag = green_text(row["Final_flag"])
    else: 
        Final_flag = red_text(row["Final_flag"])

    print_list.append(f"Final: {Final_flag: <12}")

    final_string:str = " | ".join(print_list)

    return final_string, good_tube

