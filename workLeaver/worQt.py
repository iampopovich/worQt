# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime as dt
import win32com.client as win32  
import urllib.request
import ssl
import os
import math
import sqlite3
import sys
import time
#import worQt_time_lib
from threading import Thread,Timer
'''
создать вкладку со статистикой?
'''
class DragAndDropList(QtWidgets.QListWidget):
	def __init__(self, parent=None, **args):
		super(DragAndDropList, self).__init__(parent, **args)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QtWidgets.QListWidget.InternalMove)

	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls():
			e.accept()
		else: e.ignore()

	def dropEvent(self, e):
		for url in e.mimeData().urls():
			attachment = url.url().strip('file:///')
			self.addItem(attachment)

class Ui_Dialog(QtWidgets.QDialog):
	def __init__(self,parent = None, **args):
		super(Ui_Dialog,self).__init__(parent,**args)
		self.version = "v2.11.5"
		self.FMT = "%Y-%m-%d %H:%M:%S"
		self.today = dt.datetime.today()
		self.weekday = self.today.weekday()
		self.weekendSync = False
		self.isWeekend = True# self.checkIsWeekend()
		self.timeStartOfDay = self.convertTime("08:30:00")
		self.timeEndOfDay = self.convertTime("17:45:00") 
		self.isLate = self.timeStartOfDay < dt.datetime.now() < self.timeEndOfDay
		self.isBeforeStart = dt.datetime.now() < self.timeStartOfDay
		self.timeStartOfExtra = None
		self.timeFinishOfExtra = None
		self.timeDelta = None
		self.timeDeltaLate = None
		self.timeDeltaBefore = None
		self.workForFree = ""
		self.logFile = self.getLogFile()
		self._shutdown_timer = QtCore.QTimer(self)
		self._shutdown_timer.setSingleShot(True)
		self._shutdown_timer.timeout.connect(sys.exit)#self.closeUp)
		self._shutdown_timer.start(2700000) #shutdown after 45 minutes

	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.setWindowModality(QtCore.Qt.NonModal)
		Dialog.setFixedSize(365, 370)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(7, 3, 350, 360))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		# 
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		# 
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
		# 
		self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget)
		self.timeEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit.setObjectName("timeEdit")
		self.timeEdit.setEnabled(self.isWeekend)
		self.gridLayout.addWidget(self.timeEdit, 3, 1, 1, 1)
		# 
		self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
		self.textEdit.setObjectName("textEdit")
		self.textEdit.setFont(font)
		self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)
		# 
		self.informationLabel = QtWidgets.QLabel(self.gridLayoutWidget)
		self.informationLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.informationLabel.setObjectName("informationLabel")
		self.gridLayout.addWidget(self.informationLabel, 1, 0, 1, 3)
		# 
		self.listWidget = DragAndDropList(self.gridLayoutWidget)
		self.listWidget.setObjectName("listWidget")
		self.gridLayout.addWidget(self.listWidget,6,0,3,2)
		# 
		self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText("Отправить письмо")
		self.pushButton.clicked.connect(self.sendMessage)
		self.gridLayout.addWidget(self.pushButton, 4, 2, 1, 1)
		# 
		self.pushButton1 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton1.setObjectName("pushButton1")
		self.pushButton1.setText("+")
		self.pushButton1.clicked.connect(self.addAttachment)
		self.gridLayout.addWidget(self.pushButton1,6,2,1,1)
		# 
		self.pushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton2.setObjectName("pushButton2")
		self.pushButton2.setText("-")
		self.pushButton2.clicked.connect(self.removeAttachment)
		self.gridLayout.addWidget(self.pushButton2,7,2,1,1)
		# 
		self.pushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton3.setObjectName("pushButton3")
		self.pushButton3.setText("Очистить")
		self.pushButton3.clicked.connect(self.clearAttachment)
		self.gridLayout.addWidget(self.pushButton3,8,2,1,1)
		# 
		self.pushButton4 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton4.setObjectName("pushButton4")
		self.pushButton4.setText("Отметиться")
		self.pushButton4.setEnabled(self.isWeekend)
		self.pushButton4.clicked.connect(self.sendMessage)
		self.gridLayout.addWidget(self.pushButton4, 3, 2, 1, 1)
		# 
		self.pushButton5 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton5.setObjectName("pushButton5")
		self.pushButton5.setText("Пришел позже 8:30")
		self.pushButton5.setEnabled(not self.isWeekend if self.isWeekend else self.isLate)
		self.pushButton5.clicked.connect(self.sendMessage)
		self.gridLayout.addWidget(self.pushButton5, 4, 0, 1, 1)
		# 
		self.pushButton6 = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton6.setObjectName("pushButton6")
		self.pushButton6.setText("Пришел раньше 8:30")
		self.pushButton6.setEnabled(not self.isWeekend if self.isWeekend else self.isBeforeStart)
		self.pushButton6.clicked.connect(self.sendMessage)
		self.gridLayout.addWidget(self.pushButton6, 4, 1, 1, 1)
		# 
		self.retranslateUi(Dialog)
		if self.isWeekend: self.getSessionStart()
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "WorQt %s" %self.version))
		self.timeEdit.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))
		self.pushButton.setText(_translate("Dialog", "Отправить"))
		self.pushButton1.setText(_translate("Dialog", "+"))
		self.pushButton2.setText(_translate("Dialog", "-"))
		self.pushButton3.setText(_translate("Dialog", "Очистить"))
		self.pushButton4.setText(_translate("Dialog", "Отметиться"))
		self.pushButton5.setText(_translate("Dialog", "Пришел позже 8:30"))
		self.pushButton6.setText(_translate("Dialog", "Пришел раньше 8:30"))
		self.label.setText(_translate("Dialog", "Начало рабочего дня"))

