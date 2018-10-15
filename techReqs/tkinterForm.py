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
		self.mainmenu = Menu(self.parent) 
		self.parent.config(menu=self.mainmenu) 
		self.filemenu = Menu(self.mainmenu, tearoff=0)
		self.filemenu.add_command(label="Открыть...")
		self.filemenu.add_command(label="Новый")
		self.filemenu.add_command(label="Сохранить...")
		self.filemenu.add_command(label="Выход")
		self.helpmenu = Menu(self.mainmenu, tearoff=0)
		self.helpmenu.add_command(label="Помощь")
		self.helpmenu.add_command(label="О программе", command = lambda: showProgramInfo)
		self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)
		self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)
		##left frame init
		self.frame_left = LabelFrame(parent, text = 'макет выбора1')
		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		
		#self.vsb_tree = ttk.Scrollbar(self.frame_left, orient = VERTICAL)
		#self.vsb_tree.pack(side = RIGHT, fill = BOTH)
		#self.hsb_tree = ttk.Scrollbar(self.frame_left, orient = HORIZONTAL)
		#self.hsb_tree.pack(side = BOTTOM, fill = BOTH)
		#self.tree = ttk.Treeview(self.frame_left, yscrollcommand = self.vsb_tree.set, xscrollcommand = self.hsb_tree.set)
		#self.tree.pack(side = LEFT, fill = BOTH)
		#self.hsb_tree.config(command = self.tree.xview)
		#self.vsb_tree.config(command = self.tree.yview)
		#self.tree.bind('<Double-1>', lambda x: self.appendTemplate(self,'<Double-1>'))
		#self.frame_left = LabelFrame(parent, text = 'макет выбора1')

		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		self.vsb_frame_left_listBox = ttk.Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_frame_left_listBox.pack(side = RIGHT, fill = BOTH)
		self.hsb_frame_left_listBox = ttk.Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_frame_left_listBox.pack(side = BOTTOM, fill = BOTH)
		self.frame_left_listBox = Listbox(self.frame_left, yscrollcommand = self.vsb_frame_left_listBox.set, xscrollcommand = self.hsb_frame_left_listBox.set)
		self.frame_left_listBox.pack(side = LEFT, fill = BOTH)
		self.hsb_frame_left_listBox.config(command = self.frame_left_listBox.xview)
		self.vsb_frame_left_listBox.config(command = self.frame_left_listBox.yview)
		self.frame_left_listBox.bind('<Button-1>', self.showTemplateParagraphs)
		##mid frame init
		self.frame_mid = LabelFrame(parent, text = 'макет редактора')
		self.frame_mid.grid(row = 0, column = 1, sticky = 'wens')
		self.frame_mid_textBox = Text(self.frame_mid, height = 10, font = 'arial 10',wrap = WORD)
		self.frame_mid_textBox.grid(row = 0, column = 0, sticky = 'wens', columnspan = 3)
		self.frame_mid_textBox.focus()
		self.appendButton = ttk.Button(self.frame_mid, text = 'добавить пункт ТТ')
		self.appendButton.config(command = lambda: self.appendLine(self))
		self.appendButton.grid(row = 1, column = 0, sticky = 'wens')
		self.commitEditedButton = ttk.Button(self.frame_mid, text = 'изменить пункт ТТ')
		self.commitEditedButton.config(command = lambda: self.commitEditedParagraph(self))
		self.commitEditedButton.grid(row = 1, column = 1, sticky = 'wens')
		self.commitEditedButton.config(state = DISABLED)
		self.frame_mid_listBox = Listbox(self.frame_mid)
		self.frame_mid_listBox.grid(row = 3, column = 0, sticky = 'wens', columnspan = 3)
		self.frame_mid_listBox.bind('<Button-1>', self.showTemplate)
		self.checkBox_is_active = BooleanVar()
		self.symbolsCheckBox = ttk.Checkbutton(self.frame_mid, text = 'Добавить спец. символ', variable = self.checkBox_is_active)
		self.symbolsCheckBox.config(command = lambda: self.showSymbolButtons(self))
		self.symbolsCheckBox.grid(row = 1, column = 2, sticky = 'ns')
		self.subFrame_symbols_buttons = LabelFrame(self.frame_mid, text  = 'Спец. символы')
		##right frame init
		self.frame_right = LabelFrame(parent, text = 'макет результата')
		self.frame_right.grid(row = 0, column = 2, sticky = 'wens')
		self.subFrame_frame_right_listBox = Frame(self.frame_right)
		self.subFrame_frame_right_listBox.pack(fill = BOTH)
		self.vsb_frame_right_listBox = ttk.Scrollbar(self.subFrame_frame_right_listBox, orient = VERTICAL)
		self.vsb_frame_right_listBox.pack(side = RIGHT, fill = BOTH)
		self.hsb_frame_right_listBox = ttk.Scrollbar(self.subFrame_frame_right_listBox, orient = HORIZONTAL)
		self.hsb_frame_right_listBox.pack(side = BOTTOM, fill = BOTH)	
		self.frame_right_listBox = Listbox(self.subFrame_frame_right_listBox,  font = 'arial 10', selectmode = EXTENDED, width = 70)
		self.frame_right_listBox.config(yscrollcommand = self.vsb_frame_right_listBox.set, xscrollcommand = self.hsb_frame_right_listBox.set)
		self.frame_right_listBox.pack(side = TOP, fill = BOTH)
		self.hsb_frame_right_listBox.config(command = self.frame_right_listBox.xview)
		self.vsb_frame_right_listBox.config(command = self.frame_right_listBox.yview)
		self.frame_right_listBox.bind('<Double-1>', self.editCurrentLine)
		self.frame_right_listBox.bind('<Button-1>', self.setCurrent)
		self.frame_right_listBox.bind('<Button-3>', self.showListItemSubMenu)
		self.frame_right_listBox.bind('<B1-Motion>', self.shiftSelection)
		self.subFrame_frame_right_buttons = Frame(self.frame_right)
		self.subFrame_frame_right_buttons.pack(side = TOP, fill = BOTH)
		self.commitButton = ttk.Button(self.subFrame_frame_right_buttons, text = 'создать ТТ')
		self.commitButton.pack(fill = BOTH)


