import os, random, time

DEBUG = False
CLOSED_LOOP = False
TICK_TIME = 500
GRAPH_RANGE = 35
INPUT_DELAY = 0.2
DATA_ACCURACY = 4
POWER_SUPPLIES = []
TEMPERATURE_SENSORS = []
PSU_ADDRS = [ 'ttyUSB0', 'ttyUSB1', 'ttyUSB2' ]
COIL_ADDRS = [ ['31','32'], ['35','36'], ['37','38'] ] #???
ICON_IMG_PATH='./img/icon.png'
CAGE_DATA_PATH = '/cage_data/'

def data_file_path(filename=''):
    return (str(os.getenv("HOME") + CAGE_DATA_PATH + filename))

# Gets time since the begining of the unix epoch
def unique_time():
    return int(time.time())

# Gets a human readable version of the time since the unix epoch
def unique_time_pretty():
    year, month, day, hour, min, sec, _, _, _ = time.localtime()
    return (str(hour) + ':' + str(min) + ':' + str(sec) + '-' + str(day) + '-' + str(month) + '-' + str(year))

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

# Returns whether or not a power suplly has been initialized and added to the global list
#   Used for safe checking and some error handling
def supply_available():
    return (len(POWER_SUPPLIES) > 0)

# Returns whether or not a power suplly has been initialized and added to the global list
#   Used for safe checking and some error handling
def temp_sensor_available():
    return (len(TEMPERATURE_SENSORS) > 0)

# Random offset of last value for testing the graph
def generate_static(sequence):
    switch_direction = random.randint(0, 1)
    offset = random.random()
    average = 0
    if(len(sequence) > 0): average = sequence[-1]
    if(switch_direction == 1): offset = -1 * offset
    return (average + offset)