#attachment section
	def addAttachment(self, parent):
		try:
			attachments = QtWidgets.QFileDialog.getOpenFileUrls()[0]
			for url in attachments:
				attachment = url.url().strip('file:///')
				self.listWidget.addItem(attachment)
		except Exception as ex:
			self.writeLog('crash_log',[dt.datetime.now(),'addAttachment failed with %s' %ex])

	def removeAttachment(self, parent):
		try:
			listItems = self.listWidget.selectedItems()
			if not listItems: return
			for item in listItems:
				index = self.listWidget.row(item)
				self.listWidget.takeItem(index)
		except Exception as ex:
			self.writeLog('crash_log',[dt.datetime.now(),'removeAttachment failed with %s' %ex])
	
	def clearAttachment(self, parent):
		try: self.listWidget.clear()
		except Exception as ex:
			self.writeLog('crash_log',[dt.datetime.now(),'clearAttachment failed with %s' %ex])

#time section
	def checkIsWeekend(self):
		try:
			_today = self.today.strftime("%Y%m%d")
			scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			chemeo_search_url = 'https://isdayoff.ru/%s' %_today
			response = urllib.request.urlopen(chemeo_search_url, context = scontext, timeout = 5)
			response = int(response.read().decode('utf-8'))
			outVal = True if response in [1] else False
			self.weekendSync = True
		except:	outVal = True if self.weekday in [5,6] else False
		return outVal 

	def getTime_MorningWork(self):
		self.timeDeltaBefore = self.timeStartOfDay - dt.datetime.now()
		if not(self.isWeekend) and self.timeDeltaBefore < dt.timedelta(hours = 1): 
			self.workForFree = "Отработка меньше 1 часа в будний день"	
		return True

	def getTime_ExtraWork(self):
		today = self.today.strftime("%d.%m.%Y")
		if self.isWeekend: self.timeStartOfExtra = dt.datetime.strptime("%s %s" %(today,self.timeEdit.text()), "%d.%m.%Y %H:%M:%S")
		elif self.weekday in [4]: self.timeStartOfExtra = self.convertTime("16:30:00")
		else:  self.timeStartOfExtra = self.timeEndOfDay
		self.timeFinishOfExtra = dt.datetime.now()
		self.timeDelta = self.timeFinishOfExtra - self.timeStartOfExtra
		if self.timeDelta < dt.timedelta(seconds = 1):
			self.informationLabel.setText("Рабочий день еще продолжается")
			return None
		if self.timeDelta > dt.timedelta(seconds = 1): 
			if self.isWeekend and self.timeDelta < dt.timedelta(hours = 4):
				self.workForFree = "Отработка меньше 4 часов в выходной"			
				return True
			if not(self.isWeekend) and self.timeDelta < dt.timedelta(hours = 1): 
				self.workForFree = "Отработка меньше 1 часа в будний день"	
				return True
			return True
	
	def getTime_AfterWorkStarted(self):
		if dt.datetime.now() > self.timeEndOfDay:
			self.informationLabel.setText("Уже слишком поздно")
			return None
		else: self.timeDeltaLate = dt.datetime.now() - self.timeStartOfDay
		return True
				
	def extractTimeFormat(self,tdelta):
		try:
			d = {}
			d['days'] = tdelta.days
			d['hrs'], rem = divmod(tdelta.seconds, 3600)
			d['min'], d['sec'] = divmod(rem, 60)
			for key,val in d.items():
				if d[key] < 10 : d[key] = "0%s"%(val)
			return ('%s:%s:%s' %(d['hrs'],d['min'],d['sec']))
		except Exception as ex:
			self.writeLog('crash_log',[dt.datetime.now(),'extractTimeFormat failed with %s' %ex])

	def convertTime(self, stringTime):
		out = dt.datetime.strptime("%s %s" %(self.today.date(),stringTime), self.FMT)
		return out

