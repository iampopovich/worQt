# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import re
import datetime as dt
import win32com.client as win32  
import random 
import urllib.request
import ssl
import math

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		# glob variables 
		self.today = dt.datetime.today()
		self.weekday = self.today.weekday()
		self.weekendSync = False
		self.isWeekend = self.checkIsWeekend()
		self.timeStartOfExtra = None
		self.timeFinishOfExtra = None
		self.timeDelta = None
		self.timeDeltaLate = None
		self.FMT = "%Y-%m-%d %H:%M:%S"
		# self.workForFree = False
		self.color = ['red','green','blue','black']
		############################################
		Dialog.setObjectName("Dialog")
		Dialog.setWindowModality(QtCore.Qt.NonModal)
		Dialog.setFixedSize(370, 380)
		self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 351, 361))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget)
		self.timeEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit.setObjectName("timeEdit")
		self.timeEdit.setEnabled(self.isWeekend)
		self.gridLayout.addWidget(self.timeEdit, 3, 1, 1, 2)
		self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText("Отправить письмо")
		self.pushButton.clicked.connect(self.sendMessage)
		self.gridLayout.addWidget(self.pushButton, 4, 2, 1, 1)
		self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
		self.textEdit.setObjectName("textEdit")
		font = QtGui.QFont()
		font.setPointSize(10)
		self.textEdit.setFont(font)
		self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)
		self.checkBox_2 = QtWidgets.QCheckBox(self.gridLayoutWidget)
		self.checkBox_2.setObjectName("checkBox_2")
		self.checkBox_2.stateChanged.connect(self.sorryImLate)
		self.checkBox_2.setEnabled(not self.isWeekend)
		self.gridLayout.addWidget(self.checkBox_2, 4, 0, 1, 1)
		self.checkBox_3 = QtWidgets.QCheckBox(self.gridLayoutWidget)
		self.checkBox_3.setObjectName("checkBox_3")
		self.checkBox_3.setEnabled(not self.isWeekend)
		self.checkBox_3.stateChanged.connect(self.earlyBirdy)
		self.gridLayout.addWidget(self.checkBox_3, 5, 0, 1, 1)
		self.informationLabel = QtWidgets.QLabel(self.gridLayoutWidget)
		self.informationLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.informationLabel.setObjectName("informationLabel")
		self.gridLayout.addWidget(self.informationLabel, 1, 0, 1, 3)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "WorQt"))
		self.timeEdit.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))
		self.pushButton.setText(_translate("Dialog", "Отправить"))
		self.checkBox_3.setText(_translate("Dialog", "Пришел раньше 8:30"))
		self.checkBox_2.setText(_translate("Dialog", "Пришел позже 8:30"))
		self.label.setText(_translate("Dialog", "Начало рабочего дня"))

	def sorryImLate(self):
		flag = self.checkBox_2.checkState()
		self.checkBox_3.setEnabled(not flag)

	def earlyBirdy(self,parent):
		flag = self.checkBox_3.checkState()
		self.checkBox_2.setEnabled(not flag)

	def checkIsWeekend(self):
		today = self.today.strftime("%Y%m%d")
		try:
			scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			chemeo_search_url = 'https://isdayoff.ru/%s' %today
			response = urllib.request.urlopen(chemeo_search_url, context=scontext)
			response = int(response.read().decode('utf-8'))
			outVal = True if response in [1] else False
			self.weekendSync = True
		except:	outVal = True if self.weekday in [5,6] else False
		return outVal 

	def getTime(self, mode = 1):
		today = self.today.strftime("%d.%m.%Y")
		if mode == 2:
			workDayStart = dt.datetime.strptime("%s 08:30:00" %self.today.date(), self.FMT)
			self.timeDeltaLate = dt.datetime.now() - workDayStart
		elif mode == 3:
			workDayStart = dt.datetime.strptime("%s 08:30:00" %self.today.date(), self.FMT)
			self.timeDeltaLate = workDayStart - dt.datetime.now()
			if self.timeDeltaLate < dt.timedelta(seconds = 0):
				self.informationLabel.setText("Рабочий день еще не начался")			
				return None
		else:
			if self.isWeekend: self.timeStartOfExtra = dt.datetime.strptime("%s %s" %(today,self.timeEdit.text()), "%d.%m.%Y %H:%M:%S")
			elif self.weekday in [4]: self.timeStartOfExtra = dt.datetime.strptime("%s 16:30:00" %self.today.date(), self.FMT)
			else:  self.timeStartOfExtra = dt.datetime.strptime("%s 17:45:00" %self.today.date(), self.FMT)
			self.timeFinishOfExtra = dt.datetime.now()
			self.timeDelta = self.timeFinishOfExtra - self.timeStartOfExtra
			if self.timeDelta > dt.timedelta(minutes = 1): return None
			if self.timeDelta < dt.timedelta(minutes = 1):
				self.informationLabel.setText("Рабочий день еще продолжается")
				return None
			if self.isWeekend and self.timeDelta < dt.timedelta(hours = 4):
				self.informationLabel.autoFillBackground
				self.informationLabel.setText("Отработка меньше 4 часов в выходной")			
				return None
			if self.isWeekend and self.timeDelta < dt.timedelta(hours = 1): 
				self.informationLabel.setText("Отработка меньше 1 часа в в будний день")			
				return None
		

	def sendMessage(self, parent):
		today = self.today.strftime("%d.%m.%Y")
		if self.checkBox_2.checkState():
			self.getTime(2)
			subject = 'Выход на работу - %s' %today
			message = ['<br>%s</br>' %today,
						'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
						'<br>Пришел позже на : %s</br>' %str(self.timeDeltaLate)[0:7]]
		elif self.checkBox_3.checkState():
			self.getTime(3)
			subject = 'Переработка - %s' %today
			message = ['<br>%s</br>' %today,
						'<br>Пришел на работу в : %s</br>' %dt.datetime.now().strftime('%H:%M:%S'),
						'<br>Пришел раньше на : %s</br>' %str(self.timeDeltaLate)[0:8]]	
		else:
			self.getTime(1)
			subject = 'Переработка - %s' %today
			text = (self.textEdit.toPlainText()).split('\n')
			activity = ['<br>%s</br>' %row for row in text]
			message = ['<br>%s</br>' %today,
						'<br>Ушел в : %s</br>' %self.timeFinishOfExtra.strftime('%H:%M:%S'),
						'<br>Переработано: %s ч</br>' %str(self.timeDelta)[0:8],
						'<br>Полных часов: %s ч</br>' %str(math.floor(self.timeDelta.seconds / 3600)),
						'%s' %(''.join(activity))]
			if self.isWeekend: message.insert(1,'<br>Пришел в: %s</br>' %self.timeStartOfExtra.strftime('%H:%M:%S'))
		message = ''.join(message)
		outlook = win32.Dispatch('outlook.application')
		mail = outlook.CreateItem(0)
		mail.To = '---------------------------'
		mail.CC = '---------------------------'
		mail.Subject = subject
		mail.GetInspector 
		#mail.Body = message
		index = mail.HTMLbody.find('>', mail.HTMLbody.find('<body')) 
		mail.HTMLbody = mail.HTMLbody[:index + 1] + message + mail.HTMLbody[index + 1:] 
		mail.Display(True)
		#mail.send #uncomment if you want to send instead of displaying
		#sys.exit(app.exec_())
		#else: sys.exit(app.exec_())

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	ui.getTime()
	Dialog.show()
	sys.exit(app.exec_())

