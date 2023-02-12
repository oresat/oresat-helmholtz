PY=python3 -m py_compile
DRIVER=driver.py
SRC=driver.py cage_controller.py window.py utilities.py
GUIS=window.ui
GSRC=new_window.py

all: gw i

e: execute
execute:
	python3 $(DRIVER) gui

gw: generate-window
generate-window:
	rm -rf $(GSRC)
	pyuic5 -x $(GUIS) -o $(GSRC)
	uperm -c -y -r # Uncomment this only if uperm is installed

i: install
install:
	$(PY) $(SRC)

s: setup
setup:
	python3 setup.py
