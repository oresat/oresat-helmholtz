import sys
from time import sleep

from micropython import const
from uart import blocking_get_mag_field
from ulab import numpy as np

# Calibration constants
CAL_DC_STEP = const(25)
FIELD_AVG_COUNT = const(5)

# P-loop tuning constants
PROP_GAIN = const(25)

# List to get plane names in loops from enumeration variable
PLANES = ["x", "y", "z"]


def perturb_and_measure_magfield(motor_assemblies, uart, silent):
    """
    For each motor driver, set an output current and measure the
    resultant magnetic field for the associated plane.
    """
    measurements = [[], [], []]
    for i, assembly in enumerate(motor_assemblies):
        for j in range(0, 101, CAL_DC_STEP):
            if not silent:
                sys.stdout.write(f"\rCalibrating {PLANES[i]} plane {int((j / 200) * 100)}%{'  '}")
            assembly.motor.reverse(j)
            curr = assembly.ina226.current

            avg_field = 0
            for _ in range(FIELD_AVG_COUNT):
                adjusted_fields = blocking_get_mag_field(uart)
                avg_field += adjusted_fields[i]
            avg_field /= FIELD_AVG_COUNT

            measurements[i].append((curr, int(avg_field)))

        assembly.motor.stop()

        for j in range(0, 101, CAL_DC_STEP):
            if not silent:
                sys.stdout.write(
                    f"\rCalibrating {PLANES[i]} plane {int(((100 + j) / 200) * 100)}%{'  '}"
                )
            assembly.motor.forward(j)
            curr = assembly.ina226.current

            avg_field = 0
            for _ in range(FIELD_AVG_COUNT):
                adjusted_fields = blocking_get_mag_field(uart)
                avg_field += adjusted_fields[i]
            avg_field /= FIELD_AVG_COUNT

            measurements[i].append((curr, int(avg_field)))

        assembly.motor.stop()

    return measurements


def run_calibration_sweep(state, motor_assemblies, uart):
    """
    CLI callback to calibrate the controller
    """

    sys.stdout.write("\n")

    measurements = perturb_and_measure_magfield(
        motor_assemblies=motor_assemblies, uart=uart, silent=False
    )

    lines = []

    for plane in measurements:
        curr = np.array([m[0] for m in plane])
        mag = np.array([m[1] for m in plane])
        line = np.polyfit(curr, mag, 1)
        lines.append(line)

    ret = ""

    for i, line in enumerate(lines):
        slope = line[0]
        intercept = line[1]
        state.slopes_and_intercepts[i]["slope"] = slope
        state.slopes_and_intercepts[i]["intercept"] = intercept
        ret += f"{PLANES[i]} - slope: {slope} intercept: {intercept}\r\n"

    return ret


def generate_field(state, motor_assemblies, x, y, z):
    """
    CLI callback to generate a specified magnetic field in the cage
    """
    desired_field = (x, y, z)
    sys.stdout.write(f"\nGenerating {desired_field}")

    def get_p_control():
        """
        Use the regression from calibration to calculate a control value.
        This control value is the difference between the target current and the actual current
        multiplied by the gain value constant PROP_GAIN, and intended to be used to adjust
        the duty cycle the motor drivers are currently being PWM'd at.
        """

        plane_controls = [
            {"ctrl": 0, "target": 0},
            {"ctrl": 0, "target": 0},
            {"ctrl": 0, "target": 0},
        ]

        for i, assembly in enumerate(motor_assemblies):
            slope = state.slopes_and_intercepts[i]["slope"]
            intercept = state.slopes_and_intercepts[i]["intercept"]
            # Invert equation:
            # field = slope * amps + intercept -> (field - intercept) / slope = amps
            target_curr = (desired_field[i] - intercept) / slope
            process_curr = assembly.ina226.current
            # err = target_curr - process_curr

            if target_curr < 0:
                control_output = -1 if process_curr < target_curr else 1
            elif target_curr > 0:
                control_output = 1 if process_curr < target_curr else -1

            # control_output = PROP_GAIN * err

            plane_controls[i]["ctrl"] = int(control_output)
            plane_controls[i]["target"] = target_curr

        return plane_controls

    try:
        prev_duty_cycles = [0, 0, 0]
        while True:
            try:
                plane_controls = get_p_control()

                for i, assembly in enumerate(motor_assemblies):
                    plane_ctrl = plane_controls[i]["ctrl"]
                    duty_cycle = prev_duty_cycles[i] + plane_ctrl
                    duty_cycle = max(0, min(100, duty_cycle))  # clamp between 0 - 100

                    if plane_controls[i]["target"] > 0:
                        assembly.motor.forward(duty_cycle)
                    else:
                        assembly.motor.reverse(duty_cycle)

                    prev_duty_cycles[i] = duty_cycle

                sleep(0.5)

            except KeyboardInterrupt:
                return ""
                break
    except KeyboardInterrupt:
        return ""
    except TypeError as e:
        return f"Error generating field: {e}\n"
    finally:
        for assembly in motor_assemblies:
            assembly.motor.stop()
