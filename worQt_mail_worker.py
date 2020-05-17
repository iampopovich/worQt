import smtplib
from email.mime.text import MIMEText

def templates_load():
	pass

def templates_set():
	pass

def message_send(self):
		try:
			today = self.today.strftime("%d.%m.%Y")
			if self.sender() == self.pushButton5:
				if worQt_time_lib.getTime_AfterWorkStarted(self) is None: return None
				subject = ["Выход на работу",today]
				message = ["<br>{0}</br>".format(today),
							"<br>Пришел на работу в : {0}</br>".format(dt.datetime.now().strftime("%H:%M:%S")),
							"<br>Пришел позже на : {0}</br>".format(worQt_time_lib.extractTimeFormat(self,self.timeDeltaLate)),
							"<br>Часов в отработку: {0} ч</br>".format(math.ceil(self.timeDeltaLate.seconds / 3600))]	
			elif self.sender() == self.pushButton6:
				if worQt_time_lib.getTime_MorningWork(self) is None: return None
				subject = ["Переработка",today]
				message = ["<br>{0}</br>".format(today),
							"<br>Пришел на работу в : {0}</br>".format(dt.datetime.now().strftime("%H:%M:%S")),
							"<br>Пришел раньше на : {0}</br>".format(worQt_time_lib.extractTimeFormat(self,self.timeDeltaBefore)),
							"<br>Полных часов: {0} ч</br>".format(math.floor(self.timeDeltaBefore.seconds / 3600)),
							"<br><b>{0}<b></br>".format(self.workForFree)]
			elif self.sender() == self.pushButton4:
				self.time_start_of_extra = dt.datetime.now()
				subject = ["Переработка",today] 
				message = ["<br>{0}</br>".format(today),
							"<br>Пришел на работу в : {0}</br>".format(dt.datetime.now().strftime("%H:%M:%S"))]			
			else:
				if self.getTime_ExtraWork() is None: return None
				subject = ["Переработка",today] 
				text = (self.textEdit.toPlainText()).split("\n")
				activity = ["<br>{0}</br>".format(row) for row in text]
				message = ["<br>{0}</br>".format(today),
							"<br>Ушел в : {0}</br>".format(self.time_finish_of_extra.strftime("%H:%M:%S")),
							"<br>Переработано: {0}</br>".format(worQt_time_lib.extractTimeFormat(self,self.timeDelta)),
							"<br>Полных часов: {0} ч</br>".format(math.floor(self.timeDelta.seconds / 3600)),
							"{0}".format("".join(activity)),
							"<br><b>{0}<b></br>".format(self.workForFree)]
				if self.is_weekend: message.insert(1,"<br>Пришел в: {0}</br>".format(self.time_start_of_extra.strftime("%H:%M:%S")))
			worQt_cache_lib.writeLog(self,"session_log",[self.time_start_of_extra,self.time_finish_of_extra,None,None,None])
			message = "".join(message)
			outlook = win32.Dispatch("outlook.application")
			# if win32ui.FindWindow(None, "Microsoft Outlook"): pass
			# else: os.startfile("outlook")
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
			#mail.send #uncomment if you want to send instead of displaying
			#else: sys.exit(app.exec_())
		except Exception as ex:
			worQt_cache_lib.log_dump_crash()
