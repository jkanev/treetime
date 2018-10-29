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

sys.setrecursionlimit(50)

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



class TreeTimeWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Implements the main part of the GUI.
    """

    def __init__(self, filename=None):
        super().__init__()
        self.setupUi(self)
        self.pushButtonNewChild.clicked.connect(lambda: self.createNode("child", False))
        self.pushButtonNewSibling.clicked.connect(lambda: self.createNode("sibling", False))
        self.pushButtonNewParent.clicked.connect(lambda: self.createNode("parent", False))
        self.pushButtonCopyNodeChild.clicked.connect(lambda: self.createNode("child", True))
        self.pushButtonCopyNodeSibling.clicked.connect(lambda: self.createNode("sibling", True))
        self.pushButtonCopyNodeParent.clicked.connect(lambda: self.createNode("parent", True))
        self.pushButtonCopyBranchSibling.clicked.connect(lambda: self.createNode("sibling", True, True))
        self.pushButtonLoadFile.clicked.connect(self.pushButtonLoadFileClicked)
        self.pushButtonSaveToFile.clicked.connect(self.pushButtonSaveToFileClicked)
        self.pushButtonRemove.clicked.connect(lambda: self.moveCurrentItemToNewParent(self.currentTree, None))
        self.pushButtonDelete.clicked.connect(self.pushButtonDeleteClicked)
        self.tableWidget.cellChanged.connect(self.tableWidgetCellChanged)
        self.tableWidget.verticalHeader().setSectionResizeMode(3)
        self.tabWidget.currentChanged.connect(self.tabWidgetCurrentChanged)
        self.locked = True
        self.settings = QtCore.QSettings('FreeSoftware', 'TreeTime')
        self.loadFile(filename or self.settings.value('lastFile'))
        self.showMaximized()

    def pushButtonSaveToFileClicked(self):
        result = QtWidgets.QFileDialog.getSaveFileName(self, "Save data file", '', '*.trt')[0]
        if result != '':
            self.labelCurrentFile.setText(result)
            self.writeToFile()

    def pushButtonLoadFileClicked(self):
        result = QtWidgets.QFileDialog.getOpenFileName(self, "Load data file", '', '*.trt')[0]
        if result != '':
            self.loadFile( result )

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
            self.writeToFile()
        
    def loadFile(self, filename):
        self.removeBranchTabs()
        self.tabWidgets = []
        self.treeWidgets = []
        self.currentTree = 0
        self.currentItem = None
        if filename is not None and filename != '':
            try:
                self.forest = Forest(filename)
                self.createBranchTabs()
                self.fillTreeWidgets()
                self.labelCurrentFile.setText(filename)
                self.settings.setValue('lastFile', filename)
                # select first item
                if len(self.treeWidgets):
                    firstTree = self.treeWidgets[0]
                    items = firstTree.topLevelItemCount()
                    if items:
                        firstTree.topLevelItem(items - 1).setSelected(True)
            except:
                self.pushButtonLoadFileClicked()
        else:
            self.pushButtonLoadFileClicked()
    
    def writeToFile(self):
        self.forest.writeToFile( self.labelCurrentFile.text() )
    
    
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
            newTree.setSortingEnabled(True)
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


    def treeSelectionChanged(self, treeIndex):
        
        if not self.locked:
            
            self.locked = True

            # init
            self.tableWidget.clear()
            selectedItems = self.treeWidgets[treeIndex].selectedItems()
            
            if selectedItems != []:
                
                qnode = selectedItems[0]
                
                # unselect previous item in all trees
                if self.currentItem is not None:
                    self.currentItem.select(False)
                
                # select current item in all trees
                self.currentItem = qnode.sourceNode.item
                if self.currentItem is None:
                    return
                self.currentItem.select(True)
                
                # expand current item in current tree
                parent = qnode.parent()
                while parent is not None:
                    parent.setExpanded(True)
                    parent = parent.parent()
                
                # create non-edit flags
                nonEditFlags = QtCore.Qt.ItemFlags()
                nonEditFlags != QtCore.Qt.ItemIsEnabled
                
                # go through all lines of the table
                n = 0

                # empty line
                empty0 = QtWidgets.QTableWidgetItem("")
                empty0.setFlags(nonEditFlags)
                empty1 = QtWidgets.QTableWidgetItem("")
                empty1.setFlags(nonEditFlags)
                self.tableWidget.setItem(n, 0, empty0)
                self.tableWidget.setItem(n, 1, empty1)
                n += 1

                # add name
                name = QtWidgets.QTableWidgetItem("")
                name.setFlags(nonEditFlags)
                value = QtWidgets.QTableWidgetItem(self.currentItem.name)
                font = name.font()
                font.setPointSize(font.pointSize() + 3)
                value.setFont(font)
                self.tableWidget.setItem(n, 0, name)
                self.tableWidget.setItem(n, 1, value)
                n += 1
                
                # empty line
                empty2 = QtWidgets.QTableWidgetItem("")
                empty2.setFlags(nonEditFlags)
                empty3 = QtWidgets.QTableWidgetItem("")
                empty3.setFlags(nonEditFlags)
                self.tableWidget.setItem(n, 0, empty2)
                self.tableWidget.setItem(n, 1, empty3)
                n += 1

                # add all parents in tree parent path
                for treeNumber, path in enumerate(self.currentItem.trees):
                    tree = self.forest.children[treeNumber]
                    name = QtWidgets.QTableWidgetItem(tree.name)
                    name.setFlags(nonEditFlags)
                    self.tableWidget.setItem(n, 0, name)
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

                    self.tableWidget.setCellWidget(n, 1, buttonbox)
                    n += 1
                    
                # empty line
                empty4 = QtWidgets.QTableWidgetItem("")
                empty4.setFlags(nonEditFlags)
                empty5 = QtWidgets.QTableWidgetItem("")
                empty5.setFlags(nonEditFlags)
                self.tableWidget.setItem(n, 0, empty4)
                self.tableWidget.setItem(n, 1, empty5)
                n += 1

                # add item fields
                for key in self.currentItem.fields:
                    name = QtWidgets.QTableWidgetItem(key)
                    name.setFlags(nonEditFlags)
                    if self.currentItem.fields[key]['type'] == 'text':
                        text = str(self.currentItem.fields[key]["content"])
                        widget = QtWidgets.QPlainTextEdit(text)
                        widget.textChanged.connect(lambda row=n: self.tableWidgetCellChanged(row, 1))
                        self.tableWidget.setCellWidget(n, 1, widget)
                    else:
                        value = self.currentItem.fields[key]["content"]
                        value = value and str(value) or ""     # display "None" values as empty string
                        value = QtWidgets.QTableWidgetItem(value)
                        self.tableWidget.setItem(n, 1, value)
                    self.tableWidget.setItem(n, 0, name)
                    n += 1
            
            self.locked = False
    
    
    def createParentMenu(self, treeIndex, parent):
        """
        Displays a menu with possible children to select, at the current mouse cursor position.
        """

        menu = QtWidgets.QMenu()

        # root node
        if not parent.parent:
            action = QtWidgets.QAction("Add to Top Level", menu)
            action.triggered.connect(lambda checked, t=treeIndex, p=self.forest.children[treeIndex]: self.moveCurrentItemToNewParent(t, p))
            menu.addAction(action)
            parent = self.forest.children[treeIndex]
            menu.addSeparator()

        # top level node only
        else:
            if not parent.parent.parent:
                action = QtWidgets.QAction("Remove from Tree", menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=False: self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)
                menu.addSeparator()

        # all other nodes
        currentNode = self.currentItem.viewNodes[treeIndex]
        for c in sorted(parent.children, key=lambda x: x.name):
            if c != currentNode:
                action = QtWidgets.QAction(c.name, menu)
                action.triggered.connect(lambda checked, t=treeIndex, p=c: self.moveCurrentItemToNewParent(t, p))
                menu.addAction(action)

        return menu


    '''Called when the user selects another tree in the tab widget.'''
    def tabWidgetCurrentChanged(self, tree):
        self.currentTree = tree
        self.treeSelectionChanged(tree)


    def tableWidgetCellChanged(self, row, column):
        """
        Called when the user wants to change the item name, field content or parent via the grid
        """

        if not self.locked:
            self.locked = True
            if column == 1:
                
                # the node name has been changed
                if row == 1:
                    newName = self.tableWidget.item(row,column).text()
                    self.currentItem.changeName(newName)
                
                # one of the fields has been changed
                else:
                    fieldName = self.tableWidget.item(row, 0).text()
                    fieldType = self.currentItem.fields[fieldName]['type']
                    if fieldType == 'text':
                        newValue = self.tableWidget.cellWidget(row, 1).toPlainText()
                    else:
                        newValue = self.tableWidget.item(row, 1).text()
                    result = self.currentItem.changeFieldContent(fieldName, newValue)
                    if result is not True:
                        message = "Couldn't update field content.\n" + str(result)
                        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                        msgBox.exec_()
                
            self.locked = False
            self.writeToFile()


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
            item = self.forest.itemPool.addNewItem()

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
            self.writeToFile()
    
    
    def moveCurrentItemToNewParent(self, treeIndex, newParent):
        
        treeWidget = self.treeWidgets[self.currentTree]
        if len(treeWidget.selectedItems()):

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
            elif oldParent and newParent:
                item.moveInTree(treeIndex, newParent.item.trees[treeIndex])

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
                self.treeSelectionChanged(self.currentTree)
            self.writeToFile()


class TreeTime():
    
    def __init__(self):
        
        app = QtWidgets.QApplication(sys.argv)
        if platform.system() == "Windows":
            app.setStyle("Fusion")
        mainWindow = TreeTimeWindow()

        mainWindow.show()
        sys.exit(app.exec_())

