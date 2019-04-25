import sys
import pyqtgraph as pg
import utilities as utils
from PyQt5 import QtGui, QtCore

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

        self.counter = 0
        self.graph_range = graph_range
        self.lines = []

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.plot = pg.PlotWidget(title='Magnetic Field Levels')
        self.layout.addWidget(self.plot)


    def add_line(self, line):
        self.lines.append(line)

    def update_graph(self):
        self.counter += 1
        self.lines[0].data = utils.generate_sin_sequence(self.counter)
        self.lines[0].data_size = self.counter
        self.lines[1].data = utils.generate_cos_sequence(self.counter)
        self.lines[1].data_size = self.counter
        self.lines[2].data = utils.generate_horz_line(self.counter, 1)
        self.lines[2].data_size = self.counter

        self.plot.clear()
        self.plot.setClipToView(True)
        if(self.counter < self.graph_range): min = 0
        else: min = self.counter - self.graph_range
        self.plot.setXRange(min, self.counter)
        for i in self.lines:
            self.plot.plot()
            self.plot.plot(i.data, pen=i.color)
