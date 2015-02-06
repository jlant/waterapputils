# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_interface.ui'
#
# Created: Fri Feb 06 16:42:20 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1065, 838)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_watertxt = QtGui.QWidget()
        self.tab_watertxt.setObjectName(_fromUtf8("tab_watertxt"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_watertxt)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame = QtGui.QFrame(self.tab_watertxt)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.push_button_open_file = QtGui.QPushButton(self.frame)
        self.push_button_open_file.setObjectName(_fromUtf8("push_button_open_file"))
        self.horizontalLayout_2.addWidget(self.push_button_open_file)
        self.line_edit_open_file = QtGui.QLineEdit(self.frame)
        self.line_edit_open_file.setReadOnly(True)
        self.line_edit_open_file.setObjectName(_fromUtf8("line_edit_open_file"))
        self.horizontalLayout_2.addWidget(self.line_edit_open_file)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.tab_watertxt)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.matplotlib_widget = MatplotlibWidget(self.frame_2)
        self.matplotlib_widget.setObjectName(_fromUtf8("matplotlib_widget"))
        self.verticalLayout.addWidget(self.matplotlib_widget)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.tab_watertxt)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.list_widget = QtGui.QListWidget(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_widget.sizePolicy().hasHeightForWidth())
        self.list_widget.setSizePolicy(sizePolicy)
        self.list_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.list_widget.setObjectName(_fromUtf8("list_widget"))
        self.horizontalLayout.addWidget(self.list_widget)
        self.table_widget = QtGui.QTableWidget(self.frame_3)
        self.table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_widget.setObjectName(_fromUtf8("table_widget"))
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.horizontalHeader().setCascadingSectionResizes(False)
        self.table_widget.horizontalHeader().setDefaultSectionSize(160)
        self.horizontalLayout.addWidget(self.table_widget)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.tabWidget.addTab(self.tab_watertxt, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1065, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuExit = QtGui.QMenu(self.menubar)
        self.menuExit.setObjectName(_fromUtf8("menuExit"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuExit.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuExit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.push_button_open_file.setText(_translate("MainWindow", "Open file", None))
        self.line_edit_open_file.setPlaceholderText(_translate("MainWindow", "Path to WATER.txt output text file", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_watertxt), _translate("MainWindow", "Process WATER output text file", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.menuExit.setTitle(_translate("MainWindow", "Exit", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+H", None))

from matplotlibwidget import MatplotlibWidget
