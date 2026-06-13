import sys
from time import sleep

from micropython import const
from uart import blocking_get_mag_field
from ulab import numpy as np

# Calibration constants
CAL_DC_STEP = const(10)

# P-loop tuning constants
PROP_GAIN = const(25)


def run_calibration_sweep(state, motor_assemblies, uart):
    """
    CLI callback to calibrate the controller
    """
    measurements = {
        "x": {"curr": [], "magfield": []},
        "y": {"curr": [], "magfield": []},
        "z": {"curr": [], "magfield": []},
    }

    sys.stdout.write("\n")
    for plane, assembly in motor_assemblies.items():
        for i in range(0, 101, CAL_DC_STEP):
            sys.stdout.write(f"\rCalibrating {plane} plane {int((i / 200) * 100)}%{'  '}")
            assembly.motor.reverse(i)
            curr = assembly.ina226.current
            sleep(0.5)
            adjusted_field = blocking_get_mag_field(uart)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])

        assembly.motor.stop()

        for i in range(0, 101, CAL_DC_STEP):
            sys.stdout.write(f"\rCalibrating {plane} plane {int(((100 + i) / 200) * 100)}%{'  '}")
            assembly.motor.forward(i)
            curr = assembly.ina226.current
            sleep(0.5)
            adjusted_field = blocking_get_mag_field(uart)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])

        assembly.motor.stop()

    x_currs = np.array(measurements["x"]["curr"])
    y_currs = np.array(measurements["y"]["curr"])
    z_currs = np.array(measurements["z"]["curr"])

    x_fields = np.array(measurements["x"]["magfield"])
    y_fields = np.array(measurements["y"]["magfield"])
    z_fields = np.array(measurements["z"]["magfield"])

    x_line = np.polyfit(x_currs, x_fields, 1)
    y_line = np.polyfit(y_currs, y_fields, 1)
    z_line = np.polyfit(z_currs, z_fields, 1)

    ret = f"x - Slope: {x_line[0]}, Intercept: {x_line[1]}\n"
    ret += f"y - Slope: {y_line[0]}, Intercept: {y_line[1]}\n"
    ret += f"z - Slope: {z_line[0]}, Intercept: {z_line[1]}\n"

    state.slopes_and_intercepts = {
        "x": {"slope": x_line[0], "intercept": x_line[1]},
        "y": {"slope": y_line[0], "intercept": y_line[1]},
        "z": {"slope": z_line[0], "intercept": z_line[1]},
    }

    return ret


def generate_field(state, motor_assemblies, x, y, z):
    """
    CLI callback to generate a specified magnetic field in the cage
    """
    desired_field = {"x": x, "y": y, "z": z}
    sys.stdout.write(f"\n{desired_field}")

    def get_p_control():
        """
        Use the regression from calibration to calculate a control value.
        This control value is the difference between the target current and the actual current
        multiplied by the gain value constant PROP_GAIN, and intended to be used to adjust
        the duty cycle the motor drivers are currently being PWM'd at.
        """
        plane_controls = {
            "x": {"ctrl": 0, "target": 0},
            "y": {"ctrl": 0, "target": 0},
            "z": {"ctrl": 0, "target": 0},
        }

        for plane, assembly in motor_assemblies.items():
            slope = state.slopes_and_intercepts[plane]["slope"]
            intercept = state.slopes_and_intercepts[plane]["intercept"]
            # Invert equation:
            # field = slope * amps + intercept -> (field - intercept) / slope = amps
            target_curr = (desired_field[plane] - intercept) / slope
            process_curr = assembly.ina226.current
            err = target_curr - process_curr

            if target_curr < 0:
                control_output = -1 if process_curr < target_curr else 1
            elif target_curr > 0:
                control_output = 1 if process_curr < target_curr else -1

            # control_output = PROP_GAIN * err

            sys.stdout.write(f'\ntarget: {target_curr} err: {err} control_output: {control_output}')

            plane_controls[plane]["ctrl"] = int(control_output)
            plane_controls[plane]["target"] = target_curr

        return plane_controls

    try:
        prev_duty_cycles = {"x": 50, "y": 50, "z": 50}
        while True:
            try:
                plane_controls = get_p_control()

                for plane, assembly in motor_assemblies.items():
                    plane_ctrl = plane_controls[plane]["ctrl"]
                    duty_cycle = prev_duty_cycles[plane] + plane_ctrl
                    duty_cycle = max(0, min(100, duty_cycle))  # clamp between 0 - 100

                    if plane_controls[plane]["target"] > 0:
                        assembly.motor.forward(duty_cycle)
                    else:
                        assembly.motor.reverse(duty_cycle)

                    prev_duty_cycles[plane] = duty_cycle

                sleep(0.5)

            except KeyboardInterrupt:
                return ""
                break
    except KeyboardInterrupt:
        return ""
    except TypeError as e:
        return f"Error generating field: {e}\n"
    finally:
        for assembly in motor_assemblies.values():
            assembly.motor.stop()
