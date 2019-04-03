import sys
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QMainWindow, QAction, qApp)
from PyQt5.QtGui import (QIcon, QFont)

def log(level, message):
    mode = {
        0: 'INFO',
        1: 'WARN',
        2: 'DEBUG',
        3: 'ERROR'
    }
    print("[" + mode[level] + "]:", message)
    return True

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.statusBar().showMessage('Ready')

        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle('Helm')
        self.setWindowIcon(QIcon('../icon.png'))
        self.show()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        QToolTip.setFont(QFont('Calibri', 10))

        button_1 = QPushButton('Quit', self)
        button_1.setToolTip('Quit')
        button_1.resize(button_1.sizeHint())
        button_1.move(50, 50)
        button_1.clicked.connect(QApplication.instance().quit)

        button_2 = QPushButton('Verbose Log', self)
        button_2.setToolTip('Prints the verbose log of window info to the console.')
        button_2.resize(button_2.sizeHint())
        button_2.move(50, 100)
        # button_2.clicked.connect(log(0, "Hello World"))

        self.resize(600, 600)
        self.center()

        self.setToolTip('A thing that will do something useful later.')
        self.setWindowTitle('Helmholtz Cage Controller')
        self.setWindowIcon(QIcon('../icon.png'))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.Yes): event.accept()
        else: event.ignore()

def main():
    app = QApplication(sys.argv)

    # window = Window()
    window = Menu()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
