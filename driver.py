import os, sys, serial
import utilities as utils
import cage_controller as cc
import window as gui
import command_line as cli
import atexit

def usage(message):
    utils.log(3, message + '\n\tusage: python3 driver.py [cli/gui]')

def main():
    if(len(sys.argv) == 2):
        # Guarantee that the folder for cage data exists
        if(not os.path.isdir(utils.data_file_path())):
            utils.log(1, 'Path: ' + utils.data_file_path() + ' does not exist, creating it now.')
            os.mkdir(utils.data_file_path())

        # Initialize serial ports, toggle power off
        utils.log(0, "Attempting to initialize power supplies...")
        for i in utils.PSU_ADDRS:
            try:
                supply = cc.PowerSupply(i)
                utils.POWER_SUPPLIES.append(supply)
                supply.toggle_supply(0)
            except serial.serialutil.SerialException as e:
                utils.log(3, 'Could not initialize power supply:\n\t' + str(e))
                # exit(1)

        if((not utils.supply_available())): utils.log(3, 'No power supplies were found, and cage initialization cannot continue.\n\tGracefully exiting.')

        # Main controler
        utils.log(0, 'Beginning main runtime!')

        if(sys.argv[1] == 'cli'):
            cli.interface() # Synchronous CLI Environmnet
        elif(sys.argv[1] == 'gui'):
            gui.interface() # Asynchronous GUI Environmnet
        else:
            usage('Invalid option: ' + sys.argv[1] + '!')
            exit(1)
    else:
        usage('Invalid number of options specified for the controller!')
        exit(1)
    
     # Upon exit, power off supply
    try:
        atexit.register(cli.power_off)
    except:
        utils.log(3, 'Could not power down!')
        atexit.register(cli.power_off)
        exit(1)

if __name__ == "__main__":
   try:
        main()
   except KeyboardInterrupt:
        utils.log(3, 'Interrupt Occured')
        atexit.register(cli.power_off)
        exit(1)
