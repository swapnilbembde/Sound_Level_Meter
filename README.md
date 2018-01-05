# Sound Level Meter
## Getting Started
*	Installing numpy-
	* sudo apt-get install python-numpy
*	Installing scipy-
	* sudo apt-get install python-scipy
*	Installing pyAudio-
	* sudo apt-get install python-pyaudio
*	Installing matplotlib-
	* sudo apt-get install python-matplotlib
*	Installing mySQLdb-
  *	sudo apt-get install python-mysqldb
* For gui(realTime.py) pyqt4-
  * sudo apt-get install python-qt4
  * sudo apt-get install python-qt4-qwt5  
  
## Process
* Python scripts for GUI compilation of input sound signal.
* For now we can record, buffer and proccess for given seconds.
*	Recorder.py sends the data to the MySQL server.
*	We are sending frequencies and their respective amplitudes (dB) to the database. 
*	We are also sending resulting amplitude (dB) to another database. 
*	I have calibrated loudness level wrt to SOUND METER APP.
