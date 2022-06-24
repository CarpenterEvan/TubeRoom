import pandas as pd
from datetime import datetime, timedelta

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

global ID, T1, T2, DC, FV
ID, T1, T2, DC, FV = Format_Database()
green_text  = lambda x: f"\x1b[32m{x}\x1b[0m" # I don't know how this affects string length
red_text    = lambda x: f"\x1b[31m{x}\x1b[0m"
flashing_red= lambda x: f"\x1b[31;5m{x}\x1b[0m"


def Get_Tube_Info(input_tubeID):
    try:
        tubeID = input_tubeID
        if tubeID in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT"] :
            print("All done! :) ")
            exit()
        if tubeID == "":
            return "-"*166
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
        DC_seconds = DC["HV[s]"].iloc[ tuberow ]

        try: 
            DC_total_time = str(timedelta(seconds=int(DC_seconds)))
        except ValueError:
            DC_total_time = 0

        Bend_pass_string = ID["flagE"].iloc[ tuberow ]
        T1_pass_string = T1["flag"].iloc[ tuberow ]
        T2_pass_string = T2["flag2"].iloc[ tuberow ]
        DC_pass_string = DC["flag"].iloc[ tuberow ]
        Final_pass_string = FV["ok"].iloc[ tuberow ]

        Bend_pass = green_text(Bend_pass_string) if (Bend_pass_string == "PASS") else red_text(Bend_pass_string)
        T1_pass = green_text(T1_pass_string) if "pass" in T1_pass_string else red_text(T1_pass_string)
        T2_pass = green_text(T2_pass_string) if "Pass" in T2_pass_string else red_text(T2_pass_string)
        DC_pass = green_text(DC_pass_string) if (DC_pass_string == "OK") else red_text(DC_pass_string)
        Final_pass = green_text(Final_pass_string) if (Final_pass_string == "YES") else red_text("NO")

        print_list = [f"{tubeID: ^7}", 
                    f"{shipment_date: <10}",
                    f"Bend: {Bend_pass: <12}",
                    f"T1 on {T1_date} {T1_pass: <12} {T1_tension: <7}g {T1_length : <7}mm",
                    f"T2 on {T2_date: <8} {T2_pass: <15} {T2_tension: <6}g",
                    f"DC on {DC_date} {DC_DC: >5}nA {DC_total_time: ^16} {DC_pass: ^13}",
                    f"Final: {Final_pass: ^12}"] 

            # Comment out this line to see what I was talking about ^^
        final_string = " | ".join(print_list) if tubeID!="" else "-"*166 # counter is set to zero when tubeID is "" (enter key)

        return final_string

    except ValueError:
        return f"The ID '{tubeID}' either does not exist or is not in the database yet :( "