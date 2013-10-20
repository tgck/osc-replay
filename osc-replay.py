#!/usr/bin/env
# -*- coding: utf-8 -*-
#
## osc-replay.py ###############################################################
#	 send osc messages using the log of osc-record.py
################################################################################
import liblo
import sys
import sched
import time
from datetime import datetime as dt
import datetime

defaultLog = '20131114_02_ED.csv'	# log read when executed with no args
replayWaitTime = 1	# wait-time in seconds before it starts to send
targetPort = 8001	# send-to port

#### some utility function #####################################################
#	converts the log format to unix time with microsecond
#   returns float
#      IN: '2013-10-14 16:56:12.358998' 
#	  OUT: 1381737372.3589981
################################################################################
def dateStr2timeFloat(dateStr):
	tmpDt = dt.strptime(dateStr, '%Y-%m-%d %H:%M:%S.%f')
	return (time.mktime(tmpDt.timetuple()) + tmpDt.microsecond/1e6)
	
#### osc-setups ################################################################
#	setups pyloblo
################################################################################
try:
    target = liblo.Address(targetPort)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

#### prepare before main #######################################################
# 	read log file and setup messages to send
################################################################################
if len(sys.argv) == 2:
	log = sys.argv[1]
else:
	log = defaultLog
	

lines = [line.rstrip() for line in open(log)]

firstline = lines[0]
timestamps = [line.split(',')[0] for line in lines[2:]]
messages   = [line.split(',')[1] for line in lines[2:]]

#### main #####################################################################
#	entry messages to the scheduler
#   resist callbacks to the scheduler
#	- startTime:  record-started time in the log and used to calcurate offset times
#	- offsetTime: offset time in seconds from scheduler starts.
################################################################################
startTime = dateStr2timeFloat(firstline.split(',')[0])
offsetTimes = [ dateStr2timeFloat(ts) - startTime for ts in timestamps]

# osc send 
def sendOSCMessage(idx):
	mess = messages[idx].split()
	if len(mess) == 2:
		print "send:" + str(idx) + ":" + str(mess[0]) + ":" + str(mess[1])
		liblo.send(target, mess[0], float(mess[1]))
	elif len(mess) == 1:
		print "send:" + str(idx) + ":" + str(mess[0]) 
		liblo.send(target, mess[0])
	elif len(mess) == 3:
		print "send:" + str(idx) + ":" + str(mess[0]) + ":" + str(mess[1]) + ":" + str(mess[2])
		liblo.send(target, mess[0], float(mess[1]), float(mess[2]))
	else:
		print "not send:" + str(idx)

# scheduler setup
s = sched.scheduler(time.time, time.sleep)
for idx in range(len(messages)):
	s.enter(offsetTimes[idx], 1, sendOSCMessage, (idx,))

# scheduler execute
print "scheduler setup done. osc-replay starts in [" + str(replayWaitTime) + "]second."
time.sleep(replayWaitTime)
print "osc-replay start."

tStart = time.time()
s.run()
tEnd   = time.time()

# infomation for replay
print "\n" + str(len(messages)) + " messages sended."
#print "replay started at...." + str(tStart)
#print "replay end at........" + str(tEnd)
print "replay started at...." + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tStart))
print "replay ended at......" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tEnd))
print "replay duration......" + str(tEnd - tStart) + " seconds."
print "messages per second..%6.2f" % (len(messages) / (tEnd - tStart))
print "osc-replay done."

