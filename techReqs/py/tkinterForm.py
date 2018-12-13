#мб позже для разделения пунктов на столбцы нужно будет сплитить строки по переносу строки в сублисты
#.selection_clear()
import re
import sys
from tkinter import *
from tkinter import ttk
import standardLibrary
import gc

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
		self.helpmenu.add_command(label="О программе", command = lambda: self.showProgramInfo)
		self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)
		self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)
		self.mainmenu.add_command(label='Создать ТТ', command = self.createTechReqs)
		##left frame init
		self.frame_left = LabelFrame(parent, text = 'макет выбора1')
		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		self.vsb_frame_left_listBox = ttk.Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_frame_left_listBox.pack(side = RIGHT, fill = BOTH)
		self.hsb_frame_left_listBox = ttk.Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_frame_left_listBox.pack(side = BOTTOM, fill = BOTH)
		self.frame_left_listBox = Listbox(self.frame_left, yscrollcommand = self.vsb_frame_left_listBox.set, xscrollcommand = self.hsb_frame_left_listBox.set)
		self.frame_left_listBox.config(width = 30)
		self.frame_left_listBox.pack(side = LEFT, fill = BOTH)
		self.hsb_frame_left_listBox.config(command = self.frame_left_listBox.xview)
		self.vsb_frame_left_listBox.config(command = self.frame_left_listBox.yview)
		self.frame_left_listBox.bind('<Button-1>', self.showTemplateParagraphs)
		##mid frame init
		self.frame_mid = LabelFrame(parent, text = 'макет редактора')
		self.frame_mid.grid(row = 0, column = 1, sticky = 'wens')
		self.textVariable = ''
		self.frame_mid_textBox = Text(self.frame_mid, height = 10, width = 60, font = 'arial 11',wrap = WORD)
		self.frame_mid_textBox.grid(row = 0, column = 0, sticky = 'wens', columnspan = 3)
		self.frame_mid_textBox.focus()
		self.appendButton = ttk.Button(self.frame_mid, text = 'добавить пункт ТТ')
		self.appendButton.config(command = lambda: self.appendLine(self))
		self.appendButton.grid(row = 1, column = 0, sticky = 'wens')
		self.commitEditedButton = ttk.Button(self.frame_mid, text = 'изменить пункт ТТ')
		self.commitEditedButton.config(command = lambda: self.commitEditedParagraph(self))
		self.commitEditedButton.grid(row = 1, column = 1, sticky = 'wens')
		self.commitEditedButton.config(state = DISABLED)
		self.frame_mid_subframe_listbox = Frame(self.frame_mid)
		self.frame_mid_subframe_listbox.grid(row = 3, column = 0, sticky = 'wens', columnspan = 3)
		self.vsb_frame_mid_listBox = ttk.Scrollbar(self.frame_mid_subframe_listbox, orient = VERTICAL)
		self.vsb_frame_mid_listBox.pack(side = RIGHT, fill = BOTH)
		self.hsb_frame_mid_listBox = ttk.Scrollbar(self.frame_mid_subframe_listbox, orient = HORIZONTAL)
		self.hsb_frame_mid_listBox.pack(side = BOTTOM, fill = BOTH)
		self.frame_mid_listBox = Listbox(self.frame_mid_subframe_listbox)
		self.frame_mid_listBox.pack(fill = BOTH)
		self.frame_mid_listBox.config( yscrollcommand = self.vsb_frame_mid_listBox.set, xscrollcommand = self.hsb_frame_mid_listBox.set)
		self.hsb_frame_mid_listBox.config(command = self.frame_mid_listBox.xview)
		self.vsb_frame_mid_listBox.config(command = self.frame_mid_listBox.yview)
		self.frame_mid_listBox.bind('<Button-1>', self.showTemplatePreview)
		self.frame_mid_listBox.bind('<Button-3>', self.showParagraphsItemSubMenu)
		#self.frame_mid_listBox.bind('<Leave>', self.onLeave)
		self.frame_mid_listBox.bind('<Escape>', self.refuseTemplatePreview)
		self.checkBox_is_active = BooleanVar()
		self.symbolsCheckBox = ttk.Checkbutton(self.frame_mid, text = 'Добавить спец. символ', variable = self.checkBox_is_active)
		self.symbolsCheckBox.config(command = lambda: self.showSymbolButtons(self))
		self.symbolsCheckBox.grid(row = 1, column = 2, sticky = 'ns')
		self.subFrame_symbols_buttons = LabelFrame(self.frame_mid, text  = 'Спец. символы')
		##right frame init
		self.frame_right = LabelFrame(parent, text = 'макет результата')
		self.frame_right.grid(row = 0, column = 2, sticky = 'wens')
		self.subFrame_frame_right_listBox = LabelFrame(self.frame_right)
		self.subFrame_frame_right_listBox.pack(side = LEFT, fill = BOTH)
		self.vsb_frame_right_listBox = ttk.Scrollbar(self.subFrame_frame_right_listBox, orient = VERTICAL)
		self.vsb_frame_right_listBox.pack(side = RIGHT, fill = BOTH)
		self.hsb_frame_right_listBox = ttk.Scrollbar(self.subFrame_frame_right_listBox, orient = HORIZONTAL)
		self.hsb_frame_right_listBox.pack(side = BOTTOM, fill = BOTH)	
		self.frame_right_listBox = Listbox(self.subFrame_frame_right_listBox,  font = 'arial 10', selectmode = EXTENDED, width = 70)
		self.frame_right_listBox.config(yscrollcommand = self.vsb_frame_right_listBox.set, xscrollcommand = self.hsb_frame_right_listBox.set)
		self.frame_right_listBox.pack(side = LEFT, fill = BOTH)
		self.hsb_frame_right_listBox.config(command = self.frame_right_listBox.xview)
		self.vsb_frame_right_listBox.config(command = self.frame_right_listBox.yview)
		self.frame_right_listBox.bind('<Double-1>', self.editCurrentLine)
		self.frame_right_listBox.bind('<Button-1>', self.setCurrent)
		self.frame_right_listBox.bind('<Button-3>', self.showListItemSubMenu)
		self.frame_right_listBox.bind('<B1-Motion>', self.shiftSelection)
		
		#self.commitButton = ttk.Button(self.frame_right, text = 'создать ТТ')
		#self.commitButton.pack(side = BOTTOM, fill = BOTH)

