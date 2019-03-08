#!/usr/bin/env python

pi = 3.14159 # approximation of a mysterious number
mu = 4 * pi * 10**(-7) # magnetic field constant Tm/A
halfofsidelength = 0.3302 # meters
distbetweensides = 0.4572 # meters
wireturns = 58
constmultiplier = wireturns * mu / pi

def distFromOriginSquared(d):
	return (distbetweensides/2 + d)**2 # meter^2

def dropOffFromSide(d):
	A = halfofsidelength ** 2
	offset = distFromOriginSquared(d)
	return (2 * A) / ((A + offset) * (2 * A + offset)**0.5) # meter^-1

def paramMultiplier(d):
	return dropOffFromSide(d) + dropOffFromSide(-d) # meters^(-1)

def axialMagField(current, d): #get amps return microteslas
	#get actual current for axis from PSU somehow
	return current * constmultiplier * paramMultiplier(d) *10**(6) # Teslas

# would be cool to have a function of coords get all three mag fields
# as the magnitude of a single composite

def getNeededCurrent(desiredfield): #get microteslas return amps
	return (desiredfield*10**(-6)) / (paramMultiplier(0) * constmultiplier)

def interface():
	while True:
		desiredfield = raw_input("What is the ideal strength of a magnetic field? (microTeslas)\n")
		neededcurrent = getNeededCurrent(float(desiredfield))
		print "Required current from PSU: " + str(neededcurrent) + " amps.\n"
		wantcurrent = raw_input("What is the current from the power supply? (amps)\n")
		resultfield = axialMagField(float(wantcurrent), 0)
		print "Resultant magnetic field: " + str(resultfield) + " microteslas.\n"

interface()
