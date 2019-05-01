PY=python3
ZIP=abacmonitor.zip
MAIN=main
DIR=$(PWD)
.SUFFIXES: .py
FILES = \
	abacmonitor.py
All: 
	echo " $(PY) $(DIR)/$(FILES) " \"'$$1'\" > abacmonitor
	chmod 777 abacmonitor
