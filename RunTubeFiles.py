import GetFromDB
from GetFromDB import Get_Tube_Info, ID
import re
counter = 0
global d,s # I use this dictionary and set to filter out duplicates
d = dict()
s = set()

WriteFile = (input("Cleaning? [y/n]: ") == "y")

if WriteFile:
    verifiedIDs = open("Verified_Today.txt", "a")
else: pass

while True:
    tubeid = input("Tube ID: ")
    is_this_tube = re.match("MSU[0-9]{5}", tubeid) != None
    
    counter = counter + 1  if counter<=9 else 1
    counter = counter if len(tubeid)!=0 else 0

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT"]:
        if WriteFile:
            verifiedIDs.close()
        else: pass
        print("All done! :) \n")
        for i in d:
            print(i, d[i])
        print("Total good: ", sum(d.values()))
        exit()
    
    verify_string, good_tube = Get_Tube_Info(tubeid)

    date_string = verify_string[11:21]

    not_dashes = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_string) != None 

    if date_string not in d and not_dashes and good_tube: # If I haven't seen this date before, initialize it
        d[date_string] = 1 
        if WriteFile:
            verifiedIDs.write(tubeid)
            verifiedIDs.write("\n")
        else: pass
    elif tubeid not in s and not_dashes and good_tube: # If I haven't seen this tube before, +1 to it's date in the dictionary, 
        # and add to the set, now I've seen this tube
        d[date_string] += 1 
        s.add(tubeid)
        if WriteFile:
            verifiedIDs.write(tubeid)
            verifiedIDs.write("\n")
        else: pass
    
    print("", end="\033[1A \033[1D")
    print(verify_string, counter if counter!=0 else "" )  


    
    