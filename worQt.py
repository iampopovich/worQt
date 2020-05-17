# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import csv
import os
import worQt_time_lib
import worQt_cache_lib
import worQt_mail_worker
import worQt_config

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
			attachment = url.url().strip("file:///")
			self.addItem(attachment)

class Ui_Dialog(QtWidgets.QDialog):
	def __init__(self,parent = None, **args):
		super(Ui_Dialog,self).__init__(parent,**args)
		self.version = "v3.0.1"
		self.config = worQt_config.get_config()
		self.FMT = "%Y-%m-%d %H:%M:%S"
		self.today = worQt_time_lib.get_today()
		self.is_weekend = worQt_time_lib.check_is_weekend(self.today)
		# self.time_start_of_day = self.config['work_start'] #worQt_time_lib.convert_time(self,"08:30:00") #refactor config
		# self.time_end_of_day = solf.config['worl_end'] #worQt_time_lib.convert_time(self,"17:45:00") #refactor config
		self.is_late = False #worQt_time_lib.check_is_late(self)
		self.is_before_start = False #worQt_time_lib.check_is_time_before_work_start(self)
		# self.time_start_of_extra = None
		# self.time_finish_of_extra = None
		# self.time_delta = None
		# self.time_delta_late = None
		# self.time_delta_before = None
		self.work_for_free = ""
		self.shutdown_time = 2700000
		self.file_log = worQt_cache_lib.get_file_log(self)
		self.init_shutdown_timer()
		self.workfolder = os.getcwd()

	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.setWindowModality(QtCore.Qt.NonModal)
		Dialog.setFixedSize(355, 390)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.tabWidget = QtWidgets.QTabWidget(Dialog)
		self.tabWidget.setGeometry(QtCore.QRect(0, 0, 355, 390))
		self.tabWidget.setObjectName("tabWidget")
		#tab1
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.tabWidget.addTab(self.tab, "Редактор")
		#
		self.gridLayoutWidget1 = QtWidgets.QWidget(self.tab)
		self.gridLayoutWidget1.setGeometry(QtCore.QRect(0, 0, 350, 360))
		self.gridLayoutWidget1.setObjectName("gridLayoutWidget1")
		# 
		self.gridLayout1 = QtWidgets.QGridLayout(self.gridLayoutWidget1)
		self.gridLayout1.setContentsMargins(0, 0, 0, 0)
		self.gridLayout1.setObjectName("gridLayout1")
		# 
		self.label = QtWidgets.QLabel(self.gridLayoutWidget1)
		self.label.setObjectName("label")
		self.gridLayout1.addWidget(self.label, 3, 0, 1, 1)
		# 
		self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget1)
		self.timeEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.timeEdit.setTime(QtCore.QTime(0, 0, 0))
		self.timeEdit.setObjectName("timeEdit")
		self.timeEdit.setEnabled(self.is_weekend)
		self.gridLayout1.addWidget(self.timeEdit, 3, 1, 1, 1)
		# 
		self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget1)
		self.textEdit.setObjectName("textEdit")
		self.textEdit.setFont(font)
		self.gridLayout1.addWidget(self.textEdit, 0, 0, 1, 3)
		# 
		self.informationLabel = QtWidgets.QLabel(self.gridLayoutWidget1)
		self.informationLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.informationLabel.setObjectName("informationLabel")
		self.gridLayout1.addWidget(self.informationLabel, 1, 0, 1, 3)
		# 
		self.widget_list = DragAndDropList(self.gridLayoutWidget1)
		self.widget_list.setObjectName("widget_list")
		self.gridLayout1.addWidget(self.widget_list,6,0,3,2)
		# 
		self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText("Отправить письмо")
		self.pushButton.clicked.connect(worQt_mail_worker.message_send)
		self.gridLayout1.addWidget(self.pushButton, 4, 2, 1, 1)
		# 
		self.pushButton1 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton1.setObjectName("pushButton1")
		self.pushButton1.setText("+")
		self.pushButton1.clicked.connect(self.attachment_add)
		self.gridLayout1.addWidget(self.pushButton1,6,2,1,1)
		# 
		self.pushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton2.setObjectName("pushButton2")
		self.pushButton2.setText("-")
		self.pushButton2.clicked.connect(self.attachment_remove)
		self.gridLayout1.addWidget(self.pushButton2,7,2,1,1)
		# 
		self.pushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton3.setObjectName("pushButton3")
		self.pushButton3.setText("Очистить")
		self.pushButton3.clicked.connect(self.attachment_clear)
		self.gridLayout1.addWidget(self.pushButton3,8,2,1,1)
		# 
		self.pushButton4 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton4.setObjectName("pushButton4")
		self.pushButton4.setText("Отметиться")
		self.pushButton4.setEnabled(self.is_weekend)
		self.pushButton4.clicked.connect(worQt_mail_worker.message_send)
		self.gridLayout1.addWidget(self.pushButton4, 3, 2, 1, 1)
		# 
		self.pushButton5 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton5.setObjectName("pushButton5")
		self.pushButton5.setText("Пришел позже 8:30")
		self.pushButton5.setEnabled(not self.is_weekend if self.is_weekend else self.is_late)
		self.pushButton5.clicked.connect(worQt_mail_worker.message_send_late_for_work)
		self.gridLayout1.addWidget(self.pushButton5, 4, 0, 1, 1)
		# 
		self.pushButton6 = QtWidgets.QPushButton(self.gridLayoutWidget1)
		self.pushButton6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton6.setObjectName("pushButton6")
		self.pushButton6.setText("Пришел раньше 8:30")
		self.pushButton6.setEnabled(not self.is_weekend if self.is_weekend else self.is_before_start)
		self.pushButton6.clicked.connect(worQt_mail_worker.message_send)
		self.gridLayout1.addWidget(self.pushButton6, 4, 1, 1, 1)
		#
		#tab2
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.tabWidget.addTab(self.tab_2, "Статистика (тест)")
		#
		self.gridLayoutWidget2 = QtWidgets.QWidget(self.tab_2)
		self.gridLayoutWidget2.setGeometry(QtCore.QRect(0, 0, 350, 360))
		self.gridLayoutWidget2.setObjectName("gridLayoutWidget2")
		#
		self.gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget2)
		self.gridLayout2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout2.setObjectName("gridLayout2")
		#
		self.pushButton7 = QtWidgets.QPushButton(self.gridLayoutWidget2)
		self.pushButton7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton7.setObjectName("pushButton7")
		self.pushButton7.setText("Обновить таблицу")
		self.pushButton7.clicked.connect(self.fillview)
		self.gridLayout2.addWidget(self.pushButton7, 0, 0, 1, 1)
		#
		self.pushButton8 = QtWidgets.QPushButton(self.gridLayoutWidget2)
		self.pushButton8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.pushButton8.setObjectName("pushButton8")
		self.pushButton8.setText("-----------------")
		self.pushButton8.clicked.connect(self.table_export)
		self.gridLayout2.addWidget(self.pushButton8, 0, 1, 1, 1)
		#
		self.tableWidget = QtWidgets.QTableWidget()
		self.tableWidget.setObjectName("tableView")
		self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		self.gridLayout2.addWidget(self.tableWidget, 1,0,1,8)
		#
		self.retranslateUi(Dialog)
		# if self.is_weekend: 
		# 	response = self.getSessionStart() 
		# 	if not(response):
		# 		self.timeEdit.setEnabled(True)
		# 		self.pushButton4.setEnabled(True)
		# 		self.informationLabel.setText("Не могу определить начало дня. Введите время вручную")
		# 	else: 
		# 		self.timeEdit.setTime(QtCore.QTime(response.hour,response.minute,response.second))
		# 		self.timeEdit.setEnabled(False)
		# 		self.pushButton4.setEnabled(False)

		# self.fillview()
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def init_shutdown_timer(self):
		self._shutdown_timer = QtCore.QTimer(self)
		self._shutdown_timer.setSingleShot(True)
		self._shutdown_timer.timeout.connect(sys.exit)
		self._shutdown_timer.start(self.shutdown_time)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "WorQt {0}".format(self.version)))
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
	def attachment_add(self, parent):
		try:
			attachments = QtWidgets.QFileDialog.getOpenFileUrls()[0]
			for url in attachments:
				attachment = url.url().strip("file:///")
				self.widget_list.addItem(attachment)
		except Exception as ex:
			worQt_cache_lib.log_dump_crash()

	def attachment_remove(self, parent):
		try:
			list_items = self.widget_list.selectedItems()
			if not list_items: return
			for item in list_items:
				index = self.widget_list.row(item)
				self.widget_list.takeItem(index)
		except Exception as ex:
			worQt_cache_lib.log_dump_crash()
	
	def attachment_clear(self, parent):
		try: self.widget_list.clear()
		except Exception as ex:
			worQt_cache_lib.log_dump_crash()

	#base function section
	#refactor with messages' templates
	
	#caching section		
	def fillview(self):#csv or json
		pass
		# try:
		# 	self.tableWidget.setColumnCount(0)
		# 	self.tableWidget.setRowCount(0)
		# 	connection = sqlite3.connect(self.file_log)
		# 	cursor = connection.cursor()
		# 	cursor.execute('''SELECT date_ as "Дата", 
		# 					session_start as "Начало смены",
		# 					session_end as "Конец смены",
		# 					duration as "Всего отработано",
		# 					duration_full as "Полных часов",
		# 					index_ as "Коэффициент"
		# 					FROM session_log''')
		# 	names = list(map(lambda x: x[0], cursor.description))
		# 	[self.tableWidget.insertColumn(i) for i in range(len(names))]
		# 	for row, form in enumerate(cursor):
		# 		self.tableWidget.insertRow(row)
		# 		for column, item in enumerate(form):
		# 			# self.tableWidget.insertColumn(column)
		# 			self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
		# 	self.tableWidget.setHorizontalHeaderLabels(names)
		# 	connection.close()
		# except Exception as ex:
		# 	connection.close()
		# 	worQt_cache_lib.log_dump_crash()

	def table_export(self):
		destination = QtWidgets.QFileDialog.getExistingDirectoryUrl()
		try:
			file_log = self.file_log
			fileOutput = sys.argv[2]
			inputFile = open(fileInput) #open json file
			outputFile = open(fileOutput, 'w') #load csv file
			data = json.load(inputFile) #load json content
			inputFile.close() #close the input file
			output = csv.writer(outputFile) #create a csv.write
			output.writerow(data[0].keys())  # header row
			for row in data:
				output.writerow(row.values()) #values row
		except: raise
		pass

def main():
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	Dialog.show()
	app.exec_()

if __name__ == "__main__":
	main()	
