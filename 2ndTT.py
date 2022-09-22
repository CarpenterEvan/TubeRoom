from GetTubeInfo import id_to_values
import datetime

today = datetime.datetime.today()

while True:
	tubeID = input("Tube ID: ")
	if tubeID=="stop":
		break
	print("\033[1A", end=f"{tubeID}  ")

	value_dict, good_tube_dict =  id_to_values(tubeID)
	
	T1_date = datetime.datetime.strptime(value_dict["T1_Date"], "%y-%m-%d")

	days_since_T1 = (today-T1_date).days
	
	if days_since_T1>=14:
		print("True   ")
	else: 
		print(f"{False}, {14-days_since_T1} days left")