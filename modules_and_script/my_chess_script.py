from tkinter import Tk, Label, Text
from my_functions import draw

# Creating the GUI
window = Tk()
window.title("CHESS")
window.geometry('631x320')

message_1 = ('Final Project\nCogs 18 Spring 2019\nVladimir Melnik\n')
message_2 = ('Features: \n'
		 	+ '\tMovement disabled for pieces with no legal moves\n'
	     	+ '\tKing highlighted orange when in check\n'
			+ '\tKing highlighted light pink when check mated\n'
		  	+ '\tAll movement disabled when in stale mate or check mate\n'
		 	+ '\tCastling implemented\n'
		 	+ '\tEn Passant implemented\n'
		 	+ '\tBoard Reset Implemented\n'
		  	+ '\tCritical junctures from professional games available for practice\n'
		 	+ '\tButton for easy testing of critical chess features\n')

message_label_1 = Label(window, text = message_1, font = ('Arial',12))
message_label_1.pack()

text = Text(window)
text.insert('end', message_2)
text.pack()

# Starts the Game GUI
draw()

window.mainloop()
