import GetTubeInfo
value_dict, good_tube_dict = GetTubeInfo.get_formatted_tuple("MSU05123")
print(good_tube_dict)
d = dict()
for i in range(10):
	word = input()
	if word not in d.keys():
		d[word] = 1
	
	print(d)
