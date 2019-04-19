import sys
import utilities as utils
import cage_controler as cc
import window as w

def main():
    # Initialize serial ports
    # utils.log(0, "Initialize sensor serial ports...")
    # cc.initialize_all_bus()
    # cc.toggle_all_power_supply(0)

    # Main controlerf_to_c
    utils.log(0, 'Begining main runtime!')
    utils.log(0, 'Temp: ' + str(cc.c_to_f(24)) + 'F')

    if(len(sys.argv) >= 2):
        if(sys.argv[1] == 'cli'):
            cc.interface() # Synchronous CLI Environmnet
        elif(sys.argv[1] == 'gui'):
            w.interface() # Asynchronous GUI Environmnet
        else:
            utils.log(3, 'Invalid option: ' + sys.argv[1] + '!\n\tusage: python3 driver.py [cli/gui]')
            exit(1)
    else:
        utils.log(3, 'No option specified for controller!\n\tusage: python3 driver.py [cli/gui]')
        exit(1)

    # initial magnetic field from environment
    # x0, y0, z0 = cc.magnotometer()

if __name__ == "__main__":
    main()
