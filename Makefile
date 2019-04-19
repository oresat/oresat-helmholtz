PY=python3 -m py_compile
DRIVER=driver.py
SRC=driver.py cage_controler.py window.py utilities.py
GUIS=window.ui
GSRC=window.py

all: gw i

e: execute
execute:
	python3 $(DRIVER)

gw: generate-window
generate-window:
	rm -rf $(GSRC)
	pyuic5 -x $(GUIS) -o $(GSRC)
	python3 $(GSRC)

i: install
install:
	$(PY) $(SRC)