#main window functions group
	def fillTree(self, parent):
		for i in range(1,500):
			self.tree.insert('', i, 'dir%s'%i, text='Dir %s'%i)
			self.tree.insert('dir%s'%i, i, text=' sub dir %s' %i, values = ('%sA' %i,' %sB' %i))
	
	def fillCategoriesListBox(self, parent):
		for key in sorted(standardLibrary.dict_categories.keys()):
			self.frame_left_listBox.insert(END, key)

	def loadFont():
		fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
		font = TTFont(fontPath)
		return font

	def showProgramInfo(self, master):
		pass

#

#frame_left functions group
	def showTemplateParagraphs(self,event):
		try: self.frame_mid_listBox.delete(0,'end')
		except: pass
		self.frame_left_listBox.curIndex = self.frame_left_listBox.nearest(event.y)
		text = self.frame_left_listBox.get(self.frame_left_listBox.curIndex) #text is a key
		for item in sorted(standardLibrary.dict_categories[text]):
			self.frame_mid_listBox.insert(END, item) 
#

#frame_mid functions group
	def addSymbol(self, parent, keyval):
		text = standardLibrary.dict_symbols[keyval]
		self.frame_mid_textBox.insert(END, ' '+text)

	def appendLine(self,parent):
		text = self.frame_mid_textBox.get('1.0','end-1c') #получаем содержимое поля ввода текста
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'') #стрипаем введенный разрабом порядковый номер, если он есть
		except: pass
		lastIndex = self.frame_right_listBox.size() #получаем текущий последний пункт по порядку
		text = str(lastIndex+1)+'. ' + text #добавляем в начало строки новенький пункт 
		self.frame_right_listBox.insert(END,text) #добавляем элемент в конец списка пунктов. мб можно будет вводить в произвольную позицию
		self.frame_mid_textBox.delete('1.0', END) #удаляем все содержимое поля воода
		self.frame_right_listBox.yview_scroll(lastIndex,'units') #переводит фокус на последний добавленный элемент 

	def showTemplate(self,event):
		try:
			self.frame_mid_listBox.curIndex = self.frame_mid_listBox.nearest(event.y)
			text = self.frame_mid_listBox.get(self.frame_left_listBox.curIndex) #text is a key
		except: pass

	def commitEditedParagraph(self, parent):
		index = self.frame_right_listBox.index(ACTIVE)
		text = self.frame_mid_textBox.get('1.0','end-1c')
		try:
			text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: text = str(index+1)+'. ' + text
		try:
			self.frame_right_listBox.config(state = NORMAL)
			self.frame_right_listBox.delete(index)
			self.frame_right_listBox.insert(index,text)
			self.frame_mid_textBox.delete('1.0', END)
			self.commitEditedButton.config(state = DISABLED)
			self.appendButton.config(state = NORMAL)
		except:
			self.commitEditedButton.config(state = NORMAL)
			self.appendButton.config(state = DISABLED)

	def showSymbolButtons(self, master):  # переделывать с декортаром или макетировать шаблон с заполнением из словаря
		#for child in self.subFrame_frame_right_symbols_buttons.winfo_children():
   		#	child.destroy()
		if self.checkBox_is_active.get():
			self.subFrame_symbols_buttons.grid(row = 2, column = 0, sticky = 'wens', columnspan = 3)
			self.symbolButton01 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b1', command = lambda: self.addSymbol(self,'b1'))
			self.symbolButton01.grid(row = 0, column = 0, sticky  = 'wens')
			self.symbolButton02 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b2', command = lambda: self.addSymbol(self,'b2'))
			self.symbolButton02.grid(row = 0, column = 1, sticky  = 'wens')
			self.symbolButton03 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b3', command = lambda: self.addSymbol(self,'b3'))
			self.symbolButton03.grid(row = 0, column = 2, sticky  = 'wens')
			self.symbolButton04 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b4', command = lambda: self.addSymbol(self,'b4'))
			self.symbolButton04.grid(row = 0, column = 3, sticky  = 'wens')
			self.symbolButton05 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b5', command = lambda: self.addSymbol(self,'b5'))
			self.symbolButton05.grid(row = 0, column = 4, sticky  = 'wens')
			self.symbolButton06 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b6', command = lambda: self.addSymbol(self,'b6'))
			self.symbolButton06.grid(row = 0, column = 5, sticky  = 'wens')
			self.symbolButton07 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b7', command = lambda: self.addSymbol(self,'b7'))
			self.symbolButton07.grid(row = 0, column = 6, sticky  = 'wens')
			self.symbolButton08 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b8', command = lambda: self.addSymbol(self,'b8'))
			self.symbolButton08.grid(row = 1, column = 0, sticky  = 'wens')
			self.symbolButton09 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b9', command = lambda: self.addSymbol(self,'b9'))
			self.symbolButton09.grid(row = 1, column = 1, sticky  = 'wens')
			self.symbolButton10 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b10', command = lambda: self.addSymbol(self,'b10'))
			self.symbolButton10.grid(row = 1, column = 2, sticky  = 'wens')
			self.symbolButton11 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b11', command = lambda: self.addSymbol(self,'b11'))
			self.symbolButton11.grid(row = 1, column = 3, sticky  = 'wens')
			self.symbolButton12 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b12', command = lambda: self.addSymbol(self,'b12'))
			self.symbolButton12.grid(row = 1, column = 4, sticky  = 'wens')
			self.symbolButton13 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b13', command = lambda: self.addSymbol(self,'b13'))
			self.symbolButton13.grid(row = 1, column = 5, sticky  = 'wens')
			self.symbolButton14 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b14', command = lambda: self.addSymbol(self,'b14'))
			self.symbolButton14.grid(row = 1, column = 6, sticky  = 'wens')
		else:
			self.subFrame_symbols_buttons.grid_forget()	
