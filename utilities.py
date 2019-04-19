import pyaudio
import struct
import time
import numpy as np
import matplotlib.pyplot as plt

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

# CHUNK = 1024 * 4
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
#
# p = pyaudio.PyAudio()
#
# stream = p.open(
#     format=FORMAT,
#     channels=CHANNELS,
#     rate=RATE,
#     input=True,
#     output=True,
#     frames_per_buffer=CHUNK
# )
#
# fig, ax  = plt.subplots()
# num_plots = 0
# x = np.arange(0, 2 * CHUNK, 2)
# line, = ax.plot(x, np.random.rand(CHUNK))
# ax.set_ylim(0,255)
# ax.set_xlim(0, CHUNK)
#
# while(True):
#     data = stream.read(CHUNK)
#     data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] + 127
#     line.set_ydata(data_int)
#     fig.canvas.draw()
#     fig.canvas.flush_events()
#     num_plots += 1
# print(num_plots)
