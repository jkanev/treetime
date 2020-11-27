#
# Tis file is part of TreeTime, a tree editor and data analyser
#
# Copyright (C) GPLv3, 2015, Jacob Kanev
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
from .item import *
from .tree import *
from .mainwindow import *
import datetime
import os.path
import platform
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from threading import Timer
from PyQt5.QtGui import QPalette, QColor


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

    def __init__(self, url, callback, parent=None):
        """
        Initialise
        """

        # init
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.url = url
        self.callback = callback

        # create line edit control and open button
        linewidget = QtWidgets.QLineEdit(url)
        linewidget.textChanged.connect(self.textChanged)
        openbutton = QtWidgets.QPushButton("Open")
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
    Special custom widget class for URL fields
    """


    def __init__(self, text, callback, parent=None):
        """
        Initialise
        """

        # init
        QtWidgets.QPlainTextEdit.__init__(self, text, parent=parent)
        self.callback = callback
        self.has_changed = False
        self.textChanged.connect(self.notifyChange)

    def notifyChange(self):
        self.has_changed = True

    def focusOutEvent(self, e: QtGui.QFocusEvent):
        """
        Callback, to save the new text and notify the parent that the text has changed
        """
        if self.has_changed:
            self.has_changed = False
            self.callback()
        super().focusOutEvent(e)

    def leaveEvent(self, e: QtCore.QEvent):
        """
        Callback, to save the new text and notify the parent that the text has changed
        """
        if self.has_changed:
            self.has_changed = False
            self.callback()
        super().leaveEvent(e)


class TimerWidget(QtWidgets.QWidget):
    """
    A widget displaying an hour timer - a time display (hours:minutes:seconds)
    and a button "start"/"stop"
    """

    timer = None

    def __init__(self, partial, running_since, callback, parent=None):
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
        self.linewidget.textEdited.connect(self.textEdited)
        self.startstopbutton = QtWidgets.QPushButton(buttontext)
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


class TreeTimeWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Implements the main part of the GUI.
    """

    def __init__(self, filename=None):
        """
        Initialise the application, connect all button signals to application functions, load theme and last file
        """

        # initialise main window
        super().__init__()
        self.setupUi(self)

        # connect all button signals
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
        self.pushButtonExportBranchTxt.clicked.connect(self.pushButtonExportBranchTxtClicked)
        self.pushButtonExportTreeTxt.clicked.connect(self.pushButtonExportTreeTxtClicked)
        self.pushButtonRemove.clicked.connect(lambda: self.moveCurrentItemToNewParent(self.currentTree, None))
        self.pushButtonDelete.clicked.connect(self.pushButtonDeleteClicked)
        self.tableWidget.cellChanged.connect(self.tableWidgetCellChanged)
        self.tableWidget.verticalHeader().setSectionResizeMode(3)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, 2)     # column 0: fixed
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, 2)     # column 1: fixed, 100
        self.tableWidget.horizontalHeader().resizeSection(1, 100)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, 2)     # column 2: fixed
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, 1)     # column 3: stretch
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, 2)     # column 4: fixed
        self.tabWidget.currentChanged.connect(self.tabWidgetCurrentChanged)
        self.write_delay = 0
        self.write_timer = False
        self.locked = True

        # init application settings
        self.settings = QtCore.QSettings('FreeSoftware', 'TreeTime')

        # init themes and set last theme
        self.system_palette = self.palette()
        self.fillThemeBox()
        self.fillColourBox()
        self.cboxThemeTextChanged()
        self.cboxColoursTextChanged()
        self.cboxTheme.currentTextChanged.connect(self.cboxThemeTextChanged)
        self.cboxColours.currentTextChanged.connect(self.cboxColoursTextChanged)

        # load last file
        lastFile = self.settings.value('lastFile')
        if lastFile:
            self.loadFile(lastFile)
            self.setWindowTitle("TreeTime - " + lastFile)
            self.settings.setValue('fileDir', os.path.dirname(lastFile))
            self.settings.setValue('lastFile', lastFile)
            self.labelCurrentFile.setText(lastFile)
        else:
            self.pushButtonLoadFileClicked()

        # show window
        self.showMaximized()

    def closeEvent(self, event):
        """
        Do some cleanup before you close the window
        """

        # Write state to file
        if self.write_timer:
            self.write_timer.cancel()
        self.write_delay = 0
        self.writeToFile()

        # cancel all running stop watches
        # \todo

        # continue closing the window
        event.accept()  # let the window close

    def fillThemeBox(self):
        """
        Fills the theme selection box with all themes the system is capable of
        """
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
        application.setStyle(QtWidgets.QStyleFactory.create(style))

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
            palette.setColor(QPalette.Window, QColor(50, 52, 54))
            palette.setColor(QPalette.WindowText, QtCore.Qt.white)
            palette.setColor(QPalette.Base, QColor(40, 42, 44))
            palette.setColor(QPalette.AlternateBase, QColor(50, 52, 54))
            palette.setColor(QPalette.ToolTipBase, QtCore.Qt.black)
            palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
            palette.setColor(QPalette.Text, QtCore.Qt.white)
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(150, 150, 150))
            palette.setColor(QPalette.Button, QColor(60, 62, 64))
            palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
            palette.setColor(QPalette.BrightText, QtCore.Qt.red)
            palette.setColor(QPalette.Link, QColor(60, 200, 255))
            palette.setColor(QPalette.Highlight, QColor(60, 200, 255))
            palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)

        # apply light colours
        elif colour == "Light":
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(255-53, 255-53, 255-53))
            palette.setColor(QPalette.WindowText, QtCore.Qt.black)
            palette.setColor(QPalette.Base, QColor(255-25, 255-25, 255-25))
            palette.setColor(QPalette.AlternateBase, QColor(255-53, 255-53, 255-53))
            palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
            palette.setColor(QPalette.ToolTipText, QtCore.Qt.black)
            palette.setColor(QPalette.Text, QtCore.Qt.black)
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(70, 70, 70))
            palette.setColor(QPalette.Button, QColor(255-53, 255-53, 255-53))
            palette.setColor(QPalette.ButtonText, QtCore.Qt.black)
            palette.setColor(QPalette.BrightText, QtCore.Qt.blue)
            palette.setColor(QPalette.Link, QColor(255-42, 255-130, 255-218))
            palette.setColor(QPalette.Highlight, QColor(255-42, 255-130, 255-218))
            palette.setColor(QPalette.HighlightedText, QtCore.Qt.white)

        # apply system colours
        elif colour == "System":
            palette = self.system_palette

        application.setPalette(palette)

    def pushButtonSaveToFileClicked(self):
        """
        Callback for the save-file button. Saves the current data to a new file and keeps that file connected.
        """
        fileDir = self.settings.value('fileDir') or ''
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Save new Data File", fileDir, '*.trt')[0]
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

    def pushButtonExportBranchTxtClicked(self):
        """
        Callback for the txt export. Asks for a file name, then writes branch text export into it.
        """
        if self.currentItem:
            fileDir = self.settings.value('fileDir') or ''
            file = QtWidgets.QFileDialog.getSaveFileName(self, "Export to Plain Text", fileDir, '*.txt')[0]
            if file != '':
                with open(file, "w") as f:
                    currentNode = self.currentItem.viewNodes[self.currentTree]
                    txt = currentNode.to_txt()
                    f.write(txt)

    def pushButtonExportTreeTxtClicked(self):
        """
        Callback for the txt export. Asks for a file name, then writes branch text export into it.
        """
        if self.currentItem:
            fileDir = self.settings.value('fileDir') or ''
            file = QtWidgets.QFileDialog.getSaveFileName(self, "Export to Plain Text", fileDir, '*.txt')[0]
            if file != '':
                with open(file, "w") as f:
                    rootNode = self.forest.children[self.currentTree]
                    children = sorted(rootNode.children, key=lambda a: a.name)
                    for c in children:
                        f.write('\n')
                        f.write(c.to_txt())
                        f.write('\n')

    def pushButtonNewFromTemplateClicked(self):
        """
        Callback for the new-from-template button. Loads new file and immediately saves it to a different file.
        """

        # First load template file
        templateDir = self.settings.value('templateDir') or ''
        template = QtWidgets.QFileDialog.getOpenFileName(self, "Load Template", templateDir, '*.trt')[0]
        if template != '':
            self.loadFile(template)
            self.settings.setValue('templateDir', os.path.dirname(template))

            # Then save as new file
            self.pushButtonSaveToFileClicked()

    def pushButtonDeleteClicked(self):
        message = "Deleting node \"" + self.currentItem.name + "\". \n\n" \
                  "This will remove all descendents (children, grandchildren, ...) from the tree \"" \
                  + self.forest.children[self.currentTree].name +"\".\n" \
                  "Changes are saved to file immediately and cannot be reverted."
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            self.forest.itemPool.deleteItem(self.currentItem)
            self.delayedWriteToFile()
        
    def loadFile(self, filename):
        self.removeBranchTabs()
        self.tabWidgets = []
        self.treeWidgets = []
        self.currentTree = 0
        self.currentItem = None
        self.gridInitialised = False
        if filename is not None and filename != '':
            try:
                # load file
                self.forest = Forest(filename)
                self.createBranchTabs()
                self.fillTreeWidgets()

                # select first item
                if len(self.treeWidgets):
                    firstTree = self.treeWidgets[0]
                    items = firstTree.topLevelItemCount()
                    if items:
                        firstTree.topLevelItem(0).setSelected(True)

            # in case of failure, show user message and reload
            except KeyError as e:
                msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", str(e))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                result = msgBox.exec_()
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

    def fillTreeWidgets(self):
        """
        Fills all tree tabs by creating all nodes
        """

        # for each tree in the forest
        for n, c in enumerate(self.forest.children):
            self.treeWidgets[n].itemSelectionChanged.connect(lambda x=n: self.treeSelectionChanged(x))
            self.treeWidgets[n].setHeaderLabels([""] + c.fieldOrder)
            root = self.treeWidgets[n].invisibleRootItem()
            c.viewNode = root

            # add branch
            for b in c.children:
                parent = QNode(b, c.fieldOrder)
                root.addChild(parent)
            # expand name column so all names are readable
            self.treeWidgets[n].resizeColumnToContents(0)

            # init sorting
            self.treeWidgets[n].setSortingEnabled(True)
            self.treeWidgets[n].sortItems(0, QtCore.Qt.AscendingOrder)

    def _protectCells(self, row, columns):

        if not self.gridInitialised:
            nonEditFlags = QtCore.Qt.ItemFlags()
            empties = []
            for i in columns:
                if not self.tableWidget.item(row, i):
                    empties.append(QtWidgets.QTableWidgetItem(""))
                    empties[-1].setFlags(nonEditFlags)
                    self.tableWidget.setItem(row, i, empties[-1])
                else:
                    self.tableWidget.item(row, i).setFlags(nonEditFlags)

    def treeSelectionChanged(self, treeIndex):
        
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
                self.currentItem = qnode.sourceNode.item
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
                nonEditFlags = QtCore.Qt.ItemFlags()

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
                font.setPointSize(font.pointSize() + 3)
                value.setFont(font)
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
                        button.setText("+")
                        button.setToolButtonStyle(1)  # 1 - text only
                        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)     # no down arrow is shown, menu pops up on click
                        button.setMenu(self.createParentMenu(treeNumber, self.forest))
                        buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)
                    elif len(path) == 1:
                        parent = tree.findNode(path).parent
                        button = QtWidgets.QToolButton()
                        button.setArrowType(4)     # 4 - rightarrow
                        button.setToolButtonStyle(0)     # 0 - icon only
                        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)     # no down arrow is shown, menu pops up on click
                        button.setMenu(self.createParentMenu(treeNumber, parent))
                        buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)
                    else:
                        for p in range(1, len(path)):
                            parent = tree.findNode(path[0:p])
                            button = QtWidgets.QToolButton()
                            button.setArrowType(4)     # 4 - rightarrow
                            button.setText(parent.name)
                            button.setToolButtonStyle(1)     # 2 - text beside icon
                            button.setPopupMode(QtWidgets.QToolButton.InstantPopup)     # no down arrow is shown, menu pops up on click
                            button.setMenu(self.createParentMenu(treeNumber, parent.parent))
                            buttonbox.addButton(button, QtWidgets.QDialogButtonBox.ButtonRole.ResetRole)
                        button = QtWidgets.QToolButton()
                        button.setArrowType(4)     # 4 - rightarrow
                        button.setToolButtonStyle(0)     # 0 - icon only
                        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)     # no down arrow is shown, menu pops up on click
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
                    if self.currentItem.fields[key]['type'] == 'text':
                        text = self.currentItem.fields[key]["content"]
                        text = text and str(text) or ""     # display "None" values as empty string
                        widget = TextEdit(text, lambda row=n: self.tableWidgetCellChanged(row, 3))
                        self.tableWidget.setCellWidget(n, 3, widget)
                    elif self.currentItem.fields[key]['type'] == 'url':
                        value = self.currentItem.fields[key]["content"]
                        value = value and str(value) or ""  # display "None" values as empty string
                        widget = UrlWidget(value, lambda row=n: self.tableWidgetCellChanged(row, 3))
                        self.tableWidget.setCellWidget(n, 3, widget)
                    elif self.currentItem.fields[key]['type'] == 'timer':
                        value = self.currentItem.fields[key]["content"]
                        running_since = self.currentItem.fields[key]["running_since"]
                        widget = TimerWidget(value, running_since, lambda row=n: self.tableWidgetCellChanged(row, 3))
                        self.tableWidget.setCellWidget(n, 3, widget)
                    else:
                        value = self.currentItem.fields[key]["content"]
                        value = value and str(value) or ""     # display "None" values as empty string
                        value = QtWidgets.QTableWidgetItem(value)
                        self.tableWidget.setItem(n, 3, value)
                    self.tableWidget.setItem(n, 1, name)
                    self._protectCells(n, [0, 2, 4])
                    n += 1

            # an empty page, clear an initialise
            else:
                self.tableWidget.clear()
                self.gridInitialised = False
                n = 0

            # empty lines to fill the 20 lines in the main view
            if n < 20:
                for k in range(n, 20):
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
            action = QtWidgets.QAction("Add to Top Level", menu)
            action.triggered.connect(lambda checked, t=treeIndex,
                                            p=self.forest.children[treeIndex]: self.moveCurrentItemToNewParent(t, p))
            menu.addAction(action)
            parent = self.forest.children[treeIndex]
            menu.addSeparator()

        # top level node only
        else:
            if not parent.parent.parent:
                action = QtWidgets.QAction("Remove from Tree", menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=False: self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)
                action = QtWidgets.QAction("Add to Top Level", menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=self.forest.children[treeIndex]:
                                         self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)
                parent = self.forest.children[treeIndex]
                menu.addSeparator()

        # all other nodes
        currentNode = self.currentItem.viewNodes[treeIndex]
        for c in sorted(parent.children, key=lambda x: x.name):
            if c != currentNode:
                action = QtWidgets.QAction(c.name, menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=c: self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)

        return menu

    def tabWidgetCurrentChanged(self, tree):
        '''Called when the user selects another tree in the tab widget.
        '''

        self.currentTree = tree
        self.treeSelectionChanged(tree)

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
                    if fieldType in ('text', 'url'):
                        newValue = self.tableWidget.cellWidget(row, 3).toPlainText()
                    elif fieldType == 'timer':
                        newValue = (self.tableWidget.cellWidget(row, 3).toPlainText(),
                                    self.tableWidget.cellWidget(row, 3).runningSince())
                    else:
                        newValue = self.tableWidget.item(row, 3).text()
                    result = self.currentItem.changeFieldContent(fieldName, newValue)
                    if result is not True:
                        message = "Couldn't update field content.\n" + str(result)
                        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                        msgBox.exec_()
                
            self.locked = False
            self.delayedWriteToFile()

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
                msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel);
                return msgBox.exec_()

            # find old parent
            oldParent = item.viewNodes[treeIndex]
            disappeared = False

            # either remove node from tree
            if oldParent and not newParent:

                # question to user: Really remove?
                message = "Removing node \"" + item.name + "\" from the tree \"" \
                          + self.forest.children[self.currentTree].name +"\".\n\n" \
                          "This will remove all descendents (children, grandchildren, ...). " \
                          "Changes are saved to file immediately and cannot be reverted."
                msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                result = msgBox.exec_()
                
                # remove if user has confirmed
                if result == QtWidgets.QMessageBox.Ok:
                    item.removeFromTree(treeIndex)
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
            self.treeSelectionChanged(self.currentTree)
            self.delayedWriteToFile()


class TreeTime:
    
    def __init__(self):
        
        app = QtWidgets.QApplication(sys.argv)
        if platform.system() == "Windows":
            app.setStyle("Fusion")
        mainWindow = TreeTimeWindow()
        mainWindow.show()
        sys.exit(app.exec_())

