# -*- coding: utf-8 -*-
import ssl
import urllib
import requests
import datetime as dt

def check_is_weekend(self):
	try:
		_today = self.today.strftime("%Y%m%d")
		scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		chemeo_search_url = "https://isdayoff.ru/{0}".format(_today)
		response = urllib.request.urlopen(chemeo_search_url,
			context = scontext,
			timeout = 5)
		response = int(response.read().decode("utf-8"))
		return True if response in [1] else False
	except:	return True if self.weekday in [5,6] else False

def get_time_morning_work(self):
	self.timeDeltaBefore = self.timeStartOfDay - dt.datetime.now()
	if not(self.isWeekend) and self.timeDeltaBefore < dt.timedelta(hours = 1): 
		return "Отработка меньше 1 часа в будний день"

def get_time_extra_work(self):
	_today = self.today.strftime("%d.%m.%Y")
	if self.isWeekend:
		self.timeStartOfExtra = dt.datetime.strptime("{0} {1}".format(today,self.timeEdit.text()), "%d.%m.%Y %H:%M:%S")
	elif self.weekday in [4]:
		self.timeStartOfExtra = self.convert_time("16:30:00")
	else:
		self.timeStartOfExtra = self.timeEndOfDay
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

def get_time_after_work_started(self):
	if dt.datetime.now() > self.timeEndOfDay:
		self.informationLabel.setText("Уже слишком поздно")
		return None
	else: 
		self.timeDeltaLate = dt.datetime.now() - self.timeStartOfDay
		return True
			
def extract_time_format(self, tdelta):
	try:
		d = {}
		d["days"] = tdelta.days
		d["hrs"], rem = divmod(tdelta.seconds, 3600)
		d["min"], d["sec"] = divmod(rem, 60)
		for key,val in d.items():
			if d[key] < 10 : d[key] = "0{0}".format(val)
		return ("{0}:{1}:{2}".format(d["hrs"],d["min"],d["sec"]))
	except Exception as ex:
		self.writeLog("crash_log",[dt.datetime.now(),"extract_time_format failed with {0}".format(ex)])

def convert_time(self, stringTime):
	out = dt.datetime.strptime("{0} {1}".format(self.today.date(),stringTime), self.FMT)
	return out
