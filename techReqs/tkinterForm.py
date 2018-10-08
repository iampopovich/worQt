import re
import sys
import os
import json
import csv
import xml

#from fontTools.ttLib import TTFont
from tkinter import *
from tkinter import ttk

import standardLibrary

def main():
	frame = initFrame()

def addSymbol(text, keyval):

	symbols = {'b1':'elem1', 
				'b2':'elem2'}
	text.insert(END, ' '+symbols[keyval])
	
def initFrame():
	root = Tk()
	root.title('Noname module')
	root.geometry = None
	root.minsize = None
	root.maxsize = None
	root.resizable(False,False)
	#fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
	#font = TTFont(fontPath)
	
	###frame mid
	#frame_mid = LabelFrame(root, text = 'макет выбора2 и ввода')
	#frame_mid.grid(row = 0, column = 1)
	#mid_button1 = Button(frame_mid,text='b2',width = 10,height=1,bg='black',fg='red',font='arial 14')
	#mid_textBox1 = Text(frame_mid,height=7,width = 50,font='Arial 7',wrap=WORD)
	#mid_textBox1.pack()
	#mid_button1.pack(side = BOTTOM)

	###frame left
	frame_left = LabelFrame(root, text = 'макет выбора1')
	frame_left.grid(row = 0, column = 0)
	scroll_frame = Frame(frame_left)
	scroll_frame.grid(row = 0, column = 0)
	scrollbar_v = Scrollbar(scroll_frame, orient = VERTICAL)
	scrollbar_v.pack( side = RIGHT, fill = Y )
	scrollbar_h = Scrollbar(scroll_frame, orient = HORIZONTAL)
	scrollbar_h.pack( side = BOTTOM, fill = X )
	
	tree = ttk.Treeview(scroll_frame, yscrollcommand = scrollbar_v.set, xscrollcommand = scrollbar_h.set )
	scrollbar_h.config(command = tree.xview)
	scrollbar_v.config(command = tree.yview)
	tree["columns"]=("one","two")
	tree.column("one", width=100 )
	tree.column("two", width=100)
	tree.heading("one", text="coulmn A")
	tree.heading("two", text="column B")
	tree.insert("" , 0, text="Line 1", values=("1A","1b"))
	id2 = tree.insert("", 1, "dir2", text="Dir 2")
	tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
	##alternatively:
	for i in range(4,500):
		tree.insert("", i, "dir%s"%i, text="Dir %s"%i)
		tree.insert("dir%s"%i, i, text=" sub dir 3",values=("3A"," 3B"))
	tree.pack(side = LEFT)
	
	button_frame = LabelFrame(frame_left, text = 'макет панели спецсимволов')
	button_frame.grid(row = 1, column = 0)
	specButton01 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 0)
	specButton02 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 1)
	specButton03 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 2)
	specButton04 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 3)
	specButton05 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 4)
	specButton06 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 5)
	specButton07 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 6)
	specButton08 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 7)
	specButton09 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 8)
	specButton10 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 9)
	specButton11 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 10)
	specButton12 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 11)
	specButton13 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 12)
	specButton14 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 13)
	specButton15 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b1')).grid(row = 0, column = 14)
	specButton16 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 0)
	specButton17 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 1)
	specButton18 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 2)
	specButton19 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 3)
	specButton20 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 4)
	specButton21 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 5)
	specButton22 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 6)
	specButton23 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 7)
	specButton24 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 8)
	specButton25 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 9)
	specButton26 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 10)
	specButton27 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 11)
	specButton28 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 12)
	specButton29 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 13)
	specButton30 = Button(button_frame, height = 1, width = 3, command = lambda: addSymbol(left_textBox2,'b2')).grid(row = 1, column = 14)
	
	###frame right
	frame_right = LabelFrame(root, text = 'макет результата')
	frame_right.grid(row = 0, column = 2)
	left_textBox2 = Text(frame_right,height=7,width=50,font = 'arial 7',wrap = WORD)
	left_textBox2.grid(row = 0, column = 0)
	button4 = Button(frame_right,text='b4',width=11,height=1,bg='black',fg='red',font='arial 7')
	button4.grid(row = 1, column = 0)
	root.mainloop()


if __name__ == '__main__':
	main()
