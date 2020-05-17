# -*- coding: utf-8 -*-
import ssl
import urllib
import requests
import urllib.request
import datetime as dt

def get_work_time_start():
	pass

def get_today():
	return dt.datetime.today()

def is_time_before_work_start():
	start = instant.time_start_of_day
	return  dt.datetime.now() < start

def check_is_late(instant):
	start = instant.time_start_of_day
	end = instant.time_end_of_day
	return start < dt.datetime.now() < end

def check_is_time_after_work_end(instant):
	end = instant.time_end_of_day
	return dt.datetime.now() > end
	
def check_is_weekend(day):
	try:
		today = day.strftime("%Y%m%d")
		response = urllib.request.urlopen(
			"https://isdayoff.ru/{0}".format(today),
			context = ssl.SSLContext(ssl.PROTOCOL_SSLv23),
			timeout = 5)
		response = int(response.read().decode("utf-8"))
		return True if response in [1] else False
	except:
		return True if day.weekday() in [5,6] else False

def get_time_morning_work(self):
	self.timeDeltaBefore = self.timeStartOfDay - dt.datetime.now()
	if not(self.is_weekend) and self.timeDeltaBefore < dt.timedelta(hours = 1): 
		return "Отработка меньше 1 часа в будний день"

def get_time_extra_work(self):
	_today = self.today.strftime("%d.%m.%Y")
	if self.is_weekend:
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
		if self.is_weekend and self.timeDelta < dt.timedelta(hours = 4):
			self.workForFree = "Отработка меньше 4 часов в выходной"			
			return True
		if not(self.is_weekend) and self.timeDelta < dt.timedelta(hours = 1): 
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
