DEBUG = False
TICK_TIME = 15
GRAPH_RANGE = 30
INPUT_DELAY = 0.2
PSU_ADDRS = [ 'ttyUSB0', 'ttyUSB1', 'ttyUSB2' ]

# Converts from beautiful Celsius to terrible Fahrenheit
def c_to_f(temp_in_c):
    return temp_in_c * 1.8 + 32

# Write to console with appended log level
# level:
#   0: Info
#   1: Warn
#   2: Debug
#   3: Error
# message: Console message
def log(mode, message):
    try:
        level = {
            0: 'INFO',
            1: 'WARN',
            2: 'DEBUG',
            3: 'ERROR',
        }

        print('[' + level[mode] + ']: ' + message)
        return True
    except:
        return False
