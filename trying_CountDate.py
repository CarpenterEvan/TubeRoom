from Verification import Get_Tube_Info, ID
counter = 0
global d,s
d = {}
s = set()
tubelist = [
    "MSU16430",
    "MSU16942",
    "MSU15624",
    "MSU16900",
    "MSU16880",
    "MSU17077",
    "",
    "MSU17111",
    "MSU17142",
    "MSU16375",
    "MSU16512",
    "MSU16143",
    "MSU16901",
    "MSU13100",
    "stop"
]
#while True:
for id in tubelist:
    tubeid = id#input("Tube ID: ")
    counter = counter + 1  if counter<=9 else 1
    counter = counter if len(tubeid)!=0 else 0

    if tubeid in ["stop", "Stop", "STOP", "quit", "Quit", "QUIT", "exit", "Exit", "EXIT"] :
        for i in d:
            print(i, d[i])
        print("Total:   ", sum(d.values()))
        print("All done! :) ")
        exit()

    verify_string = Get_Tube_Info(tubeid)
    date_string = verify_string[11:21]
    not_dashes = date_string != "----------"
    
    if date_string not in d and not_dashes: # If I haven't seen this date before, initialize it
        d[date_string] = 1 
        s.add(tubeid)
    elif tubeid not in s and not_dashes: # If I haven't seen this tube before, add one to it's date in the dictionary, now I've seen this tube
        d[date_string] += 1 
        s.add(tubeid)


    #print("", end="\033[1A \033[1D")
    print(verify_string, counter)  