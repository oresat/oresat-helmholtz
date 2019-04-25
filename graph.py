import sys
import pyqtgraph as pg
import numpy as np
import math
import utilities as utils
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer

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

class Line(pg.PlotItem):
    def __init__(self, color='r', data=None, data_size=0, parent=None):
        pg.PlotItem.__init__(self, parent=parent)
        self.color = color
        self.data = data
        self.data_size = data_size

    def is_empty(self):
        return (self.data_size == 0)

class Graph(QtGui.QWidget):
    def __init__(self, parent, graph_range=utils.GRAPH_RANGE):
        QtGui.QWidget.__init__(self, parent=parent)
        self.resize(640, 640)
        self.setWindowTitle('')

        self.counter = 0
        self.graph_range = graph_range
        self.lines = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(utils.TICK_TIME)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.plot = pg.PlotWidget(title='Magnetic Field Levels')
        self.layout.addWidget(self.plot)

        self.button = QtGui.QPushButton('Add point', self)
        self.button.clicked.connect(self.update_graph)
        self.layout.addWidget(self.button, 2, 0)

    def tick(self):
        self.update_graph()


    def add_line(self, line):
        self.lines.append(line)

    def update_graph(self):
        self.counter += 1
        self.lines[0].data = generate_sin_sequence(self.counter)
        self.lines[0].data_size = self.counter
        self.lines[1].data = generate_cos_sequence(self.counter)
        self.lines[1].data_size = self.counter
        self.lines[2].data = generate_horz_line(self.counter, 1)
        self.lines[2].data_size = self.counter

        self.plot.clear()
        self.plot.setClipToView(True)
        if(self.counter < self.graph_range): min = 0
        else: min = self.counter - self.graph_range
        self.plot.setXRange(min, self.counter)
        for i in self.lines:
            self.plot.plot()
            self.plot.plot(i.data, pen=i.color)

def main():
    utils.log(0, 'Graph demo')
    app = pg.mkQApp()

    x = Line(color='r', data=generate_sin_sequence(1))
    y = Line(color='g', data=generate_cos_sequence(1))
    z = Line(color='b', data=generate_horz_line(1, 1))

    graph = Graph(None)
    graph.add_line(x)
    graph.add_line(y)
    graph.add_line(z)
    graph.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