#

#frame_right functions group
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

	def recalculateParagraphs(self, parent):
		for index in range(self.frame_right_listBox.size()):
			text = self.frame_right_listBox.get(index)
			try:
				text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
			except: pass
			self.frame_right_listBox.delete(index)
			self.frame_right_listBox.insert(index,text)

	def editCurrentLine(self,event):
		self.frame_mid_textBox.focus()
		self.frame_right_listBox.config(state = DISABLED)
		self.commitEditedButton.config(state = NORMAL)
		self.appendButton.config(state = DISABLED)
		self.frame_mid_textBox.delete('1.0', END)
		index = self.frame_right_listBox.curselection()[0]
		text = self.frame_right_listBox.get(index)
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
		except:	pass
		self.frame_mid_textBox.insert(END,text)

	def removeCurrentSelection(self, parent): 
		list_index = self.frame_right_listBox.curselection()
		if len(list_index)!=0:
			list_temp = [self.frame_right_listBox.get(index) for index in range(0,self.frame_right_listBox.size()) if not(index in list_index)]
			self.frame_right_listBox.delete(0,END)
			[self.frame_right_listBox.insert(END, item) for item in list_temp]
			self.recalculateParagraphs(self)
		else: pass

	def showListItemSubMenu(self,event):
		#if self.frame_right_listBox.size() != 0:
		isEmpty = self.frame_right_listBox.size() == 0
		multiSelection = len(self.frame_right_listBox.curselection()) > 1
		self.frame_right_listBox.curIndex = self.frame_right_listBox.nearest(event.y)
		self.frame_right_listBox.selection_set(self.frame_right_listBox.curIndex)
		menu = Menu(tearoff=0)
		menu.add_command(label="Изменить", command = lambda: self.editCurrentLine(self), state = DISABLED if (isEmpty or multiSelection) else NORMAL) #заглушка. если список пуст, то не можем ничего изменить. если мультивыделение - не можем ничего менять
		menu.add_command(label="Удалить", command = lambda: self.removeCurrentSelection(self), state = DISABLED if isEmpty else NORMAL) #заглушка. если список пуст, то не можем ничего изменить. но можем удалить несколько пунктов разом
		menu.add_command(label="Треугольник") # row template
		x = event.x
		y = event.y
		menu.post(event.x_root, event.y_root)
		#else: pass
#

	

def main():
	root = Tk()
	frame = techReqsApp(root)
	#frame.fillTree(root)
	frame.fillCategoriesListBox(root)
	root.mainloop()


if __name__ == '__main__':
	main()
