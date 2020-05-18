import smtplib
import worQt_time_lib
from email.mime.text import MIMEText

def templates_load():
	pass

def templates_set():
	pass

def message_send_late_for_work(day):
	today = day.strftime("%d.%m.%Y")
	time_start = day.strftime("%H:%M:%S")
	time_delta = worQt_time_lib.get_time_delta(start,finish)
	time_full_hours = math.ceil(self.timeDeltaLate.seconds / 3600)
	if worQt_time_lib.getTime_AfterWorkStarted(self) is None: return None
	subject = ["Выход на работу",today]
	message = ["<br>{}</br>".format(today),
				"<br>Пришел на работу в : {}</br>".format(time_start),
				"<br>Пришел позже на : {}</br>".format(time_delta),
				"<br>Часов в отработку: {} ч</br>".format(time_full_hours)]		
	message_send(message)

def message_send_extrawork_morning(day):
	today = day.strftime("%d.%m.%Y")
	time_start = day.strftime("%H:%M:%S") #чекать начало сессии в день до работы
	time_delta = worQt_time_lib.get_time_delta(start,finish)
	time_full_hours = math.floor(self.timeDeltaBefore.seconds / 3600)
	if worQt_time_lib.getTime_MorningWork(self) is None: return None
	subject = ["Переработка",today]
	message = ["<br>{}</br>".format(today),
				"<br>Пришел на работу в : {}</br>".format(time_start),
				"<br>Пришел раньше на : {}</br>".format(time_delta),
				"<br>Полных часов: {} ч</br>".format(time_full_hours),
				"<br><b>{}<b></br>".format(self.workForFree)]
	message_send(message)

def message_send_extrwork_checkin(day):
	today = day.strftime("%d.%m.%Y")
	time_start = day.strftime("%H:%M:%S")
	subject = ["Переработка",today] 
	message = ["<br>{}</br>".format(today),
				"<br>Пришел на работу в : {}</br>".format(time_start)]			
	message_send(message)

def message_send_extrawork_regular(day):
	today = day.strftime("%d.%m.%Y")
	time_start = '' #get from config by day 
	time_finish = self.time_finish_of_extra.strftime("%H:%M:%S")
	time_delta = worQt_time_lib.get_time_extra_work()
	time_WTF = worQt_time_lib.extract_time_format(self,self.timeDelta)
	time_full_hours = math.floor(self.timeDelta.seconds / 3600)
	subject = ["Переработка",today] 
	text = (self.textEdit.toPlainText()).split("\n")
	activity = ["<br>{}</br>".format(row) for row in text]
	message = ["<br>{}</br>".format(today),
				"<br>Ушел в : {}</br>".format(time_finish_of_extra),
				"<br>Переработано: {}</br>".format(time_WTF),
				"<br>Полных часов: {} ч</br>".format(),
				"{}".format("".join(activity)),
				"<br><b>{}<b></br>".format(self.workForFree)]
	if self.is_weekend:
		time_weekend = self.time_start_of_extra.strftime("%H:%M:%S")
		message.insert(1,"<br>Пришел в: {}</br>".format(time_weekend))
	message_send(message)

def message_send(message):
		try:
			message = "".join(message)
			namespace = outlook.GetNameSpace("MAPI")
			user = str(namespace.CurrentUser)
			mail = outlook.CreateItem(0)
			mail.To = ""
			mail.CC = ""
			for i in range(self.widget_list.count()):
				attachment = self.widget_list.item(i).text()
				mail.Attachments.Add(attachment)
			subject.insert(1,user)
			mail.Subject = " - ".join(subject)
			mail.GetInspector 
			index = mail.HTMLbody.find(">", mail.HTMLbody.find("<body")) 
			mail.HTMLbody = mail.HTMLbody[:index + 1] + message + mail.HTMLbody[index + 1:] 
			mail.Display(True)
			try: self.getSessionStart()
			except: pass
		except Exception as ex:
			worQt_cache_lib.log_dump_crash()
