# -*- coding:utf-8 -*-

import sys

# main starting file for use with or with pyinstaller for creating executable binaries.
# For normal running please execute the software as a module (python3 -m treetime);
# this will started the treeview/__main__.py file.
import faulthandler
from treetime.treetime import TreeTime

faulthandler.enable()
if len(sys.argv)==2:
    TreeTime(filename=sys.argv[1])
else:
    TreeTime()

