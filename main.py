
# -*- coding:utf-8 -*-

# main starting file for use with debugger. Normally the software should be started by the treeview/__main__.py file.
import faulthandler
from treetime.treetime import TreeTime

faulthandler.enable()
TreeTime()
