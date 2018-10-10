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
		self.master.resizable(False, False)
		self.title = master.title('Noname module')
		self.frame_left = LabelFrame(master, text = 'макет выбора1')
		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		self.frame_mid = LabelFrame(master, text = 'макет редактора')
		self.frame_mid.grid(row = 0, column = 1, sticky = 'wens')
		self.frame_right = LabelFrame(master, text = 'макет результата')
		self.frame_right.grid(row = 0, column = 2, sticky = 'wens')
		self.vsb_tree = Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_tree.pack(side = RIGHT, fill = Y)
		self.hsb_tree = Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_tree.pack(side = BOTTOM, fill = X)
		self.tree = ttk.Treeview(self.frame_left, yscrollcommand = self.vsb_tree.set, xscrollcommand = self.hsb_tree.set)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.hsb_tree.config(command = self.tree.xview)
		self.vsb_tree.config(command = self.tree.yview)
		
		self.mid_textBox = Text(self.frame_mid, font = 'arial 7',wrap = WORD)
		self.mid_textBox.grid(row = 0, column = 0, sticky = 'wens')
		
		self.appendButton = Button(self.frame_mid, text = 'добавить пункт ТТ', command = lambda: self.commitLine(self))
		self.appendButton.grid(row = 1, column = 0, sticky = 'wens')
		self.tree.bind("<Double-1>", lambda x: self.appendNewLine(self,"<Double-1>"))
		
		self.right_listBox = Listbox(self.frame_right, height = 18, width = 50)
		self.right_listBox.grid(row = 0, column = 0, sticky = 'wens')
		self.right_listBox.bind("<Double-1>", lambda x: self.editCurrentLine(self, "<Double-1>"))

		self.commitButton = Button(self.frame_right, text = 'создать ТТ')
		self.commitButton.grid(row = 1, column = 0, sticky = 'wens')
		#self.button_frame = LabelFrame(self.frame_left, text = 'макет панели спецсимволов')
		#self.button_frame.grid(row = 1, column = 0)
		#self.specButton01 = Button(self.button_frame, height = 1, width = 3, command = lambda: addSymbol(self.mid_textBox,'b1')).grid(row = 0, column = 0)
	
	#def onClickCommit(self,master):
	#	self.right_listBox
	#	self.right_listBox
	#	pass

	def commitLine(self,master):
		text = self.mid_textBox.get("1.0",'end-1c')
		self.right_listBox.insert(END,text)
		self.mid_textBox.delete('1.0', END)

	def fillTree(self, master):
		for i in range(1,500):
			self.tree.insert("", i, "dir%s"%i, text="Dir %s"%i)
			self.tree.insert("dir%s"%i, i, text=" sub dir %s" %i,values=("%sA" %i," %sB" %i))
		
	def addSymbol(text, keyval):
		symbols = {'b1':'elem1', 
					'b2':'elem2'}
		text.insert(END, ' '+symbols[keyval])

	def appendNewLine(self, master,event):
		item = self.tree.selection()[0]
		self.mid_textBox.insert(END,("you clicked on", self.tree.item(item,"text")))

	def editCurrentLine(self, master,event):
		self.mid_textBox.delete('1.0', END)
		index = self.right_listBox.curselection()[0]
		value = self.right_listBox.get(index)
		self.mid_textBox.insert(END,value)

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
