import pyqtgraph as pg
import utilities as utils
from PyQt5 import QtCore, QtGui, QtWidgets

class Line(pg.PlotItem):
    def __init__(self, name, color, parent=None):
        pg.PlotItem.__init__(self)
        self.name = name
        self.color = color
        self.x = []
        self.y = []
        self.data_size = 0

    def push_point(self, x_point, y_point):
        self.x.append(x_point)
        self.y.append(y_point)
        self.data_size += 1

        return x_point, y_point, self.size

    def pop_point(self):
        x_point = self.x.pop(self.data_size - 1)
        y_point = self.y.pop(self.data_size - 1)
        size = self.data_size
        self.data_size -= 1

        return x_point, y_point, size

    def is_empty(self):
        return (self.data_size <= 0)

class Graph(QtGui.QWidget):
    def __init__(self, parent, graph_range=utils.GRAPH_RANGE):
        QtGui.QWidget.__init__(self, parent=parent)
        #
        # Custom graph additions (for tracking data)
        #
        self.data_size = 0
        self.lines = []
        self.graph_range = graph_range

        #
        # Graph semantics
        #
        self.plot = pg.PlotWidget(title='Cage Magnetic Field')
        self.plot.setClipToView(True)
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel('left', 'Magnetic Field', units='mT')
        self.plot.setLabel('bottom', 'Time', units='ms')

        #
        # Graph Legend
        #
        self.plot.addLegend()
        self.plot.plot([], pen='r', symbolBrush=0.2, name='MagSensor-X')
        self.plot.plot([], pen='g', symbolBrush=0.2, name='MagSensor-Y')
        self.plot.plot([], pen='b', symbolBrush=0.2, name='MagSensor-Z')

        self.dump_button = QtWidgets.QPushButton('Dump Data', self)
        self.dump_button.clicked.connect(self.dump_data_to_console)

        #
        # Layouts
        #
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plot, 0, 0)
        self.layout.addWidget(self.dump_button, 2, 0)

    # Adds a whole new line to the graph, which automatically gets plotted on the tick loop
    def add_line(self, name, color, parent=None):
        self.lines.append(Line(name, color, parent))
        return self.lines

    # Adds a point to each line endpoint and redraws the graph
    #   number: Takes an array of y-values from line 0 to n (x, y, ... z) to update at each endpoint
    def update_graph(self, numbers=None):
        # Math updates
        self.data_size += 1
        for i in range(0, len(self.lines)):
            self.lines[i].push_point(self.data_size, numbers[i])

        # Clear the graph
        self.plot.clear()

        # Determine the graph range
        if(self.data_size < self.graph_range): min = 0
        else: min = self.data_size - self.graph_range
        self.plot.setXRange(min, self.data_size)

        # Update the lines
        for i in self.lines:
            self.plot.plot(i.y, pen=i.color)

    def dump_data(self):
        results = []
        for i in range(0, self.data_size):
            results.append([self.lines[0].x[i], round(self.lines[0].y[i], utils.DATA_ACCURACY), round(self.lines[1].y[i], utils.DATA_ACCURACY), round(self.lines[2].y[i], utils.DATA_ACCURACY)])
        return results

    def dump_data_to_console(self):
        utils.log(0, 'Here\'s all that hot-n-steamy data you asked for, boss.')
        print('\tINDEX:\t\t\tX:\tY:\tZ:')
        for i in self.dump_data():
            print('\t' + str(i[0]) + '\t' + str(i[1]) + '\t' + str(i[2]) + '\t' + str(i[3]))
