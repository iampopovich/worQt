# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime as dt
import win32com.client as win32  
import urllib.request
import ssl
import os
import math
import json
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
		self.version = "v2.11.0"
		self.FMT = "%Y-%m-%d %H:%M:%S"
		self.today = dt.datetime.today()
		self.weekday = self.today.weekday()
		self.weekendSync = False
		self.isWeekend = self.checkIsWeekend()
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
		self.sessionLogDict = {}
		self.crashlogFile = self.getCrashLogFile()
		self.sessionLogFile = self.getSessionLogFile()
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
			self.writeCrashLog('addAttachment failed with %s' %ex)

	def removeAttachment(self, parent):
		try:
			listItems = self.listWidget.selectedItems()
			if not listItems: return
			for item in listItems:
				index = self.listWidget.row(item)
				self.listWidget.takeItem(index)
		except Exception as ex:
			self.writeCrashLog('removeAttachment failed with %s' %ex)
	
	def clearAttachment(self, parent):
		try: self.listWidget.clear()
		except Exception as ex:
			self.writeCrashLog('clearAttachment failed with %s' %ex)

#time section
	def checkIsWeekend(self):
		try:
			today = self.today.strftime("%Y%m%d")
			scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			chemeo_search_url = 'https://isdayoff.ru/%s' %today
			response = urllib.request.urlopen(chemeo_search_url, context = scontext, timeout = 5)
			response = int(response.read().decode('utf-8'))
			outVal = True if response in [1] else False
			self.weekendSync = True
		except:	outVal = True if self.weekday in [5,6] else False
		return outVal 

	def getTime(self, mode):
		try:
			if mode == 2:
				if dt.datetime.now() > self.timeEndOfDay:
					self.informationLabel.setText("Уже слишком поздно")
					return None
				else: self.timeDeltaLate = dt.datetime.now() - self.timeStartOfDay
				return True
			elif mode == 3:
				self.timeDeltaBefore = self.timeStartOfDay - dt.datetime.now()
				if not(self.isWeekend) and self.timeDeltaBefore < dt.timedelta(hours = 1): 
						self.workForFree = "Отработка меньше 1 часа в будний день"	
						return True
				return True
			else:
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
		except Exception as ex:
			self.writeCrashLog('getTime failed with %s' %ex)
				
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
			self.writeCrashLog('extractTimeFormat failed with %s' %ex)
	
	def convertTime(self, stringTime):
		out = dt.datetime.strptime("%s %s" %(self.today.date(),stringTime), self.FMT)
		return out

#base function section
	def sendMessage(self, parent):
		try:
			today = self.today.strftime("%d.%m.%Y")
			if self.sender() == self.pushButton5:
				if self.getTime(2) is None: return None
				subject = ['Выход на работу',today]
				message = ['<br>%s</br>' %today,
							'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
							'<br>Пришел позже на : %s</br>' %self.extractTimeFormat(self.timeDeltaLate),
							'<br>Часов в отработку: %s ч</br>' %(math.ceil(self.timeDeltaLate.seconds / 3600))]	
			elif self.sender() == self.pushButton6:
				if self.getTime(3) is None: return None
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
				self.writeSessionLog()			
			else:
				if self.getTime(1) is None: return None
				subject = ['Переработка',today] 
				text = (self.textEdit.toPlainText()).split('\n')
				activity = ['<br>%s</br>' %row for row in text]
				message = ['<br>%s</br>' %today,
							'<br>Ушел в : %s</br>' %self.timeFinishOfExtra.strftime('%H:%M:%S'),
							'<br>Переработано: %s</br>' %self.extractTimeFormat(self.timeDelta),
							'<br>Полных часов: %s ч</br>' %(math.floor(self.timeDelta.seconds / 3600)),
							'%s' %(''.join(activity)),'<br><b>%s<b></br>'%self.workForFree]
				if self.isWeekend: message.insert(1,'<br>Пришел в: %s</br>' %self.timeStartOfExtra.strftime('%H:%M:%S'))
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
			print('sendMessage failed with %s' %ex)
			self.writeCrashLog('sendMessage failed with %s' %ex)

#caching section
	def getCrashLogFile(self):
		try:
			dirName = '%s\\worqt_cache' %os.environ['APPDATA']
			fileName = '%s\\worqt_cache\\crash_log.txt' %os.environ['APPDATA']
			if os.path.isdir(dirName): pass
			else: os.mkdir(dirName)
			if os.path.isfile(fileName): return fileName 
			else: 
				with open(fileName,'a') as cache: 
					cache.close()
				return fileName
		except Exception as ex:
			self.writeCrashLog('getLog failed with %s' %ex)
		
	def writeCrashLog(self,logString):
		try:
			with open(self.crashlogFile,'a') as log:
				log.write('%s -- %s\n'%(dt.datetime.now(),logString))
			#import pyscreenshoot - slezhka
		except Exception as ex:
			#self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, 'writeCacheFile failed with %s' %ex)
			raise ex

	def getSessionLogFile(self):
		try:
			dirName = '%s\\worqt_cache' %os.environ['APPDATA']
			fileName = '%s\\worqt_cache\\session_log.txt' %os.environ['APPDATA']
			if os.path.isdir(dirName): pass
			else: os.mkdir(dirName)
			if os.path.isfile(fileName): return fileName 
			else: 
				with open(fileName,'w') as cache:
					cache.close()
				return fileName
		except Exception as ex:
			self.writeCrashLog('getLog failed with %s' %ex)
	
	def clearSessionLogFile(self):
		with open(self.sessionLogFile,'w') as cache:
			cache.close()
		pass

	def writeSessionLog(self):
		try:
			with open(self.sessionLogFile,'r') as log: 
				self.sessionLogDict = json.load(log)
			currentDate = dt.date.today().isoformat()
			dayPoint = {'begin':self.timeStartOfExtra,'end':self.timeFinishOfExtra}
			self.sessionLogDict[currentDate] = dayPoint
			with open(self.sessionLogFile,'w') as log: 
				json.dump(self.sessionLogDict,log)
		except Exception as ex:
			#self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, 'writeCacheFile failed with %s' %ex)
			raise ex
	
	def getSessionStart(self):
		try:
			with open(self.sessionLogFile,'r') as log: 
				sessionLog = json.load(log)
			currentDate = dt.date.today().isoformat()
			timeStart = sessionLog[currentDate]['begin']
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
