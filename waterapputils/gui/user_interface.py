# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_interface.ui'
#
# Created: Thu Mar 12 13:21:58 2015
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
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.main_tab_widget = QtGui.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.main_tab_widget.setFont(font)
        self.main_tab_widget.setAutoFillBackground(True)
        self.main_tab_widget.setStyleSheet(_fromUtf8(""))
        self.main_tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.main_tab_widget.setTabsClosable(False)
        self.main_tab_widget.setMovable(True)
        self.main_tab_widget.setObjectName(_fromUtf8("main_tab_widget"))
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
        self.tab_watertxt_push_button_open_file = QtGui.QPushButton(self.frame)
        self.tab_watertxt_push_button_open_file.setObjectName(_fromUtf8("tab_watertxt_push_button_open_file"))
        self.horizontalLayout_2.addWidget(self.tab_watertxt_push_button_open_file)
        self.tab_watertxt_line_edit_open_file = QtGui.QLineEdit(self.frame)
        self.tab_watertxt_line_edit_open_file.setReadOnly(True)
        self.tab_watertxt_line_edit_open_file.setObjectName(_fromUtf8("tab_watertxt_line_edit_open_file"))
        self.horizontalLayout_2.addWidget(self.tab_watertxt_line_edit_open_file)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.tab_watertxt)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tab_watertxt_matplotlib_widget = MatplotlibWidget(self.frame_2)
        self.tab_watertxt_matplotlib_widget.setObjectName(_fromUtf8("tab_watertxt_matplotlib_widget"))
        self.verticalLayout.addWidget(self.tab_watertxt_matplotlib_widget)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.tab_watertxt)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tab_watertxt_list_widget = QtGui.QListWidget(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_watertxt_list_widget.sizePolicy().hasHeightForWidth())
        self.tab_watertxt_list_widget.setSizePolicy(sizePolicy)
        self.tab_watertxt_list_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_watertxt_list_widget.setObjectName(_fromUtf8("tab_watertxt_list_widget"))
        self.horizontalLayout.addWidget(self.tab_watertxt_list_widget)
        self.tab_watertxt_table_widget = QtGui.QTableWidget(self.frame_3)
        self.tab_watertxt_table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tab_watertxt_table_widget.setObjectName(_fromUtf8("tab_watertxt_table_widget"))
        self.tab_watertxt_table_widget.setColumnCount(0)
        self.tab_watertxt_table_widget.setRowCount(0)
        self.tab_watertxt_table_widget.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_watertxt_table_widget.horizontalHeader().setDefaultSectionSize(160)
        self.horizontalLayout.addWidget(self.tab_watertxt_table_widget)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.main_tab_widget.addTab(self.tab_watertxt, _fromUtf8(""))
        self.tab_watertxtcmp = QtGui.QWidget()
        self.tab_watertxtcmp.setObjectName(_fromUtf8("tab_watertxtcmp"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_watertxtcmp)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.frame_4 = QtGui.QFrame(self.tab_watertxtcmp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.gridLayout = QtGui.QGridLayout(self.frame_4)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(-1, 9, -1, 9)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tab_watertxtcmp_push_button_open_file1 = QtGui.QPushButton(self.frame_4)
        self.tab_watertxtcmp_push_button_open_file1.setObjectName(_fromUtf8("tab_watertxtcmp_push_button_open_file1"))
        self.gridLayout.addWidget(self.tab_watertxtcmp_push_button_open_file1, 0, 0, 1, 1)
        self.tab_watertxtcmp_push_button_open_file2 = QtGui.QPushButton(self.frame_4)
        self.tab_watertxtcmp_push_button_open_file2.setObjectName(_fromUtf8("tab_watertxtcmp_push_button_open_file2"))
        self.gridLayout.addWidget(self.tab_watertxtcmp_push_button_open_file2, 2, 0, 1, 1)
        self.tab_watertxtcmp_line_edit_open_file2 = QtGui.QLineEdit(self.frame_4)
        self.tab_watertxtcmp_line_edit_open_file2.setObjectName(_fromUtf8("tab_watertxtcmp_line_edit_open_file2"))
        self.gridLayout.addWidget(self.tab_watertxtcmp_line_edit_open_file2, 2, 1, 1, 1)
        self.tab_watertxtcmp_line_edit_open_file1 = QtGui.QLineEdit(self.frame_4)
        self.tab_watertxtcmp_line_edit_open_file1.setObjectName(_fromUtf8("tab_watertxtcmp_line_edit_open_file1"))
        self.gridLayout.addWidget(self.tab_watertxtcmp_line_edit_open_file1, 0, 1, 1, 1)
        self.tab_watertxtcmp_push_button_compare = QtGui.QPushButton(self.frame_4)
        self.tab_watertxtcmp_push_button_compare.setObjectName(_fromUtf8("tab_watertxtcmp_push_button_compare"))
        self.gridLayout.addWidget(self.tab_watertxtcmp_push_button_compare, 3, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.frame_4)
        self.frame_5 = QtGui.QFrame(self.tab_watertxtcmp)
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.tab_watertxtcmp_matplotlib_widget = MatplotlibWidget(self.frame_5)
        self.tab_watertxtcmp_matplotlib_widget.setObjectName(_fromUtf8("tab_watertxtcmp_matplotlib_widget"))
        self.verticalLayout_7.addWidget(self.tab_watertxtcmp_matplotlib_widget)
        self.verticalLayout_5.addWidget(self.frame_5)
        self.frame_6 = QtGui.QFrame(self.tab_watertxtcmp)
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.tab_watertxtcmp_list_widget = QtGui.QListWidget(self.frame_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_watertxtcmp_list_widget.sizePolicy().hasHeightForWidth())
        self.tab_watertxtcmp_list_widget.setSizePolicy(sizePolicy)
        self.tab_watertxtcmp_list_widget.setObjectName(_fromUtf8("tab_watertxtcmp_list_widget"))
        self.horizontalLayout_4.addWidget(self.tab_watertxtcmp_list_widget)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tab_watertxtcmp_table_widget1 = QtGui.QTableWidget(self.frame_6)
        self.tab_watertxtcmp_table_widget1.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tab_watertxtcmp_table_widget1.setObjectName(_fromUtf8("tab_watertxtcmp_table_widget1"))
        self.tab_watertxtcmp_table_widget1.setColumnCount(0)
        self.tab_watertxtcmp_table_widget1.setRowCount(0)
        self.tab_watertxtcmp_table_widget1.horizontalHeader().setDefaultSectionSize(160)
        self.verticalLayout_4.addWidget(self.tab_watertxtcmp_table_widget1)
        self.tab_watertxtcmp_table_widget2 = QtGui.QTableWidget(self.frame_6)
        self.tab_watertxtcmp_table_widget2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tab_watertxtcmp_table_widget2.setObjectName(_fromUtf8("tab_watertxtcmp_table_widget2"))
        self.tab_watertxtcmp_table_widget2.setColumnCount(0)
        self.tab_watertxtcmp_table_widget2.setRowCount(0)
        self.tab_watertxtcmp_table_widget2.horizontalHeader().setDefaultSectionSize(160)
        self.verticalLayout_4.addWidget(self.tab_watertxtcmp_table_widget2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addWidget(self.frame_6)
        self.main_tab_widget.addTab(self.tab_watertxtcmp, _fromUtf8(""))
        self.tab_applywateruse = QtGui.QWidget()
        self.tab_applywateruse.setObjectName(_fromUtf8("tab_applywateruse"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.tab_applywateruse)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.frame_13 = QtGui.QFrame(self.tab_applywateruse)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.frame_13.setFont(font)
        self.frame_13.setToolTip(_fromUtf8(""))
        self.frame_13.setObjectName(_fromUtf8("frame_13"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_13)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.frame_7 = QtGui.QFrame(self.frame_13)
        self.frame_7.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_7.setObjectName(_fromUtf8("frame_7"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.frame_7)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.frame_9 = QtGui.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.frame_9.setFont(font)
        self.frame_9.setObjectName(_fromUtf8("frame_9"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_9)
        self.gridLayout_3.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tab_wateruse_group_box_num_sims = QtGui.QGroupBox(self.frame_9)
        self.tab_wateruse_group_box_num_sims.setToolTip(_fromUtf8(""))
        self.tab_wateruse_group_box_num_sims.setStyleSheet(_fromUtf8(""))
        self.tab_wateruse_group_box_num_sims.setObjectName(_fromUtf8("tab_wateruse_group_box_num_sims"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.tab_wateruse_group_box_num_sims)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.tab_wateruse_radio_button_one_sim = QtGui.QRadioButton(self.tab_wateruse_group_box_num_sims)
        self.tab_wateruse_radio_button_one_sim.setChecked(True)
        self.tab_wateruse_radio_button_one_sim.setObjectName(_fromUtf8("tab_wateruse_radio_button_one_sim"))
        self.verticalLayout_9.addWidget(self.tab_wateruse_radio_button_one_sim)
        self.tab_wateruse_radio_button_multi_sims = QtGui.QRadioButton(self.tab_wateruse_group_box_num_sims)
        self.tab_wateruse_radio_button_multi_sims.setObjectName(_fromUtf8("tab_wateruse_radio_button_multi_sims"))
        self.verticalLayout_9.addWidget(self.tab_wateruse_radio_button_multi_sims)
        self.gridLayout_3.addWidget(self.tab_wateruse_group_box_num_sims, 0, 0, 2, 1)
        self.tab_wateruse_group_box_type_sims = QtGui.QGroupBox(self.frame_9)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tab_wateruse_group_box_type_sims.setFont(font)
        self.tab_wateruse_group_box_type_sims.setStyleSheet(_fromUtf8(""))
        self.tab_wateruse_group_box_type_sims.setObjectName(_fromUtf8("tab_wateruse_group_box_type_sims"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.tab_wateruse_group_box_type_sims)
        self.verticalLayout_13.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.tab_wateruse_radio_button_batch = QtGui.QRadioButton(self.tab_wateruse_group_box_type_sims)
        self.tab_wateruse_radio_button_batch.setChecked(True)
        self.tab_wateruse_radio_button_batch.setObjectName(_fromUtf8("tab_wateruse_radio_button_batch"))
        self.verticalLayout_13.addWidget(self.tab_wateruse_radio_button_batch)
        self.tab_wateruse_radio_button_single = QtGui.QRadioButton(self.tab_wateruse_group_box_type_sims)
        self.tab_wateruse_radio_button_single.setObjectName(_fromUtf8("tab_wateruse_radio_button_single"))
        self.verticalLayout_13.addWidget(self.tab_wateruse_radio_button_single)
        self.gridLayout_3.addWidget(self.tab_wateruse_group_box_type_sims, 0, 2, 2, 1)
        self.verticalLayout_10.addWidget(self.frame_9)
        self.tab_wateruse_group_box_sim_info = QtGui.QGroupBox(self.frame_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_wateruse_group_box_sim_info.sizePolicy().hasHeightForWidth())
        self.tab_wateruse_group_box_sim_info.setSizePolicy(sizePolicy)
        self.tab_wateruse_group_box_sim_info.setObjectName(_fromUtf8("tab_wateruse_group_box_sim_info"))
        self.formLayout_2 = QtGui.QFormLayout(self.tab_wateruse_group_box_sim_info)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(self.tab_wateruse_group_box_sim_info)
        self.label_3.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.tab_wateruse_line_edit_basin_shp = QtGui.QLineEdit(self.tab_wateruse_group_box_sim_info)
        self.tab_wateruse_line_edit_basin_shp.setReadOnly(True)
        self.tab_wateruse_line_edit_basin_shp.setObjectName(_fromUtf8("tab_wateruse_line_edit_basin_shp"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.tab_wateruse_line_edit_basin_shp)
        self.label_4 = QtGui.QLabel(self.tab_wateruse_group_box_sim_info)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.tab_wateruse_group_box_sim_info)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.tab_wateruse_push_button_open_sim = QtGui.QPushButton(self.tab_wateruse_group_box_sim_info)
        self.tab_wateruse_push_button_open_sim.setObjectName(_fromUtf8("tab_wateruse_push_button_open_sim"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.tab_wateruse_push_button_open_sim)
        self.tab_wateruse_line_edit_open_sim = QtGui.QLineEdit(self.tab_wateruse_group_box_sim_info)
        self.tab_wateruse_line_edit_open_sim.setReadOnly(True)
        self.tab_wateruse_line_edit_open_sim.setObjectName(_fromUtf8("tab_wateruse_line_edit_open_sim"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.tab_wateruse_line_edit_open_sim)
        self.tab_wateruse_combo_box_shp_id_field = QtGui.QComboBox(self.tab_wateruse_group_box_sim_info)
        self.tab_wateruse_combo_box_shp_id_field.setObjectName(_fromUtf8("tab_wateruse_combo_box_shp_id_field"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.tab_wateruse_combo_box_shp_id_field)
        self.tab_wateruse_combo_box_shp_area_field = QtGui.QComboBox(self.tab_wateruse_group_box_sim_info)
        self.tab_wateruse_combo_box_shp_area_field.setObjectName(_fromUtf8("tab_wateruse_combo_box_shp_area_field"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.tab_wateruse_combo_box_shp_area_field)
        self.verticalLayout_10.addWidget(self.tab_wateruse_group_box_sim_info)
        self.tab_wateruse_group_box_wateruse_info = QtGui.QGroupBox(self.frame_7)
        self.tab_wateruse_group_box_wateruse_info.setCheckable(False)
        self.tab_wateruse_group_box_wateruse_info.setObjectName(_fromUtf8("tab_wateruse_group_box_wateruse_info"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_wateruse_group_box_wateruse_info)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_6 = QtGui.QLabel(self.tab_wateruse_group_box_wateruse_info)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 7, 0, 1, 1)
        self.tab_wateruse_line_edit_wateruse_factor_file = QtGui.QLineEdit(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_line_edit_wateruse_factor_file.setReadOnly(True)
        self.tab_wateruse_line_edit_wateruse_factor_file.setObjectName(_fromUtf8("tab_wateruse_line_edit_wateruse_factor_file"))
        self.gridLayout_5.addWidget(self.tab_wateruse_line_edit_wateruse_factor_file, 3, 1, 1, 2)
        self.tab_wateruse_push_button_wateruse_factor_file = QtGui.QPushButton(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_push_button_wateruse_factor_file.setObjectName(_fromUtf8("tab_wateruse_push_button_wateruse_factor_file"))
        self.gridLayout_5.addWidget(self.tab_wateruse_push_button_wateruse_factor_file, 3, 0, 2, 1)
        self.tab_wateruse_line_edit_wateruse_shp = QtGui.QLineEdit(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_line_edit_wateruse_shp.setReadOnly(True)
        self.tab_wateruse_line_edit_wateruse_shp.setObjectName(_fromUtf8("tab_wateruse_line_edit_wateruse_shp"))
        self.gridLayout_5.addWidget(self.tab_wateruse_line_edit_wateruse_shp, 5, 1, 1, 2)
        self.tab_wateruse_push_button_wateruse_shp = QtGui.QPushButton(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_push_button_wateruse_shp.setObjectName(_fromUtf8("tab_wateruse_push_button_wateruse_shp"))
        self.gridLayout_5.addWidget(self.tab_wateruse_push_button_wateruse_shp, 5, 0, 2, 1)
        self.tab_wateruse_list_widget_wateruse_files = QtGui.QListWidget(self.tab_wateruse_group_box_wateruse_info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_wateruse_list_widget_wateruse_files.sizePolicy().hasHeightForWidth())
        self.tab_wateruse_list_widget_wateruse_files.setSizePolicy(sizePolicy)
        self.tab_wateruse_list_widget_wateruse_files.setMaximumSize(QtCore.QSize(16777215, 100))
        self.tab_wateruse_list_widget_wateruse_files.setObjectName(_fromUtf8("tab_wateruse_list_widget_wateruse_files"))
        self.gridLayout_5.addWidget(self.tab_wateruse_list_widget_wateruse_files, 0, 1, 1, 1)
        self.tab_wateruse_push_button_wateruse_files = QtGui.QPushButton(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_push_button_wateruse_files.setObjectName(_fromUtf8("tab_wateruse_push_button_wateruse_files"))
        self.gridLayout_5.addWidget(self.tab_wateruse_push_button_wateruse_files, 0, 0, 1, 1)
        self.tab_wateruse_combo_box_wateruse_shp_id_field = QtGui.QComboBox(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_combo_box_wateruse_shp_id_field.setObjectName(_fromUtf8("tab_wateruse_combo_box_wateruse_shp_id_field"))
        self.gridLayout_5.addWidget(self.tab_wateruse_combo_box_wateruse_shp_id_field, 7, 1, 1, 1)
        self.tab_wateruse_checkbox_subwateruse = QtGui.QCheckBox(self.tab_wateruse_group_box_wateruse_info)
        self.tab_wateruse_checkbox_subwateruse.setObjectName(_fromUtf8("tab_wateruse_checkbox_subwateruse"))
        self.gridLayout_5.addWidget(self.tab_wateruse_checkbox_subwateruse, 8, 0, 1, 1)
        self.verticalLayout_10.addWidget(self.tab_wateruse_group_box_wateruse_info)
        self.frame_12 = QtGui.QFrame(self.frame_7)
        self.frame_12.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_12.setObjectName(_fromUtf8("frame_12"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.frame_12)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.tab_wateruse_push_button_check_inputs = QtGui.QPushButton(self.frame_12)
        self.tab_wateruse_push_button_check_inputs.setObjectName(_fromUtf8("tab_wateruse_push_button_check_inputs"))
        self.verticalLayout_11.addWidget(self.tab_wateruse_push_button_check_inputs)
        self.tab_wateruse_push_button_apply_wateruse = QtGui.QPushButton(self.frame_12)
        self.tab_wateruse_push_button_apply_wateruse.setObjectName(_fromUtf8("tab_wateruse_push_button_apply_wateruse"))
        self.verticalLayout_11.addWidget(self.tab_wateruse_push_button_apply_wateruse)
        self.tab_wateruse_text_edit = QtGui.QTextEdit(self.frame_12)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tab_wateruse_text_edit.setFont(font)
        self.tab_wateruse_text_edit.setReadOnly(True)
        self.tab_wateruse_text_edit.setObjectName(_fromUtf8("tab_wateruse_text_edit"))
        self.verticalLayout_11.addWidget(self.tab_wateruse_text_edit)
        self.verticalLayout_10.addWidget(self.frame_12)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem)
        self.horizontalLayout_5.addWidget(self.frame_7)
        self.frame_8 = QtGui.QFrame(self.frame_13)
        self.frame_8.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_8.setObjectName(_fromUtf8("frame_8"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.tab_wateruse_matplotlib_widget = MatplotlibWidget(self.frame_8)
        self.tab_wateruse_matplotlib_widget.setObjectName(_fromUtf8("tab_wateruse_matplotlib_widget"))
        self.verticalLayout_12.addWidget(self.tab_wateruse_matplotlib_widget)
        self.frame_10 = QtGui.QFrame(self.frame_8)
        self.frame_10.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_10.setObjectName(_fromUtf8("frame_10"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.frame_10)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.tab_wateruse_push_button_plot_overview_map = QtGui.QPushButton(self.frame_10)
        self.tab_wateruse_push_button_plot_overview_map.setObjectName(_fromUtf8("tab_wateruse_push_button_plot_overview_map"))
        self.horizontalLayout_6.addWidget(self.tab_wateruse_push_button_plot_overview_map)
        self.tab_wateruse_push_button_plot_zoomed_map = QtGui.QPushButton(self.frame_10)
        self.tab_wateruse_push_button_plot_zoomed_map.setObjectName(_fromUtf8("tab_wateruse_push_button_plot_zoomed_map"))
        self.horizontalLayout_6.addWidget(self.tab_wateruse_push_button_plot_zoomed_map)
        self.verticalLayout_12.addWidget(self.frame_10)
        self.horizontalLayout_5.addWidget(self.frame_8)
        self.verticalLayout_8.addWidget(self.frame_13)
        self.main_tab_widget.addTab(self.tab_applywateruse, _fromUtf8(""))
        self.tab_applygcm = QtGui.QWidget()
        self.tab_applygcm.setObjectName(_fromUtf8("tab_applygcm"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_applygcm)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.frame_14 = QtGui.QFrame(self.tab_applygcm)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.frame_14.setFont(font)
        self.frame_14.setToolTip(_fromUtf8(""))
        self.frame_14.setObjectName(_fromUtf8("frame_14"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.frame_14)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.frame_11 = QtGui.QFrame(self.frame_14)
        self.frame_11.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_11.setObjectName(_fromUtf8("frame_11"))
        self.verticalLayout_14 = QtGui.QVBoxLayout(self.frame_11)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.frame_15 = QtGui.QFrame(self.frame_11)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.frame_15.setFont(font)
        self.frame_15.setObjectName(_fromUtf8("frame_15"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_15)
        self.gridLayout_4.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tab_gcm_group_box_num_sims = QtGui.QGroupBox(self.frame_15)
        self.tab_gcm_group_box_num_sims.setToolTip(_fromUtf8(""))
        self.tab_gcm_group_box_num_sims.setStyleSheet(_fromUtf8(""))
        self.tab_gcm_group_box_num_sims.setObjectName(_fromUtf8("tab_gcm_group_box_num_sims"))
        self.verticalLayout_15 = QtGui.QVBoxLayout(self.tab_gcm_group_box_num_sims)
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.tab_gcm_radio_button_one_sims = QtGui.QRadioButton(self.tab_gcm_group_box_num_sims)
        self.tab_gcm_radio_button_one_sims.setChecked(True)
        self.tab_gcm_radio_button_one_sims.setObjectName(_fromUtf8("tab_gcm_radio_button_one_sims"))
        self.verticalLayout_15.addWidget(self.tab_gcm_radio_button_one_sims)
        self.tab_gcm_radio_button_multi_sims = QtGui.QRadioButton(self.tab_gcm_group_box_num_sims)
        self.tab_gcm_radio_button_multi_sims.setObjectName(_fromUtf8("tab_gcm_radio_button_multi_sims"))
        self.verticalLayout_15.addWidget(self.tab_gcm_radio_button_multi_sims)
        self.gridLayout_4.addWidget(self.tab_gcm_group_box_num_sims, 0, 0, 2, 1)
        self.tab_gcm_group_box_type_sims = QtGui.QGroupBox(self.frame_15)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tab_gcm_group_box_type_sims.setFont(font)
        self.tab_gcm_group_box_type_sims.setStyleSheet(_fromUtf8(""))
        self.tab_gcm_group_box_type_sims.setObjectName(_fromUtf8("tab_gcm_group_box_type_sims"))
        self.verticalLayout_16 = QtGui.QVBoxLayout(self.tab_gcm_group_box_type_sims)
        self.verticalLayout_16.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.tab_gcm_radio_button_batch = QtGui.QRadioButton(self.tab_gcm_group_box_type_sims)
        self.tab_gcm_radio_button_batch.setChecked(True)
        self.tab_gcm_radio_button_batch.setObjectName(_fromUtf8("tab_gcm_radio_button_batch"))
        self.verticalLayout_16.addWidget(self.tab_gcm_radio_button_batch)
        self.tab_gcm_radio_button_single = QtGui.QRadioButton(self.tab_gcm_group_box_type_sims)
        self.tab_gcm_radio_button_single.setObjectName(_fromUtf8("tab_gcm_radio_button_single"))
        self.verticalLayout_16.addWidget(self.tab_gcm_radio_button_single)
        self.gridLayout_4.addWidget(self.tab_gcm_group_box_type_sims, 0, 2, 2, 1)
        self.verticalLayout_14.addWidget(self.frame_15)
        self.tab_gcm_group_box_sim_info = QtGui.QGroupBox(self.frame_11)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_gcm_group_box_sim_info.sizePolicy().hasHeightForWidth())
        self.tab_gcm_group_box_sim_info.setSizePolicy(sizePolicy)
        self.tab_gcm_group_box_sim_info.setObjectName(_fromUtf8("tab_gcm_group_box_sim_info"))
        self.formLayout_3 = QtGui.QFormLayout(self.tab_gcm_group_box_sim_info)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_7 = QtGui.QLabel(self.tab_gcm_group_box_sim_info)
        self.label_7.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.tab_gcm_line_edit_basin_shp = QtGui.QLineEdit(self.tab_gcm_group_box_sim_info)
        self.tab_gcm_line_edit_basin_shp.setReadOnly(True)
        self.tab_gcm_line_edit_basin_shp.setObjectName(_fromUtf8("tab_gcm_line_edit_basin_shp"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.tab_gcm_line_edit_basin_shp)
        self.label_8 = QtGui.QLabel(self.tab_gcm_group_box_sim_info)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtGui.QLabel(self.tab_gcm_group_box_sim_info)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_9)
        self.tab_gcm_push_button_open_sim = QtGui.QPushButton(self.tab_gcm_group_box_sim_info)
        self.tab_gcm_push_button_open_sim.setObjectName(_fromUtf8("tab_gcm_push_button_open_sim"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.tab_gcm_push_button_open_sim)
        self.tab_gcm_line_edit_open_sim = QtGui.QLineEdit(self.tab_gcm_group_box_sim_info)
        self.tab_gcm_line_edit_open_sim.setReadOnly(True)
        self.tab_gcm_line_edit_open_sim.setObjectName(_fromUtf8("tab_gcm_line_edit_open_sim"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.tab_gcm_line_edit_open_sim)
        self.tab_gcm_combo_box_shp_id_field = QtGui.QComboBox(self.tab_gcm_group_box_sim_info)
        self.tab_gcm_combo_box_shp_id_field.setObjectName(_fromUtf8("tab_gcm_combo_box_shp_id_field"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.tab_gcm_combo_box_shp_id_field)
        self.tab_gcm_combo_box_shp_area_field = QtGui.QComboBox(self.tab_gcm_group_box_sim_info)
        self.tab_gcm_combo_box_shp_area_field.setObjectName(_fromUtf8("tab_gcm_combo_box_shp_area_field"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.tab_gcm_combo_box_shp_area_field)
        self.verticalLayout_14.addWidget(self.tab_gcm_group_box_sim_info)
        self.tab_gcm_group_box_gcm_info = QtGui.QGroupBox(self.frame_11)
        self.tab_gcm_group_box_gcm_info.setCheckable(False)
        self.tab_gcm_group_box_gcm_info.setObjectName(_fromUtf8("tab_gcm_group_box_gcm_info"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_gcm_group_box_gcm_info)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_10 = QtGui.QLabel(self.tab_gcm_group_box_gcm_info)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_6.addWidget(self.label_10, 5, 0, 1, 1)
        self.tab_gcm_line_edit_gcm_shp = QtGui.QLineEdit(self.tab_gcm_group_box_gcm_info)
        self.tab_gcm_line_edit_gcm_shp.setReadOnly(True)
        self.tab_gcm_line_edit_gcm_shp.setObjectName(_fromUtf8("tab_gcm_line_edit_gcm_shp"))
        self.gridLayout_6.addWidget(self.tab_gcm_line_edit_gcm_shp, 3, 1, 1, 2)
        self.tab_gcm_push_button_gcm_shp = QtGui.QPushButton(self.tab_gcm_group_box_gcm_info)
        self.tab_gcm_push_button_gcm_shp.setObjectName(_fromUtf8("tab_gcm_push_button_gcm_shp"))
        self.gridLayout_6.addWidget(self.tab_gcm_push_button_gcm_shp, 3, 0, 2, 1)
        self.tab_gcm_list_widget_gcm_files = QtGui.QListWidget(self.tab_gcm_group_box_gcm_info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_gcm_list_widget_gcm_files.sizePolicy().hasHeightForWidth())
        self.tab_gcm_list_widget_gcm_files.setSizePolicy(sizePolicy)
        self.tab_gcm_list_widget_gcm_files.setMaximumSize(QtCore.QSize(16777215, 100))
        self.tab_gcm_list_widget_gcm_files.setObjectName(_fromUtf8("tab_gcm_list_widget_gcm_files"))
        self.gridLayout_6.addWidget(self.tab_gcm_list_widget_gcm_files, 0, 1, 1, 1)
        self.tab_gcm_push_button_gcm_files = QtGui.QPushButton(self.tab_gcm_group_box_gcm_info)
        self.tab_gcm_push_button_gcm_files.setObjectName(_fromUtf8("tab_gcm_push_button_gcm_files"))
        self.gridLayout_6.addWidget(self.tab_gcm_push_button_gcm_files, 0, 0, 1, 1)
        self.tab_gcm_combo_box_gcm_shp_id_field = QtGui.QComboBox(self.tab_gcm_group_box_gcm_info)
        self.tab_gcm_combo_box_gcm_shp_id_field.setObjectName(_fromUtf8("tab_gcm_combo_box_gcm_shp_id_field"))
        self.gridLayout_6.addWidget(self.tab_gcm_combo_box_gcm_shp_id_field, 5, 1, 1, 1)
        self.tab_gcm_checkbox_subwateruse = QtGui.QCheckBox(self.tab_gcm_group_box_gcm_info)
        self.tab_gcm_checkbox_subwateruse.setObjectName(_fromUtf8("tab_gcm_checkbox_subwateruse"))
        self.gridLayout_6.addWidget(self.tab_gcm_checkbox_subwateruse, 6, 0, 1, 1)
        self.verticalLayout_14.addWidget(self.tab_gcm_group_box_gcm_info)
        self.frame_16 = QtGui.QFrame(self.frame_11)
        self.frame_16.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_16.setObjectName(_fromUtf8("frame_16"))
        self.verticalLayout_17 = QtGui.QVBoxLayout(self.frame_16)
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        self.tab_gcm_push_button_check_inputs = QtGui.QPushButton(self.frame_16)
        self.tab_gcm_push_button_check_inputs.setObjectName(_fromUtf8("tab_gcm_push_button_check_inputs"))
        self.verticalLayout_17.addWidget(self.tab_gcm_push_button_check_inputs)
        self.tab_gcm_push_button_apply_gcm = QtGui.QPushButton(self.frame_16)
        self.tab_gcm_push_button_apply_gcm.setObjectName(_fromUtf8("tab_gcm_push_button_apply_gcm"))
        self.verticalLayout_17.addWidget(self.tab_gcm_push_button_apply_gcm)
        self.tab_gcm_text_edit = QtGui.QTextEdit(self.frame_16)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tab_gcm_text_edit.setFont(font)
        self.tab_gcm_text_edit.setReadOnly(True)
        self.tab_gcm_text_edit.setObjectName(_fromUtf8("tab_gcm_text_edit"))
        self.verticalLayout_17.addWidget(self.tab_gcm_text_edit)
        self.verticalLayout_14.addWidget(self.frame_16)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_14.addItem(spacerItem1)
        self.horizontalLayout_7.addWidget(self.frame_11)
        self.frame_17 = QtGui.QFrame(self.frame_14)
        self.frame_17.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_17.setObjectName(_fromUtf8("frame_17"))
        self.verticalLayout_18 = QtGui.QVBoxLayout(self.frame_17)
        self.verticalLayout_18.setObjectName(_fromUtf8("verticalLayout_18"))
        self.tab_gcm_matplotlib_widget = MatplotlibWidget(self.frame_17)
        self.tab_gcm_matplotlib_widget.setObjectName(_fromUtf8("tab_gcm_matplotlib_widget"))
        self.verticalLayout_18.addWidget(self.tab_gcm_matplotlib_widget)
        self.frame_18 = QtGui.QFrame(self.frame_17)
        self.frame_18.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_18.setObjectName(_fromUtf8("frame_18"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.frame_18)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.tab_gcm_push_button_plot_overview_map = QtGui.QPushButton(self.frame_18)
        self.tab_gcm_push_button_plot_overview_map.setObjectName(_fromUtf8("tab_gcm_push_button_plot_overview_map"))
        self.horizontalLayout_8.addWidget(self.tab_gcm_push_button_plot_overview_map)
        self.tab_gcm_push_button_plot_zoomed_map = QtGui.QPushButton(self.frame_18)
        self.tab_gcm_push_button_plot_zoomed_map.setObjectName(_fromUtf8("tab_gcm_push_button_plot_zoomed_map"))
        self.horizontalLayout_8.addWidget(self.tab_gcm_push_button_plot_zoomed_map)
        self.verticalLayout_18.addWidget(self.frame_18)
        self.horizontalLayout_7.addWidget(self.frame_17)
        self.verticalLayout_6.addWidget(self.frame_14)
        self.main_tab_widget.addTab(self.tab_applygcm, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.main_tab_widget)
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
        self.main_tab_widget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.tab_watertxt_push_button_open_file.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open a WATER.txt output text file</p></body></html>", None))
        self.tab_watertxt_push_button_open_file.setText(_translate("MainWindow", "Open File", None))
        self.tab_watertxt_line_edit_open_file.setPlaceholderText(_translate("MainWindow", "Path to WATER.txt output text file", None))
        self.tab_watertxt_matplotlib_widget.setToolTip(_translate("MainWindow", "Plot of a parameter for selected WATER.txt output text file", None))
        self.tab_watertxt_list_widget.setToolTip(_translate("MainWindow", "List of column names for selected WATER.txt output text file", None))
        self.tab_watertxt_table_widget.setToolTip(_translate("MainWindow", "Table of values for selected WATER.txt output text file", None))
        self.tab_watertxt_table_widget.setSortingEnabled(False)
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_watertxt), _translate("MainWindow", "Process WATER output text file", None))
        self.tab_watertxtcmp_push_button_open_file1.setToolTip(_translate("MainWindow", "Open a WATER.txt output text file", None))
        self.tab_watertxtcmp_push_button_open_file1.setText(_translate("MainWindow", "Open File", None))
        self.tab_watertxtcmp_push_button_open_file2.setToolTip(_translate("MainWindow", "Open a WATER.txt output text file", None))
        self.tab_watertxtcmp_push_button_open_file2.setText(_translate("MainWindow", "Open File", None))
        self.tab_watertxtcmp_line_edit_open_file2.setPlaceholderText(_translate("MainWindow", "Path to WATER.txt output text file", None))
        self.tab_watertxtcmp_line_edit_open_file1.setPlaceholderText(_translate("MainWindow", "Path to WATER.txt output text file", None))
        self.tab_watertxtcmp_push_button_compare.setToolTip(_translate("MainWindow", "Compare selected WATER.txt output text files ", None))
        self.tab_watertxtcmp_push_button_compare.setText(_translate("MainWindow", "Compare", None))
        self.tab_watertxtcmp_matplotlib_widget.setToolTip(_translate("MainWindow", "Comparison plot of a parameter for selected WATER.txt output text file", None))
        self.tab_watertxtcmp_list_widget.setToolTip(_translate("MainWindow", "List of column names for selected WATER.txt output text files", None))
        self.tab_watertxtcmp_table_widget1.setToolTip(_translate("MainWindow", "Table of values for first selected WATER.txt output text file", None))
        self.tab_watertxtcmp_table_widget2.setToolTip(_translate("MainWindow", "Table of values for second selected WATER.txt output text file", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_watertxtcmp), _translate("MainWindow", "Compare 2 WATER output text files", None))
        self.tab_wateruse_group_box_num_sims.setTitle(_translate("MainWindow", "Number of simulation(s)", None))
        self.tab_wateruse_radio_button_one_sim.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>One batch or single WATER simulation.</p>\n"
"    <p>Example batch simulation:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>basin1/</li>\n"
"    <li>basin2/</li>\n"
"    <li>basin3/</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>Water.txt</li>\n"
"    <li>Watersheds.shp</li>\n"
"    </ul>\n"
"    </ul>\n"
"    <p>Example single simulation:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>amask/</li>\n"
"    <li>basinmask/</li>\n"
"    <li>fmask/</li>\n"
"    <li>info/</li>\n"
"    <li>rmask/</li>\n"
"    <li>Temp</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>basinMask.shp</li>\n"
"    <li>WATER.txt</li>\n"
"    <li>WATERSimulation.xml</li>\n"
"    </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_wateruse_radio_button_one_sim.setText(_translate("MainWindow", "One simulation", None))
        self.tab_wateruse_radio_button_multi_sims.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>Multiple WATER simulations. Simulations need to be contained in a single directory without any other files or directories except relevant simulation directories.</p>\n"
"    <p>Example of multiple batch simulations:</p>\n"
"    <ul>\n"
"        <li>simulations</li>\n"
"        <ul>\n"
"            <li>simulation1</li>\n"
"                <ul>\n"
"                <li>basin1/</li>\n"
"                <li>basin2/</li>\n"
"                <li>basin3/</li>\n"
"                <li>.</li>\n"
"                <li>.</li>\n"
"                <li>Water.txt</li>\n"
"                <li>Watersheds.shp</li>\n"
"                </ul>\n"
"            <li>simulation2</li>\n"
"                <ul>\n"
"                <li>basin1/</li>\n"
"                <li>basin2/</li>\n"
"                <li>basin3/</li>\n"
"                <li>.</li>\n"
"                <li>.</li>\n"
"                <li>Water.txt</li>\n"
"                <li>Watersheds.shp</li>\n"
"                </ul>\n"
"        </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_wateruse_radio_button_multi_sims.setText(_translate("MainWindow", "Multiple simulations", None))
        self.tab_wateruse_group_box_type_sims.setTitle(_translate("MainWindow", "Type of simulation(s)", None))
        self.tab_wateruse_radio_button_batch.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>A batch WATER simulation that has the following directory structure:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>basin1/</li>\n"
"    <li>basin2/</li>\n"
"    <li>basin3/</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>Water.txt</li>\n"
"    <li>Watersheds.shp</li>\n"
"    </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_wateruse_radio_button_batch.setText(_translate("MainWindow", "Batch", None))
        self.tab_wateruse_radio_button_single.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>A single WATER simulation that has the following directory structure:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>amask/</li>\n"
"    <li>basinmask/</li>\n"
"    <li>fmask/</li>\n"
"    <li>info/</li>\n"
"    <li>rmask/</li>\n"
"    <li>Temp</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>basinMask.shp</li>\n"
"    <li>WATER.txt</li>\n"
"    <li>WATERSimulation.xml</li>\n"
"    </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_wateruse_radio_button_single.setText(_translate("MainWindow", "Single", None))
        self.tab_wateruse_group_box_sim_info.setTitle(_translate("MainWindow", "Simulation Information", None))
        self.label_3.setText(_translate("MainWindow", "Basin shapefile name", None))
        self.tab_wateruse_line_edit_basin_shp.setToolTip(_translate("MainWindow", "Basin shapefile found in simulation directory.", None))
        self.tab_wateruse_line_edit_basin_shp.setPlaceholderText(_translate("MainWindow", "Watersheds.shp or basinMask.shp", None))
        self.label_4.setText(_translate("MainWindow", "Basin shapefile id field", None))
        self.label_5.setText(_translate("MainWindow", "Basin shapefile area field", None))
        self.tab_wateruse_push_button_open_sim.setToolTip(_translate("MainWindow", "Open a WATER simulation directory.", None))
        self.tab_wateruse_push_button_open_sim.setText(_translate("MainWindow", "Open directory", None))
        self.tab_wateruse_line_edit_open_sim.setToolTip(_translate("MainWindow", "Path of chosen simulation directory.", None))
        self.tab_wateruse_line_edit_open_sim.setPlaceholderText(_translate("MainWindow", "WATER simulation directory", None))
        self.tab_wateruse_combo_box_shp_id_field.setToolTip(_translate("MainWindow", "Basin shapefile fields.", None))
        self.tab_wateruse_combo_box_shp_area_field.setToolTip(_translate("MainWindow", "Basin shapefile fields.", None))
        self.tab_wateruse_group_box_wateruse_info.setTitle(_translate("MainWindow", "Water use information", None))
        self.label_6.setText(_translate("MainWindow", "Water use shapefile id field", None))
        self.tab_wateruse_line_edit_wateruse_factor_file.setPlaceholderText(_translate("MainWindow", "Water use factor file", None))
        self.tab_wateruse_push_button_wateruse_factor_file.setToolTip(_translate("MainWindow", "Open a water use factor file.", None))
        self.tab_wateruse_push_button_wateruse_factor_file.setText(_translate("MainWindow", "Open file", None))
        self.tab_wateruse_line_edit_wateruse_shp.setPlaceholderText(_translate("MainWindow", "Water use shapefile", None))
        self.tab_wateruse_push_button_wateruse_shp.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open a water use shapefile. </p></body></html>", None))
        self.tab_wateruse_push_button_wateruse_shp.setText(_translate("MainWindow", "Open file", None))
        self.tab_wateruse_push_button_wateruse_files.setToolTip(_translate("MainWindow", "Open 4 seasonal water use text files.  ", None))
        self.tab_wateruse_push_button_wateruse_files.setText(_translate("MainWindow", "Open files", None))
        self.tab_wateruse_combo_box_wateruse_shp_id_field.setToolTip(_translate("MainWindow", "Water use shapefile fields.", None))
        self.tab_wateruse_checkbox_subwateruse.setToolTip(_translate("MainWindow", "Check if applying substitute water use.", None))
        self.tab_wateruse_checkbox_subwateruse.setText(_translate("MainWindow", "Use substitute water use", None))
        self.tab_wateruse_push_button_check_inputs.setToolTip(_translate("MainWindow", "<html><head/><body><p>Makes sure all inputs were entered. Enables applying water use button and map plotting buttons.</p></body></html>", None))
        self.tab_wateruse_push_button_check_inputs.setText(_translate("MainWindow", "Check Inputs", None))
        self.tab_wateruse_push_button_apply_wateruse.setToolTip(_translate("MainWindow", "<html><head/><body><p>Applies water use to provided inputs.  </p><p>Process is run in a separate thread allowing interaction with other parts of GUI while processing occurs.</p></body></html>", None))
        self.tab_wateruse_push_button_apply_wateruse.setText(_translate("MainWindow", "Apply Water Use", None))
        self.tab_wateruse_push_button_plot_overview_map.setToolTip(_translate("MainWindow", "<html><head/><body><p>Plot an overview map of the basin(s).</p><p>Plotting is done in a separate thread allowing interaction with other parts of GUI while plotting occurs.</p></body></html>", None))
        self.tab_wateruse_push_button_plot_overview_map.setText(_translate("MainWindow", "Plot Overview Map", None))
        self.tab_wateruse_push_button_plot_zoomed_map.setToolTip(_translate("MainWindow", "<html><head/><body><p>Plot a zoomed in map of the basin(s).</p><p>Plotting is done in a separate thread allowing interaction with other parts of GUI while plotting occurs.</p></body></html>", None))
        self.tab_wateruse_push_button_plot_zoomed_map.setText(_translate("MainWindow", "Plot Zoomed Map", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_applywateruse), _translate("MainWindow", "Apply water use to WATER simulations", None))
        self.tab_gcm_group_box_num_sims.setTitle(_translate("MainWindow", "Number of simulation(s)", None))
        self.tab_gcm_radio_button_one_sims.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>One batch or single WATER simulation.</p>\n"
"    <p>Example batch simulation:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>basin1/</li>\n"
"    <li>basin2/</li>\n"
"    <li>basin3/</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>Water.txt</li>\n"
"    <li>Watersheds.shp</li>\n"
"    </ul>\n"
"    </ul>\n"
"    <p>Example single simulation:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>amask/</li>\n"
"    <li>basinmask/</li>\n"
"    <li>fmask/</li>\n"
"    <li>info/</li>\n"
"    <li>rmask/</li>\n"
"    <li>Temp</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>basinMask.shp</li>\n"
"    <li>WATER.txt</li>\n"
"    <li>WATERSimulation.xml</li>\n"
"    </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_gcm_radio_button_one_sims.setText(_translate("MainWindow", "One simulation", None))
        self.tab_gcm_radio_button_multi_sims.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>Multiple WATER simulations. Simulations need to be contained in a single directory without any other files or directories except relevant simulation directories.</p>\n"
"    <p>Example of multiple batch simulations:</p>\n"
"    <ul>\n"
"        <li>simulations</li>\n"
"        <ul>\n"
"            <li>simulation1</li>\n"
"                <ul>\n"
"                <li>basin1/</li>\n"
"                <li>basin2/</li>\n"
"                <li>basin3/</li>\n"
"                <li>.</li>\n"
"                <li>.</li>\n"
"                <li>Water.txt</li>\n"
"                <li>Watersheds.shp</li>\n"
"                </ul>\n"
"            <li>simulation2</li>\n"
"                <ul>\n"
"                <li>basin1/</li>\n"
"                <li>basin2/</li>\n"
"                <li>basin3/</li>\n"
"                <li>.</li>\n"
"                <li>.</li>\n"
"                <li>Water.txt</li>\n"
"                <li>Watersheds.shp</li>\n"
"                </ul>\n"
"        </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_gcm_radio_button_multi_sims.setText(_translate("MainWindow", "Multiple simulations", None))
        self.tab_gcm_group_box_type_sims.setTitle(_translate("MainWindow", "Type of simulation(s)", None))
        self.tab_gcm_radio_button_batch.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>A batch WATER simulation that has the following directory structure:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>basin1/</li>\n"
"    <li>basin2/</li>\n"
"    <li>basin3/</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>Water.txt</li>\n"
"    <li>Watersheds.shp</li>\n"
"    </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_gcm_radio_button_batch.setText(_translate("MainWindow", "Batch", None))
        self.tab_gcm_radio_button_single.setToolTip(_translate("MainWindow", "<html>\n"
"<head/>\n"
"<body>\n"
"    <p>A single WATER simulation that has the following directory structure:</p>\n"
"    <ul>\n"
"    <li>simulation</li>\n"
"    <ul>\n"
"    <li>amask/</li>\n"
"    <li>basinmask/</li>\n"
"    <li>fmask/</li>\n"
"    <li>info/</li>\n"
"    <li>rmask/</li>\n"
"    <li>Temp</li>\n"
"    <li>.</li>\n"
"    <li>.</li>\n"
"    <li>basinMask.shp</li>\n"
"    <li>WATER.txt</li>\n"
"    <li>WATERSimulation.xml</li>\n"
"    </ul>\n"
"    </ul>\n"
"</body>\n"
"</html>", None))
        self.tab_gcm_radio_button_single.setText(_translate("MainWindow", "Single", None))
        self.tab_gcm_group_box_sim_info.setTitle(_translate("MainWindow", "Simulation Information", None))
        self.label_7.setText(_translate("MainWindow", "Basin shapefile name", None))
        self.tab_gcm_line_edit_basin_shp.setToolTip(_translate("MainWindow", "Basin shapefile found in simulation directory.", None))
        self.tab_gcm_line_edit_basin_shp.setPlaceholderText(_translate("MainWindow", "Watersheds.shp or basinMask.shp", None))
        self.label_8.setText(_translate("MainWindow", "Basin shapefile id field", None))
        self.label_9.setText(_translate("MainWindow", "Basin shapefile area field", None))
        self.tab_gcm_push_button_open_sim.setToolTip(_translate("MainWindow", "Open a WATER simulation directory.", None))
        self.tab_gcm_push_button_open_sim.setText(_translate("MainWindow", "Open directory", None))
        self.tab_gcm_line_edit_open_sim.setToolTip(_translate("MainWindow", "Path of chosen simulation directory.", None))
        self.tab_gcm_line_edit_open_sim.setPlaceholderText(_translate("MainWindow", "WATER simulation directory", None))
        self.tab_gcm_combo_box_shp_id_field.setToolTip(_translate("MainWindow", "Basin shapefile fields.", None))
        self.tab_gcm_combo_box_shp_area_field.setToolTip(_translate("MainWindow", "Basin shapefile fields.", None))
        self.tab_gcm_group_box_gcm_info.setTitle(_translate("MainWindow", "Global climate model information", None))
        self.label_10.setText(_translate("MainWindow", "Global climate model shapefile id field", None))
        self.tab_gcm_line_edit_gcm_shp.setPlaceholderText(_translate("MainWindow", "Global climate model shapefile", None))
        self.tab_gcm_push_button_gcm_shp.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open a global climate model shapefile. </p></body></html>", None))
        self.tab_gcm_push_button_gcm_shp.setText(_translate("MainWindow", "Open file", None))
        self.tab_gcm_push_button_gcm_files.setToolTip(_translate("MainWindow", "Open 3 delta global climate model text files; Ppt.txt, Tmax.txt, PET.txt  ", None))
        self.tab_gcm_push_button_gcm_files.setText(_translate("MainWindow", "Open files", None))
        self.tab_gcm_combo_box_gcm_shp_id_field.setToolTip(_translate("MainWindow", "Water use shapefile fields.", None))
        self.tab_gcm_checkbox_subwateruse.setToolTip(_translate("MainWindow", "Check if applying substitute global climate model deltas.", None))
        self.tab_gcm_checkbox_subwateruse.setText(_translate("MainWindow", "Use substitute global climate model deltas", None))
        self.tab_gcm_push_button_check_inputs.setToolTip(_translate("MainWindow", "<html><head/><body><p>Makes sure all inputs were entered. Enables applying global climate model deltas button and map plotting buttons.</p></body></html>", None))
        self.tab_gcm_push_button_check_inputs.setText(_translate("MainWindow", "Check Inputs", None))
        self.tab_gcm_push_button_apply_gcm.setToolTip(_translate("MainWindow", "<html><head/><body><p>Applies water use to provided inputs.  </p><p>Process is run in a separate thread allowing interaction with other parts of GUI while processing occurs.</p></body></html>", None))
        self.tab_gcm_push_button_apply_gcm.setText(_translate("MainWindow", "Apply Global Climate Model Deltas", None))
        self.tab_gcm_push_button_plot_overview_map.setToolTip(_translate("MainWindow", "<html><head/><body><p>Plot an overview map of the basin(s).</p><p>Plotting is done in a separate thread allowing interaction with other parts of GUI while plotting occurs.</p></body></html>", None))
        self.tab_gcm_push_button_plot_overview_map.setText(_translate("MainWindow", "Plot Overview Map", None))
        self.tab_gcm_push_button_plot_zoomed_map.setToolTip(_translate("MainWindow", "<html><head/><body><p>Plot a zoomed in map of the basin(s).</p><p>Plotting is done in a separate thread allowing interaction with other parts of GUI while plotting occurs.</p></body></html>", None))
        self.tab_gcm_push_button_plot_zoomed_map.setText(_translate("MainWindow", "Plot Zoomed Map", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_applygcm), _translate("MainWindow", "Apply global climate model (GCM) deltas to WATER simulations", None))
        self.menuExit.setTitle(_translate("MainWindow", "Exit", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+H", None))

from matplotlibwidget import MatplotlibWidget
