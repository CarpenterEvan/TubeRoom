# TubeRoom

Code that I use for work in the Tube Room, there are different processses I do every day that can be sped up using python. 
This was originally on a Google Colab file, but it is often far too slow when taking multiple keyboard inputs. So now I run it from my console.

    Verification: 
        I want to scan the barcode ID on a tube and check from the Database file what tests it has passed. 
        I will be doing this for thousands of tubes, so I want it to be quick, easy, and compact. 
        99 percent of the time, I will be scanning 10 tubes at a time, very fast, then checking if those 10 pass.
        I made this with the intention of running it from my mac console.
    DCHeader: 
        I want to create a new .log file that will be synced with the google drive. It must be labeled with the correct date, 
        and if a file already already exists for that day, it will have to modify the name. This code can only handle 2 tests/day right now. 
        The other important feature is scanning in the tube IDs. 
    FullSearch:
        A WIP, I want to be able to enter a tube's ID and search through all testing files to find what test files it's apart of. I will need to learn Shell, and possibly some C++ (ROOT specifically) to more easily access the actual database instead of just the Google Drive
