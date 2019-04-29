import sys
import graph as g
import utilities as utils
import cage_controller as cc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

class ControllerWindow(object):
    def __init__(self):
        self.control_mode = 0

    def setupUi(self, window):
        font = QtGui.QFont()
        font.setFamily("Akaash")
        font.setPointSize(11)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        window.setObjectName("window")
        window.resize(1920, 1080)
        window.setMinimumSize(QtCore.QSize(660, 450))
        window.setMaximumSize(QtCore.QSize(1920, 1080))
        window.setSizeIncrement(QtCore.QSize(1, 1))
        window.setWindowIcon(icon)
        window.setToolTipDuration(2)
        window.setAutoFillBackground(True)
        window.setAnimated(False)
        window.setFont(font)

        self.widget = QtWidgets.QWidget(window)
        self.widget.setObjectName("widget")

        #
        # Action Menu
        #
        window.setCentralWidget(self.widget)

        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.resize(495, 26)
        self.menubar.setObjectName("menubar")

        self.save_mi = QtWidgets.QAction(window)
        self.save_mi.setObjectName("save_mi")
        self.save_mi.triggered.connect(self.save_data)

        self.save_as_mi = QtWidgets.QAction(window)
        self.save_as_mi.setObjectName("save_as_mi")
        self.save_as_mi.triggered.connect(self.save_data_as)

        self.shutdown_mi = QtWidgets.QAction(window)
        self.shutdown_mi.setObjectName("shutdown_mi")
        self.shutdown_mi.triggered.connect(self.shutdown_cage)

        self.menu_main = QtWidgets.QMenu(self.menubar)
        self.menu_main.setObjectName("menu_main")
        self.menu_main.addAction(self.save_mi)
        self.menu_main.addAction(self.save_as_mi)
        self.menu_main.addAction(self.shutdown_mi)

        window.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu_main.menuAction())

        #
        # Power Supply Control Mode Toggle
        #
        self.psu_control_mode_label = QtWidgets.QLabel(self.widget)
        self.psu_control_mode_label.setObjectName("psu_control_mode_label")

        self.psu_control_mode = QtWidgets.QComboBox(self.widget)
        self.psu_control_mode.setObjectName("psu_control_mode")
        self.psu_control_mode.addItem("")
        self.psu_control_mode.addItem("")

        self.active_control_mode_label = QtWidgets.QLabel(self.widget)
        self.active_control_mode_label.resize(100, 20)
        self.active_control_mode_label.setObjectName("active_control_mode_label")

        #
        # Power Supply Control Inputs
        #
        self.psu1_label = QtWidgets.QLabel(self.widget)
        self.psu1_label.resize(45, 20)
        self.psu1_label.setObjectName("psu1_label")

        self.psu1_input = QtWidgets.QLineEdit(self.widget)
        self.psu1_input.resize(100, 30)
        self.psu1_input.setObjectName("psu1_input")

        self.psu2_label = QtWidgets.QLabel(self.widget)
        self.psu2_label.resize(45, 20)
        self.psu2_label.setObjectName("psu2_input")

        self.psu2_input = QtWidgets.QLineEdit(self.widget)
        self.psu2_input.resize(100, 30)
        self.psu2_input.setObjectName("psu2_input")

        self.psu3_label = QtWidgets.QLabel(self.widget)
        self.psu3_label.resize(45, 20)
        self.psu3_label.setObjectName("psu3_label")

        self.psu3_input = QtWidgets.QLineEdit(self.widget)
        self.psu3_input.resize(100, 30)
        self.psu3_input.setObjectName("psu3_input")

        self.apply_button = QtWidgets.QPushButton(self.widget)
        self.apply_button.resize(100, 30)
        self.apply_button.setObjectName("apply_button")
        self.apply_button.clicked.connect(self.update_power_supplies)

        #
        # Data Accuracy Input
        #
        self.accuracy_label = QtWidgets.QLabel(self.widget)
        self.accuracy_label.resize(65, 20)
        self.accuracy_label.setObjectName("accuracy_label")

        self.accuracy_input = QtWidgets.QSpinBox(self.widget)
        self.accuracy_input.resize(81, 28)
        self.accuracy_input.setReadOnly(False)
        self.accuracy_input.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.accuracy_input.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.accuracy_input.setKeyboardTracking(False)
        self.accuracy_input.setProperty("value", 4)
        self.accuracy_input.setObjectName("accuracy_input")

        #
        # Graph
        #
        self.graph = g.Graph(self.widget)
        self.graph.add_line('Magnetometer X', 'r')
        self.graph.add_line('Magnetometer Y', 'g')
        self.graph.add_line('Magnetometer Z', 'b')
        self.graph.resize(1080, 512)
        self.graph.setAutoFillBackground(False)
        self.graph.setObjectName("graph")

        #
        # Status Bar
        #
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(utils.TICK_TIME)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Helmholtz Cage Controller"))
        window.setToolTip(_translate("window", "Helmholtz Cage Controller"))

        self.menu_main.setTitle(_translate("window", "File"))
        self.save_mi.setText(_translate("window", "Save"))
        self.save_as_mi.setText(_translate("window", "Save As"))
        self.shutdown_mi.setText(_translate("window", "Quit"))

        self.active_control_mode_label.setText(_translate("window", "Voltage (V)"))

        self.psu1_label.setText(_translate("window", "Power Supply #1:"))
        self.psu1_input.setText(_translate("window", "12"))

        self.psu2_label.setText(_translate("window", "Power Supply #2:"))
        self.psu2_input.setText(_translate("window", "12"))

        self.psu3_label.setText(_translate("window", "Power Supply #3:"))
        self.psu3_input.setText(_translate("window", "12"))

        self.apply_button.setText(_translate("window", "Apply PSU Changes"))

        self.accuracy_input.setSuffix(_translate("window", " decimals"))
        self.accuracy_label.setText(_translate("window", "Data Accuracy:"))

        self.psu_control_mode_label.setText(_translate("window", "PSU Control Mode"))

        self.psu_control_mode.setItemText(0, _translate("window", "Voltage"))
        self.psu_control_mode.setItemText(1, _translate("window", "Current"))

        # self.layout.addWidget(QWidget, stretch: int = 0, alignment: UnionQt.Alignment=None, Qt.AlignmentFlag=None Qt.Alignment())

        #
        # Layouts
        #
        self.psu_control_layout = QtWidgets.QGridLayout(self.widget)
        self.psu_control_layout.setContentsMargins(0, 0, window.width() / 2, 0)
        self.psu_control_layout.setObjectName('psu_control_layout')
        self.psu_control_layout.addWidget(self.psu_control_mode_label, 0, 0)
        self.psu_control_layout.addWidget(self.psu_control_mode, 0, 1)
        self.psu_control_layout.addWidget(self.active_control_mode_label, 1, 0)
        self.psu_control_layout.addWidget(self.psu1_label, 2, 0)
        self.psu_control_layout.addWidget(self.psu1_input, 2, 1)
        self.psu_control_layout.addWidget(self.psu2_label, 3, 0)
        self.psu_control_layout.addWidget(self.psu2_input, 3, 1)
        self.psu_control_layout.addWidget(self.psu3_label, 4, 0)
        self.psu_control_layout.addWidget(self.psu3_input, 4, 1)
        self.psu_control_layout.addWidget(self.apply_button, 5, 1)

        self.general_layout = QtWidgets.QGridLayout(self.widget)
        self.general_layout.setContentsMargins(window.width() / 2, 0, 0, 0)
        self.general_layout.addWidget(self.accuracy_label, 0, 0)
        self.general_layout.addWidget(self.accuracy_input, 1, 0)
        # self.general_layout.addWidget(self.psu_control_layout, 2, 0)
        self.general_layout.addWidget(self.graph, 0, 1)

    def tick(self):
        self.graph.update_graph()

    def toggle_control_mode(self):
        a

    def update_power_supplies(self):
        voltages = [ float(self.psu_1_voltage_input.text()), float(self.psu_2_voltage_input.text()), float(self.psu_3_voltage_input.text()) ]
        currents = [ float(self.psu_1_current_input.text()), float(self.psu2_input.text()), float(self.psu_3_current_input.text()) ]
        utils.log(0, 'Applying volts:\t\t' + str(voltages) + '\n\tApplying currents:\t' + str(currents))

        if(utils.supply_available()):
            for i in range(0, 3):
                print(str(i + 1))
                utils.POWER_SUPPLIES[i + 1].set_voltage(voltages[i])
                utils.POWER_SUPPLIES[i + 1].set_current(currents[i])
        else:
            utils.log(3, 'No supplies are available for updating!\n\tThrowing away button press event.')

    def save_data(self, filename=(str(utils.unique_time()) + '_magnetometer_data.csv')):
        filepath = utils.data_file_path(filename=i_filename)
        utils.log(0, 'Saving graph data to file: ' + filepath)
        data = self.graph.dump_data()

        file = open(filepath, mode='w')
        file.write('SAVE_TIME' + utils.unique_time_pretty() + '\n')
        file.write('INDEX,X,Y,Z\n')
        for i in self.graph.dump_data():
            file.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + '\n')
        file.close()

    def save_data_as(self, filename):
        self.save_data()

    def shutdown_cage(self):
        utils.log(0, 'Shutting cage down gracefully...')
        if(utils.supply_available()):
            for i in utils.POWER_SUPPLIES:
                i.toggle_supply(0)
        else:
            utils.log(0, 'Power supplies were not available, there is nothing to do.')

        exit(0)

def interface():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = ControllerWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
