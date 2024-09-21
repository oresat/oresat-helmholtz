# oresat-helmholtz

![alt text](https://user-images.githubusercontent.com/33878769/50576984-cde2d900-0dd2-11e9-8117-1c2e21f85c7d.png)

## Magnetic Environment Simulator for CubeSats

![helmholtz_cage](https://github.com/user-attachments/assets/35ffd680-2c4b-4acd-8774-dfff9f08daa9)




Oresat Helmholtz is an open-source and DIY Helmholtz cage controller for facilitating magnetic
field simulations. Developed for the Oresat project, this repo hosts a software designed to 
facilite the operation of the Helmholtz cage and execute dynamics testing for B-Field related 
CubeSat attitude controls.

## To Set Up Run:
`python -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`

## To run again later
`source .venv/bin/activate`
`python3 main.py -l '1-1.2.2' -s '1-1.2.3'`

## Sphinx Documenation
A convienient way to view the documentation for this project is provided through the Sphinx
documentation framework. To compile and view the docs you may use the prodecure below,
1. Enter the docs location and build the HTML file.
```
$ cd docs
$ make html
```
2. Open the index page using your browser of choice. Either navigate to `docs/_build/html/index.html` graphically and open the file, or via the command line. eg. with firefox
```
<docs location>$ firefox _build/html/index.html
```

## Detecting ports for the buck converters and arduino on linux
1. ls -la /sys/bus/usb/devices (to view all ports)
2. Crosscheck what comes up before and after plugging in the cagebox
3. Ports for the buck converters will look something like this: x-x.x.1', 'x-x.x.2', and 'x-x.x.3'
4. In helmholtzcage/ZXY6005s.py file, look for the location variables, replace with the port locations that were discovered above for the converters
5. Find location of the arduino and magnetometer - list ports again. It will look like x-x.x.x and will most likely be one less digit than the power converters.
6. If the cage box is connected to the USB port on the back of the top row on the raspberry pi, the below line of code should work.
7. Use the command `python3 main.py -l '1-1.2.2' -s '1-1.2.3'` where -l is the port for the arduino, and -s is the port for the magnetometer sensor.
