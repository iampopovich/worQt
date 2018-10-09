import re
import sys
import os
import json, csv, xml
from fontTools.ttLib import TTFont
from tkinter import *
from tkinter import ttk
import standardLibrary

class techReqsApp:
	def __init__(self, master):
		self.master = master
		self.title = master.title('Noname module')
		self.frame_left = LabelFrame(master, text = 'макет выбора1')
		self.frame_left.grid(row = 0, column = 0,sticky = 'wens')
		self.frame_right = LabelFrame(master, text = 'макет результата')
		self.frame_right.grid(row = 0, column = 1,sticky = 'wens')
		self.vsb_text = Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_text.grid(row = 0, column = 1,sticky = 'wens')
		self.hsb_text = Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_text.grid(row = 1, column = 0,sticky = 'wens')
		self.tree = ttk.Treeview(self.frame_left, yscrollcommand = self.vsb_text.set, xscrollcommand = self.hsb_text.set )
		self.tree.grid(row = 0, column = 0)
		self.hsb_text.config(command = self.tree.xview)
		self.vsb_text.config(command = self.tree.yview)
		self.right_textBox = Text(self.frame_right, font = 'arial 7',wrap = WORD)
		self.right_textBox.grid(row = 0, column = 0, sticky = 'wens')
		self.rigth_subFrame = Frame(self.frame_right)
		self.rigth_subFrame.grid(row = 1, column = 0)
		self.symbolsList = 
		self.commitButton = Button(,text = 'сформировать текст ТТ')
		
		##tree.bind("<Double-1>", lambda x: OnDoubleClick(right_textBox,"<Double-1>"))
		#self.button_frame = LabelFrame(self.frame_left, text = 'макет панели спецсимволов')
		#self.button_frame.grid(row = 1, column = 0)
		#self.specButton01 = Button(self.button_frame, height = 1, width = 3, command = lambda: addSymbol(self.right_textBox,'b1')).grid(row = 0, column = 0)
	
	
	def fillTree(self, master):
		self.tree["columns"]=("one","two")
		for i in range(1,500):
			self.tree.insert("", i, "dir%s"%i, text="Dir %s"%i)
			self.tree.insert("dir%s"%i, i, text=" sub dir %s" %i,values=("%sA" %i," %sB" %i))
		
		
	def addSymbol(text, keyval):
		symbols = {'b1':'elem1', 
					'b2':'elem2'}
		text.insert(END, ' '+symbols[keyval])

	def OnDoubleClick(text,event):
		text.insert(END, 'good')

	def loadFont():
		fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
		font = TTFont(fontPath)
		return font

def main():
	root = Tk()
	frame = techReqsApp(root)
	frame.fillTree(root)
	root.mainloop()


if __name__ == '__main__':
	main()
