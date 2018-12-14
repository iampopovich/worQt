using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Text;
using System.IO;
using System.Linq;
//using System.Resources;
//using System.Reflection;
//using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Text.RegularExpressions;
	
namespace techReqs
{
	/// <summary>
	/// Description of MainForm.
	/// </summary>
	public partial class MainForm : Form
	{
		
		public Font gostFont {get; set;}
		public string outputText {get; set;}
			
		public MainForm()
		{
			InitializeComponent();
			loadFont();
			setDefaults();
		}
				
/****************mainform functions********************/

void setDefaults(){
			rightListbox.Font = gostFont;
		}
		
void createTechReqs(object sender, EventArgs e)
		{
			DialogResult res = MessageBox.Show("Вы хотите создать ТТ и вернуться в NX?",
			                                   "Confirmation", MessageBoxButtons.OKCancel,
			                                   MessageBoxIcon.Information);
			if (res == DialogResult.OK)
			{
				foreach(var line in rightListbox.Items)
				{
					outputText += string.Format("{0}\r\n",line);
				}
				midTexbox.Clear();
				midTexbox.Text = outputText;
				//##if messagebox.askokcancel("Создать ТТ", "Вы хотите создать ТТ и выйти?"):
				Console.WriteLine(outputText);
				this.Close();
			}
			//if (res == DialogResult.Cancel) {
			//}
		}
				
private void loadFont()
		{
			PrivateFontCollection pfc = new PrivateFontCollection();
			Stream fontStream = this.GetType().Assembly.GetManifestResourceStream("techReqs.GOST_type_B.ttf");
			byte[] fontdata = new byte[fontStream.Length];
			fontStream.Read(fontdata,0,(int)fontStream.Length);
			fontStream.Close();
			unsafe
			{
				fixed(byte * pFontData = fontdata)
				{
					pfc.AddMemoryFont((System.IntPtr)pFontData,fontdata.Length);
				}
			}
			String familyName = pfc.Families[0].Name;
			this.gostFont = new Font(familyName,15, FontStyle.Regular, GraphicsUnit.Pixel);
		}
	
private void showProgramInfo(){}
		
private void fillCategoriesListBox(){
//		for key in sorted(standardLibrary.dict_categories.keys()):
//			self.frame_left_listBox.insert(END, key)
		}
/****************end mainform functions********************/


		
/****************left frame functions********************/
		
void LeftListboxSelectedIndexChanged(object sender, EventArgs e)
	{
		midListbox.Items.Clear();
		midListbox.Items.Add("item1");
		midListbox.Items.Add("item2");
		midListbox.Items.Add("item3");
		midListbox.Items.Add("item4");
		midListbox.Items.Add("item5");
	}
		
//		private void showTemplateParagraphs(){}		//event на выбор айтема листбокса
//		try: self.frame_mid_listBox.delete(0,'end')
//		except: pass
//		self.frame_left_listBox.curIndex = self.frame_left_listBox.nearest(event.y)
//		text = self.frame_left_listBox.get(self.frame_left_listBox.curIndex) #text is a key
//		for item in sorted(standardLibrary.dict_categories[text]):
//			self.frame_mid_listBox.insert(END, item) 
//		del text
//		gc.collect()
		
/****************end left frame functions********************/




/****************mid frame functions********************/

//	def addSymbol(self, parent, keyval):
//		text = standardLibrary.dict_symbols[keyval]
//		self.frame_mid_textBox.insert(END, ' '+text)
//		del text
//		gc.collect()
//

void Button1Click(object sender, EventArgs e)
{
	int listboxSize = rightListbox.Items.Count+1;
	//string st = string.Format("Строка АБВГ.12.12.1212 {0}\r\nh\r\ne\r\nh\r\ne\r\nn\r\nh\r\ne\r\nh\r\ne\r\nh\r\ne\r\ne",listboxSize);
	//rightListbox.Items.Add(st);
	string text = midTexbox.Text;
	//try {
	//	text = text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
	//Regex leaderNum = new Regex(@"\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+""]{1,}");
	//text = text.Replace(leaderNum.Match(
	//}
	//catch (Exception) {
	//throw;
	//}
	//recalculateParagraphsNumbers();
	rightListbox.Items.Add(text);
	midTexbox.Clear();
	midTexbox.Focus();
}

//		lastIndex = self.frame_right_listBox.size() #получаем текущий последний пункт по порядку
//		text = string.Format("{0}
//		text = str(lastIndex+1)+' ' + text #добавляем в начало строки новенький пункт 
//		text = self.recalculateParagraphsWrapping(self, text)
//		self.frame_right_listBox.insert(END,text) #добавляем элемент в конец списка пунктов. мб можно будет вводить в произвольную позицию


void Button2Click(object sender, EventArgs e)
{
	string text = midTexbox.Text;
	int index = rightListbox.Items.IndexOf(rightListbox.SelectedItem.ToString());
	try {
		//text = str(index+1)+' ' + text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1,}',text).group(0),'')
		text = string.Format("{0} {1}",(index+1),text);
	} catch (Exception) {
		text = string.Format("{0} {1}",(index+1),text);
		throw;
	}
	//text = self.recalculateParagraphsWrapping(self, text)
	rightListbox.Items.RemoveAt(index);
	rightListbox.Items.Insert(index, text);
	rightListbox.Enabled = true;
	button1.Enabled = true;
	button2.Enabled = false;
	midTexbox.Clear();
	//recalculateParagraphsNumbers();
}
	

//
//	def showTemplatePreview(self,event):
//		#tempText = self.frame_mid_textBox.get('1.0','end-1c')
//		self.frame_mid_listBox.curIndex = self.frame_mid_listBox.nearest(event.y)
//		paragraphText = self.frame_mid_listBox.get(self.frame_mid_listBox.curIndex)
//		self.frame_mid_textBox.delete('1.0',END)
//		self.frame_mid_textBox.insert(END,paragraphText)
//		#self.frame_mid_textBox.config(state = DISABLED) - потом надо будет чекать состояние текстбокса, оно не надо вообще
//
//	def onLeave(self, enter):
//		if len(self.frame_mid_listBox.curselection()) != 0:
//			self.frame_mid_textBox.config(state = NORMAL)
//			self.frame_mid_textBox.delete('1.0', END)
//			self.frame_mid_textBox.focus()
//			self.frame_mid_listBox.selection_clear(0,END)
//		else: pass
//
//	def refuseTemplatePreview(self, event):
//		pass
//	
//	def editTemplateParagraph(self, parent):
//		pass
//
//	def showParagraphsItemSubMenu(self,event):
//		self.frame_mid_listBox.selection_clear(0,END)
//		isEmpty = self.frame_mid_listBox.size() == 0
//		self.frame_mid_listBox.curIndex = self.frame_mid_listBox.nearest(event.y)
//		self.frame_mid_listBox.selection_set(self.frame_mid_listBox.curIndex)
//		menu = Menu(tearoff=0)
//		menu.add_command(label="Изменить", command = lambda: self.editTemplateParagraph(self))
//		menu.entryconfig(0,state = DISABLED if isEmpty else NORMAL)
//		menu.add_command(label="Добавить", command = lambda: self.appendTemplateParagraph(self))
//		menu.entryconfig(1,state = DISABLED if isEmpty else NORMAL)
//		menu.post(event.x_root, event.y_root)
//		del(menu)
//	
//	def appendTemplateParagraph(self, parent): #смотри реф на appendLine
//		index = self.frame_mid_listBox.curselection()[0]
//		text = self.frame_mid_listBox.get(index)
//		lastIndex = self.frame_right_listBox.size()
//		text = str(lastIndex+1)+' ' + text 
//		self.frame_right_listBox.insert(END,text)
//		self.frame_mid_textBox.delete('1.0', END)
//		self.frame_right_listBox.yview_scroll(lastIndex,'units')
//		pass
//

//
//	def showSymbolButtons(self, master):  # переделывать с декортаром или макетировать шаблон с заполнением из словаря
//		#for child in self.subFrame_frame_right_symbols_buttons.winfo_children():
//   		#	child.destroy()
//		if self.checkBox_is_active.get():
//			self.subFrame_symbols_buttons.grid(row = 2, column = 0, sticky = 'wens', columnspan = 3)
//			self.symbolButton01 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b1', command = lambda: self.addSymbol(self,'b1'))
//			self.symbolButton01.grid(row = 0, column = 0, sticky  = 'wens')
//			self.symbolButton02 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b2', command = lambda: self.addSymbol(self,'b2'))
//			self.symbolButton02.grid(row = 0, column = 1, sticky  = 'wens')
//			self.symbolButton03 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b3', command = lambda: self.addSymbol(self,'b3'))
//			self.symbolButton03.grid(row = 0, column = 2, sticky  = 'wens')
//			self.symbolButton04 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b4', command = lambda: self.addSymbol(self,'b4'))
//			self.symbolButton04.grid(row = 0, column = 3, sticky  = 'wens')
//			self.symbolButton05 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b5', command = lambda: self.addSymbol(self,'b5'))
//			self.symbolButton05.grid(row = 0, column = 4, sticky  = 'wens')
//			self.symbolButton06 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b6', command = lambda: self.addSymbol(self,'b6'))
//			self.symbolButton06.grid(row = 0, column = 5, sticky  = 'wens')
//			self.symbolButton07 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b7', command = lambda: self.addSymbol(self,'b7'))
//			self.symbolButton07.grid(row = 0, column = 6, sticky  = 'wens')
//			self.symbolButton08 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b8', command = lambda: self.addSymbol(self,'b8'))
//			self.symbolButton08.grid(row = 1, column = 0, sticky  = 'wens')
//			self.symbolButton09 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b9', command = lambda: self.addSymbol(self,'b9'))
//			self.symbolButton09.grid(row = 1, column = 1, sticky  = 'wens')
//			self.symbolButton10 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b10', command = lambda: self.addSymbol(self,'b10'))
//			self.symbolButton10.grid(row = 1, column = 2, sticky  = 'wens')
//			self.symbolButton11 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b11', command = lambda: self.addSymbol(self,'b11'))
//			self.symbolButton11.grid(row = 1, column = 3, sticky  = 'wens')
//			self.symbolButton12 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b12', command = lambda: self.addSymbol(self,'b12'))
//			self.symbolButton12.grid(row = 1, column = 4, sticky  = 'wens')
//			self.symbolButton13 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b13', command = lambda: self.addSymbol(self,'b13'))
//			self.symbolButton13.grid(row = 1, column = 5, sticky  = 'wens')
//			self.symbolButton14 = ttk.Button(self.subFrame_symbols_buttons, width = 4, text = 'b14', command = lambda: self.addSymbol(self,'b14'))
//			self.symbolButton14.grid(row = 1, column = 6, sticky  = 'wens')
//		else: self.subFrame_symbols_buttons.grid_forget()	
/****************end mid frame functions********************/

/****************right frame functions********************/
//	def setCurrent(self, event):
//		self.frame_right_listBox.curIndex = self.frame_right_listBox.nearest(event.y)
//

void recalculateParagraphsWrapping(){
	
}

//	def recalculateParagraphsWrapping(self,parent, text):
//		symbolsLength = len(text)
//		rowLength = len(text.split('\n'))
//		fontSize = 5
//		canvasWidth = 185
//		tmpLength = 0
//		wrappingRatio = canvasWidth/fontSize
//		replaceableText = []
//		for word in text.split():
//			tmpLength += len(word) +1 #или +2 , по госту оформление знаков препинаний идет через раздельный пробел ГОСТ 7.1—2003
//			if tmpLength >= wrappingRatio:
//				replaceableText.append('\n')
//				replaceableText.append(' '*(len(str(self.frame_right_listBox.size()))+2))
//				tmpLength = len(word)
//			else: pass
//			replaceableText.append(word+' ')
//		return(''.join(replaceableText))
//		pass
//
//	def shiftSelection(self, event):
//		index = self.frame_right_listBox.nearest(event.y)
//		if index < self.frame_right_listBox.curIndex:
//			x = self.frame_right_listBox.get(index)
//			self.frame_right_listBox.delete(index)
//			self.frame_right_listBox.insert(index+1, x)
//			self.frame_right_listBox.curIndex = index
//		elif index > self.frame_right_listBox.curIndex:
//			x = self.frame_right_listBox.get(index)
//			self.frame_right_listBox.delete(index)
//			self.frame_right_listBox.insert(index-1, x)
//			self.frame_right_listBox.curIndex = index
//		self.recalculateParagraphsNumbers(self)
//
//	def recalculateParagraphsNumbers(self, parent):
//		if self.frame_right_listBox.size() == 0: pass
//		else:
//			for index in range(self.frame_right_listBox.size()):
//				text = self.frame_right_listBox.get(index)
//				try:
//					text = str(index+1)+' ' + text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'') #вставка пробелов в начало строки для равнения по краям
//					text = (' '*(len(str(self.frame_right_listBox.size()))- len(str(index+1))))+text 
//				except: pass
//				self.frame_right_listBox.delete(index)
//				self.frame_right_listBox.insert(index,text)
//
//	def removeCurrentSelection(self, parent): 
//		list_index = self.frame_right_listBox.curselection()
//		if len(list_index)!=0:
//			list_temp = [self.frame_right_listBox.get(index) for index in range(0,self.frame_right_listBox.size()) if not(index in list_index)]
//			self.frame_right_listBox.delete(0,END)
//			[self.frame_right_listBox.insert(END, item) for item in list_temp]
//			self.recalculateParagraphsNumbers(self)
//			del(list_temp,list_index)
//		else: pass
//
//	def showListItemSubMenu(self,event):
//		self.frame_right_listBox.curIndex = self.frame_right_listBox.nearest(event.y)
//		self.frame_right_listBox.selection_set(self.frame_right_listBox.curIndex)
//		isEmpty = self.frame_right_listBox.size() == 0
//		multiSelection = len(self.frame_right_listBox.curselection()) > 1
//		menu = Menu(tearoff=0)
//		menu.add_command(label="Изменить", command = lambda: self.editCurrentLine(self))
//		menu.entryconfig(0,state = DISABLED if (isEmpty or multiSelection) else NORMAL)
//		menu.add_command(label="Удалить", command = lambda: self.removeCurrentSelection(self))
//		menu.entryconfig(1,state = DISABLED if isEmpty else NORMAL)
//		menu.add_command(label="Треугольник") 
//		menu.post(event.x_root, event.y_root)
//		del(menu)
//
//	def parseText(self, parent, text = None):
//	try:
//			joinedText = []
//			for row in text.split('\n'): 
//				try:
//					re.match(r'^\s{0,}[0-9]{1,3}\s{0,}',row).group(0)
//					joinedText.append(row)
//				except Exception as ex: 
//					joinedText[-1] += row
//					continue
//			for row in joinedText: self.frame_right_listBox.insert(END,row)
//			self.recalculateParagraphsNumbers(self)
//		except Exception as ex: self.frame_mid_textBox.insert(END,str(ex)) 


private void RightListboxDrawItem(object sender, DrawItemEventArgs e) //багается на более 260px в пункте
	{
		e.DrawBackground();
		e.DrawFocusRectangle();
		e.Graphics.DrawString(
			(string)rightListbox.Items[e.Index],
			e.Font,
			new SolidBrush(e.ForeColor),
			e.Bounds);
	}

private int GetLinesNumber(string text)
	{
		string[] splitted = text.Split('\n');
		return splitted.Length;
	}

void RightListboxMeasureItem(object sender, MeasureItemEventArgs e)
	{
		e.ItemHeight = (int)this.gostFont.Height * GetLinesNumber((string)rightListbox.Items[e.Index]);
	}
			
