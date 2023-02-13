import cage_controller
import utilities as utils
import magnetic_field_current_relation as mfcr
import time

global x0, y0, z0 #initial magnetic field, sorry about the globals
#x0, y0, z0 = cage_controller.magnotometer()

COMMAND_MAP = {
    0: 'Exit program',
    1: 'Set Voltage [Volts]',
    2: 'Set Current [Amps]',
    3: 'Turn on power supply',
    4: 'Turn off power supply',
    5: 'Get temperature data',
    6: 'Get magnetometer data',
    7: 'Set uniform magnetic field',
    8: 'Plot graph'
}

# Turn power off by request or exit
def power_off():
    if(utils.supply_available()):
        utils.log(0, 'Powering Off...')
        for i in utils.POWER_SUPPLIES:
            i.toggle_supply(0)
    else:
        utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')

# Displays the menu
def display_menu():
    utils.log(0, 'Helmholtz Cage Controller:')
    for num, description in COMMAND_MAP.items():
        print('\t' + str(num) + ': ' + description)

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
            supply_index = int(input('Power Supply [1-3] or [4] for "all": '))
            if supply_index in range(1,4):
                utils.POWER_SUPPLIES[supply_index - 1].set_voltage(voltage)
            elif supply_index == 4:
                for supply in range(supply_index):
                    utils.POWER_SUPPLIES[supply - 1].set_voltage(voltage)
            utils.log(0, 'Voltage set to ' + str(voltage) + ' Volts on Supply #' + str(supply_index))
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 2:
        if(utils.supply_available()):
            current = float(input('New current [Amps]: '))
            supply_index = int(input('Power Supply [1-3] of [4] for "all": '))
            if supply_index in range(1,4):
                utils.POWER_SUPPLIES[supply_index - 1].set_current(current)
            elif supply_index == 4:
                for supply in range(supply_index):
                    utils.POWER_SUPPLIES[supply - 1].set_current(current)
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
        power_off()
    elif control == 5:
        utils.log(0, 'Checking temperatures...')
        cage_temp_1, cage_temp_2 = cage_controller.temperature()
        utils.log(0, 'Sensor 1:\t' + str(cage_temp_1) + '°C\t' + str(utils.c_to_f(cage_temp_1) + '°F'))
        utils.log(0, 'Sensor 2:\t' + str(cage_temp_2) + '°C\t' + str(utils.c_to_f(cage_temp_2) + '°F'))
    elif control == 6:
        utils.log(0, 'Checking magnetometer, units in microTeslas')
        xMag, yMag, zMag = cage_controller.magnetometer()
        utils.log(0, 'Magnetic field Components:\n\tX: ' + str(xMag) + '\n\tY: ' + str(yMag) + '\n\tZ: ' + str(zMag))
    elif control == 7:
        if(utils.supply_available()):
            x0, y0, z0 = cage_controller.magnetometer()
            desired_x = float(input("What is the ideal strength of the x component? (microTeslas)\n"))
            desired_y = float(input("What is the ideal strength of the y component? (microTeslas)\n"))
            desired_z = float(input("What is the ideal strength of the z component? (microTeslas)\n"))
            currents = mfcr.automatic([x0, y0, z0], [desired_x, desired_y, desired_z])

            utils.log(0, 'Power Supply Current Updates:')
            for i, PS in enumerate(utils.POWER_SUPPLIES):
                PS.set_current(currents[i])
                print('\tSupply #' + str(i+1) + ': ' + str(currents[i]))
        else:
            utils.log(3, 'There are currently no power supplies available!\n\tThis option will not be available until one or more are connected and the controller is rebooted.')
    elif control == 8:
        utils.log(3, 'Function deprecated')
        #plot_graph()


# function for interacting with the user
def interface():
    control = 1
    while (control != 0):
        display_menu()
        try:
            control = int(input('Selection?[0-8]: '))
            menu(control)
        except ValueError:
            utils.log(3, 'There was a problem with your input: ' + str(control))


def poll_data(duration = 10.0, dt = 1.0):
    time_step = [0.0]
    # temp_array = [temperature()]
    mag_array = [cage_controller.magnetometer()]
    while time_step[-1] < duration:
        time.sleep(dt)
        time_step.append(time_step[-1] + dt)
        # temp_array.append(temperature())
        mag_array.append(cage_controller.magnetometer())
    return time_step, mag_array #temp_array, mag_array