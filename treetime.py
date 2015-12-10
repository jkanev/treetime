import sys
import item
from PyQt5 import QtCore, QtGui, QtWidgets, uic

with open("mainwindow.py", "w") as file:
	uic.compileUi("mainwindow.ui", file)

class QNode(QtWidgets.QTreeWidgetItem):
	
	def __init__(self, sourceNode):
		
		self.sourceNode = sourceNode
		displayStrings = [sourceNode.name]
		for d in sourceNode.fieldOrder:
			if d in self.sourceNode.fields:
				displayStrings += [self.sourceNode.fields[d].getString()]
			else:
				displayStrings += [""]
				
		super().__init__(displayStrings)
		for c in sourceNode.children:
			child = QNode(c)
			super().addChild(child)


class TreeTimeWindow(QtWidgets.QMainWindow):
	
	def __init__(self):
		self.itemPool = None
		self.itemTree = None
		self.tabWidgets = []
		self.treeWidgets = []
		self.currentBranch = 0
		super().__init__()
		uic.loadUi('mainwindow.ui', self)
	
	
	def loadItemPool(self, filename):
		self.itemPool = item.ItemPool()
		self.itemPool.readFromFile(filename)
	
	
	def buildItemTree(self):
		self.itemTree = item.Tree()
		self.itemTree.createPaths(self.itemPool)
	
	
	def createBranchTabs(self):
		for n,c in enumerate(self.itemTree.children):
			newTab = QtWidgets.QWidget()
			newTab.setObjectName("tab"+str(n))
			self.tabWidget.addTab(newTab, "")
			self.tabWidgets += [newTab]
			self.tabWidget.setTabText(n, "Tree " + str(n))
			newTree = QtWidgets.QTreeWidget(newTab)
			newTree.setGeometry(QtCore.QRect(0, 0, 731, 751))
			newTree.setAllColumnsShowFocus(True)
			newTree.setWordWrap(True)
			newTree.setObjectName("treeWidget1")
			newTree.headerItem().setText(0, "1")
			newTree.setColumnCount(4)
			self.treeWidgets += [newTree]

	
	
	def fillTreeWidgets(self):
		for n,c in enumerate(self.itemTree.children):
			self.treeWidgets[n].itemSelectionChanged.connect(lambda x=n: self.treeSelectionChanged(x))
			self.treeWidgets[n].setHeaderLabels([""] + c.fieldOrder)
			parent = QNode(c)
			self.treeWidgets[n].addTopLevelItem( parent )
			self.treeWidgets[n].expandAll()
	
	
	def treeSelectionChanged(self, treeIndex):
		
		# init
		sourceNode = self.treeWidgets[treeIndex].selectedItems()[0].sourceNode
		sourceItem = sourceNode.item
		self.tableWidget.clear()
		n = 0

		# add name
		name = QtWidgets.QTableWidgetItem("")
		value = QtWidgets.QTableWidgetItem(sourceItem.name)
		self.tableWidget.setItem(n,0,name)
		self.tableWidget.setItem(n,1,value)
		n += 1
		
		# add item fields
		for key in sourceItem.fields:
			name = QtWidgets.QTableWidgetItem(key)
			value = QtWidgets.QTableWidgetItem(str(sourceItem.fields[key]["content"]))
			self.tableWidget.setItem(n,0,name)
			self.tableWidget.setItem(n,1,value)
			n += 1
			
		# add node fields
		for key in sourceNode.fields:
			name = QtWidgets.QTableWidgetItem(key)
			value = QtWidgets.QTableWidgetItem(str(sourceNode.fields[key].getString()))
			self.tableWidget.setItem(n,0,name)
			self.tableWidget.setItem(n,1,value)
			n += 1
				

app = QtWidgets.QApplication(sys.argv)
mainWindow = TreeTimeWindow()
mainWindow.loadItemPool("items.data")
mainWindow.buildItemTree()
mainWindow.createBranchTabs()
mainWindow.fillTreeWidgets()

mainWindow.show()
sys.exit(app.exec_())
