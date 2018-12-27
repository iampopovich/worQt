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
		self.title = parent.title('leaver')
		self.frame_activity = LabelFrame(parent, text = 'Активность')
		self.frame_activity.pack()
		self.activityTextBox = Text(self.frame_activity, height = 10, width = 40, font = 'arial 10',wrap = WORD)
		self.activityTextBox.pack()
		self.activityTextBox.focus()
		self.checkBox_is_active = BooleanVar()
		self.weekendCheckBox = ttk.Checkbutton(parent, text = 'Работа в выходной день', variable = self.checkBox_is_active)
		self.weekendCheckBox.config(command = lambda: self.showWeekendTimeEntry(self))
		self.weekendCheckBox.pack()
		self.subFrame_weekendTime = LabelFrame(parent, text  = 'Начало раб.дня')
		self.timeStartEntry = Entry(self.subFrame_weekendTime)
		self.timeStartEntry.pack()
		self.nonWeekendLabel = Label(self.subFrame_weekendTime)
		self.nonWeekendLabel.config(text = 'Это точно не сегодня')
		self.nonWeekendLabel.pack()
		self.alertLabel = Label()
		self.buttonSend = ttk.Button(parent, text = 'Создать письмо', command = lambda: self.sendMessage(self))
		self.buttonSend.pack(side = BOTTOM)

	def showWeekendTimeEntry(self, master):
		if self.checkBox_is_active.get():self.subFrame_weekendTime.pack()
		else: self.subFrame_weekendTime.pack_forget()
		weekDay = dt.datetime.today().weekday()
		if weekDay in [5,6]: self.nonWeekendLabel.pack_forget()
		else:	self.timeStartEntry.pack_forget()

	def sendMessage(self, parent):
		params = list(self.getTime())
		subject = 'Переработка - %s' %params[0]
		text = (self.activityTextBox.get('1.0','end-1c')).split('\n')
		activity = ['<br>%s</br>' %row for row in text]
		message = ['<br>%s</br>' %params[0],
					'<br>Ушел в : %s</br>' %params[2],
					'<br>Переработано: %s ч</br>' %params[3],
					'<br>Полных часов: %s ч</br>' %params[4],
					'%s' %''.join(activity)]
		if params[-1]: message.insert(1,'<br>Пришел в: %s</br>' %params[1])
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
	
	def getTime(self, weekend = False):
		FMT = '%d.%m.%Y %H:%M:%S'
		today = dt.datetime.today().strftime('%d.%m.%Y')
		weekDay = dt.datetime.today().weekday()
		if weekDay in [5,6]:
			weekend = True
			stringTime = self.timeStartEntry.get()
			try:
				timeStartOfExtra = dt.datetime.strptime('%s %s:00' %(today,stringTime), FMT)
			except:
				self.alertLabel.pack()
				self.alertLabel.config(text = 'Вводи время в формате ЧЧ:ММ')
				self.timeStartEntry.delete(0,END)
				self.timeStartEntry.focus()
				return None
				#закинуть проверку на 4 часа
		elif weekDay in [4]: timeStartOfExtra = dt.datetime.strptime('%s 16:30:00' %today, FMT)
		else: timeStartOfExtra = dt.datetime.strptime('%s 17:45:00' %today, FMT)
		timeFinishOfExtra = dt.datetime.now()
		timeDelta = timeFinishOfExtra - timeStartOfExtra #боевка
		if timeDelta > dt.timedelta(minutes=1):
			timedDeltaInFact = str(timeDelta)[0:4]
			timeDelta = (str(timeDelta))[0]
		else: 
			self.activityTextBox.delete('1.0', END)
			self.activityTextBox.insert(END,'Рабочий день еще продолжается')
			return None
		return today,timeStartOfExtra.strftime('%H:%M'),timeFinishOfExtra.strftime('%H:%M'),timedDeltaInFact,timeDelta,weekend
		
def main():
	root = Tk()
	frame = Emailer(root)
	root.mainloop()

if __name__ == '__main__':
