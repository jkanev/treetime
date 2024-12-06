#
# Tis file is part of TreeTime, a tree editor and data analyser
#
# Copyright (C) GPLv3, 2015, Jacob Kanev
# Tree folding icons by Alexhuszagh/BreezeStyleSheets, slightly modified
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

# -*- coding:utf-8 -*-

#!/usr/bin/python3

import sys

from .tree import *
from .mainwindow import *
import base64
import datetime
import time
import os.path
import platform
from PyQt6 import QtCore, QtGui, QtWidgets
from threading import Timer
from PyQt6.QtGui import QPalette, QColor, QIcon, QClipboard, QGuiApplication
from PyQt6.QtWidgets import QAbstractItemView


# Use only for debugging purposes (to cause an error on purpose, if you feel there might be loops), can cause segfaults
# sys.setrecursionlimit(50)


class QNode(QtWidgets.QTreeWidgetItem):
    """
    The GUI counterpart of a node. Displays the contents of a node.
    """
    
    def __init__(self, sourceNode, fieldOrder):
        
        # initialise display
        self.sourceNode = sourceNode
        displayStrings = [sourceNode.name]
        for d in fieldOrder:
            if d in self.sourceNode.fields:
                displayStrings += [self.sourceNode.fields[d].getString()]
            else:
                displayStrings += [""]
                
        super().__init__(displayStrings)
        
        # build reverse field order dictionary
        self.fieldOrder = {}
        for i,f in enumerate(fieldOrder):
            self.fieldOrder[f] = i+1     # plus one because column 0 is the node name
        
        # recurse
        for c in sourceNode.children:
            child = QNode(c, fieldOrder)
            super().addChild(child)
        
        # register callbacks
        self.registerCallbacks()

    def parent(self):
        """
        Returns the parent of a node
        """
        return super().parent() or self.treeWidget().invisibleRootItem() or None

    def registerCallbacks(self):
        """
        Registers QNode-specific callbacks with the source node
        """
        self.sourceNode.registerNameChangeCallback(self.notifyNameChange)
        self.sourceNode.registerFieldChangeCallback(self.notifyFieldChange)
        self.sourceNode.registerDeletionCallback(self.notifyDeletion)
        self.sourceNode.registerSelectionCallback(lambda x: self.notifySelection(x))
        self.sourceNode.registerMoveCallback(self.notifyMove)
        self.sourceNode.registerViewNode(self)

    def notifyNameChange(self, newName):
        super().setText(0, newName)

    def notifyFieldChange(self, fieldName, fieldContent):
        if fieldName in self.fieldOrder:
            super().setText(self.fieldOrder[fieldName], fieldContent)

    def notifyDeletion(self):
        # unlink node
        self.sourceNode = None
        
        # unlink from parent
        if self.parent() is not None:
            self.parent().removeChild(self)
        else:
            print("I have no parent, so I'll stay.")

    def notifyMove(self):

        # unlink from parent
        self.parent().removeChild(self)
        newParent = self.sourceNode.parent.viewNode
        newParent.addChild(self)

    def notifySelection(self, select):
        self.setSelected(select)


class UrlWidget(QtWidgets.QWidget):
    """
    Special custom widget class for URL fields
    """

    def __init__(self, url, callback, font, parent=None):
        """
        Initialise
        """

        # init
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.url = url
        self.callback = callback

        # create line edit control and open button
        linewidget = QtWidgets.QLineEdit(url)
        linewidget.setFont(font)
        linewidget.textChanged.connect(self.textChanged)
        openbutton = QtWidgets.QPushButton("Open")
        openbutton.setFont(font)
        openbutton.clicked.connect(self.buttonClicked)

        # put them next to each other
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(openbutton)
        layout.addWidget(linewidget)

    def textChanged(self, text):
        """
        Callback, to save the new text and notify the parent that the text has changed
        """
        self.url = text
        self.callback()

    def toPlainText(self):
        """
        Callback, called by the GUI to retrieve (possibly changed) URL
        """
        return self.url

    def buttonClicked(self):
        """
        Callback, called when the button has been clicked. Opens the URL with the system
        default software.
        """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.url))


class TextEdit(QtWidgets.QPlainTextEdit):
    """
    Special custom widget class for text fields
    """

    update_timer = None

    def __init__(self, text, callback, height, parent=None):
        """
        Initialise
        """

        # init
        QtWidgets.QPlainTextEdit.__init__(self, text, parent=parent)
        self.callback = callback
        self.has_changed = False
        self.textChanged.connect(self.notifyChange)
        self.setFixedHeight(height * int(self.height()/25))
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.update)

    def notifyChange(self):
        self.has_changed = True

    def update(self):
        if self.has_changed:
            self.has_changed = False
            self.callback()

    def focusInEvent(self, e: QtGui.QFocusEvent):
        """
        Callback, to start timer for periodic update. Doing this on focus-out is too slow during meetings.
        """
        self.update_timer.start(1000)
        super().focusInEvent(e)

    def focusOutEvent(self, e: QtGui.QFocusEvent):
        """
        Callback, to save the new text and notify the parent that the text has changed
        """
        if self.has_changed:
            self.has_changed = False
            self.callback()
        self.update_timer.stop()
        super().focusOutEvent(e)

    def leaveEvent(self, e: QtCore.QEvent):
        """
        Callback, to save the new text and notify the parent that the text has changed
        """
        self.update()
        super().leaveEvent(e)


class TimerWidget(QtWidgets.QWidget):
    """
    A widget displaying an hour timer - a time display (hours:minutes:seconds)
    and a button "start"/"stop"
    """

    timer = None

    def __init__(self, partial, running_since, callback, font, parent=None):
        """
        initialise the timer object
        """

        # init
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.start = running_since and datetime.datetime.strptime(running_since, "%Y-%m-%d %H:%M:%S")  # time when the timer was started last, or None if not running
        self.partial = partial or 0.0     # stored time span + time since timer was started
        self.total = self.partial
        if self.start:
            buttontext = "Stop"
            linetext = "(running)"
        else:
            buttontext = "Start"
            linetext = str(self.partial)
        self.callback = callback

        # create line edit control and open button
        self.linewidget = QtWidgets.QLineEdit(linetext)
        self.linewidget.setFont(font)
        self.linewidget.textEdited.connect(self.textEdited)
        self.startstopbutton = QtWidgets.QPushButton(buttontext)
        self.startstopbutton.setFont(font)
        self.startstopbutton.clicked.connect(self.buttonClicked)

        # put them next to each other
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.startstopbutton)
        layout.addWidget(self.linewidget)

        # start timer if it is loaded as running from file
        if self.start:
            self.updateValue()

    def textEdited(self, text):
        """
        Callback, to save the new text and notify the parent that the text has changed
        """
        if self.start:
            self.linewidget.setText("stop watch running")
        else:
            if text:
                try:
                    d = json.loads(text)
                except json.JSONDecodeError:
                    d = 0.0
            else:
                d = 0.0
            self.total = d
            self.partial = self.total
            self.callback()

    def toPlainText(self):
        """
        Callback, called by the GUI to retrieve (possibly changed) total value
        """
        return str(self.total)

    def runningSince(self):
        """
        Callback, returns the time the timer was started as YYYY-MM-DD hh.mm.ss string
        """
        return self.start and self.start.strftime("%Y-%m-%d %H:%M:%S") or False

    def buttonClicked(self):
        """
        Callback, called when the button has been clicked. Opens the URL with the system
        default software.
        """
        if self.start:
            self.stopTimer()
        else:
            self.startTimer()

    def startTimer(self):
        """
        Starts the timer
        """

        # save the time the timer was started
        self.start = datetime.datetime.now()
        self.startstopbutton.setText("Stop")
        self.linewidget.setText("stop watch running")

        # trigger the first update
        self.updateValue()

    def stopTimer(self):
        """
        Stops the timer
        """
        if self.start:

            # stop the timer, remove possible running timer objects
            self.startstopbutton.setText("Start")

            # store total value
            self.updateValue(update=False)
            self.partial = round(self.total*10000.0) / 10000.0
            self.total = self.partial
            self.start = None
            self.linewidget.setText(str(self.total))

            # notify back-end
            self.callback()

    def updateValue(self, update=True):
        """
        Updates the value in the GUI once and triggers the next update
        Used for sequencial updates while the timer is running. Updates are triggered using a threading.Timer object
        and occur every five seconds
        """

        # first, update the total time
        elapsed = datetime.datetime.now() - self.start
        self.total = self.partial \
                     + elapsed.days * 24.0 \
                     + elapsed.seconds / 60.0 / 60.0 \
                     + elapsed.microseconds / 60.0 / 1000000.0
        if update:
            self.callback()


