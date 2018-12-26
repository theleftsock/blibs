__author__ = 'biagio'
import datetime
import time
from time import gmtime, strftime

def get_ts(mode = 0):
    date_list = datetime.datetime.now().time()
    # print "date_list: ", date_list
    if (mode == 0): # 2015-06-02 09:52
        ts = strftime("%Y-%m-%d %H:%M")
    if (mode == 4): # 2015-06-02 09:52:30
        ts = strftime("%Y-%m-%d %H:%M:%S")
    if (mode == 1): # 2015-06-02 13:52:41
        ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if (mode == 2): # 201506020952
        ts = strftime("%Y%m%d%H%M")
    if (mode == 3): # 20150602095306
        ts = strftime("%Y%m%d%H%M%S")
    #print "ts: ", ts
    return ts

def seconds_to_time(secs):  # takes number of seconds and returns a tuple up to days of time
    if secs > 60:
        mins = int(secs) / 60
        secs = int(secs) % 60
    else:
        mins = 0
    if mins > 60:
        hours = int(mins) / 60
        mins = int(mins) % 60
    else:
        hours = 0
    if hours > 24:
        days = int(hours) / 24
        hours = int(hours) % 24
    else:
        days = 0
    return(secs, mins, hours, days)