#main window functions group
	#def fillTree(self, parent):
	#	for i in range(1,500):
	#		self.tree.insert('', i, 'dir%s'%i, text='Dir %s'%i)
	#		self.tree.insert('dir%s'%i, i, text=' sub dir %s' %i, values = ('%sA' %i,' %sB' %i))
	
	def fillCategoriesListBox(self, parent):
		for key in sorted(standardLibrary.dict_categories.keys()):
			self.frame_left_listBox.insert(END, key)

	#def loadFont():
	#	fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
	#	font = TTFont(fontPath)
	#	return font

	def createTechReqs(self):
		for line in self.frame_right_listBox.get(0,END):
			self.textVariable+=line+'\n'
		##if messagebox.askokcancel("Создать ТТ", "Вы хотите создать ТТ и выйти?"):
		self.parent.destroy()

	def showProgramInfo(self, parent):
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
		del text
		gc.collect()
#

#frame_mid functions group
	def addSymbol(self, parent, keyval):
		text = standardLibrary.dict_symbols[keyval]
		self.frame_mid_textBox.insert(END, ' '+text)
		del text
		gc.collect()

	def appendLine(self,parent): # можно задать (self,parent,text = self.frame_mid_textBox.get('1.0','end-1c')) и вызывать с параметром другого текста
		text = self.frame_mid_textBox.get('1.0','end-1c') #получаем содержимое поля ввода текста
		try:
			text = text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'') #стрипаем введенный разрабом порядковый номер, если он есть
		except: pass
		lastIndex = self.frame_right_listBox.size() #получаем текущий последний пункт по порядку
		text = str(lastIndex+1)+' ' + text #добавляем в начало строки новенький пункт 
		text = self.recalculateParagraphsWrapping(self, text)
		self.frame_right_listBox.insert(END,text) #добавляем элемент в конец списка пунктов. мб можно будет вводить в произвольную позицию
		self.frame_mid_textBox.delete('1.0', END) #удаляем все содержимое поля воода
		self.recalculateParagraphsNumbers(self)
		self.frame_right_listBox.yview_scroll(lastIndex,'units') #переводит фокус на последний добавленный элемент 
		self.frame_mid_textBox.focus()

	def showTemplatePreview(self,event):
		#tempText = self.frame_mid_textBox.get('1.0','end-1c')
		self.frame_mid_listBox.curIndex = self.frame_mid_listBox.nearest(event.y)
		paragraphText = self.frame_mid_listBox.get(self.frame_mid_listBox.curIndex)
		self.frame_mid_textBox.delete('1.0',END)
		self.frame_mid_textBox.insert(END,paragraphText)
		#self.frame_mid_textBox.config(state = DISABLED) - потом надо будет чекать состояние текстбокса, оно не надо вообще

	def onLeave(self, enter):
		if len(self.frame_mid_listBox.curselection()) != 0:
			self.frame_mid_textBox.config(state = NORMAL)
			self.frame_mid_textBox.delete('1.0', END)
			self.frame_mid_textBox.focus()
			self.frame_mid_listBox.selection_clear(0,END)
		else: pass

	def refuseTemplatePreview(self, event):
		pass
	
	def editTemplateParagraph(self, parent):
		pass

	def showParagraphsItemSubMenu(self,event):
		self.frame_mid_listBox.selection_clear(0,END)
		isEmpty = self.frame_mid_listBox.size() == 0
		self.frame_mid_listBox.curIndex = self.frame_mid_listBox.nearest(event.y)
		self.frame_mid_listBox.selection_set(self.frame_mid_listBox.curIndex)
		menu = Menu(tearoff=0)
		menu.add_command(label="Изменить", command = lambda: self.editTemplateParagraph(self))
		menu.entryconfig(0,state = DISABLED if isEmpty else NORMAL)
		menu.add_command(label="Добавить", command = lambda: self.appendTemplateParagraph(self))
		menu.entryconfig(1,state = DISABLED if isEmpty else NORMAL)
		menu.post(event.x_root, event.y_root)
		del(menu)
	
	def appendTemplateParagraph(self, parent): #смотри реф на appendLine
		index = self.frame_mid_listBox.curselection()[0]
		text = self.frame_mid_listBox.get(index)
		lastIndex = self.frame_right_listBox.size()
		text = str(lastIndex+1)+' ' + text 
		self.frame_right_listBox.insert(END,text)
		self.frame_mid_textBox.delete('1.0', END)
		self.frame_right_listBox.yview_scroll(lastIndex,'units')
		pass

	def commitEditedParagraph(self, parent):
		index = self.frame_right_listBox.index(ACTIVE)
		text = self.frame_mid_textBox.get('1.0','end-1c')
		try:
			text = str(index+1)+' ' + text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: text = str(index+1)+' ' + text
		text = self.recalculateParagraphsWrapping(self, text)
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
		self.recalculateParagraphsNumbers(self)

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

	def recalculateParagraphsWrapping(self,parent, text):
		symbolsLength = len(text)
		rowLength = len(text.split('\n'))
		fontSize = 5
		canvasWidth = 185
		tmpLength = 0
		wrappingRatio = canvasWidth/fontSize
		replaceableText = []
		for word in text.split():
			tmpLength += len(word) +1 #или +2 , по госту оформление знаков препинаний идет через раздельный пробел ГОСТ 7.1—2003
			if tmpLength >= wrappingRatio:
				replaceableText.append('\n')
				replaceableText.append(' '*(len(str(self.frame_right_listBox.size()))+2))
				tmpLength = len(word)
			else: pass
			replaceableText.append(word+' ')
		return(''.join(replaceableText))
		pass

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
		self.recalculateParagraphsNumbers(self)

	def recalculateParagraphsNumbers(self, parent):
		if self.frame_right_listBox.size() == 0: pass
		else:
			for index in range(self.frame_right_listBox.size()):
				text = self.frame_right_listBox.get(index)
				try:
					text = str(index+1)+' ' + text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'') #вставка пробелов в начало строки для равнения по краям
					text = (' '*(len(str(self.frame_right_listBox.size()))- len(str(index+1))))+text 
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
			text = text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
			text = text.replace(re.search(r'\n[\s]{1,}',text).group(0),'\n')
		except:	pass
		self.frame_mid_textBox.insert(END,text)

	def removeCurrentSelection(self, parent): 
		list_index = self.frame_right_listBox.curselection()
		if len(list_index)!=0:
			list_temp = [self.frame_right_listBox.get(index) for index in range(0,self.frame_right_listBox.size()) if not(index in list_index)]
			self.frame_right_listBox.delete(0,END)
			[self.frame_right_listBox.insert(END, item) for item in list_temp]
			self.recalculateParagraphsNumbers(self)
			del(list_temp,list_index)
		else: pass

	def showListItemSubMenu(self,event):
		self.frame_right_listBox.curIndex = self.frame_right_listBox.nearest(event.y)
		self.frame_right_listBox.selection_set(self.frame_right_listBox.curIndex)
		isEmpty = self.frame_right_listBox.size() == 0
		multiSelection = len(self.frame_right_listBox.curselection()) > 1
		menu = Menu(tearoff=0)
		menu.add_command(label="Изменить", command = lambda: self.editCurrentLine(self))
		menu.entryconfig(0,state = DISABLED if (isEmpty or multiSelection) else NORMAL)
		menu.add_command(label="Удалить", command = lambda: self.removeCurrentSelection(self))
		menu.entryconfig(1,state = DISABLED if isEmpty else NORMAL)
		menu.add_command(label="Треугольник") 
		menu.post(event.x_root, event.y_root)
		del(menu)

	def parseText(self, parent, text = None):
		try:
			joinedText = []
			for row in text.split('\n'): 
				try:
					re.match(r'^\s{0,}[0-9]{1,3}\s{0,}',row).group(0)
					joinedText.append(row)
				except Exception as ex: 
					joinedText[-1] += row
					continue
			for row in joinedText: self.frame_right_listBox.insert(END,row)
			self.recalculateParagraphsNumbers(self)
		except Exception as ex: self.frame_mid_textBox.insert(END,str(ex)) 
#		

def main(argv):
	root = Tk()
	frame = techReqsApp(root)
	frame.fillCategoriesListBox(root)
	try: frame.parseText(root,argv[1])
	except: pass
	root.mainloop()
	sys.stdout.write(frame.textVariable)
	sys.stdout.flush()
	
if __name__ == '__main__':
	main(sys.argv)
