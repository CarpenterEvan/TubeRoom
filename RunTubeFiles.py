import Verification
from Verification import Get_Tube_Info

while True:
    tubeid = input("Tube ID: ")
    string = Get_Tube_Info(tubeid) 
    print("", end="\033[1A \033[1D")
    print(string)