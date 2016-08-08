
import os.path
from PyQt5 import QtCore, QtGui, QtWidgets, uic

# compile ui file if necessary
if os.path.getmtime("mainwindow.py") < os.path.getmtime("mainwindow.ui"):
    with open("mainwindow.py", "w") as file:
        print("compiling ui")
        uic.compileUi("mainwindow.ui", file)