	void editCurrentLine(object sender, EventArgs e)
	{
		if (rightListbox.SelectedItems.Count == 1)
		{
			int countSelected = rightListbox.SelectedItems.Count;
			midTexbox.Focus();
			midTexbox.Clear();
			rightListbox.Enabled = false;
			button1.Enabled = false;
			button2.Enabled = true;
			string text = rightListbox.SelectedItem.ToString();
			//text = text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'')
			//text = text.replace(re.search(r'\n[\s]{1,}',text).group(0),'\n')
			midTexbox.Text += text;
		}
		else {}
	}

	void recalculateParagraphsNumbers(){
		if (rightListbox.Items.Count == 0){}
		else{ 
			for(int index = 0; index <rightListbox.Items.Count; index++){
				string text = rightListbox.Items[index].ToString();
				try {
					//text = string.Format("{0} {1}", index+1, )
//					text = str(index+1)+' ' + text.replace(re.match(r'\s{0,}[0-9]{1,3}[\s]{0,}|[,\.;\'~!@\#$%^&*()_+"]{1}',text).group(0),'') #вставка пробелов в начало строки для равнения по краям
//					text = (' '*(len(str(self.frame_right_listBox.size()))- len(str(index+1))))+text 
				} catch (Exception) {
					//pass
					throw;
				}
				rightListbox.Items.RemoveAt(index);
   				rightListbox.Items.Insert(index, text);
			}
		}
	}




/****************end right frame functions********************/
		
	}
}
