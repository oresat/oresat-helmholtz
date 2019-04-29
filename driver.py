import os, sys, serial
import utilities as utils
import cage_controller as cc
import window as w

def usage(message):
    utils.log(3, message + '\n\tusage: python3 driver.py [cli/gui]')

def main():
    if(len(sys.argv) == 2):
        # Guarentee that the folder for cage data exists
        if(not os.path.isdir(utils.data_file_path())):
            utils.log(1, 'Path: ' + utils.data_file_path() + ' does not exist, creating it now.')
            os.mkdir(utils.data_file_path())

        # Initialize serial ports
        utils.log(0, "Attemting to initialize power supplies...")
        try:
            for i in utils.PSU_ADDRS:
                supply = cc.PowerSupply(i)
                utils.POWER_SUPPLIES.append(supply)
                supply.toggle_supply(1)
        except serial.serialutil.SerialException as e:
            utils.log(3, 'Could not initialize power supply:\n\t' + str(e))
            # exit(1)

        # Main controlerf_to_c
        utils.log(0, 'Begining main runtime!')

        if(sys.argv[1] == 'cli'):
            cc.interface() # Synchronous CLI Environmnet
        elif(sys.argv[1] == 'gui'):
            w.interface() # Asynchronous GUI Environmnet
        else:
            usage('Invalid option: ' + sys.argv[1] + '!')
            exit(1)
    else:
        usage('Invalid number of options specified for the controller!')
        exit(1)

if __name__ == "__main__":
    main()
