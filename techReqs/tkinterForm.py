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
		self.frame_midSub = LabelFrame(self.frame_mid, text = 'макет результата')
		self.frame_midSub.grid(row = 2, column = 0, sticky = 'wens', columnspan = 3)
		self.vsb_tree = Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_tree.pack(side = RIGHT, fill = Y)
		self.hsb_tree = Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_tree.pack(side = BOTTOM, fill = X)
		self.tree = ttk.Treeview(self.frame_left, yscrollcommand = self.vsb_tree.set, xscrollcommand = self.hsb_tree.set)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.hsb_tree.config(command = self.tree.xview)
		self.vsb_tree.config(command = self.tree.yview)
		self.tree.bind("<Double-1>", lambda x: self.appendTemplate(self,"<Double-1>"))
		self.mid_textBox = Text(self.frame_mid, height = 10, font = 'arial 10',wrap = WORD)
		self.mid_textBox.grid(row = 0, column = 0, sticky = 'wens', columnspan = 3)
		self.mid_textBox.focus()
		
		self.appendButton = Button(self.frame_mid, text = 'добавить пункт ТТ', command = lambda: self.appendLine(self))
		self.appendButton.grid(row = 1, column = 0, sticky = 'wens')
		self.commitEditedButton = Button(self.frame_mid, text = 'изменить пункт ТТ', command = lambda: self.commitEditedParagraph(self))
		self.commitEditedButton.grid(row = 1, column = 1, sticky = 'wens')
		self.commitEditedButton.config(state=DISABLED)
		self.removeSelectedButton = Button(self.frame_mid, text = 'удалить пункт ТТ', command = lambda: self.removeCurrentSelection(self))
		self.removeSelectedButton.grid(row = 1, column = 2, sticky = 'wens')
		self.removeSelectedButton.config(state=DISABLED)

		self.frame_midSubSub = Frame(self.frame_midSub)
		self.frame_midSubSub.pack(side = TOP, fill = X)
		self.vsb_listBox = Scrollbar(self.frame_midSubSub, orient = VERTICAL)
		self.vsb_listBox.pack(side = RIGHT, fill = Y)
		self.hsb_listBox = Scrollbar(self.frame_midSubSub, orient = HORIZONTAL)
		self.hsb_listBox.pack(side = BOTTOM, fill = X)		
		self.midSub_listBox = Listbox(self.frame_midSubSub, height = 10, font = 'arial 10', selectmode = EXTENDED)
		self.midSub_listBox.config(yscrollcommand = self.vsb_listBox.set, xscrollcommand = self.hsb_listBox.set)
		self.midSub_listBox.pack(side = LEFT, fill = X)
		self.hsb_listBox.config(command = self.midSub_listBox.xview)
		self.vsb_listBox.config(command = self.midSub_listBox.yview)

		self.midSub_listBox.bind("<Double-1>", self.editCurrentLine)
		self.midSub_listBox.bind('<Button-1>', self.setCurrent)
		self.midSub_listBox.bind('<B1-Motion>', self.shiftSelection)
		self.commitButton = Button(self.frame_midSub, text = 'создать ТТ')
		self.commitButton.pack(side = TOP, fill = X)
		
		#self.button_frame = LabelFrame(self.frame_left, text = 'макет панели спецсимволов')
		#self.button_frame.grid(row = 1, column = 0)
		#self.specButton01 = Button(self.button_frame, height = 1, width = 3, command = lambda: addSymbol(self.mid_textBox,'b1')).grid(row = 0, column = 0)
	
	#def onClickCommit(self,master):
	#	self.midSub_listBox
	#	self.midSub_listBox
	#	pass
	def setCurrent(self, event):
		self.midSub_listBox.curIndex = self.midSub_listBox.nearest(event.y)

	def shiftSelection(self, event):
		i = self.midSub_listBox.nearest(event.y)
		if i < self.midSub_listBox.curIndex:
			x = self.midSub_listBox.get(i)
			self.midSub_listBox.delete(i)
			self.midSub_listBox.insert(i+1, x)
			self.midSub_listBox.curIndex = i
		elif i > self.midSub_listBox.curIndex:
			x = self.midSub_listBox.get(i)
			self.midSub_listBox.delete(i)
			self.midSub_listBox.insert(i-1, x)
			self.midSub_listBox.curIndex = i
		self.recalculateParagraphs(self)

	def appendLine(self,master):
		text = self.mid_textBox.get("1.0",'end-1c')
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: pass
		lastIndex = self.midSub_listBox.size()
		text = str(lastIndex+1)+'. ' + text
		self.midSub_listBox.insert(END,text)
		self.mid_textBox.delete('1.0', END)
		self.midSub_listBox.yview_scroll(lastIndex,'units')

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
		for index in range(self.midSub_listBox.size()):
			text = self.midSub_listBox.get(index)
			try:
				text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
			except: pass
			self.midSub_listBox.delete(index)
			self.midSub_listBox.insert(index,text)

	def editCurrentLine(self,event):
		self.commitEditedButton.config(state = NORMAL)
		self.appendButton.config(state = DISABLED)
		self.mid_textBox.delete('1.0', END)
		index = self.midSub_listBox.curselection()[0]
		text = self.midSub_listBox.get(index)
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
		except:	pass
		self.mid_textBox.insert(END,text)
	
	def commitEditedParagraph(self,mastrer):
		index = self.midSub_listBox.curselection()[0]
		text = self.mid_textBox.get("1.0",'end-1c')
		try:
			text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: text = str(index+1)+'. ' + text 
		try:
			self.midSub_listBox.delete(index)
			self.midSub_listBox.insert(index,text)
			self.mid_textBox.delete('1.0', END)
			self.commitEditedButton.config(state = DISABLED)
			self.appendButton.config(state = NORMAL)
		except:
			self.commitEditedButton.config(state = NORMAL)
			self.appendButton.config(state = DISABLED)

	def deleteCurrentLine():
		pass
	
	def activeListener(self, master):
		pass

	def loadFont():
		fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
		font = TTFont(fontPath)
		return font

def main():
	root = Tk()
	frame = techReqsApp(root)
	frame.fillTree(root)
	frame.activeListener(root)
	root.mainloop()


if __name__ == '__main__':
	main()
