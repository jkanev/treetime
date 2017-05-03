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
            self.fieldOrder[f] = i+1 # plus one because column 0 is the node name
        
        # recurse
        for c in sourceNode.children:
            child = QNode(c, fieldOrder)
            super().addChild(child)
        
        # register callbacks
        self.registerCallbacks()
        

    def parent(self):
        return super().parent() or self.treeWidget().invisibleRootItem() or None
    
    def registerCallbacks(self):
        # register callbacks with source node
        self.sourceNode.registerNameChangeCallback(self.notifyNameChange)
        self.sourceNode.registerFieldChangeCallback(self.notifyFieldChange)
        self.sourceNode.registerDeletionCallback(self.notifyDeletion)
        self.sourceNode.registerSelectionCallback(lambda x: self.notifySelection(x))
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
        self.pushButtonRemove.clicked.connect(lambda: self.moveToNewParent(self.currentItem, self.currentTree, None))
        self.pushButtonDelete.clicked.connect(self.pushButtonDeleteClicked)
        self.tableWidget.cellChanged.connect(self.tableWidgetCellChanged)
        self.tableWidget.verticalHeader().setSectionResizeMode(3)
        self.tabWidget.currentChanged.connect(self.tabWidgetCurrentChanged)
        self.locked = True
        self.settings = QtCore.QSettings('', 'TreeTime')
        self.loadFile(filename or self.settings.value('lastFile'))

    def pushButtonSaveToFileClicked(self):
        result = QtWidgets.QFileDialog.getSaveFileName(self, "Save data file", "", ".trt")[0]
        if result != '':
            self.labelCurrentFile.setText(result)
            self.writeToFile()

    def pushButtonLoadFileClicked(self):
        result = QtWidgets.QFileDialog.getOpenFileName(self, "Load data file", "", ".trt")[0]
        if result != '':
            self.loadFile( result )

    def pushButtonDeleteClicked(self):
        message = "Deleting item \n\t" + self.currentItem.name + ".\nChanges are saved to file immediately and cannot be reverted."
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel);
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
        for n,c in enumerate(self.forest.children):
            self.treeWidgets[n].itemSelectionChanged.connect(lambda x=n: self.treeSelectionChanged(x))
            self.treeWidgets[n].setHeaderLabels([""] + c.fieldOrder)
            root = self.treeWidgets[n].invisibleRootItem()
            c.viewNode = root
            for b in c.children:
                parent = QNode(b, c.fieldOrder)
                #self.treeWidgets[n].addTopLevelItem( parent )
                root.addChild(parent)
            # self.treeWidgets[n].expandAll()


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
                
                # add name
                name = QtWidgets.QTableWidgetItem("")
                name.setFlags(nonEditFlags)
                value = QtWidgets.QTableWidgetItem(self.currentItem.name)
                self.tableWidget.setItem(n,0,name)
                self.tableWidget.setItem(n,1,value)
                n += 1
                
                # add tree parents
                for treeNumber,path in enumerate(self.currentItem.trees):
                    tree = self.forest.children[treeNumber]
                    name = QtWidgets.QTableWidgetItem(tree.name)
                    name.setFlags(nonEditFlags)
                    self.tableWidget.setItem(n,0,name)
                    parent = tree.findNode(path).parent
                    parentName = parent.name
                    if parentName == "":
                        parentName == "          "
                    menu = QtWidgets.QMenu(parent.name)
                    menu.addAction(parentName, lambda a=self.currentItem, b=treeNumber, c=tree: self.showChildMenu(a,b,c))
                    self.tableWidget.setCellWidget(n, 1, menu)
                    # parent = QtWidgets.QTableWidgetItem(parent)
                    # self.tableWidget.setItem(n,1,parent)
                    n += 1
                    
                # add item fields
                for key in self.currentItem.fields:
                    name = QtWidgets.QTableWidgetItem(key)
                    name.setFlags(nonEditFlags)
                    if self.currentItem.fields[key]['type'] == 'text':
                        text = str(self.currentItem.fields[key]["content"])
                        widget = QtWidgets.QPlainTextEdit(text)
                        widget.textChanged.connect( lambda row=n: self.tableWidgetCellChanged(row, 1) )
                        self.tableWidget.setCellWidget(n, 1, widget)
                    else:
                        value = QtWidgets.QTableWidgetItem(str(self.currentItem.fields[key]["content"]))
                        self.tableWidget.setItem(n,1,value)
                    self.tableWidget.setItem(n,0,name)
                    n += 1
            
            self.locked = False
    
    
    '''Displays a menu with possible children to select, at the current mouse cursor position. '''
    def showChildMenu(self, item, treeIndex, parent, parentMenu=None):
        isRoot = False
        if parentMenu is None:
            isRoot = True
            parentMenu = QtWidgets.QMenu()
        if parentMenu.isEmpty():
            parentMenu.addAction(parent.name, lambda x=item, y=treeIndex, z=parent: self.moveToNewParent(x,y,z))
            if isRoot:
                parentMenu.addAction("(None)", lambda x=item, y=treeIndex: self.moveToNewParent(x,y,None))
            parentMenu.addSeparator()
            for c in parent.children:
                submenu = QtWidgets.QMenu(c.name, parentMenu)
                submenu.aboutToShow.connect(lambda a=item, b=treeIndex, c=c, d=submenu: self.showChildMenu(a,b,c,d))
                parentMenu.addMenu(submenu)
        if isRoot:
            parentMenu.exec(QtGui.QCursor.pos())


    '''Called when the user selects another tree in the tab widget.'''
    def tabWidgetCurrentChanged(self, tree):
        self.currentTree = tree
        self.treeSelectionChanged(tree)

    
    
    ''' Called when the user wants to change the item name, field content or parent via the grid'''
    def tableWidgetCellChanged(self, row, column):
        if not self.locked:
            self.locked = True
            if column == 1:
                
                # the node name has been changed
                if row == 0:
                    newName = self.tableWidget.item(row,column).text()
                    self.currentItem.changeName(newName)
                
                # one of the parents has been changed
                elif row <= len(self.forest.children):
                    newParent = self.tableWidget.item(row,1).text()
                    tree = self.tableWidget.item(row,0).text()
                    self.moveToNewParent(tree, newParent)
                
                # one of the fields has been changed
                else:
                    fieldName = self.tableWidget.item(row,0).text()
                    fieldType = self.currentItem.fields[fieldName]['type']
                    if fieldType == 'text':
                        newValue = self.tableWidget.cellWidget(row,1).toPlainText()
                    else:
                        newValue = self.tableWidget.item(row,1).text()
                    result = self.currentItem.changeFieldContent(fieldName, newValue)
                    if result is not True:
                        message = "Couldn't update field content.\n" + str(result)
                        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                        msgBox.exec_()
                
            self.locked = False
            self.writeToFile()


    def createNode(self, insertas, copy, recurse = False, srcItem = None, destItem = None):
        
        treeWidget = self.treeWidgets[self.currentTree]
        if len(treeWidget.selectedItems()):
            
            # set source and destination nodes and qnodes
            if recurse and srcItem is not None and destItem is not None:
                sourceItem = srcItem
                sourceNode = srcItem.viewNodes[self.currentTree]
                sourceQNode = sourceNode.viewNode
                destNode = destItem.viewNodes[self.currentTree]
                destQNode = destNode.viewNode
            else:
                sourceQNode = treeWidget.selectedItems()[0]
                sourceNode = sourceQNode.sourceNode
                sourceItem = sourceNode.item
                destNode = sourceNode.parent
                destQNode = sourceQNode.parent()
                
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
                for t in item.trees:
                    item.trees[t] = []
            
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
    
    
    def moveToNewParent(self, item, treeIndex, newParent):
        
        treeWidget = self.treeWidgets[self.currentTree]
        if len(treeWidget.selectedItems()):
        
            # find tree and node
            tree = self.forest.children[treeIndex]
            node = item.viewNodes[treeIndex]
            
            # change
            if newParent is None:
                message = "Removing node\n\t" + item.name + "\nfrom the tree. Please make sure you don't orphan nodes.\nChanges will be saved to file immediately and cannot be reverted."
                msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel);
                result = msgBox.exec_()
                
                # remove node from old parent
                if result == QtWidgets.QMessageBox.Ok:
                    item.removeFromTree(treeIndex)
                    
                # or leave this function
                else:
                    return
                
            else:
                # remove node from old parent
                item.removeFromTree(treeIndex)
                
                # assign node to new parent
                if node is None:
                    node = newParent.addItemAsChild(item)
                else:
                    node.item = item
                    node.registerCallbacks()
                    newParent.addNodeAsChild(node)
                newQNode = QNode(node, tree.fieldOrder)
                newParent.viewNode.addChild(newQNode)
            
            # save change
            item.notifyFieldChange('')
            self.treeSelectionChanged(self.currentTree)
            self.writeToFile()


class TreeTime():
    
    def __init__(self):
        
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = TreeTimeWindow()

        mainWindow.show()
        sys.exit(app.exec_())

