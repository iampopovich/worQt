# -*- coding: utf-8 -*-
import ssl
import urllib
import requests
import urllib.request
import datetime as dt
import time as tt


def get_work_time_start():
    pass


def get_today():
    return dt.datetime.today()


def get_now():
    return dt.datetime.now()


def get_delta(time_start, time_finish):
    return time_finish - time_start


def check_is_extrawork(time_start, time_end):
    if check_is_weekend:
        return True
    return not(time_start < dt.datetime.now().strftime("%H:%M:%S") < time_end)


def get_time_extra_work(time_start):
    time_finish = dt.datetime.now()
    time_delta = get_delta(time_start, time_finish)
    if time_delta > dt.timedelta(seconds=1):
        return time_delta


def check_is_late(time_start, time_end):
    return start < dt.datetime.now() < end


def check_is_weekend(day=dt.datetime.today()):
    try:
        today = day.strftime("%Y%m%d")
        response = urllib.request.urlopen(
            "https://isdayoff.ru/{0}".format(today),
            context=ssl.SSLContext(ssl.PROTOCOL_SSLv23),
            timeout=5)
        response = int(response.read().decode("utf-8"))
        return response in [1]
    except:
        return day.weekday() in [5, 6]


def extract_time_format(self, tdelta):
    try:
        d = {}
        d["days"] = tdelta.days
        d["hrs"], rem = divmod(tdelta.seconds, 3600)
        d["min"], d["sec"] = divmod(rem, 60)
        for key, val in d.items():
            if d[key] < 10:
                d[key] = "0{0}".format(val)
        return ("{0}:{1}:{2}".format(d["hrs"], d["min"], d["sec"]))
    except Exception as ex:
        raise
