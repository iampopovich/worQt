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
		self.parent = parent
		self.parent.resizable(False, False)
		self.title = parent.title('Noname module')
		self.frame_left = LabelFrame(parent, text = 'макет выбора1')
		self.frame_left.grid(row = 0, column = 0, sticky = 'wens')
		self.frame_mid = LabelFrame(parent, text = 'макет редактора')
		self.frame_mid.grid(row = 0, column = 1, sticky = 'wens')
		self.frame_midSub = LabelFrame(self.frame_mid, text = 'макет списка')
		self.frame_midSub.grid(row = 2, column = 0, sticky = 'wens', columnspan = 3)
		self.frame_right = LabelFrame(parent, text = 'макет результата')
		self.frame_right.grid(row = 0, column = 2, sticky = 'wens')
		self.vsb_tree = Scrollbar(self.frame_left, orient = VERTICAL)
		self.vsb_tree.pack(side = RIGHT, fill = Y)
		self.hsb_tree = Scrollbar(self.frame_left, orient = HORIZONTAL)
		self.hsb_tree.pack(side = BOTTOM, fill = X)
		self.tree = ttk.Treeview(self.frame_left, yscrollcommand = self.vsb_tree.set, xscrollcommand = self.hsb_tree.set)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.hsb_tree.config(command = self.tree.xview)
		self.vsb_tree.config(command = self.tree.yview)
		self.tree.bind('<Double-1>', lambda x: self.appendTemplate(self,'<Double-1>'))
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
		self.removeSelectedButton = Button(self.frame_mid, text = 'удалить пункт ТТ')
		self.removeSelectedButton.config(command = lambda: self.removeCurrentSelection(self))
		self.removeSelectedButton.grid(row = 1, column = 2, sticky = 'wens')
		#self.removeSelectedButton.config(state=DISABLED) #see also listener definition at the bottom
		self.removeSelectedButton.config(state = NORMAL)
		
		self.frame_midSubSub = Frame(self.frame_midSub)
		self.frame_midSubSub.pack(side = TOP, fill = BOTH)
		self.vsb_listBox = Scrollbar(self.frame_midSubSub, orient = VERTICAL)
		self.vsb_listBox.pack(side = RIGHT, fill = Y)
		self.hsb_listBox = Scrollbar(self.frame_midSubSub, orient = HORIZONTAL)
		self.hsb_listBox.pack(side = BOTTOM, fill = X)		
		self.midSub_listBox = Listbox(self.frame_midSubSub, height = 7, font = 'arial 10', selectmode = EXTENDED)
		self.midSub_listBox.config(yscrollcommand = self.vsb_listBox.set, xscrollcommand = self.hsb_listBox.set)
		self.midSub_listBox.pack(fill = BOTH)
		self.hsb_listBox.config(command = self.midSub_listBox.xview)
		self.vsb_listBox.config(command = self.midSub_listBox.yview)

		self.midSub_listBox.bind('<Double-1>', self.editCurrentLine)
		self.midSub_listBox.bind('<Button-1>', self.setCurrent)
		self.midSub_listBox.bind('<B1-Motion>', self.shiftSelection)
		self.commitButton = Button(self.frame_midSub, text = 'создать ТТ')
		self.commitButton.pack(side = TOP, fill = X)

		self.vsb_resultCanvas = Scrollbar(self.frame_right, orient = VERTICAL)
		self.vsb_resultCanvas.pack(side = RIGHT, fill = Y)
		self.resultCanvas = Canvas(self.frame_right,width = 700) #канвас оказался лютой заплаткой. мб заменю на пиловский image с ресайзом и кастомным фонтом
		self.resultCanvas.config(yscrollcommand = self.vsb_resultCanvas.set)#, scrollregion=(0,0,0,1500))
		self.resultCanvas.pack(side = TOP, expand = True, fill = BOTH)
		self.resultCanvas.bind('<MouseWheel>', self.on_mousewheel)
		self.vsb_resultCanvas.config(command = self.resultCanvas.yview)
		self.scale_resultCanvas = Scale(self.frame_right, from_= 5, to = 20, orient = HORIZONTAL)
		self.scale_resultCanvas.set(10) #юзлес фича, мб заменю на выпадающий листбокс, занимает много места и не выглядит юзабельно 
		self.scale_resultCanvas.config(command = lambda x: self.resizeCanvasFont(self))
		self.scale_resultCanvas.pack(side = BOTTOM, fill = X)

	def on_mousewheel(self, event):
		self.resultCanvas.yview_scroll(int(-1*(event.delta/120)), 'units')	# юзлес
	
	def resizeCanvasFont(self,master):
		self.refreshResultCanvas(self)
	
	def setCurrent(self, event):
		self.midSub_listBox.curIndex = self.midSub_listBox.nearest(event.y)

	def shiftSelection(self, event):
		index = self.midSub_listBox.nearest(event.y)
		if index < self.midSub_listBox.curIndex:
			x = self.midSub_listBox.get(index)
			self.midSub_listBox.delete(index)
			self.midSub_listBox.insert(index+1, x)
			self.midSub_listBox.curIndex = index
		elif index > self.midSub_listBox.curIndex:
			x = self.midSub_listBox.get(index)
			self.midSub_listBox.delete(index)
			self.midSub_listBox.insert(index-1, x)
			self.midSub_listBox.curIndex = index
		self.recalculateParagraphs(self)

	def appendLine(self,parent):
		text = self.mid_textBox.get('1.0','end-1c') #получаем содержимое поля ввода текста
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'') #стрипаем введенный разрабом порядковый номер, если он есть
		except: pass
		lastIndex = self.midSub_listBox.size() #получаем текущий последний пункт по порядку
		text = str(lastIndex+1)+'. ' + text #добавляем в начало строки новенький пункт 
		self.midSub_listBox.insert(END,text) #добавляем элемент в конец списка пунктов. мб можно будет вводить в произвольную позицию
		self.mid_textBox.delete('1.0', END) #удаляем все содержимое поля воода
		self.midSub_listBox.yview_scroll(lastIndex,'units') #переводит фокус на последний добавленный элемент 
		self.refreshResultCanvas(self)

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
		for index in range(self.midSub_listBox.size()):
			text = self.midSub_listBox.get(index)
			try:
				text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
			except: pass
			self.midSub_listBox.delete(index)
			self.midSub_listBox.insert(index,text)

	def editCurrentLine(self,event):
		self.mid_textBox.focus()
		self.midSub_listBox.config(state = DISABLED)
		self.commitEditedButton.config(state = NORMAL)
		self.appendButton.config(state = DISABLED)
		self.removeSelectedButton.config(state = DISABLED)
		self.mid_textBox.delete('1.0', END)
		index = self.midSub_listBox.curselection()[0]
		text = self.midSub_listBox.get(index)
		try:
			text = text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
		except:	pass
		self.mid_textBox.insert(END,text)
	
	def commitEditedParagraph(self, parent):
		index = self.midSub_listBox.index(ACTIVE)#self.midSub_listBox.curselection()[0]
		text = self.mid_textBox.get('1.0','end-1c')
		try:
			text = str(index+1)+'. ' + text.replace(re.match(r'[0-9]{1,3}\.[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		except: text = str(index+1)+'. ' + text
		try:
			self.midSub_listBox.config(state = NORMAL)
			self.midSub_listBox.delete(index)
			self.midSub_listBox.insert(index,text)
			self.mid_textBox.delete('1.0', END)
			self.commitEditedButton.config(state = DISABLED)
			self.removeSelectedButton.config(state = NORMAL)
			self.appendButton.config(state = NORMAL)
		except:
			self.commitEditedButton.config(state = NORMAL)
			self.removeSelectedButton.config(state = DISABLED)
			self.appendButton.config(state = DISABLED)
		self.refreshResultCanvas(self)

	def removeCurrentSelection(self, parent): 
		list_index = self.midSub_listBox.curselection()
		if len(list_index)!=0:
			list_temp = [self.midSub_listBox.get(index) for index in range(0,self.midSub_listBox.size()) if not(index in list_index)]
			self.midSub_listBox.delete(0,END)
			[self.midSub_listBox.insert(END, item) for item in list_temp]
			self.recalculateParagraphs(self)
		else: pass
		self.refreshResultCanvas(self)
	
	def refreshResultCanvas(self, parent):
		textfont = 'Arial %s' %(self.scale_resultCanvas.get())
		self.resultCanvas.delete('all')
		XBASE, YBASE, DISTANCE = 10, 20, int(re.search(r'[0-9]{1,}',textfont).group(0))+10
		if self.midSub_listBox.size()!= 0:
			for i,item in enumerate(self.midSub_listBox.get(0,END)):
				self.resultCanvas.create_text((XBASE, YBASE + i * DISTANCE), font = textfont, anchor = W, fill='blue', text = item)
		pass

	###experimental unworked feture
	def activeListener(self, parent):
		if len(self.midSub_listBox.curselection())!=0:
			self.removeSelectedButton.config(state=NORMAL)
		else: self.removeSelectedButton.config(state=DISABLED)
		self.activeListener(self) 

	def loadFont():
		fontPath = '%s\\GOST_Type_A.ttf' %os.path.dirname(os.path.realpath(__file__))
		font = TTFont(fontPath)
		return font

def main():
	root = Tk()
	frame = techReqsApp(root)
	frame.fillTree(root)
	#root.after(1000, frame.activeListener(root))
	root.mainloop()


if __name__ == '__main__':
	main()
