''' Check the Readme for the description of numbers
 1) ###########################################################################################
'''
import pandas as pd
import datetime

df = pd.read_csv("./Desktop/TUBEDB.txt", 
                 names = ["ID", "T1", "T2", "DC", "Fin"],  
                 delimiter = "|")


'''
 2) ###########################################################################################
'''
df["justID"] = df["ID"].str.strip().str.split(" ", expand=True)[0]

'''
 3) ###########################################################################################
'''
df["ID"] = df["ID"].str.strip().str.split(" ") # [ID, IHEP, Date recieved, l[mb*l/s], "", bend, PASS/Fail]
df["T1"] = df["T1"].str.strip().str.split(" ") # [Date tested, Length, Frequency, Tension, pass/fail/----, letter]
df["T2"] = df["T2"].str.strip().str.split(" ") # [dF, "", "", dT, "", Dt, Pass/Pass2/Pass2*]
df["DC"] = df["DC"].str.strip().str.split(" ") # [Date, CAEN/UM, "", "", DC, seconds on HV, OK/WARN/BAD]
df["Fin"] = df["Fin"].str.strip().str.split(" ") # [Date, "", done?, YES/NO, comments could make this length change]
df = df[["justID", "ID", "T1", "T2", "DC", "Fin"]]

'''
 4) ###########################################################################################
'''
tube = "MSU00000" # Initialize variable with format of ID
counter = 0

green_text = lambda x: f"\x1b[32m{x}\x1b[0m" # I don't know how this affects string length
red_text = lambda x: f"\x1b[31m{x}\x1b[0m"
flashing_red = lambda x: f"\x1b[31;5m{x}\x1b[0m"

find = lambda x: x.loc[ tuberow[0] ] # find(x) gives dataframe row, do find(df["ID"]) to test
'''
 5) ###########################################################################################
'''
while True: # For quick testing, use the for loop, and comment out the input and the ANSI escape line
#for tubeID in ["MSU05123", "MSU00220"]:  #MSU05123 passes everything, MSU0220 fails all except bend test 
    try:
        tubeID = input("Tube ID: ")
        tuberow = df.index[ df["justID"].str.contains(tubeID) ] # index of the row with True, which is row with ID
        counter = counter + 1 if counter <=9 else 1

        '''
        6) ###########################################################################################
        '''
        shipment_date = find(df["ID"])[2]

        try:
            T1_date = find(df["T1"])[0]
            T1_tension = float(find(df["T1"])[3])
        except ValueError: 
            T1_date = "11-11-11"
            T1_tension = 0.

        T1_datetime = datetime.datetime.strptime(T1_date, "%y-%m-%d")

        try:
            T2_tension_delta = float(find(df["T2"])[-4])
            T2_time_delta_string = int(find(df["T2"])[-2][:2])
        except ValueError: 
            T2_tension_delta =  -T1_tension
            T2_time_delta_string = int(0)

        T2_time_delta = datetime.timedelta(days = T2_time_delta_string)
        T2_date = datetime.datetime.strftime(T1_datetime + T2_time_delta, "%y-%m-%d")
        T2_tension = round(T1_tension + T2_tension_delta , 3)


        DC_date = find(df["DC"])[0]

        Bend_pass_string = find(df["ID"])[-1]
        T1_pass_string = find(df["T1"])[-2]
        T2_pass_string = find(df["T2"])[-1]
        DC_pass_string = find(df["DC"])[-1]
        
        Final_pass_string = find(df["Fin"])[3]

        '''
        7) ###########################################################################################
        '''
        Bend_pass = green_text(Bend_pass_string) if (Bend_pass_string == "PASS") else red_text(Bend_pass_string)
        T1_pass = green_text(T1_pass_string) if "pass" in T1_pass_string else red_text(T1_pass_string)
        T2_pass = green_text(T2_pass_string) if "Pass" in T2_pass_string else red_text(T2_pass_string)
        DC_pass = green_text(DC_pass_string) if (DC_pass_string == "OK") else red_text(DC_pass_string)
        Final_pass = green_text(Final_pass_string) if (Final_pass_string == "YES") else red_text("NO")

        '''
        8) ###########################################################################################
        '''
        print("", end="\033[1A \033[1D") # Comment out this line to see what I was talking about ^^
        print(f"{tubeID: ^7} | {shipment_date: <10} | Bend: {Bend_pass: <12} | T1 on {T1_date} {T1_pass: <12} {T1_tension: <7} | T2 on {T2_date} {T2_pass: <15} {T2_tension: <7} | DC on {DC_date} {DC_pass: ^13} | Final: {Final_pass: ^12} | {counter: >2}")
    except IndexError:
        print("", end="\033[1A \033[1D")
        print("All done! :) ")
        break
