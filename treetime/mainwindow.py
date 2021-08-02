# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(250, 0))
        self.toolBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.toolBox.setToolTip("")
        self.toolBox.setObjectName("toolBox")
        self.pageFile = QtWidgets.QWidget()
        self.pageFile.setGeometry(QtCore.QRect(0, 0, 236, 806))
        self.pageFile.setObjectName("pageFile")
        self.formLayout = QtWidgets.QFormLayout(self.pageFile)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.label_8 = QtWidgets.QLabel(self.pageFile)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.label_8)
        self.labelCurrentFile = QtWidgets.QLabel(self.pageFile)
        self.labelCurrentFile.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCurrentFile.sizePolicy().hasHeightForWidth())
        self.labelCurrentFile.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(True)
        self.labelCurrentFile.setFont(font)
        self.labelCurrentFile.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCurrentFile.setWordWrap(True)
        self.labelCurrentFile.setOpenExternalLinks(True)
        self.labelCurrentFile.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.labelCurrentFile.setObjectName("labelCurrentFile")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.labelCurrentFile)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.SpanningRole, spacerItem1)
        self.label_5 = QtWidgets.QLabel(self.pageFile)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.label_5)
        self.pushButtonNewFromTemplate = QtWidgets.QPushButton(self.pageFile)
        self.pushButtonNewFromTemplate.setObjectName("pushButtonNewFromTemplate")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.pushButtonNewFromTemplate)
        self.pushButtonLoadFile = QtWidgets.QPushButton(self.pageFile)
        self.pushButtonLoadFile.setObjectName("pushButtonLoadFile")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.pushButtonLoadFile)
        self.pushButtonSaveToFile = QtWidgets.QPushButton(self.pageFile)
        self.pushButtonSaveToFile.setObjectName("pushButtonSaveToFile")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.pushButtonSaveToFile)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(8, QtWidgets.QFormLayout.SpanningRole, spacerItem2)
        self.label_11 = QtWidgets.QLabel(self.pageFile)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.label_11)
        self.radioButtonExportBranch = QtWidgets.QRadioButton(self.pageFile)
        self.radioButtonExportBranch.setChecked(True)
        self.radioButtonExportBranch.setObjectName("radioButtonExportBranch")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.radioButtonExportBranch)
        self.radioButtonExportTree = QtWidgets.QRadioButton(self.pageFile)
        self.radioButtonExportTree.setObjectName("radioButtonExportTree")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.SpanningRole, self.radioButtonExportTree)
        self.label_6 = QtWidgets.QLabel(self.pageFile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.comboBoxExportDepth = QtWidgets.QComboBox(self.pageFile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxExportDepth.sizePolicy().hasHeightForWidth())
        self.comboBoxExportDepth.setSizePolicy(sizePolicy)
        self.comboBoxExportDepth.setObjectName("comboBoxExportDepth")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.comboBoxExportDepth.addItem("")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.comboBoxExportDepth)
        self.pushButtonExportTxt = QtWidgets.QPushButton(self.pageFile)
        self.pushButtonExportTxt.setObjectName("pushButtonExportTxt")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.SpanningRole, self.pushButtonExportTxt)
        self.pushButtonExportHtml = QtWidgets.QPushButton(self.pageFile)
        self.pushButtonExportHtml.setObjectName("pushButtonExportHtml")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.SpanningRole, self.pushButtonExportHtml)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(16, QtWidgets.QFormLayout.SpanningRole, spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(17, QtWidgets.QFormLayout.SpanningRole, spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(18, QtWidgets.QFormLayout.SpanningRole, spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(19, QtWidgets.QFormLayout.SpanningRole, spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(20, QtWidgets.QFormLayout.SpanningRole, spacerItem7)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(21, QtWidgets.QFormLayout.SpanningRole, spacerItem8)
        self.pushButtonExportCsv = QtWidgets.QPushButton(self.pageFile)
        self.pushButtonExportCsv.setObjectName("pushButtonExportCsv")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.SpanningRole, self.pushButtonExportCsv)
        self.toolBox.addItem(self.pageFile, "")
        self.pageEdit = QtWidgets.QWidget()
        self.pageEdit.setGeometry(QtCore.QRect(0, 0, 250, 754))
        self.pageEdit.setMinimumSize(QtCore.QSize(200, 716))
        self.pageEdit.setObjectName("pageEdit")
        self.formLayout1 = QtWidgets.QFormLayout(self.pageEdit)
        self.formLayout1.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout1.setObjectName("formLayout1")
        self.label = QtWidgets.QLabel(self.pageEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout1.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.pushButtonNewChild = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonNewChild.setObjectName("pushButtonNewChild")
        self.formLayout1.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.pushButtonNewChild)
        self.pushButtonNewSibling = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonNewSibling.setObjectName("pushButtonNewSibling")
        self.formLayout1.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pushButtonNewSibling)
        self.pushButtonNewParent = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonNewParent.setObjectName("pushButtonNewParent")
        self.formLayout1.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.pushButtonNewParent)
        self.label_2 = QtWidgets.QLabel(self.pageEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout1.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.label_2)
        self.pushButtonCopyNodeChild = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonCopyNodeChild.setObjectName("pushButtonCopyNodeChild")
        self.formLayout1.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButtonCopyNodeChild)
        self.pushButtonCopyNodeSibling = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonCopyNodeSibling.setObjectName("pushButtonCopyNodeSibling")
        self.formLayout1.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.pushButtonCopyNodeSibling)
        self.pushButtonCopyNodeParent = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonCopyNodeParent.setObjectName("pushButtonCopyNodeParent")
        self.formLayout1.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.pushButtonCopyNodeParent)
        self.label_3 = QtWidgets.QLabel(self.pageEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout1.setWidget(12, QtWidgets.QFormLayout.SpanningRole, self.label_3)
        self.label_61 = QtWidgets.QLabel(self.pageEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_61.sizePolicy().hasHeightForWidth())
        self.label_61.setSizePolicy(sizePolicy)
        self.label_61.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_61.setObjectName("label_61")
        self.formLayout1.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_61)
        self.pushButtonCopyBranchSibling = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonCopyBranchSibling.setToolTipDuration(-1)
        self.pushButtonCopyBranchSibling.setObjectName("pushButtonCopyBranchSibling")
        self.formLayout1.setWidget(15, QtWidgets.QFormLayout.SpanningRole, self.pushButtonCopyBranchSibling)
        self.pushButtonCopyChildrenSiblings = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonCopyChildrenSiblings.setObjectName("pushButtonCopyChildrenSiblings")
        self.formLayout1.setWidget(16, QtWidgets.QFormLayout.SpanningRole, self.pushButtonCopyChildrenSiblings)
        self.label_4 = QtWidgets.QLabel(self.pageEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout1.setWidget(18, QtWidgets.QFormLayout.SpanningRole, self.label_4)
        self.pushButtonRemoveNode = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonRemoveNode.setObjectName("pushButtonRemoveNode")
        self.formLayout1.setWidget(19, QtWidgets.QFormLayout.SpanningRole, self.pushButtonRemoveNode)
        self.pushButtonDeleteNode = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonDeleteNode.setObjectName("pushButtonDeleteNode")
        self.formLayout1.setWidget(20, QtWidgets.QFormLayout.SpanningRole, self.pushButtonDeleteNode)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout1.setItem(1, QtWidgets.QFormLayout.SpanningRole, spacerItem9)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout1.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem10)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout1.setItem(11, QtWidgets.QFormLayout.SpanningRole, spacerItem11)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout1.setItem(17, QtWidgets.QFormLayout.SpanningRole, spacerItem12)
        self.comboBoxCopyDepth = QtWidgets.QComboBox(self.pageEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxCopyDepth.sizePolicy().hasHeightForWidth())
        self.comboBoxCopyDepth.setSizePolicy(sizePolicy)
        self.comboBoxCopyDepth.setObjectName("comboBoxCopyDepth")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.comboBoxCopyDepth.addItem("")
        self.formLayout1.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.comboBoxCopyDepth)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout1.setItem(26, QtWidgets.QFormLayout.SpanningRole, spacerItem13)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout1.setItem(21, QtWidgets.QFormLayout.SpanningRole, spacerItem14)
        self.label_12 = QtWidgets.QLabel(self.pageEdit)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.formLayout1.setWidget(22, QtWidgets.QFormLayout.SpanningRole, self.label_12)
        self.pushButtonRemoveBranch = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonRemoveBranch.setObjectName("pushButtonRemoveBranch")
        self.formLayout1.setWidget(23, QtWidgets.QFormLayout.SpanningRole, self.pushButtonRemoveBranch)
        self.pushButtonDeleteBranch = QtWidgets.QPushButton(self.pageEdit)
        self.pushButtonDeleteBranch.setObjectName("pushButtonDeleteBranch")
        self.formLayout1.setWidget(24, QtWidgets.QFormLayout.SpanningRole, self.pushButtonDeleteBranch)
        self.toolBox.addItem(self.pageEdit, "")
        self.pageView = QtWidgets.QWidget()
        self.pageView.setGeometry(QtCore.QRect(0, 0, 250, 754))
        self.pageView.setObjectName("pageView")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.pageView)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem15, 0, 0, 1, 1)
        self.toolBox.addItem(self.pageView, "")
        self.pageSettings = QtWidgets.QWidget()
        self.pageSettings.setGeometry(QtCore.QRect(0, 0, 250, 754))
        self.pageSettings.setObjectName("pageSettings")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pageSettings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem16)
        self.label_9 = QtWidgets.QLabel(self.pageSettings)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.cboxTheme = QtWidgets.QComboBox(self.pageSettings)
        self.cboxTheme.setObjectName("cboxTheme")
        self.verticalLayout_2.addWidget(self.cboxTheme)
        self.cboxColours = QtWidgets.QComboBox(self.pageSettings)
        self.cboxColours.setObjectName("cboxColours")
        self.verticalLayout_2.addWidget(self.cboxColours)
        spacerItem17 = QtWidgets.QSpacerItem(20, 136, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem17)
        self.label_10 = QtWidgets.QLabel(self.pageSettings)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.label_7 = QtWidgets.QLabel(self.pageSettings)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        spacerItem18 = QtWidgets.QSpacerItem(20, 136, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem18)
        self.toolBox.addItem(self.pageSettings, "")
        self.horizontalLayout.addWidget(self.toolBox)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMidLineWidth(0)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(10)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(10)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(-1)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tree Time"))
        self.label_8.setText(_translate("MainWindow", "Connected to Data File:"))
        self.labelCurrentFile.setToolTip(_translate("MainWindow", "The current data file. All changes made are silently written to this file."))
        self.labelCurrentFile.setText(_translate("MainWindow", "[current file name]"))
        self.label_5.setText(_translate("MainWindow", "Load and Save"))
        self.pushButtonNewFromTemplate.setToolTip(_translate("MainWindow", "<b>Create a new tree sheet from a template file</b><br/><br/>• Lets you choose a template in a file dialog, then choose a file location for your new file.<br/>• Changes are silently written to the new file."))
        self.pushButtonNewFromTemplate.setText(_translate("MainWindow", "New from Template"))
        self.pushButtonLoadFile.setToolTip(_translate("MainWindow", "<b>Load an existing tree sheet</b><br/><br/>Subsequent changes will be written silently to the loaded file."))
        self.pushButtonLoadFile.setText(_translate("MainWindow", "Load File"))
        self.pushButtonSaveToFile.setToolTip(_translate("MainWindow", "<b>Save the current file to a new location</b><br/><br/>Subsequent changes will be written silently to the new location."))
        self.pushButtonSaveToFile.setText(_translate("MainWindow", "Save As"))
        self.label_11.setText(_translate("MainWindow", "Export"))
        self.radioButtonExportBranch.setText(_translate("MainWindow", "Selected Branch"))
        self.radioButtonExportTree.setText(_translate("MainWindow", "Entire tree"))
        self.label_6.setText(_translate("MainWindow", "Depth  "))
        self.comboBoxExportDepth.setToolTip(_translate("MainWindow", "<b>Select a level down to which the current branch is copied</b>"))
        self.comboBoxExportDepth.setItemText(0, _translate("MainWindow", "all levels"))
        self.comboBoxExportDepth.setItemText(1, _translate("MainWindow", "1 level"))
        self.comboBoxExportDepth.setItemText(2, _translate("MainWindow", "2 levels"))
        self.comboBoxExportDepth.setItemText(3, _translate("MainWindow", "3 levels"))
        self.comboBoxExportDepth.setItemText(4, _translate("MainWindow", "4 levels"))
        self.comboBoxExportDepth.setItemText(5, _translate("MainWindow", "5 levels"))
        self.comboBoxExportDepth.setItemText(6, _translate("MainWindow", "6 levels"))
        self.comboBoxExportDepth.setItemText(7, _translate("MainWindow", "7 levels"))
        self.comboBoxExportDepth.setItemText(8, _translate("MainWindow", "8 levels"))
        self.comboBoxExportDepth.setItemText(9, _translate("MainWindow", "9 levels"))
        self.comboBoxExportDepth.setItemText(10, _translate("MainWindow", "10 levels"))
        self.pushButtonExportTxt.setToolTip(_translate("MainWindow", "<b>Export the current branch to a text file</b><br/><br/>• The file will contain all tree fields.<br/>• Text graphics show the tree structure."))
        self.pushButtonExportTxt.setText(_translate("MainWindow", "Export to Text"))
        self.pushButtonExportHtml.setToolTip(_translate("MainWindow", "<b>Export the current tree to a text file.</b><br/><br/>• The file will contain all tree fields.<br/>• Text graphics show the tree structure."))
        self.pushButtonExportHtml.setText(_translate("MainWindow", "Export to HTML"))
        self.pushButtonExportCsv.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Export the current branch or tree to a CSV file</span><br/><br/>• The file will contain all tree fields.<br/>• The first field (&quot;Tree&quot;) shows the tree structure.</p><p>• The second field (&quot;Name&quot;) shows the name.</p></body></html>"))
        self.pushButtonExportCsv.setText(_translate("MainWindow", "Export to CSV"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pageFile), _translate("MainWindow", "File"))
        self.label.setText(_translate("MainWindow", "Insert New Nodes"))
        self.pushButtonNewChild.setToolTip(_translate("MainWindow", "<b>Create a new item and link it as a child to the selected node</b><br/><br/>Only this tree will be affected."))
        self.pushButtonNewChild.setText(_translate("MainWindow", "New Child"))
        self.pushButtonNewSibling.setToolTip(_translate("MainWindow", "<b>Create a new item and link it as a sibling next to the selected node</b><br/><br/>Only this tree will be affected."))
        self.pushButtonNewSibling.setText(_translate("MainWindow", "New Sibling"))
        self.pushButtonNewParent.setToolTip(_translate("MainWindow", "<b>Create a new item and insert it as a parent above the selected node</b><br/><br/>Only this tree will be affected."))
        self.pushButtonNewParent.setText(_translate("MainWindow", "New Parent"))
        self.label_2.setText(_translate("MainWindow", "Copy Existing Nodes"))
        self.pushButtonCopyNodeChild.setToolTip(_translate("MainWindow", "<b>Insert a new child underneath</b><br/><br/>• The child will be a copy of the current node.<br/>• In all other trees the new item will appear as sibling."))
        self.pushButtonCopyNodeChild.setText(_translate("MainWindow", "Copy Node as Child"))
        self.pushButtonCopyNodeSibling.setToolTip(_translate("MainWindow", "<b>Insert a new sibling</b><br/><br/>• The sibling will be a copy of the current node.<br/>• In all other trees the new item will appear as sibling."))
        self.pushButtonCopyNodeSibling.setText(_translate("MainWindow", "Copy Node as Sibling"))
        self.pushButtonCopyNodeParent.setToolTip(_translate("MainWindow", "<b>Insert a new parent above</b><br/><br/>• The parent will be a copy of the current node.<br/>• In all other trees the new item will appear as sibling."))
        self.pushButtonCopyNodeParent.setText(_translate("MainWindow", "Copy Node as Parent"))
        self.label_3.setText(_translate("MainWindow", "Copy Parts of the Tree"))
        self.label_61.setText(_translate("MainWindow", "Depth  "))
        self.pushButtonCopyBranchSibling.setToolTip(_translate("MainWindow", "<b>Copy the current branch</b><br/><br/>• The current node and all its children will be copied.<br/>• The copy will be inserted as sibling.<br/>• Other trees are not affected."))
        self.pushButtonCopyBranchSibling.setText(_translate("MainWindow", "Copy Branch as Sibling"))
        self.pushButtonCopyChildrenSiblings.setToolTip(_translate("MainWindow", "<b>Copy all child branches</b><br/><br/>• All children are copied underneath the siblings of the current node.<br/>• The copy depth can be selected in the box above.<br/>• Other trees are not affected."))
        self.pushButtonCopyChildrenSiblings.setText(_translate("MainWindow", "Copy Children to Siblings"))
        self.label_4.setText(_translate("MainWindow", "Remove Single Node"))
        self.pushButtonRemoveNode.setToolTip(_translate("MainWindow", "<b>Remove the current node</b><br/><br/>• Children of the node are moved up, to be children of the node\'s parent.<br/>• Other trees are not affected."))
        self.pushButtonRemoveNode.setText(_translate("MainWindow", "Remove Node (this Tree)"))
        self.pushButtonDeleteNode.setToolTip(_translate("MainWindow", "<b>Delete the current item</b><br/><br/>• In each tree, children of the node are moved up, to be children of the node\'s parent.<br/>• The node is removed from all trees."))
        self.pushButtonDeleteNode.setText(_translate("MainWindow", "Delete Item (all Trees)"))
        self.comboBoxCopyDepth.setToolTip(_translate("MainWindow", "<b>Select a level down to which the current branch is copied</b>"))
        self.comboBoxCopyDepth.setItemText(0, _translate("MainWindow", "all levels"))
        self.comboBoxCopyDepth.setItemText(1, _translate("MainWindow", "1 level"))
        self.comboBoxCopyDepth.setItemText(2, _translate("MainWindow", "2 levels"))
        self.comboBoxCopyDepth.setItemText(3, _translate("MainWindow", "3 levels"))
        self.comboBoxCopyDepth.setItemText(4, _translate("MainWindow", "4 levels"))
        self.comboBoxCopyDepth.setItemText(5, _translate("MainWindow", "5 levels"))
        self.comboBoxCopyDepth.setItemText(6, _translate("MainWindow", "6 levels"))
        self.comboBoxCopyDepth.setItemText(7, _translate("MainWindow", "7 levels"))
        self.comboBoxCopyDepth.setItemText(8, _translate("MainWindow", "8 levels"))
        self.comboBoxCopyDepth.setItemText(9, _translate("MainWindow", "9 levels"))
        self.comboBoxCopyDepth.setItemText(10, _translate("MainWindow", "10 levels"))
        self.label_12.setText(_translate("MainWindow", "Remove Branch"))
        self.pushButtonRemoveBranch.setToolTip(_translate("MainWindow", "<b>Remove the current branch</b><br/><br/>• All descentants (children, grandchildren, ...), are removed.<br/>• Other trees are not affected.</li></ul>"))
        self.pushButtonRemoveBranch.setText(_translate("MainWindow", "Remove Branch (this Tree)"))
        self.pushButtonDeleteBranch.setToolTip(_translate("MainWindow", "<b>Delete the entire branch from all trees</b><br/><br/>• All descendants (children, grandchildren, etc) in all trees are deleted.<br/>• Children of a node are deleted recursively across trees.<br/>• Please make sure there are no unwanted connections before use."))
        self.pushButtonDeleteBranch.setText(_translate("MainWindow", "Delete Branch (all Trees)"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pageEdit), _translate("MainWindow", "Edit"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pageView), _translate("MainWindow", "View"))
        self.label_9.setText(_translate("MainWindow", "Look and Feel"))
        self.label_10.setText(_translate("MainWindow", "About"))
        self.label_7.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">     TreeTime 2021.5</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">     Updates and source code:<br />     <a href=\"https://github.com/jkanev/treetime\"><span style=\" text-decoration: underline; color:#2980b9;\">github.com/jkanev/treetime</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Documentation:<br />     <a href=\"https://treetime-data-manager.readthedocs.io\"><span style=\" text-decoration: underline; color:#2980b9;\">treetime-data-manager.</span></a><br />     <a href=\"https://treetime-data-manager.readthedocs.io\"><span style=\" text-decoration: underline; color:#2980b9;\">readthedocs.io</span></a></p></body></html>"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pageSettings), _translate("MainWindow", "Settings"))
        self.tableWidget.setSortingEnabled(False)
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
