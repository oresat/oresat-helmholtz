#!/usr/bin/env python
from math import pi

mu = 4 * pi * 10**(-7) # magnetic field constant Tm/A
halfofsidelength = 0.3302 # meters, physical parameter, check this
distbetweensides = 0.34 #0.4572 # meters, physical parameter, check this
wireturns = 56 #58 # physical parameter, doc says 56, not sure what actual

constmultiplier = wireturns * mu / pi # pulling constants into a single variable

def distFromOriginSquared(d):
    return (distbetweensides/2 + d)**2 # meter^2

def dropOffFromSide(d):
    A = halfofsidelength ** 2
    offset = distFromOriginSquared(d)
    return (2 * A) / ((A + offset) * (2 * A + offset)**0.5) # meter^-1

def paramMultiplier(d): # parameter is distance from origin, we usually only care about d=0
    return (dropOffFromSide(d) + dropOffFromSide(-d)) * constmultiplier * 10**(6) # microT/A

def getNeededCurrent(desiredfield): #get microteslas return amps
    return desiredfield / paramMultiplier(0)

def axialMagField(current, d): #get amps return microteslas
    #need to get actual current for axis from program or PSU somehow
    return current * paramMultiplier(d)

def fieldToCurrent(efx, efy, efz):
    desiredfield = float(raw_input("What is the ideal strength of the uniform magnetic field? (microTeslas)\n"))
    #print "What is the initial strength of Earth's magnetic field? (microTeslas) (x, y, z)"
    # in the future these initial values should come from magnotometer
    #efx = float(raw_input("x: "))
    #efy = float(raw_input("y: "))
    #efz = float(raw_input("z: "))
        
    #compensation
    diffx = desiredfield - efx
    diffy = desiredfield - efy
    diffz = desiredfield - efz
        
    #negative amps means amps with a 180 degree polarity from normal
    neededcurrentx = getNeededCurrent(diffx)
    neededcurrenty = getNeededCurrent(diffy)
    neededcurrentz = getNeededCurrent(diffz)
        
    return neededcurrentx, neededcurrenty, neededcurrentz
        
    # psu1=z, psu2=y, psu3=x
    #print "Required current from PSU 1: " + str(neededcurrentz) + " amps.\n"
    #print "Required current from PSU 2: " + str(neededcurrenty) + " amps.\n"
    #print "Required current from PSU 3: " + str(neededcurrentx) + " amps.\n"
        
    #this block was just for testing equation in the other direction
    #wantcurrent = raw_input("What is the current from the power supply? (amps)\n")
    #resultfield = axialMagField(float(wantcurrent), 0)
    #print "Resultant magnetic field: " + str(resultfield) + " microteslas.\n"
