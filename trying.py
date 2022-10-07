top_left, top_right = chr(9556), chr(9559)
spacer  = chr(9552)*19 
wall = chr(9553)
separator_left, separator_right = chr(9568), chr(9571)
bot_left, bot_right = chr(9562), chr(9565)


cap_of_box =          top_left + spacer + top_right
box_entry = lambda item:  wall +  item  + wall
box_seperator = separator_left + spacer + separator_right
U_of_box =            bot_left + spacer + bot_right
print(chr(80258))

print(cap_of_box)
print(box_entry(" "*len(spacer)))
print(box_seperator)
print(U_of_box)
