import serial
import smbus
import utilities as utils
import cage_controler as cc
import window as w

def main():
    utils.log(0, "Initialize sensor serial ports...")

    # Dummy serial adresses of the sensors
    ser1 = '0e'
    ser2 = '0f'
    ser3 = '10'

    # Initialize serial ports
    # cc.initialize_all_bus()
    # cc.toggle_all_power_supply(0)

    # Main controlerf_to_c
    utils.log(0, 'Begining main runtime!')
    utils.log(0, 'Temp: ' + str(cc.c_to_f(32)) + 'F')

    # cc.interface() # Synchronous CLI Environmnet
    w.interface() # Asynchronous GUI Environmnet

    # initial magnetic field from environment
    x0, y0, z0 = magnotometer()

if __name__ == "__main__":
    main()
