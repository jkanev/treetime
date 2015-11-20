import sys
from PyQt4 import QtGui
import mainwindow

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.advanceSlider)

    def advanceSlider(self):
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

app = QtGui.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
