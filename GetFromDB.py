from os import lstat
import pandas as pd
from datetime import datetime, timedelta

global ID, T1, T2, DC, FV
green_text  = lambda x: f"\x1b[32m{x}\x1b[0m" # I don't know how this affects string length
#white_text  = lambda x: f""
red_text    = lambda x: f"\x1b[31m{x}\x1b[0m"
flashing_red= lambda x: f"\x1b[31;5m{x}\x1b[0m"

def color_pass_string(string, flag):
    if flag:
        return green_text(string)  
    elif not flag: 
        return red_text(string)

def Format_Database():
    path = "./Google Drive/Shared drives/sMDT Tube Testing Reports/TUBEDB.txt"
    df = pd.read_csv(path, 
                    names = ["ID", "T1", "T2", "DC", "FV"],  
                    delimiter = "|",
                    memory_map = True)
    df = df.applymap(lambda string: " ".join(string.split()))
    df = df.applymap(lambda string: string.split(" "))
    ID = pd.DataFrame(df["ID"].tolist()[2:], columns=["tubeID",  "End",     "Received", "l[mb*l/s]", "bend", "flagE"])
    T1 = pd.DataFrame(df["T1"].tolist()[2:], columns=["Tension", "Len[mm]", "F[Hz]",    "T[g]",      "flag", "L"])
    T2 = pd.DataFrame(df["T2"].tolist()[2:], columns=["dF[Hz]",  "dT[g]",   "Dt[d]",    "flag2"])
    DC = pd.DataFrame(df["DC"].tolist()[2:], columns=["DCday",   "sys",     "DC[nA]",   "HV[s]",     "flag"])
    FV = pd.DataFrame(df["FV"].tolist()[2:], columns=["ENDday",  "done?",   "ok",       "Comment",   "None", "None"])
    return ID, T1, T2, DC, FV

ID, T1, T2, DC, FV = Format_Database()


def Get_Tube_Info(input_tubeID:str):
    try:
        tubeID = input_tubeID
        if len(tubeID) == 0:
            return ("-"*166, False)
        tuberow, = ID.index[ ID["tubeID"].str.contains(tubeID) ] # index of the row with True, which is row with ID
        # tuberow, unpacks just the first value of the tuple into the variable tuberow

        shipment_date = ID["Received"].iloc[ tuberow ]

        try:
            T1_date = T1["Tension"].iloc[ tuberow ]
            T1_tension = float(T1["T[g]"].iloc[ tuberow ])
            T1_length = float(T1["Len[mm]"].iloc[ tuberow ])
        except ValueError: 
            T1_date = "11-11-11"
            T1_tension = 0.
            T1_length = 0.
        T1_datetime = datetime.strptime(T1_date, "%y-%m-%d")

        # I keep these seperate because it has been the case where there is no T1 and there is a T2
        # putting the two try/except blocks together would drop an error on no T1 and ignore the T2
        try: 
            T2_tension_delta = float(T2["dT[g]"].iloc[ tuberow ])
            T2_time_delta_string = int(T2["Dt[d]"].iloc[ tuberow ][:-1])
        except ValueError: 
            T2_tension_delta =  -T1_tension
            T2_time_delta_string = int(0)

        T2_time_delta = timedelta(days = T2_time_delta_string)
        

        T2_date = datetime.strftime(T1_datetime + T2_time_delta, "%y-%m-%d") if T2_time_delta > timedelta(days=0) else 0
        T2_tension = round(T1_tension + T2_tension_delta , 3)

        DC_date = DC["DCday"].iloc[ tuberow ]
        DC_DC = DC["DC[nA]"].iloc[ tuberow ]
        DC_seconds = int(DC["HV[s]"].iloc[ tuberow ])

        try: 
            DC_hours = DC_seconds // 3600
            DC_minutes = (DC_seconds - DC_hours * 3600) // 60
            DC_seconds = DC_seconds - DC_minutes * 60 - DC_hours * 3600
            DC_total_time = f"{DC_hours:0>2}:{DC_minutes:0>2}:{DC_seconds:0>2}" 
        except ValueError:
            DC_total_time = 0

        Bend_pass_string = ID["flagE"].iloc[ tuberow ]
        T1_pass_string = T1["flag"].iloc[ tuberow ]
        T2_pass_string = T2["flag2"].iloc[ tuberow ]
        DC_pass_string = DC["flag"].iloc[ tuberow ]
        Final_pass_string = FV["ok"].iloc[ tuberow ]

        Bend_flag = (Bend_pass_string == "PASS")
        T1_flag =  ("pass" in T1_pass_string)
        T2_flag = ("Pass" in T2_pass_string)
        DC_flag = (DC_pass_string == "OK") and (DC_hours>5)

        good_tube = Bend_flag and T1_flag and T2_flag and DC_flag and (Final_pass_string == "YES") 
        
        Bend_pass = color_pass_string(Bend_pass_string, Bend_flag) 
        T1_pass = color_pass_string(T1_pass_string, T1_flag) 
        T2_pass = color_pass_string(T2_pass_string, T2_flag)
        DC_pass = color_pass_string(DC_pass_string, DC_flag)
        Final_pass = green_text(Final_pass_string) if good_tube else red_text("NO")

        print_list = [f"{tubeID: ^7}", 
                      f"{shipment_date: <10}",
                      f"Bend: {Bend_pass: <12}",
                      f"T1 on {T1_date} {T1_pass: <12} {T1_tension:0<7}g {T1_length :0<7}mm",
                      f"T2 on {T2_date: <8} {T2_pass: <15} {T2_tension:0<7}g",
                      f"DC on {DC_date} {DC_DC: >6}nA {DC_total_time: ^10} {DC_pass: >13}",
                      f"Final: {Final_pass: <12}"] 

            # Comment out this line to see what I was talking about ^^
        final_string = " | ".join(print_list)

        return final_string, good_tube

    except ValueError:
        return f"The ID '{tubeID}' either does not exist or is not in the database yet :( ", False