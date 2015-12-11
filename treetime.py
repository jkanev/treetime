import sys
import item
from PyQt5 import QtCore, QtGui, QtWidgets, uic

#with open("mainwindow.py", "w") as file:
#	uic.compileUi("mainwindow.ui", file)
#import mainwindow

class QNode(QtWidgets.QTreeWidgetItem):
	
	def __init__(self, sourceNode, fieldOrder):
		
		self.sourceNode = sourceNode
		displayStrings = [sourceNode.name]
		for d in fieldOrder:
			if d in self.sourceNode.fields:
				displayStrings += [self.sourceNode.fields[d].getString()]
			else:
				displayStrings += [""]
				
		super().__init__(displayStrings)
		for c in sourceNode.children:
			child = QNode(c, fieldOrder)
			super().addChild(child)


class TreeTimeWindow(QtWidgets.QMainWindow):
	
	def __init__(self, filename):
		self.forest = item.Forest(filename)
		self.tabWidgets = []
		self.treeWidgets = []
		self.currentTree = 0
		super().__init__()
		uic.loadUi('mainwindow.ui', self)
		self.createBranchTabs()
		self.fillTreeWidgets()
	
		
	def createBranchTabs(self):
		for n,c in enumerate(self.forest.children):
			newTab = QtWidgets.QWidget()
			newTab.setObjectName("tab"+str(n))
			self.tabWidget.addTab(newTab, "")
			self.tabWidgets += [newTab]
			self.tabWidget.setTabText(n, c.name)
			newTree = QtWidgets.QTreeWidget(newTab)
			newTree.setGeometry(QtCore.QRect(0, 0, 731, 751))
			newTree.setAllColumnsShowFocus(True)
			newTree.setWordWrap(True)
			newTree.headerItem().setText(0, "1")
			newTree.setColumnCount(len(c.fieldOrder))
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
mainWindow = TreeTimeWindow("items.data")

mainWindow.show()
sys.exit(app.exec_())
