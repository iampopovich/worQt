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
		self.tree.bind("<Double-1>", lambda x: self.appendTemplate(self,"<Double-1>"))
		
		self.mid_textBox = Text(self.frame_mid, font = 'arial 7',wrap = WORD)
		self.mid_textBox.grid(row = 0, column = 0, sticky = 'wens', columnspan = 2)
		self.mid_textBox.focus()
		
		self.appendButton = Button(self.frame_mid, text = 'добавить пункт ТТ', command = lambda: self.commitLine(self))
		self.appendButton.grid(row = 1, column = 0, sticky = 'wens')
		self.commitEditedButton = Button(self.frame_mid, text = 'изменить пункт ТТ', command = lambda: self.commitEditedParagraph(self))
		self.commitEditedButton.grid(row = 1, column = 1, sticky = 'wens')
		self.commitEditedButton.config(state=DISABLED)
		
		self.right_listBox = Listbox(self.frame_right, height = 18, width = 50)
		self.right_listBox.grid(row = 0, column = 0, sticky = 'wens')
		self.right_listBox.bind("<Double-1>", self.editCurrentLine)
		self.right_listBox.bind('<Button-1>', self.setCurrent)
		self.right_listBox.bind('<B1-Motion>', self.shiftSelection)

		self.commitButton = Button(self.frame_right, text = 'создать ТТ')
		self.commitButton.grid(row = 1, column = 0, sticky = 'wens')
		
		#self.button_frame = LabelFrame(self.frame_left, text = 'макет панели спецсимволов')
		#self.button_frame.grid(row = 1, column = 0)
		#self.specButton01 = Button(self.button_frame, height = 1, width = 3, command = lambda: addSymbol(self.mid_textBox,'b1')).grid(row = 0, column = 0)
	
	#def onClickCommit(self,master):
	#	self.right_listBox
	#	self.right_listBox
	#	pass
	def setCurrent(self, event):
		self.right_listBox.curIndex = self.right_listBox.nearest(event.y)

	def shiftSelection(self, event):
		i = self.right_listBox.nearest(event.y)
		if i < self.right_listBox.curIndex:
			x = self.right_listBox.get(i)
			self.right_listBox.delete(i)
			self.right_listBox.insert(i+1, x)
			self.right_listBox.curIndex = i
		elif i > self.right_listBox.curIndex:
			x = self.right_listBox.get(i)
			self.right_listBox.delete(i)
			self.right_listBox.insert(i-1, x)
			self.right_listBox.curIndex = i
		self.recalculateParagraphs(self)

	def commitLine(self,master):
		text = self.mid_textBox.get("1.0",'end-1c')
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: pass
		lastIndex = self.right_listBox.size()
		text = str(lastIndex+1)+'. ' + text
		self.right_listBox.insert(END,text)
		self.mid_textBox.delete('1.0', END)

	def fillTree(self, master):
		for i in range(1,500):
			self.tree.insert("", i, "dir%s"%i, text="Dir %s"%i)
			self.tree.insert("dir%s"%i, i, text=" sub dir %s" %i, values =("%sA" %i," %sB" %i))
		
	def addSymbol(text, keyval):
		symbols = {'b1':'elem1', 
					'b2':'elem2'}
		text.insert(END, ' '+symbols[keyval])

	def appendTemplate(self, master,event):
		item = self.tree.selection()[0]
		self.mid_textBox.insert(END,("you clicked on", self.tree.item(item,"text")))

	def recalculateParagraphs(self, master):
		for index in range(self.right_listBox.size()):
			text = self.right_listBox.get(i)
			try:
				text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),str(index+1)+'. ')
			except: pass
			self.right_listBox.delete(index)
			self.right_listBox.insert(index,text)

	def editCurrentLine(self,event):
		self.commitEditedButton.config(state = NORMAL)
		self.mid_textBox.delete('1.0', END)
		index = self.right_listBox.curselection()[0]
		text = self.right_listBox.get(index)
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
		except:	pass
		self.mid_textBox.insert(END,text)
	
	def commitEditedParagraph(self,mastrer):
		self.commitEditedButton.config(state = DISABLED)
		index = self.right_listBox.curselection()[0]
		text = self.mid_textBox.get("1.0",'end-1c')
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),str(index+1)+'. ')
		except: text = str(index+1)+'. ' + text 
		self.mid_textBox.delete('1.0', END)
		self.right_listBox.delete(index)
		self.right_listBox.insert(index,text)
		

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
