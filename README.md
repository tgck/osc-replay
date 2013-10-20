osc-replay
======================
A simple OSC message recorder and replayer.
Depends on Python, liblo:
 - Python 2.7.3
 - pyliblo-0.9.1
 	(http://das.nasophon.de/pyliblo/)
 - liblo 0.26
	(http://liblo.sourceforge.net/)

OSCメッセージを受信してログ出力するスクリプトと、そのログを元に記録した時系列でメッセージを再生するスクリプトのセットです。Mac OS X 10.6.8および上記のソフトウェアバージョンで動作確認をしています。
ローカルマシン上のプロセス間通信を対象としており、ホスト間通信はサポートしていません。

How to use
------
1. Run message receiver and record messages as csv file.
	./osc-record.py > anyfile.csv
	
	To Terminate, kill the process with Ctrl+D.

2. Run message sender and send messages with csv file.
	./osc-replay.py anyfile.csv

	The process terminates when it reaches the end of csv.

コンソールから、Pythonスクリプトを起動・停止する要領で実行してください。


Paramaters (hard coded in *py)
------	
1. osc-record.py
	- receive-at port number (default 8001)
	- address-patterns which are accepted and logged (ll.41-51, ll.26-39)
	
2. osc-replay.py
	- send-to port number (default 8001)
	- address-patterns which are processed to send (ll.61-74)
		just for now, can handle 'none', 'f', 'ff' osc-messages.(can't handle other types for now.. )

現状諸々、ハードコーディングとなっています。送受信したいアドレスパターンとそのハンドラを、osc-replay.pyに記述する必要があります。ゆくゆくは設定ファイルに外出しするか、どんなメッセージでも捌けるように改修したいところ。

Copyright (C) 2013  kohei taniguchi