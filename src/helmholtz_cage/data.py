import sys
from time import sleep

from magfield import perturb_and_measure_magfield
from uart import blocking_get_mag_field


def print_curr_mag_csv(motor_assemblies, uart):
    """
    CLI callback to print a csv of currents and associated magnetic field measurements
    """
    sys.stdout.write("\nGenerating CSV of current and magfield measurements...\n")

    measurements = perturb_and_measure_magfield(
        motor_assemblies=motor_assemblies, uart=uart, silent=True
    )

    sys.stdout.write("X,Current,Magfield,Y,Current,Magfield,Z,Current,Magfield\n")
    try:
        for i in range(len(measurements[0])):
            sys.stdout.write(
                f'\
            ,{measurements[0][i][0]},{measurements[0][i][1]},\
            ,{measurements[1][i][0]},{measurements[1][i][1]},\
            ,{measurements[2][i][0]},{measurements[2][i][1]}\n'
            )
    except IndexError as e:
        sys.stdout.write(f"Error: {e}\n")


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
