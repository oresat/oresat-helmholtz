# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(481, 240)
        window.setMinimumSize(QtCore.QSize(275, 240))
        window.setMaximumSize(QtCore.QSize(1080, 240))
        font = QtGui.QFont()
        font.setFamily("Akaash")
        font.setPointSize(11)
        window.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        window.setWindowIcon(icon)
        window.setToolTipDuration(2)
        window.setAutoFillBackground(True)
        window.setWindowFilePath("")
        window.setAnimated(False)
        self.widget = QtWidgets.QWidget(window)
        self.widget.setObjectName("widget")
        self.psu_1_voltage_input = QtWidgets.QLineEdit(self.widget)
        self.psu_1_voltage_input.setGeometry(QtCore.QRect(40, 30, 100, 30))
        self.psu_1_voltage_input.setObjectName("psu_1_voltage_input")
        self.psu_1_label = QtWidgets.QLabel(self.widget)
        self.psu_1_label.setGeometry(QtCore.QRect(10, 35, 45, 20))
        self.psu_1_label.setObjectName("psu_1_label")
        self.apply_button = QtWidgets.QPushButton(self.widget)
        self.apply_button.setGeometry(QtCore.QRect(180, 160, 85, 30))
        self.apply_button.setObjectName("apply_button")
        self.psu_1_current_input = QtWidgets.QLineEdit(self.widget)
        self.psu_1_current_input.setGeometry(QtCore.QRect(160, 30, 100, 30))
        self.psu_1_current_input.setObjectName("psu_1_current_input")
        self.voltage_label = QtWidgets.QLabel(self.widget)
        self.voltage_label.setGeometry(QtCore.QRect(50, 10, 100, 20))
        self.voltage_label.setObjectName("voltage_label")
        self.current_label = QtWidgets.QLabel(self.widget)
        self.current_label.setGeometry(QtCore.QRect(160, 10, 100, 20))
        self.current_label.setObjectName("current_label")
        self.psu_2_current_input = QtWidgets.QLineEdit(self.widget)
        self.psu_2_current_input.setGeometry(QtCore.QRect(160, 65, 100, 30))
        self.psu_2_current_input.setObjectName("psu_2_current_input")
        self.psu_2_voltage_input = QtWidgets.QLineEdit(self.widget)
        self.psu_2_voltage_input.setGeometry(QtCore.QRect(40, 65, 100, 30))
        self.psu_2_voltage_input.setObjectName("psu_2_voltage_input")
        self.psu_2_label = QtWidgets.QLabel(self.widget)
        self.psu_2_label.setGeometry(QtCore.QRect(10, 70, 45, 20))
        self.psu_2_label.setObjectName("psu_2_label")
        self.psu_3_current_input = QtWidgets.QLineEdit(self.widget)
        self.psu_3_current_input.setGeometry(QtCore.QRect(160, 100, 100, 30))
        self.psu_3_current_input.setObjectName("psu_3_current_input")
        self.psu_3_voltage_input = QtWidgets.QLineEdit(self.widget)
        self.psu_3_voltage_input.setGeometry(QtCore.QRect(40, 100, 100, 30))
        self.psu_3_voltage_input.setObjectName("psu_3_voltage_input")
        self.psu_3_label = QtWidgets.QLabel(self.widget)
        self.psu_3_label.setGeometry(QtCore.QRect(10, 105, 45, 20))
        self.psu_3_label.setObjectName("psu_3_label")
        self.graph = QtWidgets.QMdiArea(self.widget)
        self.graph.setGeometry(QtCore.QRect(270, 30, 200, 160))
        self.graph.setObjectName("graph")
        window.setCentralWidget(self.widget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 481, 24))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.actionExport_Graph_Data = QtWidgets.QAction(window)
        self.actionExport_Graph_Data.setObjectName("actionExport_Graph_Data")
        self.menubar.addAction(self.menuMain.menuAction())

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Helmholtz Cage Controller"))
        window.setToolTip(_translate("window", "Helmholtz Cage Controller"))
        self.psu_1_voltage_input.setText(_translate("window", "12"))
        self.psu_1_label.setText(_translate("window", "PSU 1"))
        self.apply_button.setText(_translate("window", "Apply"))
        self.psu_1_current_input.setText(_translate("window", "1.5"))
        self.voltage_label.setText(_translate("window", "Voltage (V)"))
        self.current_label.setText(_translate("window", "Current (A)"))
        self.psu_2_current_input.setText(_translate("window", "1.5"))
        self.psu_2_voltage_input.setText(_translate("window", "12"))
        self.psu_2_label.setText(_translate("window", "PSU 2"))
        self.psu_3_current_input.setText(_translate("window", "1.5"))
        self.psu_3_voltage_input.setText(_translate("window", "12"))
        self.psu_3_label.setText(_translate("window", "PSU 3"))
        self.menuMain.setTitle(_translate("window", "Main"))
        self.actionExport_Graph_Data.setText(_translate("window", "Export Graph Data"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
