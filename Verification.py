'''
    I want to scan a tube ID from the Database file, and check if it is good or bad. 
    I will be doing this for thousands of tubes, so I want it to be quick, easy, and compact. 
    99 percent of the time, I will be scanning 10 tubes at a time, very fast, then checking if those 10 pass
    I made this with the intention of running it from my mac console.

    The following text describes the code, use it as a reference, not a book!!
    1)  I use pandas to open the database as a csv, and rename the columns to have shorter names
        Now the dataframe is created and there is a long string in each cell

    2)  I strip the whitespace and split the ID column to extract just the tube IDs from the long string
        I then put this ID into a new column called justID.

    3)  I strip the whitespace from every cell, then split each cell into a list with " " as a delimiter
        this means some entries in the list are "", but I don't care enough about those to try and filter them out.
        I re-order the dataframe columns so justID is on the left. This does not serve any purpose now, but it was 
        nicer to display the dataframe this way when I was setting up the code :)

    4)  I initialize two variables, tubeID and counter, tubeID will be the string that is input and searched for. 
        I set up counter so that when I scan tubes, I can easily see that the fourth and seventh tubes are bad, for example.
        I define some lambda functions just to reduce clutter, they take in a string and use the ANSI escape codes to color the text displayed. 
        The last lambda function (find) is for searching the dataframe for the index of the row with the tube ID

    5)  This is the while loop, it will continuously take in an input, and try to find it in the justID column, 
        if the input string is not in the column, it should pass an index error, which will be caught by the except case, 
        this is the best way to stop the code (by typing "stop")

    6)  After finding the ID, the code takes out the relevant data from the lists in the row, 
        I only care about the date the test happened, and if it passed. 
        I do some datetime formatting, the second tension test is recorded in terms of changes, delta tension, 
        the number of days since the first tension test, etc, so I need to do a datetime difference

    7)  Check if the pass/fail strings say pass or fail, "pass" is written differently for each test
        The string is color coded green or red if it is true (matches the pass) or false
        instead of trying to figure out all of the false cases, it just returns whatever the string is if it is not pass, and colors it red

    8)  To make the output more compact, I use ANSI escape characters to move the command line cursor up one line, 
        and re-write over the input dialogue. 
        You can comment out this line and run the code to see what I mean

        Then I have the code print all of the extracted, colored values
'''

'''
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