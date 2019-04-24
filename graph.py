from PyQt5 import QtGui
import pyqtgraph as pg

app = QtGui.QApplication([])

w = QtGui.QWidget()

button = QtGui.QPushButton('press me')
text_box = QtGui.QLineEdit('put something in here')

grid = QtGui.QGridLayout()
w.setLayout(grid)

grid.addWidget(button, 0, 0)
grid.addWidget(text_box, 0, 1)

w.show()
app.exec_()
