import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
full = "icmeas-20220908-100918.csv"

with open(full, "r") as tests:
	lines = tests.readlines()
	lines_list = list(map(lambda string: string.strip(" \n").split(","), lines))
	stop_times = [0]
	for index, value in enumerate(lines_list[:-1]):
		current_mode = value[-1]
		next_mode = lines_list[index+1][-1]
		if current_mode=="ULTRA" and next_mode=="GROSS":
			stop_times.append(index)


df = pd.read_csv(full,
				 parse_dates=["Date"],
				 date_parser=dateparse,
                 infer_datetime_format=True)

test_list = []
for i in range(len(stop_times)-1):
	test = df.iloc[stop_times[i]:stop_times[i+1]]
	test = test.set_index("Date")
	LeakSeries = test["Leak rate"]
	test_list.append(LeakSeries)


for one_test in test_list:
	plt.plot(one_test)
	plt.ylabel("Leak Rate [mbar*L/s]")
	plt.xlabel("Time [s]")
	plt.yticks(np.arange(1*10**(-12), 1*10**(-3), 10))
	plt.yscale('log')
plt.show()

		



exit()










df = pd.read_csv(three,
				 #index_col="Date",
				 parse_dates=["Date"],
				 date_parser=dateparse,
                 infer_datetime_format=True)

'''
How to seperate data
Time spent in GROSS
Time spent in ULTRA
leak rate change time
'''

plt.plot(df["Date"], df["Leak rate"])
plt.plot(df["Date"][df["Vacuum range"]!="GROSS"], df["Leak rate"][df["Vacuum range"]!="GROSS"])
plt.ylabel("Leak Rate [mbar*L/s]")
plt.xlabel("Time [s]")
plt.yticks(np.arange(1*10**(-12), 1*10**(-5), 8))
plt.xticks()
plt.yscale('log')
plt.show()