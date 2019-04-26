PY=python3 -m py_compile
DRIVER=driver.py
SRC=driver.py cage_controler.py window.py utilities.py
GUIS=window.ui
GSRC=window.py

all: gw i

e: execute
execute:
	python3 $(DRIVER) gui

gw: generate-window
generate-window:
	rm -rf $(GSRC)
	pyuic5 -x $(GUIS) -o $(GSRC)
	uperm -c -y -s -r # Uncomment this only if uperm is installed
	python3 $(GSRC)

i: install
install:
	$(PY) $(SRC)
