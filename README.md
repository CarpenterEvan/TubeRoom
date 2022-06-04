# TubeRoom
Code that I use for work
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
