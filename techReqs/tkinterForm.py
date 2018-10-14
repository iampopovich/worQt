#мб позже для разделения пунктов на столбцы нужно будет сплитить строки по переносу строки в сублисты
import re
import sys
import os
import json, csv, xml
from fontTools.ttLib import TTFont
from tkinter import *
from tkinter import ttk
import standardLibrary

class techReqsApp:
	def __init__(self, parent):
		##window init
		self.parent = parent
		self.parent.resizable(False, False)
		self.title = parent.title('Noname module')
		##left frame init
		self.frame_left = LabelFrame(parent, text = 'макет выбора1')
		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		self.vsb_tree = Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_tree.pack(side = RIGHT, fill = BOTH)
		self.hsb_tree = Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_tree.pack(side = BOTTOM, fill = BOTH)
		self.tree = ttk.Treeview(self.frame_left, yscrollcommand = self.vsb_tree.set, xscrollcommand = self.hsb_tree.set)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.hsb_tree.config(command = self.tree.xview)
		self.vsb_tree.config(command = self.tree.yview)
		self.tree.bind('<Double-1>', lambda x: self.appendTemplate(self,'<Double-1>'))
		##mid frame init
		self.frame_mid = LabelFrame(parent, text = 'макет редактора')
		self.frame_mid.grid(row = 0, column = 1, sticky = 'wens')
		self.mid_textBox = Text(self.frame_mid, height = 10, font = 'arial 10',wrap = WORD)
		self.mid_textBox.grid(row = 0, column = 0, sticky = 'wens', columnspan = 3)
		self.mid_textBox.focus()
		self.appendButton = Button(self.frame_mid, text = 'добавить пункт ТТ')
		self.appendButton.config(command = lambda: self.appendLine(self))
		self.appendButton.grid(row = 1, column = 0, sticky = 'wens')
		self.commitEditedButton = Button(self.frame_mid, text = 'изменить пункт ТТ')
		self.commitEditedButton.config(command = lambda: self.commitEditedParagraph(self))
		self.commitEditedButton.grid(row = 1, column = 1, sticky = 'wens')
		self.commitEditedButton.config(state = DISABLED)
		self.frame_mid_listBox = Listbox(self.frame_mid)
		self.frame_mid_listBox.grid(row = 2, column = 0, sticky = 'wens', columnspan = 3)
		self.checkBox_is_active = BooleanVar()
		self.symbolsCheckBox = ttk.Checkbutton(self.frame_mid, text = 'Добавить спец. символ', variable = self.checkBox_is_active)
		self.symbolsCheckBox.config(command = lambda: self.showSymbolButtons(self))
		self.symbolsCheckBox.grid(row = 1, column = 2, sticky = 'ns')
		##right frame init
		self.frame_right = LabelFrame(parent, text = 'макет результата')
		self.frame_right.grid(row = 0, column = 2, sticky = 'wens')
		self.subFrame_frame_right_listbox = Frame(self.frame_right)
		self.subFrame_frame_right_listbox.pack(fill = BOTH)
		self.vsb_frame_right_listBox = Scrollbar(self.subFrame_frame_right_listbox, orient = VERTICAL)
		self.vsb_frame_right_listBox.pack(side = RIGHT, fill = BOTH)
		self.hsb_frame_right_listBox = Scrollbar(self.subFrame_frame_right_listbox, orient = HORIZONTAL)
		self.hsb_frame_right_listBox.pack(side = BOTTOM, fill = BOTH)	
		self.frame_right_listBox = Listbox(self.subFrame_frame_right_listbox,  font = 'arial 10', selectmode = EXTENDED, width = 70)
		self.frame_right_listBox.config(yscrollcommand = self.vsb_frame_right_listBox.set, xscrollcommand = self.hsb_frame_right_listBox.set)
		self.frame_right_listBox.pack(side = TOP, fill = BOTH)
		self.hsb_frame_right_listBox.config(command = self.frame_right_listBox.xview)
		self.vsb_frame_right_listBox.config(command = self.frame_right_listBox.yview)
		self.frame_right_listBox.bind('<Double-1>', self.editCurrentLine)
		self.frame_right_listBox.bind('<Button-1>', self.setCurrent)
		self.frame_right_listBox.bind('<B1-Motion>', self.shiftSelection)
		self.subFrame_frame_right_buttons = Frame(self.frame_right, bg = 'black')
		self.subFrame_frame_right_buttons.pack(side = TOP, fill = BOTH)
		self.removeSelectedButton = Button(self.subFrame_frame_right_buttons, text = 'удалить пункт ТТ')
		self.removeSelectedButton.config(command = lambda: self.removeCurrentSelection(self))
		self.removeSelectedButton.pack(side = LEFT, fill = BOTH)
		self.removeSelectedButton.config(state = NORMAL)
		self.commitButton = Button(self.subFrame_frame_right_buttons, text = 'создать ТТ')
		self.commitButton.pack(side = RIGHT, fill = BOTH)
		self.subFrame_frame_right_symbols = LabelFrame(self.frame_right)
		self.subFrame_frame_right_symbols.pack(side = TOP, fill = BOTH)

		#self.symbolsComboBox.bind('<<CheckboxSelected>>', self.redrawSymbolButtons)
		self.subFrame_frame_right_symbols_buttons = Frame(self.subFrame_frame_right_symbols)
		self.subFrame_frame_right_symbols_buttons.grid(row = 1, column = 0, sticky = 'wens')


	def setCurrent(self, event):
		self.frame_right_listBox.curIndex = self.frame_right_listBox.nearest(event.y)

	def shiftSelection(self, event):
		index = self.frame_right_listBox.nearest(event.y)
		if index < self.frame_right_listBox.curIndex:
			x = self.frame_right_listBox.get(index)
			self.frame_right_listBox.delete(index)
			self.frame_right_listBox.insert(index+1, x)
			self.frame_right_listBox.curIndex = index
		elif index > self.frame_right_listBox.curIndex:
			x = self.frame_right_listBox.get(index)
			self.frame_right_listBox.delete(index)
			self.frame_right_listBox.insert(index-1, x)
			self.frame_right_listBox.curIndex = index
		self.recalculateParagraphs(self)

	def appendLine(self,parent):
		text = self.mid_textBox.get('1.0','end-1c') #получаем содержимое поля ввода текста
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'') #стрипаем введенный разрабом порядковый номер, если он есть
		except: pass
		lastIndex = self.frame_right_listBox.size() #получаем текущий последний пункт по порядку
		text = str(lastIndex+1)+'. ' + text #добавляем в начало строки новенький пункт 
		self.frame_right_listBox.insert(END,text) #добавляем элемент в конец списка пунктов. мб можно будет вводить в произвольную позицию
		self.mid_textBox.delete('1.0', END) #удаляем все содержимое поля воода
		self.frame_right_listBox.yview_scroll(lastIndex,'units') #переводит фокус на последний добавленный элемент 

	def fillTree(self, parent):
		for i in range(1,500):
			self.tree.insert('', i, 'dir%s'%i, text='Dir %s'%i)
			self.tree.insert('dir%s'%i, i, text=' sub dir %s' %i, values = ('%sA' %i,' %sB' %i))

	def addSymbol(text, keyval):
		symbols = {'b1':'elem1', 
					'b2':'elem2'}
		text.insert(END, ' '+symbols[keyval])

	def appendTemplate(self, parent,event):
		item = self.tree.selection()[0]
		self.mid_textBox.insert(END,('you clicked on', self.tree.item(item,'text')))

	def recalculateParagraphs(self, parent):
		for index in range(self.frame_right_listBox.size()):
			text = self.frame_right_listBox.get(index)
			try:
				text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
			except: pass
			self.frame_right_listBox.delete(index)
			self.frame_right_listBox.insert(index,text)

	def editCurrentLine(self,event):
		self.mid_textBox.focus()
		self.frame_right_listBox.config(state = DISABLED)
		self.commitEditedButton.config(state = NORMAL)
		self.appendButton.config(state = DISABLED)
		self.removeSelectedButton.config(state = DISABLED)
		self.mid_textBox.delete('1.0', END)
		index = self.frame_right_listBox.curselection()[0]
		text = self.frame_right_listBox.get(index)
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
		except:	pass
		self.mid_textBox.insert(END,text)
	
	def commitEditedParagraph(self, parent):
		index = self.frame_right_listBox.index(ACTIVE)#self.frame_right_listBox.curselection()[0]
		text = self.mid_textBox.get('1.0','end-1c')
		try:
			text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: text = str(index+1)+'. ' + text
		try:
			self.frame_right_listBox.config(state = NORMAL)
			self.frame_right_listBox.delete(index)
			self.frame_right_listBox.insert(index,text)
			self.mid_textBox.delete('1.0', END)
			self.commitEditedButton.config(state = DISABLED)
			self.removeSelectedButton.config(state = NORMAL)
			self.appendButton.config(state = NORMAL)
		except:
			self.commitEditedButton.config(state = NORMAL)
			self.removeSelectedButton.config(state = DISABLED)
			self.appendButton.config(state = DISABLED)

	def removeCurrentSelection(self, parent): 
		list_index = self.frame_right_listBox.curselection()
		if len(list_index)!=0:
			list_temp = [self.frame_right_listBox.get(index) for index in range(0,self.frame_right_listBox.size()) if not(index in list_index)]
			self.frame_right_listBox.delete(0,END)
			[self.frame_right_listBox.insert(END, item) for item in list_temp]
			self.recalculateParagraphs(self)
		else: pass
	
	def loadFont():
		fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
		font = TTFont(fontPath)
		return font

	def showSymbolButtons(self, master):  # переделывать с декортаром или макетировать шаблон с заполнением из словаря
		#for child in self.subFrame_frame_right_symbols_buttons.winfo_children():
   		#	child.destroy()
		if self.checkBox_is_active.get():
			self.subFrame_frame_right_symbols_buttons.destroy()
			print(self.checkBox_is_active.get())
			self.symbolsPack = Frame(self.subFrame_frame_right_symbols_buttons)
			self.symbolsPack.config(height = 25)
			self.symbolsPack.pack(side = TOP, fill =BOTH)
			self.symbolButton01 = Button(self.symbolsPack, text = 'b1')
			self.symbolButton01.grid(row = 0, column = 0, sticky  = 'wens')
			self.symbolButton02 = Button(self.symbolsPack, text = 'b2')
			self.symbolButton02.grid(row = 0, column = 1, sticky  = 'wens')
			self.symbolButton03 = Button(self.symbolsPack, text = 'b3')
			self.symbolButton03.grid(row = 0, column = 2, sticky  = 'wens')
			self.symbolButton04 = Button(self.symbolsPack, text = 'b4')
			self.symbolButton04.grid(row = 0, column = 3, sticky  = 'wens')
			self.symbolButton05 = Button(self.symbolsPack, text = 'b5')
			self.symbolButton05.grid(row = 0, column = 4, sticky  = 'wens')
			self.symbolButton06 = Button(self.symbolsPack, text = 'b6')
			self.symbolButton06.grid(row = 0, column = 5, sticky  = 'wens')
			self.symbolButton07 = Button(self.symbolsPack, text = 'b7')
			self.symbolButton07.grid(row = 1, column = 0, sticky  = 'wens')
			self.symbolButton08 = Button(self.symbolsPack, text = 'b8')
			self.symbolButton08.grid(row = 1, column = 1, sticky  = 'wens')
			self.symbolButton09 = Button(self.symbolsPack, text = 'b9')
			self.symbolButton09.grid(row = 1, column = 2, sticky  = 'wens')
			self.symbolButton10 = Button(self.symbolsPack, text = 'b10')
			self.symbolButton10.grid(row = 1, column = 3, sticky  = 'wens')
			self.symbolButton11 = Button(self.symbolsPack, text = 'b11')
			self.symbolButton11.grid(row = 1, column = 4, sticky  = 'wens')
			self.symbolButton12 = Button(self.symbolsPack, text = 'b12')
			self.symbolButton12.grid(row = 1, column = 5, sticky  = 'wens')
		else:
			self.subFrame_frame_right_symbols_buttons.destroy()
			
			



def main():
	root = Tk()
	frame = techReqsApp(root)
	frame.fillTree(root)
	root.mainloop()


if __name__ == '__main__':
	main()
