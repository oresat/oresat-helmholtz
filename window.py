import sys
import graph as g
import utilities as utils
import cage_controller as cc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ControllerWindow(object):
    def __init__(self, window):
        self.control_mode = 0
        self.window = window
        self.font = QtGui.QFont()
        self.font.setFamily("Akaash")
        self.font.setPointSize(11)

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(utils.ICON_IMG_PATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.window.setObjectName("window")
        self.window.resize(720, 480)
        self.window.setMinimumSize(QtCore.QSize(720, 480))
        self.window.setMaximumSize(QtCore.QSize(1920, 1080))
        self.window.setSizeIncrement(QtCore.QSize(1, 1))
        self.window.setWindowIcon(self.icon)
        self.window.setToolTipDuration(2)
        self.window.setAutoFillBackground(True)
        self.window.setAnimated(False)
        self.window.setFont(self.font)

        self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        self.width = self.window.width()
        self.height = self.window.height()

    def initialize_user_interface(self):
        self.central_widget = QtWidgets.QWidget(self.window)
        self.central_widget.setObjectName('central_widget')
        self.widget = QtWidgets.QWidget(self.central_widget)
        self.widget.setObjectName('widget')

        #
        # Action Menu
        #
        self.menubar = QtWidgets.QMenuBar(self.window)
        self.menubar.resize(495, 26)
        self.menubar.setObjectName("menubar")

        self.scan_supplies = QtWidgets.QAction(self.window)
        self.scan_supplies.setObjectName("scan_supplies")
        self.scan_supplies.triggered.connect(self.affirm_power_supplies)

        self.toggle_scan = QtWidgets.QAction(self.window)
        self.toggle_scan.setCheckable(True)
        self.toggle_scan.setObjectName("toggle_scan")
        self.toggle_scan.changed.connect(self.toggle_scanning)

        self.save_mi = QtWidgets.QAction(self.window)
        self.save_mi.setObjectName("save_mi")
        self.save_mi.triggered.connect(self.save_data)

        self.save_as_mi = QtWidgets.QAction(self.window)
        self.save_as_mi.setObjectName("save_as_mi")
        self.save_as_mi.triggered.connect(self.save_data_as)

        self.shutdown_mi = QtWidgets.QAction(self.window)
        self.shutdown_mi.setObjectName("shutdown_mi")
        self.shutdown_mi.triggered.connect(self.confirm_shutdown)

        self.menu_main = QtWidgets.QMenu(self.menubar)
        self.menu_main.setObjectName("menu_main")
        self.menu_main.addAction(self.scan_supplies)
        self.menu_main.addAction(self.toggle_scan)
        self.menu_main.addSeparator()
        self.menu_main.addAction(self.save_mi)
        self.menu_main.addAction(self.save_as_mi)
        self.menu_main.addSeparator()
        self.menu_main.addAction(self.shutdown_mi)

        self.window.setMenuBar(self.menubar)
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
        self.psu_control_mode.currentIndexChanged.connect(self.toggle_control_mode)

        #
        # Power Supply Control Inputs
        #
        self.active_control_mode_label = QtWidgets.QLabel(self.widget)
        self.active_control_mode_label.resize(100, 20)
        self.active_control_mode_label.setObjectName("active_control_mode_label")

        self.psu1_label = QtWidgets.QLabel(self.widget)
        self.psu1_label.setObjectName("psu1_label")

        self.psu1_input = QtWidgets.QLineEdit(self.widget)
        self.psu1_input.setObjectName("psu1_input")

        self.psu2_label = QtWidgets.QLabel(self.widget)
        self.psu2_label.setObjectName("psu2_input")

        self.psu2_input = QtWidgets.QLineEdit(self.widget)
        self.psu2_input.setObjectName("psu2_input")

        self.psu3_label = QtWidgets.QLabel(self.widget)
        self.psu3_label.setObjectName("psu3_label")

        self.psu3_input = QtWidgets.QLineEdit(self.widget)
        self.psu3_input.setObjectName("psu3_input")

        self.apply_button = QtWidgets.QPushButton(self.widget)
        self.apply_button.setObjectName("apply_button")
        self.apply_button.clicked.connect(self.apply_psu_changes)

        #
        # Data Accuracy Input
        #
        self.accuracy_label = QtWidgets.QLabel(self.widget)
        self.accuracy_label.setObjectName("accuracy_label")

        self.accuracy_input = QtWidgets.QSpinBox(self.widget)
        self.accuracy_input.setReadOnly(False)
        self.accuracy_input.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.accuracy_input.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.accuracy_input.setKeyboardTracking(False)
        self.accuracy_input.setProperty("value", 4)
        self.accuracy_input.setObjectName("accuracy_input")
        self.accuracy_input.setDisabled(True)
        self.accuracy_input.valueChanged.connect(self.update_data_accuracy)

        #
        # Misc
        #
        self.quit_button = QtWidgets.QPushButton(self.widget)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.clicked.connect(self.confirm_shutdown)

        #
        # Graph
        #
        self.graph = g.Graph(self.widget)
        self.graph.add_line('Magnetometer X', 'r')
        self.graph.add_line('Magnetometer Y', 'g')
        self.graph.add_line('Magnetometer Z', 'b')
        self.graph.setGeometry(QtCore.QRect(0, 700, self.width, self.height / 3))
        self.graph.setAutoFillBackground(True)
        self.graph.setObjectName("graph")

        #
        # Status Bar
        #
        self.statusbar = QtWidgets.QStatusBar(self.window)
        self.statusbar.setObjectName("statusbar")
        self.window.setStatusBar(self.statusbar)

        self.toggle_control_mode()
        self.translate_user_interface()
        self.update_layouts(10, self.height / 2)
        QtCore.QMetaObject.connectSlotsByName(self.window)

        #
        # Tick loop timer
        #
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(utils.TICK_TIME)

    def translate_user_interface(self):
        _translate = QtCore.QCoreApplication.translate
        self.window.setWindowTitle(_translate("window", "Helmholtz Cage Controller"))
        self.window.setToolTip(_translate("window", "Helmholtz Cage Controller"))

        self.menu_main.setTitle(_translate("window", "File"))
        self.scan_supplies.setText(_translate("window", "Scan for PSU's"))
        self.toggle_scan.setText(_translate("window", "Ignore PSU check"))
        self.save_mi.setText(_translate("window", "Save"))
        self.save_as_mi.setText(_translate("window", "Save As"))
        self.shutdown_mi.setText(_translate("window", "Quit"))

        self.psu_control_mode_label.setText(_translate("window", "PSU Control Mode"))

        self.active_control_mode_label.setText(_translate("window", "PSU_MODE_CONTROL"))

        self.psu1_label.setText(_translate("window", "Power Supply #1:"))
        self.psu1_input.setText(_translate("window", "12"))

        self.psu2_label.setText(_translate("window", "Power Supply #2:"))
        self.psu2_input.setText(_translate("window", "12"))

        self.psu3_label.setText(_translate("window", "Power Supply #3:"))
        self.psu3_input.setText(_translate("window", "12"))

        self.apply_button.setText(_translate("window", "PSU_BUTTON_UPDATE"))

        self.accuracy_label.setText(_translate("window", "Data Accuracy:"))
        self.accuracy_input.setSuffix(_translate("window", " decimals"))
        # self.accuracy_input.setValue(utils.DATA_ACCURACY)

        self.quit_button.setText(_translate("window", "Shutdown Cage"))

        self.psu_control_mode.setItemText(0, _translate("window", "Voltage"))
        self.psu_control_mode.setItemText(1, _translate("window", "Current"))

        self.toggle_control_mode()
        self.affirm_power_supplies()

    def update_layouts(self, x_off, y_off, spacing=10, lw=80, lh=45, iw=100, ih=45):
        #
        # Geometries
        #
        self.psu_control_mode_label.setGeometry(QtCore.QRect(   x_off + self.width - 200 - spacing, y_off, iw, ih))
        self.psu_control_mode.setGeometry(QtCore.QRect(         x_off + self.width - 120 - spacing, y_off, iw, ih))

        self.active_control_mode_label.setGeometry(QtCore.QRect(x_off, y_off - lh / 4, lw * 3, ih))
        self.psu1_label.setGeometry(QtCore.QRect(x_off + iw * 0,    y_off,         iw, ih))
        self.psu1_input.setGeometry(QtCore.QRect(x_off + iw * 0,    y_off + 2 * ih / 3,    iw, ih))
        self.psu2_label.setGeometry(QtCore.QRect(x_off + iw * 1,    y_off,         iw, ih))
        self.psu2_input.setGeometry(QtCore.QRect(x_off + iw * 1,    y_off + 2 * ih / 3,    iw, ih))
        self.psu3_label.setGeometry(QtCore.QRect(x_off + iw * 2,    y_off,         iw, ih))
        self.psu3_input.setGeometry(QtCore.QRect(x_off + iw * 2,    y_off + 2 * ih / 3,    iw, ih))
        self.apply_button.setGeometry(QtCore.QRect(x_off + iw * 2,  y_off + 5 * lh / 3, iw, ih))

        self.accuracy_label.setGeometry(QtCore.QRect(x_off + self.width - 200 - spacing, y_off + ih + spacing, iw, ih))
        self.accuracy_input.setGeometry(QtCore.QRect(x_off + self.width - 120 - spacing, y_off + ih + spacing + 0, iw, ih))
        self.quit_button.setGeometry(QtCore.QRect(self.width - 110 - spacing, self.height - 130, iw, ih))
        self.graph.setGeometry(QtCore.QRect(0, 0, self.width, self.height / 2))

        #
        # Layouts
        #
        self.psu_cml = QtWidgets.QHBoxLayout(self.widget)
        self.psu_cml.setObjectName('psu_cml')
        self.psu_cml.setContentsMargins(0, 0, 0, 0)
        self.psu_cml.addWidget(self.psu_control_mode_label)
        self.psu_cml.addWidget(self.psu_control_mode)

        self.psu_ci1 = QtWidgets.QHBoxLayout(self.widget)
        self.psu_ci1.setObjectName('psu_ci1')
        self.psu_ci1.setContentsMargins(0, 0, 0, 0)
        self.psu_ci1.addWidget(self.psu1_label)
        self.psu_ci1.addWidget(self.psu1_input)

        self.psu_ci2 = QtWidgets.QHBoxLayout(self.widget)
        self.psu_ci2.setObjectName('psu_ci2')
        self.psu_ci2.setContentsMargins(0, 0, 0, 0)
        self.psu_ci2.addWidget(self.psu2_label)
        self.psu_ci2.addWidget(self.psu2_input)

        self.psu_ci3 = QtWidgets.QHBoxLayout(self.widget)
        self.psu_ci3.setObjectName('psu_ci3')
        self.psu_ci3.setContentsMargins(0, 0, 0, 0)
        self.psu_ci3.addWidget(self.psu3_label)
        self.psu_ci3.addWidget(self.psu3_input)

        self.dai = QtWidgets.QHBoxLayout(self.widget)
        self.dai.setObjectName('dai')
        self.dai.setContentsMargins(0, 0, 0, 0)
        self.dai.addWidget(self.accuracy_label)
        self.dai.addWidget(self.accuracy_input)

        self.psu_cmt = QtWidgets.QGridLayout(self.widget)
        self.psu_cmt.setObjectName('psu_cmt')
        self.psu_cmt.setContentsMargins(0, 0, 0, 0)
        self.psu_cmt.addLayout(self.psu_cml,0, 1)
        self.psu_cmt.addLayout(self.psu_ci1,0, 2)
        self.psu_cmt.addLayout(self.psu_ci2,0, 3)
        self.psu_cmt.addLayout(self.psu_ci3,0, 4)
        self.psu_cmt.addLayout(self.dai, 0, 5)

        self.master = QtWidgets.QVBoxLayout(self.widget)
        self.master.setObjectName('master')
        self.master.setContentsMargins(0, 0, 0, 0)
        self.master.addWidget(self.graph)
        self.master.addLayout(self.psu_cmt)

        self.window.setCentralWidget(self.widget)

    def toggle_gui_features(self, mode):
        features = [self.psu_control_mode, self.psu1_input, self.psu2_input, self.psu3_input, self.apply_button, self.graph.dump_button, self.graph.toggle_button]
        if(mode):
            for i in features:
                utils.log(2, 'Enabling: ' + str(i))
                i.setDisabled(False)
        else:
            for i in features:
                utils.log(2, 'Disabling: ' + str(i))
                i.setDisabled(True)

    def affirm_power_supplies(self):
        if(not utils.supply_available()):
            self.toggle_gui_features(False)
            response_box = QMessageBox()
            response_box.setIcon(QMessageBox.Warning)
            response_box.setText("No Power supplies were found.")
            response_box.setInformativeText('Please try the following:\n1.) Turn off all PSU\'s\n2.) Check the cable connections\n3.) Rescan for PSU\'s')
            response_box.setStandardButtons(QMessageBox.Ok)
            response = response_box.exec_()
        else: self.toggle_gui_features(True)

    def toggle_scanning(self):
        if(self.toggle_scan.isChecked()): self.toggle_gui_features(True)
        else: self.affirm_power_supplies()

    def tick(self):
        # Generates dummy data just for testing the graph
        # x = utils.generate_static(self.graph.lines[0].y)
        # y = utils.generate_static(self.graph.lines[1].y)
        # z = utils.generate_static(self.graph.lines[2].y)

        # Actual magnetometer data
        x, y, z = cc.magnetometer()

        self.width = self.window.width()
        self.height = self.window.height()
        self.graph.update_graph([x, y, z])
        self.update_layouts(10, self.height / 2)

    # Changes all the input fields to indicate controlling for either:
    #   voltage over current
    #   current over voltage
    def toggle_control_mode(self):
        labels = [ 'Voltage[V]:', 'Current[A]:' ]
        button_labels = [ 'Apply voltage', 'Apply current']
        input_defaults = [ '12.0', '1.0']

        self.control_mode = self.psu_control_mode.currentIndex()
        self.active_control_mode_label.setText('Actively controlling for: ' + labels[self.control_mode])
        self.psu1_input.setText(input_defaults[self.control_mode])
        self.psu2_input.setText(input_defaults[self.control_mode])
        self.psu3_input.setText(input_defaults[self.control_mode])
        self.apply_button.setText(button_labels[self.control_mode])

    def update_data_accuracy(self):
        utils.DATA_ACCURACY = self.accuracy_input.value

    # Applies changes to the power supply
    def apply_psu_changes(self):
        values = [ float(self.psu1_input.text()), float(self.psu2_input.text()), float(self.psu3_input.text()) ]
        utils.log(0, 'Applying values:\t\t' + str(values))

        if(utils.supply_available()):
            if(self.control_mode == 0):
                for i in range(0, len(utils.POWER_SUPPLIES)):
                    utils.POWER_SUPPLIES[i].set_voltage(values[i])
            elif(self.control_mode == 0):
                for i in range(0, len(utils.POWER_SUPPLIES)):
                    utils.POWER_SUPPLIES[i].set_current(values[i])
            else:
                utils.log(3, 'An invalid control mode was specified: ' + str(self.control_mode) + '!\n\tThis input will be ignored and the power supplies cannot be modified until this is resolved.')
        else:
            utils.log(3, 'No supplies are available for updating!\n\tThrowing away button press event.')

    # Writes graph data to a CSV file auto-generated and puts it in ~/cage_data
    def save_data(self):
        filename = str(utils.unique_time()) + '_magnetometer_data.csv'
        filepath = utils.data_file_path(filename=filename)
        utils.log(0, 'Saving graph data to file: ' + filepath)

        file = open(filepath, mode='w')
        file.write(',,,,,SAVE_TIME:,' + utils.unique_time_pretty() + '\n')
        file.write('INDEX,TIME(ms),X,Y,Z\n')
        index = 1
        for i in self.graph.get_data():
            file.write(str(index) + ',' + str(index * utils.TICK_TIME)  + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + '\n')
            index += 1
        file.close()

        response_box = QMessageBox()
        response_box.setIcon(QMessageBox.Information)
        response_box.setText("Magnetometer Data was saved!")
        response_box.setInformativeText('Data was saved to file: ' + filepath)
        response_box.setStandardButtons(QMessageBox.Ok)
        response = response_box.exec_()

    # Writes graph data to a file specified by the user
    def save_data_as(self, filename):
        self.save_data() # TODO: change this to open a window asking the user for a new path to save to

    def keyPress(self, e):
        utils.log(0, str(e))

    def confirm_shutdown(self, event):
        response_box = QMessageBox()
        response_box.setIcon(QMessageBox.Question)
        response_box.setText("Would you like to shut down the cage?")
        response_box.setInformativeText('You will lose any unsaved data.')
        response_box.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
        response_box.setDefaultButton(QMessageBox.No)
        response = response_box.exec_()

        if(response == QtWidgets.QMessageBox.Yes):
            self.shutdown_cage()
            exit(0)

    # Ensures all physical equiptment is in its cloesd safe state then exits
    def shutdown_cage(self):
        utils.log(0, 'Shutting cage down gracefully...')
        if(utils.supply_available()):
            for i in utils.POWER_SUPPLIES:
                i.toggle_supply(0)
        else:
            utils.log(0, 'Power supplies were not available, there is nothing to do.')

# Function called by the driver to launch the GUI
def interface():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = ControllerWindow(window)
    ui.initialize_user_interface()
    window.show()
    sys.exit(app.exec_())
