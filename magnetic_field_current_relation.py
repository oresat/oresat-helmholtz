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
    return (desiredfield / paramMultiplier(0)) * 2 # multiply by 2 because 2 coils split current

# def axialMagField(current, d): #get amps return microteslas
#     return current * paramMultiplier(d)

def fieldToCurrent(e_field, new_field):
    #compensation
    diffx = new_field[0] - e_field[0]
    diffy = new_field[1] - e_field[1]
    diffz = new_field[2] - e_field[2]

    #negative amps means amps with a 180 degree polarity from normal
    neededcurrentx = getNeededCurrent(diffx)
    neededcurrenty = getNeededCurrent(diffy)
    neededcurrentz = getNeededCurrent(diffz)

    return [neededcurrentx, neededcurrenty, neededcurrentz]
