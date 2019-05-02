import cage_controller
import utilities as utils
import magnetic_field_current_relation as mfcr

COMMAND_MAP = {
    0: 'Exit program',
    1: 'Set Voltage [Volts]',
    2: 'Set Current [Amps]',
    3: 'Turn on power supply',
    4: 'Turn off power supply',
    5: 'Get temperature data',
    6: 'Get magnetometer data',
    7: 'Set uniform magnetic field',
    8: 'Print data',
    9: 'Plot graph'
}

# Displays the menu
def display_menu():
    utils.log(0, 'Helmholtz Cage Controller:')
    for num, description in COMMAND_MAP.items():
        print('\t' + str(num) + ': ' + description)

# Prints data?
def print_data():
    time, mag = cage_controller.poll_data(20, 1)
    i = 0
    for t in time:
        print(time[i], mag[i])
        i += 1

#
# Legacy cage controller interface
#   (Can be used by specifying `cli` in the driver)
#
def menu(control):
    if control == 0:
        utils.log(0, 'Exiting...')
    elif control == 1:
        if(utils.supply_available()):
            voltage = float(input('New voltage [Volts]: '))
            supply_index= int(input('Power Supply [1-3]: '))
            utils.POWER_SUPPLIES[supply_index - 1].set_voltage(voltage)
            utils.log(0, 'Voltage set to ' + str(voltage) + ' Volts on Supply #' + str(supply_index))
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 2:
        if(utils.supply_available()):
            current = float(input('New current [Amps]: '))
            supply_index= int(input('Power Supply [1-3]: '))
            utils.POWER_SUPPLIES[supply_index].set_current(current)
            utils.log(0, 'Amperage set to ' + str(current) + ' Amps on Supply #' + str(supply_index))
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 3:
        if(utils.supply_available()):
            utils.log(0, 'Powering On...')
            for i in utils.POWER_SUPPLIES:
                i.toggle_supply(1)
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 4:
        if(utils.supply_available()):
            utils.log(0, 'Powering Off...')
            for i in utils.POWER_SUPPLIES:
                i.toggle_supply(0)
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 5:
        utils.log(0, 'Checking temperatures...')
        cage_temp_1, cage_temp_2 = cage_controller.temperature()
        utils.log(0, 'Sensor 1:\t' + str(cage_temp_1) + '°C\t' + str(utils.c_to_f(cage_temp_1) + '°F'))
        utils.log(0, 'Sensor 2:\t' + str(cage_temp_2) + '°C\t' + str(utils.c_to_f(cage_temp_2) + '°F'))
    elif control == 6:
        utils.log(0, 'Checking magnotometer, units in microTeslas')
        xMag, yMag, zMag = cage_controller.magnetometer()
        utils.log(0, 'Manetic field Components:\n\tX: ' + str(xMag) + '\n\tY: ' + str(yMag) + '\n\tZ: ' + str(zMag))
    elif control == 7:
        if(utils.supply_available()):
            # TODO: Add back the current get to power supply
            currents = mfcr.fieldToCurrent(x0, y0, z0)

            utils.log(0, 'Power Supply Current Updates:')
            for i in range(0, len(currents)):
                utils.POWER_SUPPLIES.set_current(currents[i])
                print('\tSupply #' + str(i) + ': ' + str(currents[i]))
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 8:
        print_data()
    elif control == 9:
        plot_graph()

# function for interacting with the user
def interface():
    control = 1
    while (control != 0):
        display_menu()
        try:
            control = int(input('Selection?[0-9]: '))
            menu(control)
        except ValueError:
            utils.log(3, 'There was a problem with your input: ' + str(control))
