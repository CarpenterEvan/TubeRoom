from GetTubeInfo import DB, id_to_values
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Verify import check_file_for_IDs_with_regex, get_formatted_tuple
import os
shipmentdate = "230331" #input("Which Shipment? [yymmdd]: ")
shipment_file = f"Summary/Tubes_From_20{shipmentdate}.txt"
bad_IDs = []
for file in sorted(os.listdir("Summary"))[-10:]:
	ID_list = check_file_for_IDs_with_regex(f"Summary/{file}")
	lengths = []
	for ID in ID_list:
		length = float(id_to_values(ID)[0]["T1_Length"][5:-4])	
		if length>1625.25:
			bad_IDs.append(ID)
			lengths.append(length) 
		else: continue
	print(file, len(lengths))
for tube in bad_IDs:
	print_list, value_dict = get_formatted_tuple(tube)
	print(" | ".join(print_list))
    
    
