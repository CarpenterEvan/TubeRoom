# Welcome to the UofM ATLAS Tube Room!!
1.    If you're reading this, then I'm probably not in lab anymore, hello from ~beyond the grave~ wherever I am that's not here. 
1.    During my time in the Tube Room, I learned a lot about experimentation, quality assurance, and most importantly, tubes! 
1.    I also figured out how to use tools like Python, Bash, LabVIEW, and GitHub to make my life easier. 
1.    I want to pass on this information so it is not lost after I leave, so your life can be easier too! 
1.    When I started in lab, I had no knowledge of any of this, so I prefer to assume you have no knowledge either.
1.    This GitHub repository is full of files that help with different processses I did every day that are just sped up using python.
1.    This is still for lab use, meaning you'll need access to the lab's Google Drive. Get someone to add you to the google drive, if you can't find anyone else to add you (impossible) email me `ecarp@umich.edu`. 
1.    I run these files from the command-line. 
## Running Python Files
1. I personally reccomend, downloading [Anaconda](https://www.anaconda.com/) for the python package managing (so you don't have to individually install numpy, matplotlib.pyplot, scipy, pandas, ...), [Google Drive Desktop](https://www.google.com/drive/download/) for accessing the database files easier, and [Visual Studio Code](https://code.visualstudio.com/) for reading the code. They should be straightforward downloads. 
1. Download this repository (green "Code" button)
1. Open Terminal (Mac) or Command Prompt (Windows)
1. Navigate to the downloaded folder (use cd to change directory, figuring out how to use that and other commands on your own is a good idea, things like cd, ls, pwd, etc.)
1. Run a file like Verify.py file with `python Verify.py`

###    `Verify.py`
I want to scan the barcode ID on a tube and check from the Database file what tests it has passed. 
I will be doing this for thousands of tubes, so I want it to be quick, easy, and compact. 
99% of the time, I will be scanning 10 tubes at a time, very fast, then checking if those 10 pass.
- `python Verify.py save` will save all IDs scanned into a file, you can then re-run all of the IDs in that file with `python Verify.py check`

###    `DCHeader.py` 
I want to create a new .log file that will be synced with the google drive. It must be labeled with the correct date, 
and if a file already already exists for that day, it will have to modify the name. This code can only handle 2 tests/day right now. 
The other important feature is scanning in the tube IDs. 

###   `TensionSearch.sh`
Using bash, grep through the tension files in the Google Drive and see if a tube's ID appears in any tension files, this can be used for checking if a tube has been tension tested before the database has been updated. 
