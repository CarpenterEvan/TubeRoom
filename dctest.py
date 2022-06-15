counter = 0
DC_tube_IDs = []
ID_set = set()
while True:
    board_number = 4 if counter <= 23 else 1 
    this_tube = input(f"Board {board_number} Position {counter % 24}: ")

    if this_tube == "stop":
        break
    if this_tube not in ID_set:
        ID_set.add(this_tube)
        DC_tube_IDs.append(this_tube)
    counter +=  1


print(DC_tube_IDs)