#base function section
	def sendMessage(self, parent):
		try:
			today = self.today.strftime("%d.%m.%Y")
			if self.sender() == self.pushButton5:
				if self.getTime_AfterWorkStarted() is None: return None
				subject = ['Выход на работу',today]
				message = ['<br>%s</br>' %today,
							'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
							'<br>Пришел позже на : %s</br>' %self.extractTimeFormat(self.timeDeltaLate),
							'<br>Часов в отработку: %s ч</br>' %(math.ceil(self.timeDeltaLate.seconds / 3600))]	
			elif self.sender() == self.pushButton6:
				if self.getTime_MorningWork() is None: return None
				subject = ['Переработка',today]
				message = ['<br>%s</br>' %today,
							'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
							'<br>Пришел раньше на : %s</br>' %self.extractTimeFormat(self.timeDeltaBefore),
							'<br>Полных часов: %s ч</br>' %(math.floor(self.timeDeltaBefore.seconds / 3600)),
							'<br><b>%s<b></br>'%self.workForFree]
			elif self.sender() == self.pushButton4:
				self.timeStartOfExtra = dt.datetime.now()
				subject = ['Переработка',today] 
				message = ['<br>%s</br>' %today,
					'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S')]			
			else:
				if self.getTime_ExtraWork() is None: return None
				subject = ['Переработка',today] 
				text = (self.textEdit.toPlainText()).split('\n')
				activity = ['<br>%s</br>' %row for row in text]
				message = ['<br>%s</br>' %today,
							'<br>Ушел в : %s</br>' %self.timeFinishOfExtra.strftime('%H:%M:%S'),
							'<br>Переработано: %s</br>' %self.extractTimeFormat(self.timeDelta),
							'<br>Полных часов: %s ч</br>' %(math.floor(self.timeDelta.seconds / 3600)),
							'%s' %(''.join(activity)),'<br><b>%s<b></br>'%self.workForFree]
				if self.isWeekend: message.insert(1,'<br>Пришел в: %s</br>' %self.timeStartOfExtra.strftime('%H:%M:%S'))
			self.writeLog('session_log',[self.timeStartOfExtra,self.timeFinishOfExtra])
			message = ''.join(message)
			outlook = win32.Dispatch('outlook.application')
			# if win32ui.FindWindow(None, "Microsoft Outlook"): pass
			# else: os.startfile("outlook")
			namespace = outlook.GetNameSpace("MAPI")
			user = str(namespace.CurrentUser)
			mail = outlook.CreateItem(0)
			mail.To = ''
			mail.CC = ''
			for i in range(self.listWidget.count()):
				attachment = self.listWidget.item(i).text()
				mail.Attachments.Add(attachment)
			subject.insert(1,user)
			mail.Subject = ' - '.join(subject)
			mail.GetInspector 
			index = mail.HTMLbody.find('>', mail.HTMLbody.find('<body')) 
			mail.HTMLbody = mail.HTMLbody[:index + 1] + message + mail.HTMLbody[index + 1:] 
			mail.Display(True)
			#mail.send #uncomment if you want to send instead of displaying
			#else: sys.exit(app.exec_())
		except Exception as ex:
			self.writeLog('crash_log',[dt.datetime.now(),'sendMessage failed with %s' %ex])

