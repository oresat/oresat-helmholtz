#!/usr/bin/env python
from math import pi

mu = 4 * pi * 10**(-7) # magnetic field constant Tm/A
halfofsidelength = 0.3302 # meters, physical parameter, check this
distbetweensides = 0.49 #0.4572 # meters, physical parameter, check this
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
    return (desiredfield / paramMultiplier(0)) * 2

def axialMagField(current, d): #get amps return microteslas
    #need to get actual current for axis from program or PSU somehow
    return current * paramMultiplier(d)

# given the environmental and desired fields, what currents must we pull?
def automatic(env_field, ideal_field):
    #compensation
    diff = [ideal_field[i] - env_field[i] for i in range(3)]

    #negative amps just means amps with a 180 degree polarity
    needed_current = [getNeededCurrent(diff[i]) for i in range(3)]
    return needed_current
