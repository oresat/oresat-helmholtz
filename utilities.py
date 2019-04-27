import math

DEBUG = False
TICK_TIME = 1
GRAPH_RANGE = 50
INPUT_DELAY = 0.2
POWER_SUPPLIES = []
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

# Returns whether or not a power suplly has been initialized and added to the global list
#   Used for safe checking and some error handling
def supply_available():
    return (len(POWER_SUPPLIES) > 0)

#
# Math things
#

# Generate array of y = x numbers up to max
def generate_y_x_sequence(max):
    y = []
    for i in range(0, max):
        y.append(i)
    return y

def generate_horz_line(max, num):
    y = []
    for i in range(0, max):
        y.append(num)
    return y

# Generate array of 2^x numbers up to max
def generate_pow_2_x_sequence(max):
    y =[]
    for i in range(0, max):
        y.append(math.pow(2,i))
    return y

# Generate array of fibbonacci numbers up to max
def generate_fib_sequence(max):
    y =[]
    for i in range(0, max):
        if(i <= 1): new_num = fibbonacci(i)
        else: new_num = fibbonacci(i, j=(i-2), a=y[i - 2], b=y[i - 1])
        y.append(new_num)
    return y

def generate_sin_sequence(max):
    y = []
    for i in range(0, max):
        y.append(math.sin(i))
    return y

def generate_cos_sequence(max):
    y = []
    for i in range(0, max):
        y.append(math.cos(i))
    return y

# A simple function for generating numbers in the fibbonacci sequence
def fibbonacci(i, j=0, a=0, b=1):
    if(i == 0): sum = 0
    elif(i == 1): sum = 1
    else: sum = a + b

    if(utils.DEBUG): utils.log(2, ("i: " + str(i) + "\tj: " + str(j), "\ta: " + str(a) + "\tb: " + str(b) + "\tsum: " + str(sum)))

    if(j < i):
        sum = fibbonacci(i, (j + 1), a=b, b=sum)
    return sum