class EntryDialog(QtWidgets.QDialog):
    """
    Dialog that is shown when the software is openend for the first time.
    Contains an informative message, and a button "load file", and a button
    "new from template".
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Not connected to Data Source")

        buttons = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText("Create new Data File from Template")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Open existing Data File")

        self.layout = QtWidgets.QVBoxLayout()
        message = "To start, please choose to either:"\
            "<ul>"\
            "<li>Create a new data file using an existing template file to define your data structure.<br/>"\
            "Template files are standard <i>TreeTime</i> files (*.empty.trt) without data.<br/>"\
            "They define your data structure (number of trees, item fields, display fields).<br/>"\
            "First you will be asked to select a template file,<br/>"\
            "then you'll be asked for a file name for your new data file.<br/></li>"\
            "<li>Open an existing data file.<br/>"\
            "Data files are <i>TreeTime</i> files (*.trt) containing data.</li>"\
            "</ul>"\
            "<i>TreeTime</i> saves all changes to its data file on the fly.<br/>"\
            "Next time you open <i>TreeTime</i> it will be auto-connected to the file used last.<br/><br/>"\
            "<i>TreeTime</i> comes with several template files and example files.<br/>"\
            "If you're new to <i>TreeTime</i>, you might want to try the Tutorial first.<br/>"\
            "Please have a look in the data directory of your installation.<br/><br/>"
        message = QtWidgets.QLabel(message)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class TreeTimeWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Implements the main part of the GUI.
    """

    def __init__(self, filename=None):
        """
        Initialise the application, connect all button signals to application functions, load theme and last file
        """

        print("starting TreeTime...")

        # initialise main window
        super().__init__()
        self.setupUi(self)

        # connect all button signals
        print("setting up GUI...")
        self.pushButtonNewChild.clicked.connect(lambda: self.createNode("child", False))
        self.pushButtonNewSibling.clicked.connect(lambda: self.createNode("sibling", False))
        self.pushButtonNewParent.clicked.connect(lambda: self.createNode("parent", False))
        self.pushButtonCopyNodeChild.clicked.connect(lambda: self.createNode("child", True))
        self.pushButtonCopyNodeSibling.clicked.connect(lambda: self.createNode("sibling", True))
        self.pushButtonCopyNodeParent.clicked.connect(lambda: self.createNode("parent", True))
        self.pushButtonCopyBranchSibling.clicked.connect(lambda: self.createNode("sibling", True, True))
        self.pushButtonNewFromTemplate.clicked.connect(self.pushButtonNewFromTemplateClicked)
        self.pushButtonLoadFile.clicked.connect(self.pushButtonLoadFileClicked)
        self.pushButtonSaveToFile.clicked.connect(self.pushButtonSaveToFileClicked)
        self.pushButtonExport.clicked.connect(self.pushButtonExportClicked)
        self.pushButtonRemoveNode.clicked.connect(self.pushButtonRemoveNodeClicked)
        self.pushButtonDeleteNode.clicked.connect(self.pushButtonDeleteNodeClicked)
        self.pushButtonRemoveBranch.clicked.connect(lambda: self.moveCurrentItemToNewParent(self.currentTree, None))
        self.pushButtonDeleteBranch.clicked.connect(self.pushButtonDeleteBranchClicked)
        self.pushButtonDataFields.clicked.connect(self.pushButtonDataFieldsClicked)
        self.pushButtonTreeFields.clicked.connect(self.pushButtonTreeFieldsClicked)
        self.sliderZoom.valueChanged.connect(self.sliderZoomChanged)
        self.tableWidget.cellChanged.connect(self.tableWidgetCellChanged)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)     # column 0: fixed
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Fixed)     # column 1: fixed, 100
        self.tableWidget.horizontalHeader().resizeSection(1, 100)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Fixed)     # column 2: fixed
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)     # column 3: stretch
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Fixed)     # column 4: fixed
        self.tabWidget.currentChanged.connect(self.tabWidgetCurrentChanged)
        self.write_delay = 0
        self.write_timer = False
        self.locked = True
        self.export_continuous = False
        self.auto_updates = []
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.updateTimers)
        self.update_timer.start(1000)
        self.tabWidgets = []
        self.treeWidgets = []
        self.currentTree = 0
        self.currentItem = None
        self.currentColumn = None
        self.gridInitialised = False
        self.editMode = 'content'     # one of 'content', 'tree', or 'data'

        # init application settings
        print("loading system settings...")
        self.settings = QtCore.QSettings('FreeSoftware', 'TreeTime')

        # store system font size
        self._dataFontPointSize = int(self.centralwidget.font().pointSize())

        # show last exported file
        self.labelCurrentExportFile.setText(self.settings.value('exportFile') or "[last exported file]")

        # load last file
        print("opening last file...")
        if filename:
            loadFile = filename
        else:
            loadFile = self.settings.value('lastFile')

        # try loading silently once
        try:
            self.loadFile(loadFile)
            self.setWindowTitle("TreeTime - " + loadFile)
            self.settings.setValue('fileDir', os.path.dirname(loadFile))
            self.settings.setValue('lastFile', loadFile)
            self.labelCurrentFile.setText(loadFile)
            fileLoaded = True
        except BaseException:
            fileLoaded = False

        # keep trying
        while not fileLoaded:
            try:
                msg = EntryDialog(self)
                if msg.exec():
                    self.pushButtonNewFromTemplateClicked()
                else:
                    self.pushButtonLoadFileClicked()
                fileLoaded = True
            except BaseException:
                pass

        # init themes and set last theme
        print("initialising fonts and colours...")
        self.system_palette = self.palette()
        self.fillThemeBox()
        self.fillColourBox()
        self.cboxThemeTextChanged()
        self.cboxColoursTextChanged()
        self.cboxTheme.currentTextChanged.connect(self.cboxThemeTextChanged)
        self.cboxColours.currentTextChanged.connect(self.cboxColoursTextChanged)

        # show window
        print("showing main window...")
        self.showMaximized()

    def endisableButtons(self, state):
        """
        Enables all buttons if state==True, disables them otherwise
        :param state: the button state to set
        """
        self.pushButtonNewChild.setEnabled(state)
        self.pushButtonNewSibling.setEnabled(state)
        self.pushButtonNewParent.setEnabled(state)
        self.pushButtonCopyNodeChild.setEnabled(state)
        self.pushButtonCopyNodeSibling.setEnabled(state)
        self.pushButtonCopyNodeParent.setEnabled(state)
        self.pushButtonCopyBranchSibling.setEnabled(state)
        self.pushButtonNewFromTemplate.setEnabled(state)
        self.pushButtonLoadFile.setEnabled(state)
        self.pushButtonSaveToFile.setEnabled(state)
        self.pushButtonExport.setEnabled(state)
        self.pushButtonRemoveNode.setEnabled(state)
        self.pushButtonDeleteNode.setEnabled(state)
        self.pushButtonRemoveBranch.setEnabled(state)
        self.pushButtonDeleteBranch.setEnabled(state)
        self.pushButtonDataFields.setEnabled(state)
        self.pushButtonTreeFields.setEnabled(state)

    def closeEvent(self, event):
        """
        Do some cleanup before you close the window
        """

        # Write state to file
        if self.write_timer:
            self.write_timer.cancel()
        self.write_delay = 0
        try:
            self.writeToFile()
        except AttributeError:
            pass

        # continue closing the window
        event.accept()  # let the window close

    def fillThemeBox(self):
        """
        Fills the theme selection box with all themes the system is capable of
        """

        # our own theme, basically Fusion with some changes
        self.cboxTheme.addItem("Organic")

        # built-in themes
        for k in QtWidgets.QStyleFactory.keys():
            self.cboxTheme.addItem(k)
        current = self.settings.value('theme')
        if current:
            self.cboxTheme.setCurrentText(current)

    def fillColourBox(self):
        """
        Fills the theme selection box with all themes the system is capable of
        """
        self.cboxColours.addItem("Dark")
        self.cboxColours.addItem("Light")
        self.cboxColours.addItem("System")
        current = self.settings.value('colours')
        if current:
            self.cboxColours.setCurrentText(current)

    def cboxThemeTextChanged(self):
        """
        Callback from the theme selector combo box. Sets a new theme and stores it in the settings.
        """
        application = QtWidgets.QApplication.instance()
        style = self.cboxTheme.currentText()
        self.settings.setValue('theme', style)

        # set style sheets first and then apply QStyle, otherwise the stylesheet break everything
        if 'Organic' in style:
            wd = __file__[:-12].replace('\\', '/')     # for windows file separators
            colour = wd + '/themes/' + (self.cboxColours.currentText() == "Light" and "light" or "dark")

            # QML for more padding and folding icons
            baseColour = application.palette().base().color().name()
            qss = (
                # padding on the buttons
                "QPushButton { padding: 0.3em;}"
                "QToolButton { padding: 0.3em; margin-top: 0.1em; margin-bottom: 0.1em; margin-right: 0.0em; margin-left: 0.0em;}"
                "QTreeView::item { padding: 0.2em; }"
                                                                                                                  
                # tree decorators
                # has-siblings: not the last in the sibling list; !has-siblings: the last in the sibling list
                # adjoins-item: the direct markers (the last before the text); 
                # !adjoins-item: the higher-level unfolded markers (the non-rightmost tree markers);
                #                if set the children and siblings flags apply to the respective level parent
                # has-children / !has-children: whether or nor there are children
                # open / closed: whether the item is folded or unfolded
                # border-image: scales with multi-line entries
                # image: does not scale with multi-line entres
                "QTreeView::branch:has-children:closed:adjoins-item { image:url(" + colour + "_triangle_right.svg); }"
                "QTreeView::branch:has-children:closed:adjoins-item:hover { image:url(" + colour + "_triangle_right_hover.svg); }"
                "QTreeView::branch:has-children:open:adjoins-item { image:url(" + colour + "_triangle_down.svg); }"
                "QTreeView::branch:has-children:open:adjoins-item:hover { image:url(" + colour + "_triangle_down_hover.svg); }"
                "QTreeView::branch:has-siblings:adjoins-item { border-image:url(" + colour + "_branch_full.svg); }"
                "QTreeView::branch:has-siblings:!has-children:adjoins-item { image:url(" + colour + "_twig_empty.svg); }"
                "QTreeView::branch:!has-siblings:adjoins-item { border-image:url(" + colour + "_branch_top.svg); }"
                "QTreeView::branch:!has-siblings:!has-children:adjoins-item { image:url(" + colour + "_twig_empty.svg); }"
                "QTreeView::branch:has-siblings:!adjoins-item { border-image:url(" + colour + "_branch_full.svg); }"
                                                                                              
                # make sure the branch area is not made invisible because it has the same colour as the selection
                "QTreeView::branch:selected { background-color: " + baseColour + ";}"
            )
            application.setStyleSheet(qss)

        style = QtWidgets.QStyleFactory.create(style)
        application.setStyle(style)
        self.itemSelectionChanged()

    def cboxColoursTextChanged(self):
        """
        Callback from the theme selector combo box. Sets a new theme and stores it in the settings.
        """
        application = QtWidgets.QApplication.instance()
        colour = self.cboxColours.currentText()
        self.settings.setValue('colours', colour)
        palette = QPalette()

        # Apply dark colours
        if colour == "Dark":
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(50, 52, 54))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(50, 52, 54))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(150, 150, 150))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(100, 100, 100))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(60, 62, 64))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Link, QColor(60, 200, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(60, 200, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Light, QColor(80, 84, 88))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Midlight, QColor(60, 63, 66))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(40, 42, 44))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Mid, QColor(30, 31, 33))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Dark, QColor(20, 21, 22))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Shadow, QColor(10, 10, 11))

        # apply light colours
        elif colour == "Light":
            palette = QPalette()
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(255-53, 255-53, 255-53))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(255-53, 255-53, 255-53))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(70, 70, 70))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(150, 150, 150))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(255-53, 255-53, 255-53))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.BrightText, QColor(0, 0, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Link, QColor(255-42, 255-130, 255-218))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(255-42, 255-130, 255-218))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Light, QColor(255-10, 255-10, 255-10))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Midlight, QColor(255-20, 255-20, 255-20))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(255-25, 255-25, 255-25))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Mid, QColor(255-100, 255-100, 255-100))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Dark, QColor(255-150, 255-150, 255-150))
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Shadow, QColor(255-200, 255-200, 255-200))

        # apply system colours
        elif colour == "System":
            palette = self.system_palette
        application.setPalette(palette)
        self.cboxThemeTextChanged()

    def sliderZoomChanged(self):
        """
        Scales the font size of the data display part of the UI by the offide of the slider
        """

        # get current value of slider and store default font size
        offset = self.sliderZoom.value()
        font = self.centralwidget.font()
        system_size = font.pointSize()
        self._dataFontPointSize = int(system_size + offset)
        font.setPointSize(self._dataFontPointSize)

        # change font in data item view
        self.tableWidget.setFont(font)
        self.showContentInDataView(self.currentTree)    # redraw data pane

        # change font in all tree widgets
        for tree in self.treeWidgets:
            tree.setFont(font);

        # change label
        self.labelZoom.setText("Zoom {}{}".format(offset > 0 and '+' or '', offset))


    def pushButtonSaveToFileClicked(self):
        """
        Callback for the save-file button. Saves the current data to a new file and keeps that file connected.
        """
        fileDir = self.settings.value('fileDir') or ''
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Save new Data File", fileDir, 'TreeTime Files (*.trt)')[0]
        if file != '':
            self.labelCurrentFile.setText(file)
            self.writeToFile()
            self.setWindowTitle("TreeTime - " + file)
            self.settings.setValue('fileDir', os.path.dirname(file))
            self.settings.setValue('lastFile', file)

    def pushButtonLoadFileClicked(self):
        """
        Callback for the load-file button. Loads new file and keeps that file connected.
        """
        fileDir = self.settings.value('fileDir') or ''
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Load Data File", fileDir, 'TreeTime Files (*.trt)')[0]
        if file != '':
            self.loadFile(file)
            self.setWindowTitle("TreeTime - " + file)
            self.settings.setValue('fileDir', os.path.dirname(file))
            self.settings.setValue('lastFile', file)
            self.labelCurrentFile.setText(file)

    def pushButtonDataFieldsClicked(self):
        """
        Callback for the data field edit button. Toggles the tree-field edit mode.
        """
        if self.editMode == 'data':
            self.changeEditMode('content')
        else:
            self.changeEditMode('data')

    def pushButtonTreeFieldsClicked(self):
        """
        Callback for the data field edit button. Toggles the tree-field edit mode.
        """
        if self.editMode == 'tree':
            self.changeEditMode('content')
        else:
            self.changeEditMode('tree')

    def pushButtonExportClicked(self):

        file = ""

        # We're not in contiuous mode -- show file dialog
        if not self.export_continuous:
            if self.currentItem:

                exportFormat = self.comboBoxExportFormat.currentText()
                exportToFile = self.radioButtonExportToFile.isChecked()
                if exportToFile:
                    extensions = {
                        "HTML (Tiles)": "HTML Files (*.html)",
                        "HTML (List)": "HTML Files (*.html)",
                        "Text/Unicode": "Text Files (*.txt)",
                        "CSV": "CSV (Comma-separated Values) Files (*.csv)"
                    }
                    fileDir = os.path.dirname(self.settings.value('exportFile')) or ''
                    file = QtWidgets.QFileDialog.getSaveFileName(self, "Export to " + exportFormat, fileDir,
                                                                 extensions[exportFormat])[0]
                    if not file:
                        return

                # we're starting continous mode -- set the texts, set the flag, and call the timer function
                if self.radioButtonExportContinuously.isChecked():
                    self.pushButtonExport.setText("Stop Conticontinuous export")
                    self.labelExportFileDescription.setText("Exporting continuously to:")
                    self.radioButtonExportContinuously.setDisabled(True)
                    self.radioButtonExportOnce.setDisabled(True)
                    self.export_continuous = True
                    self.delayedContinuousExport(file)

                # we're doing a standard export
                self.export(file)

        # We're stopping continuous mode -- set the texts, set the flag
        else:
            self.pushButtonExport.setText("Export")
            self.labelExportFileDescription.setText("Last exported file:")
            self.radioButtonExportContinuously.setEnabled(True)
            self.radioButtonExportOnce.setEnabled(True)
            self.export_continuous = False


    def delayedContinuousExport(self, file):
        """
        Writes to file using current settings, then checks current state (user may have stopped), then waits for three
        seconds, then calls itself
        Used to loop the continuous file writing.
        """

        # First writes to file
        self.export(file, continuous=True)

        # If mode active, either calls itself after two seconds
        if self.export_continuous:
            self.export_timer = Timer(3, lambda: self.delayedContinuousExport(file))
            self.export_timer.start()

        # If not, do nothing

    def export(self, file, continuous=False):
        """
        Callback for the text/html/csv export. Asks for a file name, then writes branch text export into it.
        """

        if self.currentItem:

            # read file format
            exportFormat = self.comboBoxExportFormat.currentText()
            allFields = self.radioButtonExportAllFields.isChecked()

            # Select target file or cancel
            exportToFile = self.radioButtonExportToFile.isChecked()

            # The target string for file write / clipboard write
            data = ""
            depth = self.comboBoxExportDepth.currentIndex() - 1

            # export current branch
            if self.radioButtonExportBranch.isChecked():

                currentNode = self.currentItem.viewNodes[self.currentTree]
                if currentNode:

                    # write to data string
                    if exportFormat == "CSV":
                        data = currentNode.to_csv(depth=depth, fields=allFields)
                    elif exportFormat == "Text/Unicode":
                        data = currentNode.to_txt(depth=depth, fields=allFields)
                    elif exportFormat == "HTML (List)":
                        dummy, data = currentNode.to_html(header=True, footer=True, depth=depth, fields=allFields,
                                                          style='list', continuous=continuous)
                    else:
                        dummy, data = currentNode.to_html(header=True, footer=True, depth=depth, fields=allFields,
                                                          style='tiles', continuous=continuous)
                else:
                    if continuous:
                        return
                    else:
                        data = ("No branch selected, export is empty")

            # export entire tree
            elif self.radioButtonExportTree.isChecked():

                # pick up the source
                rootNode = self.forest.children[self.currentTree]
                children = sorted(rootNode.children, key=lambda a: a.name)

                # write data string
                if exportFormat == "CSV":
                    first = True
                    for c in children:
                        data += c.to_csv(first=first, depth=depth, fields=allFields)
                        first = False
                elif exportFormat == "Text/Unicode":
                    for c in children:
                        data += '\n'
                        data += c.to_txt(depth=depth, fields=allFields)
                        data += '\n'
                else:
                    next_background = {'blue': 'green', 'green': 'red', 'red': 'blue'}
                    background = 'blue'
                    style = (exportFormat == "HTML (List)" and "list") or "tiles"
                    for c in range(0, len(children)):
                        if c == 0:
                            background = next_background[background]
                            data += children[c].to_html(header=True, depth=depth,
                                                        fields=allFields, style=style, continuous=continuous)[1]
                        elif c == len(children) - 1:
                            background = next_background[background]
                            data += children[c].to_html(footer=True, depth=depth,
                                                        fields=allFields, style=style, continuous=continuous)[1]
                        else:
                            background = next_background[background]
                            data += children[c].to_html(depth=depth,
                                                        fields=allFields, style=style, continuous=continuous)[1]

            # export current node with context
            else:
                path = self.currentItem.trees[self.currentTree]
                currentNode = self.forest.children[self.currentTree].findNode(path[:1])
                if currentNode:

                    # write to data string
                    if exportFormat == "CSV":
                        data = currentNode.to_csv(depth=depth, fields=allFields, context=path)
                    elif exportFormat == "Text/Unicode":
                        data = currentNode.to_txt(depth=depth, fields=allFields, context=path)
                    elif exportFormat == "HTML (List)":
                        dummy, data = currentNode.to_html(header=True, footer=True, depth=depth, context=path,
                                                          fields=allFields, style='list', continuous=continuous)
                    else:
                        dummy, data = currentNode.to_html(header=True, footer=True, depth=depth, context=path,
                                                          fields=allFields, style='tiles', continuous=continuous)
                else:
                    data = ("No branch selected, export is empty")

            # save to file or to clipboard
            if exportToFile:
                with open(file, "w") as f:
                    f.write(data)
                self.labelCurrentExportFile.setText(file)
                self.settings.setValue("exportFile", file)
            else:
                clipboard = QGuiApplication.clipboard()
                clipboard.setText(data, QClipboard.Mode.Clipboard)
                clipboard.setText(data, QClipboard.Mode.FindBuffer)
                if clipboard.supportsSelection():
                    clipboard.setText(data, QClipboard.Mode.Selection)
                time.sleep(0.001)

    def pushButtonNewFromTemplateClicked(self):
        """
        Callback for the new-from-template button. Loads new file and immediately saves it to a different file.
        """

        # First load template file
        templateDir = self.settings.value('templateDir') or ''
        template = QtWidgets.QFileDialog.getOpenFileName(self, "Load Template", templateDir,
                                                         'TreeTime Templates (*.empty.trt)')[0]
        if template != '':
            self.loadFile(template)
            self.settings.setValue('templateDir', os.path.dirname(template))

            # Then save as new file
            self.pushButtonSaveToFileClicked()

    def pushButtonRemoveNodeClicked(self):
        """
        Remove the current node from the tree and move all children in this tree to their parent
        """
        message = "Removing node \"" \
                  + self.currentItem.name \
                  + "\". \n\n" \
                  + "This will move all children in this tree to the node's parent.\n" \
                  + "Changes are saved to file immediately and cannot be reverted."
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle("TreeTime Message")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        result = msgBox.exec()

        # remove if the user has confirmed
        if result == QtWidgets.QMessageBox.StandardButton.Ok:

            # move all children to parent node
            currentNode = self.currentItem.viewNodes[self.currentTree]
            parent = currentNode.parent
            while len(currentNode.children):
                currentNode.children[0].item.moveInTree(self.currentTree, parent.path)

            # delete item and update file
            item = self.currentItem
            item.removeFromTree(self.currentTree)
            if not sum([len(t) for t in item.trees]):
                self.forest.itemPool.deleteItem(item)
            self.delayedWriteToFile()

    def pushButtonDeleteNodeClicked(self):
        """
        Delete Node single node and move all children in all branches to the node's parent
        """
        message = "Deleting node \"" + self.currentItem.name + "\". \n\n" \
                  + "This will move all children in all trees to their nodes' parents.\n" \
                  + "Changes are saved to file immediately and cannot be reverted."
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle("TreeTime Message")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        result = msgBox.exec()

        # delete if the user has confirmed
        if result == QtWidgets.QMessageBox.StandardButton.Ok:

            # move all children in all trees to parent node
            for t in range(0, len(self.forest.children)):
                node = self.currentItem.viewNodes[t]
                if node:
                    while len(node.children):
                        node.children[0].item.moveInTree(t, node.parent.path)

            # remove running timers
            for f in self.currentItem.fields.keys():
                if self.currentItem.fields[f]['type'] == 'timer':
                    self.currentItem.fields[f]['running_since'] = False
                    self.adjustAutoUpdate(self.currentItem, f)

            # delete item and update file
            self.forest.itemPool.deleteItem(self.currentItem)
            self.delayedWriteToFile()

    def pushButtonDeleteBranchClicked(self):
        """
        Delete Node single node and move all children in all branches to the node's parent
        """
        message = "Deleting branch \"" + self.currentItem.name + "\". \n\n" \
                  + "This will delete all branches in all trees.\n" \
                  + "This remove large parts of your data due to connections between trees.\n" \
                  + "Changes are saved to file immediately and cannot be reverted."
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle("TreeTime Message")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        result = msgBox.exec()

        # delete if the user has confirmed
        if result == QtWidgets.QMessageBox.StandardButton.Ok:

            # recursive function to collect all child nodes in all trees
            def collect_children(item, item_list):
                if item not in item_list:
                    item_list += [item]
                    for t in range(0, len(item.trees)):
                        node = item.viewNodes[t]
                        if node:
                            for child in node.children:
                                collect_children(child.item, item_list)

            # find unique list of children to delete, in all trees
            to_delete = []
            collect_children(self.currentItem, to_delete)

            message = ("The selected action will remove {} of all {} nodes.\n"
                       + "This is {:.0f} % of your data.\n"
                       + "Are you sure?").format(len(to_delete), len(self.forest.itemPool.items),
                                                 100.0*len(to_delete)/len(self.forest.itemPool.items))
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(message)
            msgBox.setWindowTitle("TreeTime Message")
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            result = msgBox.exec()

            # delete if the user has confirmed
            if result == QtWidgets.QMessageBox.StandardButton.Ok:
                # remove all running timers
                for i in to_delete:
                    for f in i.fields.keys():
                        if i.fields[f]['type'] == 'timer':
                            i.fields[f]['running_since'] = False
                            self.adjustAutoUpdate(i, f)

                # delete items and update file
                for i in to_delete:
                    self.forest.itemPool.deleteItem(i)
                self.delayedWriteToFile()

    def changeEditMode(self, mode):
        """
        Changes the current editing mode to the mode in the parameters.
        Disables/enables buttons, changes button text.
        :param mode: The new mode
        """

        # set button states and texts
        self.endisableButtons(mode == 'content' and True or False)
        self.pushButtonTreeFields.setText(mode != 'tree' and "View Tree Fields" or "Finished")
        self.pushButtonDataFields.setText(mode != 'data' and "View Data Fields" or "Finished")
        self.pushButtonTreeFields.setEnabled(mode != 'data' and True or False)
        self.pushButtonDataFields.setEnabled(mode != 'tree' and True or False)

        # clear data view
        self.tableWidget.clear()
        self.gridInitialised = False

        # entering tree field mode
        if mode == 'tree' and self.editMode != 'tree':

            # set selection type
            for tree in self.treeWidgets:
                tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
                tree.clearSelection()

            # fold tree and select first item
            currentTree = self.treeWidgets[self.currentTree]
            rootItem = currentTree.invisibleRootItem()
            for c in range(0, rootItem.childCount()):
                currentTree.collapseItem(rootItem.child(c))

            # init display
            self.tableWidget.clear()
            self.gridInitialised = False

        # entering content edit mode
        elif mode != 'tree' and self.editMode == 'tree':

            # set selection type
            for tree in self.treeWidgets:
                tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
                tree.clearSelection()

            # enable tabs
            for tab in self.tabWidgets:
                tab.setEnabled(True)

            # init display
            self.tableWidget.clear()
            self.gridInitialised = False

        # entering data field edit mode
        elif mode == 'data':
            self.showDataFieldsInDataView()

        self.editMode = mode

    def loadFile(self, filename):
        self.removeBranchTabs()
        self.tabWidgets = []
        self.treeWidgets = []
        self.currentTree = 0
        self.currentItem = None
        self.gridInitialised = False
        self.editMode = 'content'     # one of 'content', 'tree', or 'data'
        if filename is not None and filename != '':
            try:
                # load file
                self.forest = Forest(filename)
                self.createBranchTabs()
                self.fillTreeWidgets()

                # init all timers
                self.initAllAutoUpdates()

                # select first item
                if len(self.treeWidgets):
                    firstTree = self.treeWidgets[0]
                    items = firstTree.topLevelItemCount()
                    if items:
                        firstTree.topLevelItem(0).setSelected(True)

            # in case of failure, show user message and reload
            except KeyError as e:

                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(str(e))
                msgBox.setWindowTitle("TreeTime Message")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                result = msgBox.exec()
                self.pushButtonLoadFileClicked()

        else:
            self.pushButtonLoadFileClicked()

    def delayedWriteToFile(self, countdown=False):
        """
        Schedules a write after 5 seconds. A timer is called that stops after 1 second and decreases a counter.
        If the counter is at zero, a write-to-file is performed. If the counter is > 0, it is counted down and a
        new timer is started.
        When changing cell contents, each cell change calls a delayed write. The file is only written if there has
        been no change for 5 seconds (otherwise the continuous file writing slows the user input down).
        :param countdown: Whether to count down and trigger a write at zero (=True),
                          or whether to init a new run (=False)
        :return:
        """

        # We've been called by a timer process, count down and possibly write
        if countdown:
            if self.write_delay > 0:
                self.write_delay -= 1
                if self.write_delay == 0:
                    self.writeToFile()
                self.write_timer = False

        # We've been called after a cell change, init the counter
        else:
            self.write_delay = 5

        # The counter is up, start another 2-second timer
        if self.write_delay > 0 and not self.write_timer:
            self.write_timer = Timer(1, self.delayedWriteToFile, kwargs={'countdown': True})
            self.write_timer.start()

    def writeToFile(self, delayed=False, countdown=False):
            self.forest.writeToFile(self.labelCurrentFile.text())

    def removeBranchTabs(self):
            self.tabWidget.clear()
            self.tabWidgets = []

    def createBranchTabs(self):
        
        self.locked = True
        
        # create tabs and tree widgets
        for n,c in enumerate(self.forest.children):
            newTab = QtWidgets.QWidget()
            newTab.setObjectName("tab"+str(n))
            newGridLayout = QtWidgets.QGridLayout(newTab)
            self.tabWidget.addTab(newTab, "")
            self.tabWidgets += [newTab]
            self.tabWidget.setTabText(n, c.name)
            newTree = QtWidgets.QTreeWidget(newTab)
            newTree.setGeometry(QtCore.QRect(0, 0, 731, 751))
            newTree.setAllColumnsShowFocus(True)
            newTree.setWordWrap(True)
            newTree.headerItem().setText(0, "1")
            newTree.setColumnCount(len(c.fieldOrder))
            newGridLayout.addWidget(newTree, 0, 0, 1, 1)
            self.treeWidgets += [newTree]
        
        self.locked = False

    def resizeNameColumn(self):
        self.treeWidgets[self.currentTree].resizeColumnToContents(0)

    def fillTreeWidgets(self):
        """
        Fills all tree tabs by creating all nodes
        """

        # for each tree in the forest
        for n, c in enumerate(self.forest.children):
            self.treeWidgets[n].itemSelectionChanged.connect(self.itemSelectionChanged)
            self.treeWidgets[n].itemCollapsed.connect(self.resizeNameColumn)
            self.treeWidgets[n].itemExpanded.connect(self.resizeNameColumn)
            self.treeWidgets[n].setHeaderLabels([""] + c.fieldOrder)
            root = self.treeWidgets[n].invisibleRootItem()
            c.viewNode = root

            # add branch
            for b in c.children:
                parent = QNode(b, c.fieldOrder)
                root.addChild(parent)

            # init sorting
            self.treeWidgets[n].setSortingEnabled(True)
            self.treeWidgets[n].sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

            # expand name column so all names are readable
            self.treeWidgets[n].resizeColumnToContents(0)


    def _protectCells(self, row, columns):

        if not self.gridInitialised:
            nonEditFlags = QtCore.Qt.ItemFlag.NoItemFlags
            empties = []
            for i in columns:
                if not self.tableWidget.item(row, i):
                    empties.append(QtWidgets.QTableWidgetItem(""))
                    empties[-1].setFlags(nonEditFlags)
                    self.tableWidget.setItem(row, i, empties[-1])
                else:
                    self.tableWidget.item(row, i).setFlags(nonEditFlags)

    def itemSelectionChanged(self):

        if self.editMode == 'content':
            self.showContentInDataView(self.currentTree)
        elif self.editMode == 'tree':
            self.showTreeFieldInDataView(self.currentTree)

    def showContentInDataView(self, treeIndex):
        if not self.locked:
            
            self.locked = True

            # init
            selectedItems = self.treeWidgets[treeIndex].selectedItems()

            # we have something to write
            if selectedItems != []:

                qnode = selectedItems[0]
                
                # unselect previous item in all trees
                if self.currentItem is not None:
                    try:
                        self.currentItem.select(False)
                    except:
                        print("warning: Unselecting of {} didn't work".format(self.currentItem.name))
                        pass

                # select current item in all trees
                self.currentItem = qnode and (qnode.sourceNode and qnode.sourceNode.item or None) or None
                if self.currentItem is None:
                    self.tableWidget.clear()
                    self.gridInitialised = False
                    self.locked = False
                    return
                self.currentItem.select(True)
                
                # expand current item in current tree
                parent = qnode.parent()
                while parent is not None:
                    parent.setExpanded(True)
                    parent = parent.parent()
                
                # create non-edit flags
                nonEditFlags = QtCore.Qt.ItemFlag.NoItemFlags

                # go through all lines of the table
                n = 0

                # empty line
                self._protectCells(0, [0, 1, 2, 3, 4])
                n += 1

                # add name
                name = QtWidgets.QTableWidgetItem("")
                name.setFlags(nonEditFlags)
                value = QtWidgets.QTableWidgetItem(self.currentItem.name)
                font = name.font()
                font.setPointSize(self._dataFontPointSize + 3)
                value.setFont(font)
                font.setPointSize(self._dataFontPointSize)
                self.tableWidget.setItem(n, 1, name)
                self.tableWidget.setItem(n, 3, value)
                self._protectCells(n, [0, 2, 4])
                n += 1
                
                # empty line
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # add all parents in tree parent path
                for treeNumber, path in enumerate(self.currentItem.trees):
                    tree = self.forest.children[treeNumber]
                    name = QtWidgets.QTableWidgetItem(tree.name)
                    name.setFlags(nonEditFlags)
                    name.setTextAlignment(0x82)
                    self.tableWidget.setItem(n, 1, name)
                    buttonbox = QtWidgets.QDialogButtonBox()
                    if not len(path):
                        button = QtWidgets.QToolButton()
                        button.setFont(font)
                        button.setText("")
                        button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
                        button.setFixedWidth(button.sizeHint().height())
                        button.setFixedHeight(button.sizeHint().height())
                        button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)     # no down arrow is shown, menu pops up on click
                        button.setStyleSheet("::menu-indicator{ image: none; }")
                        button.setMenu(self.createParentMenu(treeNumber, self.forest))
                        buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)
                    elif len(path) == 1:
                        parent = tree.findNode(path).parent
                        button = QtWidgets.QToolButton()
                        button.setFont(font)
                        button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
                        # get square buttons of same size as text buttons for > buttons
                        button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
                        button.setStyleSheet("::menu-indicator{ image: none; }")
                        button.setFixedWidth(button.sizeHint().height())
                        button.setFixedHeight(button.sizeHint().height())
                        button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
                        button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)     # no down arrow is shown, menu pops up on click
                        button.setMenu(self.createParentMenu(treeNumber, parent))
                        buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)
                    else:
                        for p in range(1, len(path)):
                            parent = tree.findNode(path[0:p])
                            button = QtWidgets.QToolButton()
                            button.setFont(font)
                            button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
                            button.setText(parent.name)
                            button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
                            button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)     # no down arrow is shown, menu pops up on click
                            button.setStyleSheet("::menu-indicator{image:none;}")
                            button.setMenu(self.createParentMenu(treeNumber, parent.parent))
                            buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)
                        button = QtWidgets.QToolButton()
                        button.setFont(font)
                        button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
                        button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)     # get square buttons of same size as text buttons for > buttons
                        button.setStyleSheet("::menu-indicator{ image: none; }")
                        button.setFixedWidth(button.sizeHint().height())
                        button.setFixedHeight(button.sizeHint().height())
                        button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
                        button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)     # no down arrow is shown, menu pops up on click
                        button.setMenu(self.createParentMenu(treeNumber, parent))
                        buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)

                    self.tableWidget.setCellWidget(n, 3, buttonbox)
                    self._protectCells(n, [0, 2, 4])
                    n += 1
                    
                # empty line
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # add item fields
                for key in sorted(self.currentItem.fields):
                    name = QtWidgets.QTableWidgetItem(key)
                    name.setFlags(nonEditFlags)
                    name.setTextAlignment(0x82)
                    if self.currentItem.fields[key]['type'] in ('text', 'longtext'):
                        text = self.currentItem.fields[key]["content"]
                        text = text and str(text) or ""     # display "None" values as empty string
                        height = self.currentItem.fields[key]['type'] == 'text' and 10 or 25
                        widget = TextEdit(text, lambda row=n: self.tableWidgetCellChanged(row, 3), height)
                        widget.setFont(font)
                        self.tableWidget.setCellWidget(n, 3, widget)
                    elif self.currentItem.fields[key]['type'] == 'url':
                        value = self.currentItem.fields[key]["content"]
                        value = value and str(value) or ""  # display "None" values as empty string
                        widget = UrlWidget(value, lambda row=n: self.tableWidgetCellChanged(row, 3), font)
                        self.tableWidget.setCellWidget(n, 3, widget)
                    elif self.currentItem.fields[key]['type'] == 'timer':
                        value = self.currentItem.fields[key]["content"]
                        running_since = self.currentItem.fields[key]["running_since"]
                        widget = TimerWidget(value, running_since, lambda row=n: self.tableWidgetCellChanged(row, 3),
                                             font)
                        self.tableWidget.setCellWidget(n, 3, widget)
                    else:
                        value = self.currentItem.fields[key]["content"]
                        value = value and str(value) or ""     # display "None" values as empty string
                        value = QtWidgets.QTableWidgetItem(value)
                        self.tableWidget.setItem(n, 3, value)
                    self.tableWidget.setItem(n, 1, name)
                    self._protectCells(n, [0, 2, 4])
                    n += 1

            # an empty page, clear and initialise
            else:
                self.tableWidget.clear()
                self.gridInitialised = False
                n = 0

            # empty lines to fill the 23 lines in the main view
            if n < 23:
                for k in range(n, 23):
                    self._protectCells(k, [0, 1, 2, 3, 4])

            self.gridInitialised = True
            self.locked = False

    def showTreeFieldInDataView(self, treeIndex):
        """ Shows the content of the tree field indicated by the current column
        :param treeIndex: The ID of the tree
        :return: None
        """

        if not self.locked:
            self.locked = True

            # init
            self.currentColumn = self.treeWidgets[treeIndex].currentColumn()

            # we have something to write
            if self.currentColumn > 0:

                # create non-edit flags
                nonEditFlags = QtCore.Qt.ItemFlag.NoItemFlags

                # go through all lines of the table
                n = 0

                # empty line
                self._protectCells(0, [0, 1, 2, 3, 4])
                n += 1

                # find field
                fieldname = self.forest.children[treeIndex].fieldOrder[self.currentColumn-1]
                field = self.forest.children[treeIndex].fields[fieldname]

                # field name plus empty line
                name = QtWidgets.QTableWidgetItem("")
                name.setFlags(nonEditFlags)
                value = QtWidgets.QTableWidgetItem(fieldname)
                font = name.font()
                font.setPointSize(self._dataFontPointSize + 3)
                value.setFont(font)
                self.tableWidget.setItem(n, 1, name)
                self.tableWidget.setItem(n, 3, value)
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # field type plus empty line
                self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem("Type"))
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(field.fieldType))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # own fields, sibling fields, parent fields
                self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem("Own fields"))
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(str(field.ownFields)))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1
                self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem("Child fields"))
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(str(field.childFields)))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1
                self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem("Sibling fields"))
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(str(field.siblingFields)))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1
                self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem("Parent fields"))
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(str(field.parentFields)))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

            # an empty page, clear and initialise
            else:
                self.tableWidget.clear()
                self.gridInitialised = False
                n = 0

            # empty lines to fill the 23 lines in the main view
            if n < 23:
                for k in range(n, 23):
                    self._protectCells(k, [0, 1, 2, 3, 4])

            self.gridInitialised = True
            self.locked = False

    def showDataFieldsInDataView(self):
        """ Shows the content of the tree field indicated by the current column
        :param treeIndex: The ID of the tree
        :return: None
        """

        if not self.locked:
            self.locked = True

            # create non-edit flags
            nonEditFlags = QtCore.Qt.ItemFlag.NoItemFlags

            fields = self.forest.itemTypes.items[0].fields

            # go through all lines of the table
            n = 0

            # empty line
            self._protectCells(n, [0, 1, 2, 3, 4])
            n += 1

            # go through all fields
            for name, field in fields.items():

                # field name
                fieldName = QtWidgets.QTableWidgetItem("Name")
                fieldName.setFlags(nonEditFlags)
                fieldName.setTextAlignment(0x82)
                self.tableWidget.setItem(n, 1, fieldName)
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(name))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # field type
                fieldType = QtWidgets.QTableWidgetItem("Type")
                fieldType.setFlags(nonEditFlags)
                fieldType.setTextAlignment(0x82)
                self.tableWidget.setItem(n, 1, fieldType)
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(field['type']))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # field content
                fieldContent = QtWidgets.QTableWidgetItem("Default Content")
                fieldContent.setFlags(nonEditFlags)
                fieldContent.setTextAlignment(0x82)
                self.tableWidget.setItem(n, 1, fieldContent)
                self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem(field['content']))
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

                # empty line
                self._protectCells(n, [0, 1, 2, 3, 4])
                n += 1

            # empty lines to fill the 23 lines in the main view
            if n < 23:
                for k in range(n, 23):
                    self._protectCells(k, [0, 1, 2, 3, 4])

            self.gridInitialised = True
            self.locked = False

    def createParentMenu(self, treeIndex, parent):
        """
        Displays a menu with possible children to select, at the current mouse cursor position.
        """
        menu = QtWidgets.QMenu()

        # root node
        if not parent.parent:
            action = QtGui.QAction("Add to Top Level", menu)
            action.triggered.connect(lambda checked, t=treeIndex,
                                            p=self.forest.children[treeIndex]: self.moveCurrentItemToNewParent(t, p))
            menu.addAction(action)
            parent = self.forest.children[treeIndex]
            menu.addSeparator()

        # top level node only
        else:
            if not parent.parent.parent:
                action = QtGui.QAction("Remove from Tree", menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=False: self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)
                action = QtGui.QAction("Add to Top Level", menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=self.forest.children[treeIndex]:
                                         self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)
                parent = self.forest.children[treeIndex]
                menu.addSeparator()

        # all other nodes
        currentNode = self.currentItem.viewNodes[treeIndex]
        for c in sorted(parent.children, key=lambda x: x.name):
            if c != currentNode:
                action = QtGui.QAction(c.name, menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=c: self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)

        return menu

    def tabWidgetCurrentChanged(self, tree):
        '''Called when the user selects another tree in the tab widget.
        '''

        self.currentTree = tree
        self.itemSelectionChanged()

    def tableWidgetCellChanged(self, row, column):
        """
        Called when the user wants to change the item name, field content or parent via the grid
        """

        if not self.locked:
            self.locked = True
            if column == 3:
                
                # the node name has been changed
                if row == 1:
                    newName = self.tableWidget.item(row, column).text()
                    self.currentItem.changeName(newName)
                
                # one of the fields has been changed
                else:
                    fieldName = self.tableWidget.item(row, 1).text()
                    fieldType = self.currentItem.fields[fieldName]['type']
                    if fieldType in ('longtext', 'text', 'url'):
                        newValue = self.tableWidget.cellWidget(row, 3).toPlainText()
                    elif fieldType == 'timer':
                        newValue = (self.tableWidget.cellWidget(row, 3).toPlainText(),
                                    self.tableWidget.cellWidget(row, 3).runningSince())
                    else:
                        newValue = self.tableWidget.item(row, 3).text()
                    result = self.currentItem.changeFieldContent(fieldName, newValue)
                    if result is not True:
                        message = "Couldn't update field content.\n" + str(result)
                        result = QtWidgets.QMessageBox.warning(self, message)

                    # add/remove timer to list
                    if fieldType == 'timer':
                        self.adjustAutoUpdate(self.currentItem, fieldName)

            self.locked = False
            self.delayedWriteToFile()

    def adjustAutoUpdate(self, item, fieldName):
        """ Adds or removes a timer to the list of fields to auto-update.
        """
        if item.fields[fieldName]['type'] == 'timer':
            # if timer is running, add it to the list
            if item.fields[fieldName]['running_since']:
                if (item, fieldName) not in self.auto_updates:
                    self.auto_updates.append((item, fieldName))

            # if timer is stopped, remove it from the list
            else:
                if (item, fieldName) in self.auto_updates:
                    del self.auto_updates[self.auto_updates.index((item, fieldName))]

    def initAllAutoUpdates(self):
        """
        Initialise all auto-update fields after loading.
        """
        for i in self.forest.itemPool.items:
            for f in i.fields:
                    self.adjustAutoUpdate(i, f)

    def updateTimers(self):
        # update all timers that are running
        for item, fieldName in self.auto_updates:
            result = item.changeFieldContent(fieldName, [True])
        # remove timers that are problematic

    def createNode(self, insertas, copy, recurse = False, srcItem = None, destItem = None):
        
        treeWidget = self.treeWidgets[self.currentTree]

        # set source and destination nodes and qnodes
        if recurse and srcItem is not None and destItem is not None:
            sourceItem = srcItem
            sourceNode = srcItem.viewNodes[self.currentTree]
            sourceQNode = sourceNode.viewNode
            destNode = destItem.viewNodes[self.currentTree]
            destQNode = destNode.viewNode
        elif len(treeWidget.selectedItems()):
            sourceQNode = treeWidget.selectedItems()[0]
            sourceNode = sourceQNode.sourceNode
            sourceItem = sourceNode.item
            destNode = sourceNode.parent
            destQNode = sourceQNode.parent()
        else:
            sourceQNode = treeWidget.invisibleRootItem()
            sourceNode = self.forest.children[self.currentTree]
            sourceItem = sourceNode.item
            destQNode = sourceQNode
            destNode = sourceNode
            insertas = 'root'

        if destQNode is None:
            destQNode = treeWidget.invisibleRootItem()

        if copy:
            item = self.forest.itemPool.copyItem(sourceItem)
            for n,t in enumerate(self.forest.children):
                if n != self.currentTree and item.trees[n] != []:
                    oldNode = t.findNode(item.trees[n])
                    newNode = oldNode.parent.addItemAsChild(item)
                    newQNode = QNode(newNode, self.forest.children[n].fieldOrder)
                    parent = oldNode.viewNode.parent()
                    if parent is None:
                        parent = self.treeWidgets[n].invisibleRootItem()
                    parent.addChild(newQNode)
        else:
            # add new item by copying the first type
            item = self.forest.itemPool.copyItem(self.forest.itemTypes.items[0])

        if insertas == "root":

            # create default node and add item to it
            node = sourceNode.addItemAsChild(item)
            qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
            sourceQNode.addChild(qnode)

            # expand new entry
            qnode.setExpanded(True)

        if insertas == "child":

            # create default node and add item to it
            node = sourceNode.addItemAsChild(item)
            qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
            sourceQNode.addChild(qnode)

            # expand parent and select new item
            sourceQNode.setExpanded(True)

        elif insertas == "sibling":

            if destNode is None or destQNode is None:
                return

            # create default node and add item to it
            node = destNode.addItemAsChild(item)
            qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
            destQNode.addChild(qnode)

            # expand parent and select new item
            destQNode.setExpanded(True)

        elif insertas == "parent":

            if destNode is None or destQNode is None:
                return

            node = destNode.addItemAsChild(item)

            # move original node to be child of new parent
            destNode.removeChild(sourceNode)
            node.addNodeAsChild(sourceNode)
            destQNode.removeChild(sourceQNode)
            qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
            destQNode.addChild(qnode)

            # expand parent and select new item
            qnode.setExpanded(True)

        if recurse:
            for c in sourceNode.children:
                self.createNode(insertas, copy, recurse, c.item, node.item)

        if srcItem is None:
            treeWidget.setCurrentItem(qnode)
            self.delayedWriteToFile()
    
    def moveCurrentItemToNewParent(self, treeIndex, newParent):
        treeWidget = self.treeWidgets[self.currentTree]
        if len(treeWidget.selectedItems()):

            self.locked = True

            # save current item
            item = self.currentItem

            # error message if recursion is tried
            if newParent and (newParent.item == item):
                message = "You are trying to set\n" + item.name + "\nto be its own parent. This is not supported."
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(message)
                msgBox.setWindowTitle("TreeTime Message")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                return msgBox.exec()

            # find old parent
            oldParent = item.viewNodes[treeIndex]
            disappeared = False

            # either remove node from tree
            if oldParent and not newParent:

                # question to user: Really remove?
                message = "Removing node \"" + item.name + "\" from the tree \"" \
                          + self.forest.children[self.currentTree].name +"\".\n\n" \
                          "This will remove all descendants (children, grandchildren, ...). " \
                          "Changes are saved to file immediately and cannot be reverted.\nProceed?"
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(message)
                msgBox.setWindowTitle("TreeTime Message")
                msgBox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
                result = msgBox.exec()

                # remove if the user has confirmed
                if result == QtWidgets.QMessageBox.StandardButton.Ok:

                    # recursive function to collect all child nodes in the trees
                    def collect_children(item, item_list, tree):
                        if item not in item_list:
                            item_list += [item]
                            node = item.viewNodes[tree]
                            if node:
                                for child in node.children:
                                    collect_children(child.item, item_list, tree)

                    # find unique list of children to remove, and remove them
                    to_remove = []
                    collect_children(self.currentItem, to_remove, treeIndex)
                    for i in to_remove:

                        # remove single item
                        i.removeFromTree(treeIndex)

                        # delete if orphaned
                        if not sum([len(t) for t in i.trees]):
                            self.forest.itemPool.deleteItem(i)

                    if treeIndex == self.currentTree:
                        disappeared = True     # remember that we've removed a node from the current tree
                else:
                    return

            # or move node within the tree
            elif oldParent and newParent and newParent.item:
                item.moveInTree(treeIndex, newParent.item.trees[treeIndex])
            elif oldParent and newParent and not newParent.item:
                item.moveInTree(treeIndex, [])

            # or add node to tree
            elif not oldParent and newParent:
                tree = self.forest.children[treeIndex]
                node = newParent.addItemAsChild(item)
                newQNode = QNode(node, tree.fieldOrder)
                newParent.viewNode.addChild(newQNode)
            
            # save change
            item.notifyFieldChange('')

            # select new item after moving, if it is still part of the current tree
            if not disappeared:
                treeWidget.setCurrentItem(item.viewNodes[self.currentTree].viewNode)

            # clear table widget to prevent segfault crash in qt lib
            self.locked = False
            self.gridInitialised = False
            self.tableWidget.clear()

            # update table and write to file
            self.itemSelectionChanged()
            self.delayedWriteToFile()