#caching section		
	def getLogFile(self):
		try:
			dirName = '%s\\worqt_cache' %os.environ['APPDATA']
			fileName = '%s\\worqt_cache\\worqt_log.sqlite' %os.environ['APPDATA']
			if os.path.isdir(dirName): pass
			else: os.mkdir(dirName)
			connection = sqlite3.connect(fileName)
			cursor = connection.cursor()
			try: 
				query = '''select * from session_log limit 1'''
				cursor.execute(query)
			except:
				self.createLogFile(fileName, connection, cursor)
			connection.close()
			return fileName 
		except Exception as ex:
			self.writeLog('crash_log',[dt.datetime.now(),'getLog failed with %s' %ex])
	
	def createLogFile(self, fname, conn, curs):
		queries = [
				'''create table session_log
					(date_ text, session_start text, session_end text)''',
				'''create table crash_log
				(date_ text, datetime_ text, log_string varchar)'''
			]
		for q in queries:
			curs.execute(q)
			conn.commit()

	def writeLog(self, table, values):
		try:
			print(table)
			print(values)
			query = ''
			connection = sqlite3.connect(self.logFile)
			cursor = connection.cursor() 
			currentDate = dt.date.today().isoformat()
			values.insert(0, currentDate)
			if table == 'session_log':
				query = 'select * from session_log where date_ like \'{0}\''.format(currentDate)
				if cursor.execute(query).fetchone() is None:
					st_values = ['\'%s\''%s for s in values]
					query = 'insert into {0} values ({1})'.format(table, ','.join(st_values))	
				else:				
					query = '''update session_log 
					set session_end = \'{0}\' 
					where date_ like \'{1}\' and
					session_end is \'None\''''.format(self.timeFinishOfExtra,currentDate)
					cursor.execute(query)
					connection.commit()
					connection.close()
					return None
			if table == 'crash_log':
				st_values = ['\'%s\''%s for s in values]
				query = 'insert into {0} values ({1})'.format(table, ','.join(st_values))
			cursor.execute(query)
			connection.commit()
			connection.close()
		except Exception as ex:
			#self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, 'writeCacheFile failed with %s' %ex)
			raise ex
	
	def getSessionStart(self):
		try:
			connection = sqlite3.connect(self.logFile)
			#connection.row_factory = sqlite3.Row
			cursor = connection.cursor()
			currentDate = dt.date.today().isoformat()
			query = 'select session_start from session_log where date_ like \'{0}\''.format(currentDate)
			timeStart = cursor.execute(query).fetchone()[0]
			sessionStart = dt.datetime.strptime(timeStart, "%Y-%m-%d %H:%M:%S.%f")
			self.timeEdit.setTime(QtCore.QTime(sessionStart.hour,sessionStart.minute,sessionStart.second))
		except Exception as ex:
			self.informationLabel.setText('Не могу определить начало дня. Введите время вручную')


def main(args):
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	Dialog.show()
	app.exec_()

if __name__ == "__main__":
	main(sys.argv)	
