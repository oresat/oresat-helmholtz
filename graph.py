import sys
import pyqtgraph as pg
import numpy as np
import math
import utilities as utils
from PyQt5 import QtGui, QtCore

# Generate array of y = x numbers up to max
def generate_y_x_sequence(max):
    y = []
    for i in range(0, max):
        y.append(i)
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
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent=parent)
        self.resize(640, 640)
        self.setWindowTitle('')

        self.counter = 0
        self.lines = []

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.plot = pg.PlotWidget(title='Magnetic Field Levels')
        self.layout.addWidget(self.plot)

        self.button = QtGui.QPushButton('Add point', self)
        self.button.clicked.connect(self.update_graph)
        self.layout.addWidget(self.button, 2, 0)

        # self.update_graph()

    def add_line(self, line):
        self.lines.append(line)

    def update_graph(self):
        self.counter += 1
        self.lines[0].data = generate_fib_sequence(self.counter)
        self.lines[0].data_size = self.counter
        self.lines[1].data = generate_pow_2_x_sequence(self.counter)
        self.lines[1].data_size = self.counter
        self.lines[2].data = generate_y_x_sequence(self.counter)
        self.lines[2].data_size = self.counter

        self.plot.clear()
        for i in self.lines:
            self.plot.plot(i.data, pen=i.color)

def main():
    utils.log(0, 'Graph demo')
    app = pg.mkQApp()

    x = Line(color='r', data=generate_fib_sequence(1))
    y = Line(color='g', data=generate_pow_2_x_sequence(1))
    z = Line(color='b', data=generate_y_x_sequence(1))

    graph = Graph(None)
    graph.add_line(x)
    graph.add_line(y)
    graph.add_line(z)
    graph.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
