import win32com.client as win32   
import datetime as dt
from tkinter import *
from tkinter import ttk

#не работает для шаблонов , оформленных чисто доками, без маркапов

class Emailer:
	def __init__(self, parent):
		##window init
		self.parent = parent
		self.parent.resizable(False, False)
		self.title = parent.title('leaver v1.1')
		self.frame_activity = LabelFrame(parent, text = 'Активность')
		self.frame_activity.pack()
		self.activityTextBox = Text(self.frame_activity, height = 10, width = 40, font = 'arial 10',wrap = WORD)
		self.activityTextBox.pack()
		self.activityTextBox.focus()
		self.checkBox_is_active = BooleanVar()
		#self.weekendCheckBox = ttk.Checkbutton(parent, text = 'Работа в выходной день', variable = self.checkBox_is_active)
		#self.weekendCheckBox.config(command = lambda: self.showWeekendTimeEntry(self))
		#self.weekendCheckBox.pack()
		self.subFrame_weekendTime = LabelFrame(parent, text  = 'Начало рабочего дня в выходной')
		self.timeStartEntry = Entry(self.subFrame_weekendTime)
		self.timeStartEntry.pack()
		self.nonWeekendLabel = Label(self.subFrame_weekendTime)
		self.nonWeekendLabel.config(text = 'Это точно не сегодня')
		self.nonWeekendLabel.pack()
		self.alertLabel = Label()
		self.buttonSend = ttk.Button(parent, text = 'Создать письмо', command = lambda: self.sendMessage(self))
		self.buttonSend.pack(side = BOTTOM)
		###custom variables
		self.timeStartOfExtra = None
		self.timeFinishOfExtra = None
		self.timeDelta = None
		self.timeDeltaInFact = None
		self.today = dt.datetime.today().strftime('%d.%m.%Y')
		self.weekDay = dt.datetime.today().weekday()
		self.isWeekend = self.weekDay in [5,6]
		self.FMT = '%d.%m.%Y %H:%M:%S'
		self.showWeekendTimeEntry(self)


	def showWeekendTimeEntry(self, master):
		if self.isWeekend:
			self.subFrame_weekendTime.pack()
			self.nonWeekendLabel.pack_forget()
		else: 
			self.timeStartEntry.pack_forget()
			self.subFrame_weekendTime.pack_forget()

	def sendMessage(self, parent):
		if self.getTime() is None: return None
		subject = 'Переработка - %s' %self.today
		text = (self.activityTextBox.get('1.0','end-1c')).split('\n')
		activity = ['<br>%s</br>' %row for row in text]
		message = ['<br>%s</br>' %self.today,
					'<br>Ушел в : %s</br>' %self.timeFinishOfExtra.strftime('%H:%M'),
					'<br>Переработано: %s ч</br>' %self.timeDeltaInFact,
					'<br>Полных часов: %s ч</br>' %self.timeDelta,
					'%s' %''.join(activity)]
		if self.isWeekend: message.insert(1,'<br>Пришел в: %s</br>' %self.timeStartOfExtra.strftime('%H:%M'))
		message = ''.join(message)
		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = 'exampleTo@company.uk'
		mail.CC = 'exampleCopy@company.us'
		mail.Subject = subject
		mail.GetInspector 
		#mail.Body = message
		index = mail.HTMLbody.find('>', mail.HTMLbody.find('<body')) 
		mail.HTMLbody = mail.HTMLbody[:index + 1] + message + mail.HTMLbody[index + 1:] 
		mail.Display(True)
		#mail.send #uncomment if you want to send instead of displaying
		self.parent.destroy()
	
	def getTime(self):
		if self.isWeekend:
			stringTime = self.timeStartEntry.get()
			try:
				self.timeStartOfExtra = dt.datetime.strptime('%s %s:00' %(self.today,stringTime), self.FMT)
			except:
				self.alertLabel.pack()
				self.alertLabel.config(text = 'Вводи время в формате ЧЧ:ММ')
				self.timeStartEntry.delete(0,END)
				self.timeStartEntry.focus()
				return None
				#закинуть проверку на 4 часа!!!!
		elif self.weekDay in [4]: self.timeStartOfExtra = dt.datetime.strptime('%s 16:30:00' %self.today, self.FMT)
		else: self.timeStartOfExtra = dt.datetime.strptime('%s 17:45:00' %self.today, self.FMT)
		self.timeFinishOfExtra = dt.datetime.now()
		self.timeDelta = self.timeFinishOfExtra - self.timeStartOfExtra #боевка
		if self.timeDelta > dt.timedelta(minutes=1):
			self.timeDeltaInFact = str(self.timeDelta)[0:4]
			self.timeDelta = (str(self.timeDelta))[0]
		else: 
			self.activityTextBox.delete('1.0', END)
			self.activityTextBox.insert(END,'Рабочий день еще продолжается')			
			return None
		return 1
		
def main():
	root = Tk()
	frame = Emailer(root)
	root.mainloop()

if __name__ == '__main__':
	main()
