from GetTubeInfo import Create_Final_Tuple
import re
import datetime 
import sys
counter = 0
global d,s # I use this dictionary and set to filter out duplicates
d = dict()
s = set()

WriteFile = (sys.argv[-1] == "clean")
CheckFile = (sys.argv[-1] == "check")
Match = (sys.argv[-1] == "match" )
if Match:
    match_list = sys.argv[-2].split(",")
    print(match_list[0])
if WriteFile:
    verifiedIDs = open(f"Verified_{datetime.date.today().strftime('%Y%m%d')}.txt", "a") # Writes to a file with yyyymmdd format in name
    print("\x1b[32;5mCLEANING\x1b[0m") # Blinking green text "CLEANING"
else: 
    print("\x1b[31;5mNOT CLEANING\x1b[0m") # Blinking red text "NOT CLEANING"

if CheckFile:
    tube_list = open("Verified_Today.txt", "r").readlines()
    newlist = [i.strip() for i in tube_list]
    newlist.append("stop")

#for tube in newlist: #tubeid = tube
while True:
    tubeid = input("Tube ID: ")
    #if tubeid in match_list:
    #    print("\a")
    counter = counter + 1  if counter<=9 else 1
    counter = counter if len(tubeid)!=0 else 0

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT", "SAL"]:
        if WriteFile:
            verifiedIDs.close()
        else: pass
        for i in sorted(d):
            print(i, d[i])
        print("Total: ", sum(d.values()))
        print("\n All done! :) \n")
        exit()
    
    verify_string, good_tube = Create_Final_Tuple(tubeid)

    good_tube = good_tube if WriteFile=="True" else True 
    # I only use good_tube for counting only the good tubes when writing the file, 
    #when not writing the file, I want to count every tube

    date_string = verify_string[11:21]
    not_dashes = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_string) != None 
    if (good_tube) and (not_dashes):
        if date_string not in d.keys():
            d[date_string] = 1
            s.add(tubeid)
        elif (tubeid not in s):
            s.add(tubeid)
            d[date_string] += 1
        else: pass
    else: pass
    '''if date_string not in d and not_dashes and good_tube: # If I haven't seen this date before, initialize it
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
        else: pass'''
    print("", end="\033[1A")
    print(verify_string, 
          counter if counter!=0 else "" )  

