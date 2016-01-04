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

import sys
import item
import tree
import datetime
import os.path
from PyQt5 import QtCore, QtGui, QtWidgets, uic

# compile ui file if necessary
if os.path.getmtime("mainwindow.py") < os.path.getmtime("mainwindow.ui"):
    with open("mainwindow.py", "w") as file:
        print("compiling ui")
        uic.compileUi("mainwindow.ui", file)
        
import mainwindow


class QNode(QtWidgets.QTreeWidgetItem):

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
        


    def registerCallbacks(self):
        # register callbacks with source node
        self.sourceNode.registerNameChangeCallback(self.notifyNameChange)
        self.sourceNode.registerFieldChangeCallback(self.notifyFieldChange)
        self.sourceNode.registerDeletionCallback(self.notifyDeletion)
        self.sourceNode.registerViewNode(self)
        


    def notifyNameChange(self, newName):
        super().setText(0, newName)

        
    def notifyFieldChange(self, fieldName, fieldContent):
        if fieldName in self.fieldOrder:
            if self.sourceNode is not None and self.sourceNode.name == "Task 2":
                print("")
            super().setText(self.fieldOrder[fieldName], fieldContent)

    def notifyDeletion(self):
        # unlink node
        self.sourceNode = None
        
        # unlink from parent
        if self.parent() is not None:
            self.parent().removeChild(self)
        



class TreeTimeWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self, filename):
        super().__init__()
        self.setupUi(self)
        self.pushButtonNewChild.clicked.connect(lambda: self.createNode("child", False))
        self.pushButtonNewSibling.clicked.connect(lambda: self.createNode("sibling", False))
        self.pushButtonNewParent.clicked.connect(lambda: self.createNode("parent", False))
        self.pushButtonCopyNodeChild.clicked.connect(lambda: self.createNode("child", True))
        self.pushButtonCopyNodeSibling.clicked.connect(lambda: self.createNode("sibling", True))
        self.pushButtonCopyNodeParent.clicked.connect(lambda: self.createNode("parent", True))
        self.pushButtonLoadFile.clicked.connect(lambda: self.loadFile())
        self.tableWidget.cellChanged.connect(self.tableWidgetCellChanged)
        self.tableWidget.verticalHeader().setSectionResizeMode(3)
        self.tabWidget.currentChanged.connect(self.tabWidgetCurrentChanged)
        self.locked = True
        self.lineEditNewFileName.setText(filename)
        self.loadFile()


    def loadFile(self):
        self.removeBranchTabs()
        filename = self.lineEditNewFileName.text()
        self.forest = tree.Forest(filename)
        self.tabWidgets = []
        self.treeWidgets = []
        self.currentTree = 0
        self.currentItem = None
        self.createBranchTabs()
        self.fillTreeWidgets()
        self.labelCurrentFile.setText(filename)
    
    
    def removeBranchTabs(self):
            self.tabWidget.clear()
            self.tabWidgets = []


    def createBranchTabs(self):
        
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


    def fillTreeWidgets(self):
        for n,c in enumerate(self.forest.children):
            self.treeWidgets[n].itemSelectionChanged.connect(lambda x=n: self.treeSelectionChanged(x))
            self.treeWidgets[n].setHeaderLabels([""] + c.fieldOrder)
            root = self.treeWidgets[n].invisibleRootItem()
            for b in c.children:
                parent = QNode(b, c.fieldOrder)
                #self.treeWidgets[n].addTopLevelItem( parent )
                root.addChild(parent)
            self.treeWidgets[n].expandAll()


    def treeSelectionChanged(self, treeIndex):
        
        # init
        qnode = self.treeWidgets[treeIndex].selectedItems()[0]
        self.currentItem = qnode.sourceNode.item
        if self.currentItem is None:
            return
        
        self.tableWidget.clear()
        n = 0
        self.locked = True
        
        # create non-edit flags
        nonEditFlags = QtCore.Qt.ItemFlags()
        nonEditFlags != QtCore.Qt.ItemIsEnabled
        
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
            parent = tree.findNode(path).parent.name
            parent = QtWidgets.QTableWidgetItem(parent)
            self.tableWidget.setItem(n,0,name)
            self.tableWidget.setItem(n,1,parent)
            n += 1
            
        # add item fields
        for key in self.currentItem.fields:
            name = QtWidgets.QTableWidgetItem(key)
            name.setFlags(nonEditFlags)
            value = QtWidgets.QTableWidgetItem(str(self.currentItem.fields[key]["content"]))
            self.tableWidget.setItem(n,0,name)
            self.tableWidget.setItem(n,1,value)
            n += 1
        
        self.locked = False
        
    
    
    '''Called when the user selects another tree in the tab widget.'''
    def tabWidgetCurrentChanged(self, tree):
        self.currentTree = tree

    
    
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
                    newValue = self.tableWidget.item(row,1).text()
                    result = self.currentItem.changeFieldContent(fieldName, newValue)
                    if result is not True:
                        message = "Couldn't update field content.\n" + str(result)
                        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                        msgBox.exec_()
                
            self.locked = False
                


    def createNode(self, insertas, copy):
        
        treeWidget = self.treeWidgets[self.currentTree]
        if len(treeWidget.selectedItems()):
        
            sourceQNode = treeWidget.selectedItems()[0]
            sourceNode = sourceQNode.sourceNode
            sourceItem = sourceNode.item
            parentNode = sourceNode.parent
            parentQNode = sourceQNode.parent()
            if parentQNode is None:
                parentQNode = treeWidget.invisibleRootItem()
            item = None
            if copy:
                item = self.forest.itemPool.copyItem(sourceItem)
                for n,t in enumerate(self.forest.children):
                    if n != self.currentTree:
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
                    t = []
            
            if insertas == "child":
                
                # create default node and add item to it
                node = sourceNode.addItemAsChild(item)
                qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
                sourceQNode.addChild(qnode)
                
                # expand parent and select new item
                sourceQNode.setExpanded(True)
            
            elif insertas == "sibling":
                
                if parentNode is None or parentQNode is None:
                    return
                
                # create default node and add item to it
                node = parentNode.addItemAsChild(item)
                qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
                parentQNode.addChild(qnode)
                
                # expand parent and select new item
                parentQNode.setExpanded(True)
            
            elif insertas == "parent":
            
                if parentNode is None or parentQNode is None:
                    return
                
                node = parentNode.addItemAsChild(item)
                
                # move original node to be child of new parent
                parentNode.removeChild(sourceNode)
                node.addNodeAsChild(sourceNode)
                parentQNode.removeChild(sourceQNode)
                qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
                parentQNode.addChild(qnode)
                
                # expand parent and select new item
                qnode.setExpanded(True)
                
            treeWidget.setCurrentItem(qnode)
            self.forest.writeToFile( self.labelCurrentFile.text() )
    
    
    def moveToNewParent(self, treeName, newParentName):
        
        treeWidget = self.treeWidgets[self.currentTree]
        if len(treeWidget.selectedItems()):
        
            # find item
            item = treeWidget.selectedItems()[0].sourceNode.item
            
            # find tree and node
            tree = None
            treeIndex = None
            for n,t in enumerate(self.forest.children):
                if t.name == treeName:
                    tree = t
                    treeIndex = n
                    break
            node = item.viewNodes[treeIndex]
            oldParent = node.parent
            
            # find new parent
            newParent = tree.findNodeByName(newParentName)
            
            # change
            if newParent is None:
                message = "Cannot find a node with name '" + newParentName + "' in tree '" + treeName + "'.\nPlease check your spelling or create a node with the name '" + newParentName + "' in the '" + treeName + "' tab."
                msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tree Time Message", message)
                msgBox.exec_()
            else:
                # remove node from old parent
                item.removeFromTree(treeIndex)
                
                # assign node to new parent
                node.item = item
                newParent.addNodeAsChild(node)
                newQNode = QNode(node, tree.fieldOrder)
                newParent.viewNode.addChild(newQNode)
                self.forest.writeToFile("items.data")

app = QtWidgets.QApplication(sys.argv)
mainWindow = TreeTimeWindow("//home/jacob/software/tree-time/treetime/items.data")

mainWindow.show()
sys.exit(app.exec_())
