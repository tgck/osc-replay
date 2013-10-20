osc-replay
======================
A simple OSC message recorder and replayer.
Depends on Python, liblo:
 - Python 2.7.3
 - pyliblo-0.9.1
 	(http://das.nasophon.de/pyliblo/)
 - liblo 0.26
	(http://liblo.sourceforge.net/)

How to use
------
1. Run message receiver and record messages as csv file.
	./osc-record.py > anyfile.csv
	
	To Terminate, kill the process with Ctrl+D.

2. Run message sender and send messages with csv file.
	./osc-replay.py anyfile.csv

	The process terminates when it reaches the end of csv.


Paramaters (hard coded in *py)
------	
1. osc-record.py
	- receive-from port number (default 8001)
	- address-patterns which are accepted and logged (ll.41-51, ll.26-39)
	
2. osc-replay.py
	- send-to port number (default 8001)
	- address-patterns which are processed to send (ll.61-74)
		just for now, can handle 'none', 'f', 'ff' osc-messages.(can't handle other types for now.. )


Copyright (C) 2013  kohei taniguchi