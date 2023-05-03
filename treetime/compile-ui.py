
import os.path
from PyQt6 import uic

# compile ui file if necessary
if os.path.getmtime("mainwindow.py") < os.path.getmtime("mainwindow.ui"):
    with open("mainwindow.py", "w") as file:
        print("compiling ui")
        uic.compileUi("mainwindow.ui", file)

