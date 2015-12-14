# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 847)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setMinimumSize(QtCore.QSize(200, 0))
        self.toolBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.toolBox.setObjectName("toolBox")
        self.pageTree = QtWidgets.QWidget()
        self.pageTree.setGeometry(QtCore.QRect(0, 0, 200, 722))
        self.pageTree.setObjectName("pageTree")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.pageTree)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonNewSibling = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonNewSibling.setObjectName("pushButtonNewSibling")
        self.gridLayout_2.addWidget(self.pushButtonNewSibling, 1, 0, 1, 1)
        self.pushButtonNewChild = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonNewChild.setObjectName("pushButtonNewChild")
        self.gridLayout_2.addWidget(self.pushButtonNewChild, 0, 0, 1, 1)
        self.pushButtonCopyNodeChild = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonCopyNodeChild.setObjectName("pushButtonCopyNodeChild")
        self.gridLayout_2.addWidget(self.pushButtonCopyNodeChild, 2, 0, 1, 1)
        self.pushButtonRemove = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.gridLayout_2.addWidget(self.pushButtonRemove, 5, 0, 1, 1)
        self.pushButtonDelete = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridLayout_2.addWidget(self.pushButtonDelete, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 1)
        self.pushButtonCopyNodeSibling = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonCopyNodeSibling.setObjectName("pushButtonCopyNodeSibling")
        self.gridLayout_2.addWidget(self.pushButtonCopyNodeSibling, 3, 0, 1, 1)
        self.pushButtonCopyBranchSibling = QtWidgets.QPushButton(self.pageTree)
        self.pushButtonCopyBranchSibling.setObjectName("pushButtonCopyBranchSibling")
        self.gridLayout_2.addWidget(self.pushButtonCopyBranchSibling, 4, 0, 1, 1)
        self.toolBox.addItem(self.pageTree, "")
        self.pageGlobal = QtWidgets.QWidget()
        self.pageGlobal.setGeometry(QtCore.QRect(0, 0, 200, 722))
        self.pageGlobal.setObjectName("pageGlobal")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.pageGlobal)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 0, 0, 1, 1)
        self.toolBox.addItem(self.pageGlobal, "")
        self.horizontalLayout.addWidget(self.toolBox)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(-1)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tree Time"))
        self.pushButtonNewSibling.setText(_translate("MainWindow", "New Sibling"))
        self.pushButtonNewChild.setText(_translate("MainWindow", "New Child"))
        self.pushButtonCopyNodeChild.setText(_translate("MainWindow", "Copy Node as Child"))
        self.pushButtonRemove.setText(_translate("MainWindow", "Remove from this Tree"))
        self.pushButtonDelete.setText(_translate("MainWindow", "Delete Item"))
        self.pushButtonCopyNodeSibling.setText(_translate("MainWindow", "Copy Node as Sibling"))
        self.pushButtonCopyBranchSibling.setText(_translate("MainWindow", "Copy Branch as Sibling"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pageTree), _translate("MainWindow", " Local Operations "))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pageGlobal), _translate("MainWindow", "Global Operations"))
        self.tableWidget.setSortingEnabled(False)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

