__author__ = "Evan Carpenter"
__version__ = "3.1"

import os.path
from re import match
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path 

home = Path.home()
GDrive_to_DB = Path("Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt")
path_to_local = Path.joinpath(Path("").absolute().parent, "TubeRoom/Verifying", "TUBEDB.txt")
final_path = Path.joinpath(home, GDrive_to_DB)


'''This is a module designed to take in the ID of an sMDT barcode and not only find it in the TUBEDB.txt file, 
which is stored in the Google Drive, but to format the values so that the result is easy to read'''
green_text  = lambda x: f"\x1b[32m{x}\x1b[0m" # It seems that this adds +9 to length of string
red_text    = lambda x: f"\x1b[31m{x}\x1b[0m"
flashing_red= lambda x: f"\x1b[31;5m{x}\x1b[0m"

def color_string(string, goal):
    '''Colors a string green or red using ANSI escape codes depending on if the string matches the goal'''
    passes = match(string, goal)
    if passes:
        return (green_text(string), True)
    elif not passes: 
        return (red_text(string), False)
        
def format_database():
    '''Opens Google Drive path to get to the .txt file in the shared drive, hoping to change this in the future to reduce dependency on Google Drive Desktop...'''
    try:

        df = pd.read_csv(final_path, 
                        names = ["ID", "T1", "T2", "DC", "FV"],  
                        delimiter = "|",
                        memory_map = True,
                        dtype=str).dropna(axis=0)
        path_used = final_path

    except FileNotFoundError:

        print(f'''
        
              1.) Hmm... Could not access {home}/Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt
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

            exit(f"\t3.) If you get this message, still could not find TUBEDB.txt, either install Google Drive Desktop or copy TUBEDB.txt from the Google Drive into {path_to_local.parent}\n")

    if __name__ == "GetTubeInfo":

        print(f"Database File is from: {path_used}")
        print(f"Last Updated:", datetime.fromtimestamp(os.path.getmtime(path_used)))

    df = df.applymap(lambda string: " ".join(string.split()))
    df = df.applymap(lambda string: string.split(" "))

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
    defaults = {"d": "MSU05123", # default (good)
                "f": "MSU01341", # fails multiple tests
                "b": "MSU00229"} # bad, multiple tests missing, good for testing "-----"
    tubeID = input_tubeID
    try:
        istube = match("MSU[0-9]{5}", tubeID) 
        assert istube # this will raise an AssertionError if the ID does not look like "MSU" followed by 5 numbers
        # "tuberow_index, " unpacks just the first value of the tuple into the variable tuberow
        tuberow_index, = DB["tubeID"].index[ DB["tubeID"].str.contains(tubeID) ] # index of the row with True, which is row with ID
        return tuberow_index     

    except AssertionError: # This means ID was not valid, possibly a default key

        if len(tubeID) == 1 and tubeID in defaults.keys():
                tubeID = defaults[tubeID] # Default
                tuberow_index, = DB["tubeID"].index[ DB["tubeID"].str.contains(tubeID) ] # index of the row with True, which is row with ID
                return tuberow_index
        else: 
            return -1
    except ValueError: # This means the ID is valid but not in the DB
        return -2 
        
def filter_columns(tuberow_index):
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

def format_values(row:dict):

    tubeID = row["tubeID"]
    shipment_date_string = row["Shipment_date"].strip()
    shipment_date = datetime.strptime(shipment_date_string, "%Y-%m-%d")

    Bend_flag, Bend_passed = color_string(row["Bend_flag"], "PASS")
    T1_flag, T1_passed = color_string(row["T1_flag"], "pass")
    T2_flag, T2_passed = color_string(row["T2_flag"], "Pass2")
    DC_flag, DC_passed = color_string(row["DC_flag"], "OK")

    try:
        
        T1_date:str = row["T1_date"] # Date of UM Tension test, so technically the second tension test, this gets assigned to T2_date later
        T1_tension  = float(row["T1_tension"])
        T1_length   = float(row["T1_length"])

    except ValueError:
        
        T1_date = "01-01-01"
        T1_tension  = 0.
        T1_length   = 0.

    T1_datetime = datetime.strptime(T1_date, "%y-%m-%d")
    # I keep these seperate because it has been the case where there is no T1 and there is a T2
    # putting the two try/except blocks together would drop an error on no T1 and ignore the T2
    try: 

        T2_tension_delta = float(row["T2_tension_delta"])
        T2_time_delta_string = int(row["T2_time_delta"][:-1]) # 13D --> 13

    except ValueError: 

        T2_tension_delta =  -T1_tension
        T2_time_delta_string = int(0)

    T2_time_delta = timedelta(days = T2_time_delta_string)
    T2_tension = round(T1_tension + T2_tension_delta , 3)

    if shipment_date < T1_datetime and timedelta(days=0) < T2_time_delta: 

        T2_date = T1_date # Our T1 is the second tension test, so I want to call it T2
        T1_date = datetime.strftime(T1_datetime - T2_time_delta, "%y-%m-%d")

    else: 

        T2_date = "--------"
    

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
                  "T2_Date": T2_date, "T2_Flag": T2_flag, "T2_Tension": T2_tension,
                  "DC_Date": DC_date, "DC_DC": DC_DC, "DC_Time": DC_total_time, "DC_Flag": DC_flag}

    return value_dict, good_tube_dict

def id_to_values(input_tubeID:str):
    tuberow_index = locate_tube_row(input_tubeID)
    row = filter_columns(tuberow_index)
    value_dict, good_tube_dict = format_values(row)
    return value_dict, good_tube_dict

def get_formatted_tuple(input_tubeID:str):
    tuberow = locate_tube_row(input_tubeID)

    filler_string = "-"*166
    error_string = f"The ID '{input_tubeID}' either does not exist or is not in the database yet :("
    if tuberow == -1:
        return filler_string, False
    elif tuberow == -2:
        return error_string, False
    else: 
        pass

    full_tuberow = locate_tube_row(input_tubeID)

    row = filter_columns(full_tuberow)

    value, good_tube_dict = format_values(row)
    good_tube = all(good_tube_dict.values())

    print_list = [f"{value['ID']}",
                  f"{value['Ship_Date']: <10}", 
                  f"Bend: {value['Bend_Flag']: <12}",
                  f"T1 on {value['T1_Date']} {value['T1_Flag']: <12} {value['T1_Tension']:0<7}g {value['T1_Length']:0<7}mm",
                  f"T2 on {value['T2_Date']: <9} {value['T2_Flag']: <15} {value['T2_Tension']:0<7}g",
                  f"DC on {value['DC_Date']} {value['DC_DC']: >6}nA {value['DC_Time']: ^10} {value['DC_Flag']: >13}"]
    if row["Final_flag"] == "YES" and good_tube:
        Final_flag = green_text(row["Final_flag"])
    else: 
        Final_flag = red_text(row["Final_flag"])

    print_list.append(f"Final: {Final_flag: <12}")
    final_string = " | ".join(print_list)

    return final_string, good_tube