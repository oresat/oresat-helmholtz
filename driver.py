import sys
import utilities as utils
import cage_controller as cc
import window as w

def main():
    if(len(sys.argv) >= 2):
        # Initialize serial ports
        utils.log(0, "Initializing power supply busses...")
        sensors = []
        for i in utils.PSU_ADDRS:
            sensors.append(cc.PowerSupply(i))
            sensors[-1].toggle_supply(1)

        # Main controlerf_to_c
        utils.log(0, 'Begining main runtime!')
        utils.log(0, 'Temp: ' + str(utils.c_to_f(-10)) + 'F')

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

if __name__ == "__main__":
    main()
