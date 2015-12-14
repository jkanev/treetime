import sys
import item
import tree

from PyQt5 import QtCore, QtGui, QtWidgets, uic

with open("mainwindow.py", "w") as file:
	uic.compileUi("mainwindow.ui", file)


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
		

	
	def notifyNameChange(self, newName):
		super().setText(0, newName)

		
	def notifyFieldChange(self, fieldName, fieldContent):
		super().setText(self.fieldOrder[fieldName], fieldContent)
	
	def notifyDeletion(self):
		pass
		



class TreeTimeWindow(QtWidgets.QMainWindow):
	
	def __init__(self, filename):
		self.forest = tree.Forest(filename)
		self.tabWidgets = []
		self.treeWidgets = []
		self.currentTree = 0
		self.currentItem = None
		super().__init__()
		uic.loadUi('mainwindow.ui', self)
		self.createBranchTabs()
		self.fillTreeWidgets()
		self.pushButtonCreateNew.clicked.connect(self.pushButtonCreateNewClicked)
		self.tableWidget.cellChanged.connect(self.tableWidgetCellChanged)
		self.locked = True
	
		
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
			parent = QNode(c, self.forest.children[n].fieldOrder)
			self.treeWidgets[n].addTopLevelItem( parent )
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
		
	
	def tableWidgetCellChanged(self, row, column):
		if not self.locked:
			self.locked = True
			if column == 1:
				if row == 0:
					# the node name has been changed
					newName = self.tableWidget.item(row,column).text()
					self.currentItem.changeName(newName)
			self.locked = False
				

	def pushButtonCreateNewClicked(self):
		
		# get current node in current tree
		treeWidget = self.treeWidgets[self.currentTree]
		if len(treeWidget.selectedItems()):
			sourceQNode = treeWidget.selectedItems()[0]
			sourceNode = sourceQNode.sourceNode
			sourceItem = sourceNode.item

			# create default node and add item to it
			item = self.forest.itemPool.addNewItem()
			node = sourceNode.addItemAsChild(item)
			qnode = QNode(node, self.forest.children[self.currentTree].fieldOrder)
			sourceQNode.addChild(qnode)
			
			# expand parent and select new item
			sourceQNode.setExpanded(True)
			treeWidget.setCurrentItem(qnode)
		else:
			pass
			
app = QtWidgets.QApplication(sys.argv)
mainWindow = TreeTimeWindow("items.data")

mainWindow.show()
sys.exit(app.exec_())
