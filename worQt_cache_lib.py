import os
import math
import datetime

def set_file_error(self):
	date = datetime.now().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date, login)
	if os.path.exists(file_error):
		self.file_error = file_error
	else:
		file = create_file_error()
		self.file_error = file

def set_file_log(self):
	date = datetime.now().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	if os.path.exists(file_log):
		self.file_log = file_log 
	else:
		file = create_file_log()
		self.file_error = file

def create_file_log(self):
	date = datetime.now().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	with open('{}_{}.log','a') as out_log:
		out_log.close()
	return file_log

def create_file_error(self):
	date = datetime.now().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date, login)
	with open(file_error,'a') as out_error:
		out_error.close()
	return file_error

def get_file_log(self):
	pass

def get_file_error(self):
	pass

def create_file_config(self):
	pass

def set_file_config(self, config):
	pass

def get_file_config(self):
	pass

def log_dump_crash(self):
	pass

def log_write_action(self):
	pass

# def getLogFile(self):
# 	try:
# 		dirName = "{0}\\worqt_cache".format(os.environ["APPDATA"])
# 		fileName = "{0}\\worqt_cache\\worqt_log.sqlite".format(os.environ["APPDATA"])
# 		if os.path.isdir(dirName): pass
# 		else: os.mkdir(dirName)
# 		connection = sqlite3.connect(fileName)
# 		cursor = connection.cursor()
# 		try: 
# 			query = """select * from session_log limit 1"""
# 			cursor.execute(query)
# 		except:
# 			if createLogFile(fileName, connection, cursor): pass #а вот тут надо вдолбить обработчик
# 			else: pass
# 		connection.close()
# 		return fileName 
# 	except Exception as ex:
# 		connection.close()
# 		self.writeLog("crash_log",[dt.datetime.now(),"getLog failed with {0}".format(ex)])

# def createLogFile(fname, conn, curs):
# 	try:
# 		queries = [
# 			"""create table session_log
# 				(date_ text, 
# 				session_start text,
# 				session_end text,
# 				duration text,
# 				duration_full text,
# 				index_ text
# 				)""",
# 			"""create table crash_log
# 			(date_ text, datetime_ text, log_string varchar)"""
# 			]
# 		for q in queries:
# 			curs.execute(q)
# 			conn.commit()
# 		return True
# 	except:	return False

# def writeLog(self, table, values):
# 	try:
# 		query = ""
# 		connection = sqlite3.connect(self.logFile)
# 		cursor = connection.cursor() 
# 		currentDate = dt.date.today().isoformat()
# 		values.insert(0, currentDate)
# 		if table == "session_log":
# 			query = "select * from session_log where date_ like \"{0}\"".format(currentDate)
# 			if cursor.execute(query).fetchone() is None:
# 				st_values = ",".join(["\"{0}\"".format(v) for v in values])
# 				query = "insert into {0} values ({1})".format(table,st_values)	
# 			else:				
# 				query = """update session_log 
# 				set session_end = \"{0}\",
# 					duration = \"{1}\",
# 					duration_full = \"{2}\",
# 					index_ = \"{3}\"
# 				where date_ like \"{4}\" and
# 				session_end is \"None\"""".format(self.timeFinishOfExtra,
# 												worQt_time_lib.extractTimeFormat(self,self.timeDelta),
# 												math.floor(self.timeDelta.seconds / 3600),
# 												[2 if self.isWeekend else 1.5],
# 												currentDate)
# 				cursor.execute(query)
# 				connection.commit()
# 				connection.close()
# 				return None
# 		if table == "crash_log":
# 			st_values = ",".join(["\"{0}\"".format(v) for v in values])
# 			query = "insert into {0} values ({1})".format(table,st_values)
# 		cursor.execute(query)
# 		connection.commit()
# 		connection.close()
# 	except Exception as ex:
# 		connection.close()
# 		#self.theUI.NXMessageBox.Show(self.moduleName, self.MSG_Error, "writeCacheFile failed with {0}".format(%ex) )

# def getSessionStart(self):
# 	try:
# 		connection = sqlite3.connect(self.logFile)
# 		#connection.row_factory = sqlite3.Row
# 		cursor = connection.cursor()
# 		currentDate = dt.date.today().isoformat()
# 		query = "select session_start from session_log where date_ like \"{0}\"".format(currentDate)
# 		timeStart = cursor.execute(query).fetchone()[0]
# 		sessionStart = dt.datetime.strptime(timeStart, "%Y-%m-%d %H:%M:%S.%f")
# 		connection.close()
# 		return sessionStart
# 	except Exception as ex:
# 		connection.close()
# 		return False
