from PyQt5 import QtCore, QtWidgets
import os
import worQt_timer
import json

STATS_KEYS = ['Date', 'Start', 'Finish', 'Duration']

def fill_view_statistic(self, file_sessions = 'sessions.json'):#csv or json
	with open(file_sessions, 'r') as f:
		data = json.load(f)
		# cursor.execute('''SELECT date_ as "Дата", 
		# 				session_start as "Начало смены",
		# 				session_end as "Конец смены",
		# 				duration as "Всего отработано",
		# 				duration_full as "Полных часов",
		# 				index_ as "Коэффициент"
		# 				FROM session_log''')
		# names = list(map(lambda x: x[0], cursor.description))
		# [self.tableWidget.insertColumn(i) for i in range(len(names))]
	sessions = data['sessions']
	for i , session in enumerate(sessions):
		self.tableWidget.insertRow(self.tableWidget.rowCount())
		for j, k in enumerate(STATS_KEYS):
			it = QtWidgets.QTableWidgetItem()
			it.setData(QtCore.Qt.DisplayRole, str(session[k]))
			self.tableWidget.setItem(i,j,it)
	self.tableWidget.show()
	
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
	except: pass #unstable sorry 
	pass

def set_file_error(self, file_error):
	self.file_error = file_error

def set_file_log(self, file_log):
	self.file_log = file_log 

def set_check_in(self):
	session = {
		'Date': None,
		'Start': None,
		'Finish': None,
		'Duration': None,
		}
	i = self.tableWidget.rowCount()
	self.tableWidget.insertRow(i)
	for j, (k,v) in enumerate(session.items()):
		it = QtWidgets.QTableWidgetItem()
		it.setData(QtCore.Qt.DisplayRole, str(session[k]))
		self.tableWidget.setItem(i,j,it)
	self.tableWidget.show()

def create_file_log():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	with open('{}_{}.log','a') as out_log:
		out_log.close()
	return file_log

def create_file_error():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date, login)
	with open(file_error,'a') as out_error:
		out_error.close()
	return file_error

def get_file_log():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	return file_log if os.path.exists(file_log) else create_file_log()

def get_file_error():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date,login)
	return file_log if os.path.exists(file_error) else create_file_error()

def log_dump_crash():
	pass

def log_write_action():
	pass