class TreeTime:
    
    def __init__(self, filename=None):
        
        app = QtWidgets.QApplication(sys.argv)
        if platform.system() == "Windows":
            app.setStyle("Fusion")

        # start main window
        main_window = TreeTimeWindow(filename=filename)

        # add application icon; test several options, different deploy methods are doing different things with the
        # resources, unfortunately
        logo = ApplicationLogo()
        main_window.setWindowIcon(logo.icon)

        # run
        main_window.show()
        sys.exit(app.exec())


class ApplicationLogo:

    _data = ("iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAMAAABrrFhUAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9"
             "kT1Iw0AcxV8/pCKVDnaQ4pChCopdVMRRq1CECqFWaNXB5NIvaNKQpLg4Cq4FBz8Wqw4uzro6uAqC"
             "4AeIq4uToouU+L+k0CLGg+N+vLv3uHsH+JtVpprBWUDVLCOTSgq5/KoQekUQMUQwhlGJmfqcKKbh"
             "Ob7u4ePrXYJneZ/7c/QrBZMBPoF4lumGRbxBPL1p6Zz3iaOsLCnE58TjBl2Q+JHrsstvnEsO+3lm"
             "1Mhm5omjxEKpi+UuZmVDJZ4ijiuqRvn+nMsK5y3OarXO2vfkLwwXtJVlrtMcQgqLWIIIATLqqKAK"
             "CwlaNVJMZGg/6eGPOX6RXDK5KmDkWEANKiTHD/4Hv7s1i5MTblI4CfS82PbHMBDaBVoN2/4+tu3W"
             "CRB4Bq60jr/WBGY+SW90tPgRENkGLq47mrwHXO4Ag0+6ZEiOFKDpLxaB9zP6pjwwcAv0rbm9tfdx"
             "+gBkqav0DXBwCIyUKHvd49293b39e6bd3w/a8HLQYu1JmQAAAwBQTFRFfwAAgQIAgwQBhAYDhQgE"
             "hQkMiA4OixIQgxUMhhgOhhgUiRwWih0cjB4YhiIcjSAfjyEaiCQdkCMhiiYfiiYkkiYjii0mii4s"
             "kS0pjDAtjTEulDAsizYvkjUyjDc1mTQvjTg2jjk3mzYxkDoznDc3kDs4jj85mTw3j0A6j0FAnD45"
             "l0E+kUNCkEdDokM+o0VFlExMoElFm0tEkVBNl09PmlBMpU5JqFBMlFhTqlJTlFlZm1hWlltbqVhV"
             "mV1dlV9dl2Ffp11crlxZmWNhsV9comVfmGhjrmJdo2ZmmWpqoWtom21trmlmmXButGlom3JwoHFx"
             "p3BtnXRytG5rnnVzm3l1p3ZwsnR0p3h4nnx3u3Vxnn1+s3t4unp0nYKBpIF9qYB+n4SDpoWGoYeG"
             "pImIwYKBvISAoIyJw4SDuIiIo4+LpZCNr42Oo5GTtoyKwomGrJGQxIuHvo2NqZSRopaXx46KspaV"
             "ppqauJWWypGNo56dr5uYqZ2eyJWPwpeUpaCfyJeXv5ydqKOiy5mZwp6Zq6alzpybvqKhp6mm0J6e"
             "uKWns6enxqKdrqmoqauoqqypq62qzqOgtqqqyKWmrK6rra+s0aWiua2urrGtr7Kux6uq1KimsLOv"
             "sbSws7Wy16ypzLCvtbe0tri1wbW2t7m2uLq317Ktubu4zLe02bSvu726xrq62LW207e2vL67wr27"
             "w768vcC83Li5wMK/2Ly71L6737u84Ly9w8XC1MDD3L++z8PExcfE3sHAxsnGyMrH08fH4cTDz8rI"
             "yczIzM7L5MfG0s3M2MzMzdDMztHO58rJ0NLP0dPQ487K19LQ0tTR3dHR09bS1dfU6NLO4NTU29bU"
             "1tnV6NTX3djW2NrX69XR7dbT2t3a493c3d/c8NrW3uDd6d3d3+He4OPg7ODg4uXh4+bi8OPj5efk"
             "5+nm8+bm6Orn6evo6u3q9+rr7O/r7vDt9O/u8PLv8fTw+PPx9Pbz+vXz9fj0/Pf29vn2/vn4+fv4"
             "+/36//z6/P/7////RZ/1PwAAAAF0Uk5TAEDm2GYAAAABYktHRACIBR1IAAAACXBIWXMAAA9hAAAP"
             "YQGoP6dpAAAAB3RJTUUH5wQaDzUmdtGQ1wAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lN"
             "UFeBDhcAABB3SURBVHja7Z17cBXVHcezExLShIcgSIlAARUBxUrrk6JRo7RAAy1CWwRT8QUMptSK"
             "RWwVDdWe0vYmSi6dVCYoJgRT3HZCeShhIp1QMiYYEzRthhSWTG7MJRlv4BLicONOz9m9z3Dv7jnZ"
             "H2d3b/j+m5vd/X727OM8vvtLSNCWbF8lGJdsdw1s98YYhG1CsK/6jSAu3IcY9Nu+EB9iRBBv9lkR"
             "xKF9FQGbfyH+JA9s+3QI4tu/PoF4969HIO7tEw10/1oEePtPnZG5aMWanJw12QszpqWZT4Cv/2EZ"
             "a1CE1s8ZZS4Brv4nZaMoWjPVRAI8bwCjVgQsO8XK6rrGpqbGuuqKMidCK9PNBcDHf8ZrqvvCikYp"
             "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"
             "RVekrf8DQpnvQNJVVVIAAAAASUVORK5CYII=")

    def __init__(self):
        self._buffer = base64.b64decode(self._data)
        self._pixmap = QtGui.QPixmap()
        self._pixmap.loadFromData(self._buffer, format='png')
        self.icon = QIcon(self._pixmap)
