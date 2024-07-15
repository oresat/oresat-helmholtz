# oresat-helmholtz

![alt text](https://user-images.githubusercontent.com/33878769/50576984-cde2d900-0dd2-11e9-8117-1c2e21f85c7d.png)

## Magnetic Environment Simulator for CubeSats

SOP can be found [here](http://psu-epl.github.io/doc/equip/testing/ETL/) at the Electronics Prototyping Lab website

![alt text](https://user-images.githubusercontent.com/33878769/48651456-dfe9f300-e9af-11e8-9a90-02227cccc314.jpg)

MCECS BETA Project 2018

## To Set Up Run:
`python -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`

## To run again later
`source .venv/bin/activate`
`python main.py`

## Detecting ports for the buck converters and arduino on linux
1. ls -la /sys/bus/usb/devices (to view all ports)
2. Crosscheck what comes up before and after plugging in the cagebox
3. Ports for the buck converters will look something like this: x-x.x.1', 'x-x.x.2', and 'x-x.x.3'
4. In helmholtzcage/ZXY6005s.py file, look for the location variables, replace with the port locations that were discovered above for the converters
5. Find location of the arduino - list ports again. It will look like x-x.x
6. If running from a computer and not the Rasp Pi, use the command `python main.py -l x-x.x` wherex-x.x is the port of the arduino