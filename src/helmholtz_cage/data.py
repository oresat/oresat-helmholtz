from time import sleep

from ulab import numpy as np

from uart import blocking_get_mag_field


def print_curr_mag_csv(logger, motor_assemblies, uart):
    logger.info("Generating CSV of current and magfield measurements")
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

    print("X,Current,Magfield,Y,Current,Magfield,Z,Current,Magfield")

    try:
        for i in range(len(measurements["x"]["curr"])):
            print(
                f'\
            ,{measurements["x"]["curr"][i]},{measurements["x"]["magfield"][i]},\
            ,{measurements["y"]["curr"][i]},{measurements["y"]["magfield"][i]},\
            ,{measurements["z"]["curr"][i]},{measurements["z"]["magfield"][i]}'
            )
    except IndexError as e:
        logger.error("%s", e)

    x_currs = np.array(measurements["x"]["curr"])
    y_currs = np.array(measurements["y"]["curr"])
    z_currs = np.array(measurements["z"]["curr"])

    x_fields = np.array(measurements["x"]["magfield"])
    y_fields = np.array(measurements["y"]["magfield"])
    z_fields = np.array(measurements["z"]["magfield"])

    x_line = np.polyfit(x_currs, x_fields, 1)
    y_line = np.polyfit(y_currs, y_fields, 1)
    z_line = np.polyfit(z_currs, z_fields, 1)

    print(f'calculated slope,,{x_line[0]},,{y_line[0]},,{z_line[0]}')
    print(f'calculated intercept,,{x_line[1]},,{y_line[1]},,{z_line[1]}')


def print_fields_csv(time, uart):
    print("time (s),x (mG),y (mG),z (mG)")
    for i in range(time):
        fields = blocking_get_mag_field(uart)
        x = fields["x"]
        y = fields["y"]
        z = fields["z"]
        print(f'{i},{x},{y},{z}')
        sleep(1)


def print_dci_csv(plane, motor_assemblies):
    assembly = motor_assemblies[plane]
    csv = "Duty Cycle,Current,\n"
    for i in range(100, 0, -1):
        csv += f"-{i},"
        assembly.motor.reverse(i)
        csv += str(assembly.ina226.current) + ","
        assembly.motor.stop()
        csv += "\n"
    for i in range(101):
        csv += f"{i},"
        assembly.motor.forward(i)
        csv += str(assembly.ina226.current) + ","
        assembly.motor.stop()
        csv += "\n"

    print(csv)
