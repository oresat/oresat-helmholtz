import sys
from time import sleep

from uart import blocking_get_mag_field
from ulab import numpy as np


def print_curr_mag_csv(motor_assemblies, uart):
    """
    CLI callback to print a csv of currents and associated magnetic field measurements
    """
    sys.stdout.write("\nGenerating CSV of current and magfield measurements...\n")
    measurements = {
        "x": {"curr": [], "magfield": []},
        "y": {"curr": [], "magfield": []},
        "z": {"curr": [], "magfield": []},
    }

    stepsize = 10

    for plane, assembly in motor_assemblies.items():
        for i in range(0, 101, stepsize):
            assembly.motor.reverse(i)
            curr = assembly.ina226.current
            sleep(0.5)
            adjusted_field = blocking_get_mag_field(uart)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])
            assembly.motor.stop()
            sleep(0.5)

        for i in range(0, 101, stepsize):
            assembly.motor.forward(i)
            curr = assembly.ina226.current
            sleep(0.5)
            adjusted_field = blocking_get_mag_field(uart)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])
            assembly.motor.stop()
            sleep(0.5)

    sys.stdout.write("X,Current,Magfield,Y,Current,Magfield,Z,Current,Magfield\n")

    try:
        for i in range(len(measurements["x"]["curr"])):
            sys.stdout.write(
                f'\
            ,{measurements["x"]["curr"][i]},{measurements["x"]["magfield"][i]},\
            ,{measurements["y"]["curr"][i]},{measurements["y"]["magfield"][i]},\
            ,{measurements["z"]["curr"][i]},{measurements["z"]["magfield"][i]}\n'
            )
    except IndexError as e:
        sys.stdout.write(f"Error: {e}\n")

    x_currs = np.array(measurements["x"]["curr"])
    y_currs = np.array(measurements["y"]["curr"])
    z_currs = np.array(measurements["z"]["curr"])

    x_fields = np.array(measurements["x"]["magfield"])
    y_fields = np.array(measurements["y"]["magfield"])
    z_fields = np.array(measurements["z"]["magfield"])

    x_line = np.polyfit(x_currs, x_fields, 1)
    y_line = np.polyfit(y_currs, y_fields, 1)
    z_line = np.polyfit(z_currs, z_fields, 1)

    sys.stdout.write(f'calculated slope,,{x_line[0]},,{y_line[0]},,{z_line[0]}\n')
    sys.stdout.write(f'calculated intercept,,{x_line[1]},,{y_line[1]},,{z_line[1]}\n')


def print_fields_csv(uart, time):
    """
    CLI callback to print a csv of magnetic field measurements from the bridge over time
    """
    sys.stdout.write("\ntime (s),x (mG),y (mG),z (mG)\n")
    for i in range(time):
        fields = blocking_get_mag_field(uart)
        x = fields["x"]
        y = fields["y"]
        z = fields["z"]
        sys.stdout.write(f'{i},{x},{y},{z}\n')
        sleep(1)


def print_dci_csv(motor_assemblies, plane):
    """
    CLI callback to print a csv of motor driver pwm duty cycles and the associated output current
    """
    assembly = motor_assemblies[plane]
    csv = "Duty Cycle,Current,\n"
    for i in range(100, 0, -1):
        csv += f"-{i},"
        assembly.motor.reverse(i)
        csv += str(assembly.ina226.current) + ","
        assembly.motor.stop()
        sys.stdout.write(f"\n{csv}")
        csv = ""
    for i in range(101):
        csv += f"{i},"
        assembly.motor.forward(i)
        csv += str(assembly.ina226.current) + ","
        assembly.motor.stop()
        sys.stdout.write(f"\n{csv}")
        csv = ""
