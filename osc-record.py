#!/usr/bin/env python
# -*- coding: utf-8 -*-

import liblo
import sys
from datetime import datetime as dt
import datetime

# config for listening
listeningPort = 8001

# now method
def now():
	return dt.today()

# start time
print '%s,INFO:osc-record started.\n' % now()

# create server, listening on given port
try:
    server = liblo.Server(listeningPort)
except liblo.ServerError, err:
    print str(err)
    sys.exit()

# callback functions 
def n_callback(path):
    print '%s,%s' % (now(), path)

def f_callback(path, args):
	print '%s,%s %f' % (now(), path, args[0])

def ff_callback(path, args):
	print '%s,%s %f %f' % (now(), path, args[0], args[1])

def fallback(path, args, types, src):
    print "got unknown message '%s' from '%s'" % (path, src.get_url())
    for a, t in zip(args, types):
        print "argument of type '%s': %s" % (t, a)

# register method taking an int and a float
server.add_method("/pedal", None, n_callback)
server.add_method("/steerRight", None, n_callback)
server.add_method("/steerLeft", None, n_callback)
server.add_method("/steerReset", None, n_callback)
server.add_method("/brake", None, n_callback)

server.add_method("/speed", 'f', f_callback)
server.add_method("/steerAngle", 'f', f_callback)
server.add_method("/direction", 'f', f_callback)
server.add_method("/location", 'ff', ff_callback)

# register a fallback for unhandled messages
server.add_method(None, None, fallback)

# loop and dispatch messages every 100ms
while True:
    server.recv(100)

