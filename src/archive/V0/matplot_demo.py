import pyaudio
import struct
import time
import numpy as np
import matplotlib.pyplot as plt

# Global stuff
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio() # Audio driver

stream = p.open( # Open teh stream
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

fig, ax  = plt.subplots() # Create plot space
num_plots = 0 # Plot count for end-of-life
x = np.arange(0, 2 * CHUNK, 2) # Ordered bits
line, = ax.plot(x, np.random.rand(CHUNK)) # Fill random byte data, this will be overwrittten within 1/40th of a second
ax.set_ylim(0,255) # Set y-axis
ax.set_xlim(0, CHUNK) # Set x-axis

# Start the main loop
while(True):
    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] + 127
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots)
