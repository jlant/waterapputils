import sys, os
from PyQt4 import QtGui, QtCore
import osgeo.ogr
import osgeo.osr
from gui.user_interface import Ui_MainWindow
from modules import watertxt
from modules import helpers
from modules import spatialvectors
from modules import wateruse_processing
import user_settings

# my modules
class MainWindow(QtGui.QMainWindow):
	""" Subclass of QMainWindow that creates the main window """

	def __init__(self, parent = None):

		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("WATERAPPUTILS GUI")

		# water text file tab
		self.tab_watertxt_data = None
		self.filepath = None
		self.filename = None
		self.filedir = None

		# water text file comparison tab
		self.tab_watertxtcmp_data1 = None
		self.tab_watertxtcmp_data2 = None
		self.filepath1 = None
		self.filename1 = None
		self.filedir1 = None
		self.filepath2 = None
		self.filename2 = None
		self.filedir2 = None

		# water use tab
		self.tab_wateruse_sim_dir = None
		self.is_batch_simulation = None

		self.tab_wateruse_basin_shp_path = None
		self.tab_wateruse_basin_shp_dir = None		
		self.tab_wateruse_basin_shp_file = None		
		self.tab_wateruse_basin_shp_id_field = None
		self.tab_wateruse_basin_shp_area_field = None
		self.tab_wateruse_basin_shp_dict = None

		self.tab_wateruse_wateruse_data_files = None
		self.tab_wateruse_wateruse_factor_file_path = None

		self.tab_wateruse_centroids_shp_path = None
		self.tab_wateruse_centroids_shp_dir = None
		self.tab_wateruse_centroids_shp_file = None
		self.tab_wateruse_centroids_shp_id_field = None
		self.tab_wateruse_centroids_shp_dict = None

		# set up the ui
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) # method in *_ui.py file of the Ui_MainWindow class

		# connections for tab titled Process WATER output text file 
		self.ui.actionExit.triggered.connect(self.close)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.tab_watertxt_push_button_open_file.clicked.connect(self.process_watertxt_file)
		self.ui.tab_watertxt_list_widget.itemSelectionChanged.connect(self.plot_tab_watertxt_list_item)

		# connections for tab titled Compare 2 WATER output text files
		self.ui.tab_watertxtcmp_push_button_open_file1.clicked.connect(self.select_watertxt_file_cmp)
		self.ui.tab_watertxtcmp_push_button_open_file2.clicked.connect(self.select_watertxt_file_cmp)
		self.ui.tab_watertxtcmp_push_button_compare.clicked.connect(self.compare_watertxt_files)
		self.ui.tab_watertxtcmp_list_widget.itemSelectionChanged.connect(self.plot_tab_watertxtcmp_list_item)

		# connections for tab titled Apply water use to WATER simulation(s)
		self.ui.tab_wateruse_push_button_open_sim.clicked.connect(self.select_water_sim)
		self.ui.tab_wateruse_push_button_wateruse_files.clicked.connect(self.select_wateruse_files)
		self.ui.tab_wateruse_push_button_wateruse_factor_file.clicked.connect(self.select_wateruse_factor_file)
		self.ui.tab_wateruse_push_button_wateruse_shp.clicked.connect(self.select_wateruse_shp_file)
		self.ui.tab_wateruse_push_button_apply_wateruse.clicked.connect(self.apply_wateruse)
		self.ui.tab_wateruse_push_button_check_inputs.clicked.connect(self.check_wateruse_inputs)

		self.ui.tab_wateruse_combo_box_shp_id_field.activated['QString'].connect(self.handleActivated)
		self.ui.tab_wateruse_combo_box_shp_area_field.currentIndexChanged['QString'].connect(self.handleChanged)


		# disble the plot area until a file is opened 
		self.ui.tab_watertxt_matplotlib_widget.setEnabled(False)
		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(False)

		# disable compare button until both line edit boxes have text
		self.ui.tab_watertxtcmp_push_button_compare.setEnabled(False)

		# disable apply wateruse button until all proper input exists
		self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

	#-------------------------------- Tab: Process WATER output text file ------------------------------------

	def process_watertxt_file(self):
		""" Open a file dialog to select, read, display column names, and plot a WATER.txt file."""
		try:
			self.filepath = self.select_watertxt_file()
			if self.filepath:

				self.filedir, self.filename = helpers.get_file_info(str(self.filepath))

				self.update_status_bar(msg = "Processing: {}".format(self.filename))

				self.tab_watertxt_data = self.read_watertxt_file(self.filepath)

				self.add_to_list_widgets(widget_names = ["tab_watertxt_list_widget"], items = self.tab_watertxt_data["column_names"])
				self.add_to_table_widgets(widget_names = ["tab_watertxt_table_widget"], data_list = [self.tab_watertxt_data])

				self.setup_tab_watertxt_matplotlib_widget()
				self.plot_on_tab_watertxt_matplotlib_widget(parameter_name = self.tab_watertxt_data["column_names"][0])		# plot the first parameter in column names

				self.update_status_bar()

		except IOError as error:
			print("Error: {}".format(error.message))

	def select_watertxt_file(self):
		""" Open a QtDialog to select a WATER.txt file and show the file in the line edit widget """

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a WATER.txt file", directory = "../data/watertxt-datafiles/", filter = "Text files (*.txt);; All files (*.*)")	
		if filepath:
			self.ui.tab_watertxt_line_edit_open_file.setText(filepath)

		return filepath

	def setup_tab_watertxt_matplotlib_widget(self):
		""" Setup the matplotlib widget """

		self.ui.tab_watertxt_matplotlib_widget.setup_watertxt_plot()

	def plot_on_tab_watertxt_matplotlib_widget(self, parameter_name):
		""" Plot data from self.tab_watertxt_data to matplotlibe widget on the watertxt tab """

		self.ui.tab_watertxt_matplotlib_widget.setEnabled(True)
		self.ui.tab_watertxt_matplotlib_widget.plot_watertxt_parameter(watertxt_data = self.tab_watertxt_data, name = parameter_name)

	def plot_tab_watertxt_list_item(self):
		""" Plot the item selected in the list widget """
		
		item_type = str(self.ui.tab_watertxt_list_widget.currentItem().text())
		self.plot_on_tab_watertxt_matplotlib_widget(parameter_name = item_type)


	#-------------------------------- Tab: Compare 2 WATER output text files ------------------------------------

	def select_watertxt_file_cmp(self):
		""" Open a QtDialog to select a WATER.txt file and show the file in the line edit widget """

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a WATER.txt file", directory = "../data/watertxt-datafiles/", filter = "Text files (*.txt);; All files (*.*)")

		sender = self.sender()
		sender_object_name = sender.objectName()

		if sender_object_name == "tab_watertxtcmp_push_button_open_file1":
			self.ui.tab_watertxtcmp_line_edit_open_file1.setText(filepath)

		elif sender_object_name == "tab_watertxtcmp_push_button_open_file2":
			self.ui.tab_watertxtcmp_line_edit_open_file2.setText(filepath)

		# enable compare button if both line edit boxes have text
		if self.ui.tab_watertxtcmp_line_edit_open_file1.text() and self.ui.tab_watertxtcmp_line_edit_open_file2.text():
			self.ui.tab_watertxtcmp_push_button_compare.setEnabled(True)
		

	def compare_watertxt_files(self):
		""" Compare two WATER.txt files """ 
		try:
			
			self.filepath1 = self.ui.tab_watertxtcmp_line_edit_open_file1.text()
			self.filepath2 = self.ui.tab_watertxtcmp_line_edit_open_file2.text()

			self.filedir1, self.filename1 = helpers.get_file_info(str(self.filepath1))
			self.filedir2, self.filename2 = helpers.get_file_info(str(self.filepath2))

			self.update_status_bar(msg = "Processing: {} and {}".format(self.filename1, self.filename2))

			self.tab_watertxtcmp_data1 = self.read_watertxt_file(filepath = self.filepath1)
			self.tab_watertxtcmp_data2 = self.read_watertxt_file(filepath = self.filepath2)

			self.validate_watertxt_data_for_comparison(data_list = [self.tab_watertxtcmp_data1, self.tab_watertxtcmp_data2], filepaths = [self.filepath1, self.filepath2])

			self.add_to_list_widgets(widget_names = ["tab_watertxtcmp_list_widget"], items = self.tab_watertxtcmp_data1["column_names"])
			self.add_to_table_widgets(widget_names = ["tab_watertxtcmp_table_widget1", "tab_watertxtcmp_table_widget2"], data_list = [self.tab_watertxtcmp_data1, self.tab_watertxtcmp_data2])

			self.setup_tab_watertxtcmp_matplotlib_widget()
			self.plot_on_tab_watertxtcmp_matplotlib_widget(data_list = [self.tab_watertxtcmp_data1, self.tab_watertxtcmp_data2], filenames = [self.filename1, self.filename2], parameter_name = self.tab_watertxtcmp_data1["column_names"][0])		

			self.update_status_bar()

		except IOError as error:
			print("Error: {}".format(error.message))

		except AssertionError as error:
			print("Error: {}".format(error.message))

	def setup_tab_watertxtcmp_matplotlib_widget(self):
		""" Setup the matplotlib widget """

		self.ui.tab_watertxtcmp_matplotlib_widget.setup_watertxtcmp_plot()

	def plot_on_tab_watertxtcmp_matplotlib_widget(self, data_list, filenames, parameter_name,):
		""" Plot data from self.tab_watertxt_data to matplotlibe widget on the watertxt tab """

		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(True)
		self.ui.tab_watertxtcmp_matplotlib_widget.plot_watertxtcmp_parameter(watertxt_data1 = data_list[0], watertxt_data2 = data_list[1], 
																			 filename1 = filenames[0], filename2 = filenames[1],
																			 name = parameter_name
		)

	def plot_tab_watertxtcmp_list_item(self):
		""" Plot the item selected in the list widget """
		
		item_type = str(self.ui.tab_watertxtcmp_list_widget.currentItem().text())
		self.plot_on_tab_watertxtcmp_matplotlib_widget(data_list = [self.tab_watertxtcmp_data1, self.tab_watertxtcmp_data2], filenames = [self.filename1, self.filename2], parameter_name = item_type)

	#-------------------------------- Tab: Apply water use to WATER simulation(s) ------------------------------------


	def check_wateruse_inputs(self):
		""" validate water use inputs """

		self.tab_wateruse_basin_shp_id_field = str(self.ui.tab_wateruse_combo_box_shp_id_field.currentText())
		self.tab_wateruse_basin_shp_area_field = str(self.ui.tab_wateruse_combo_box_shp_area_field.currentText())
		self.tab_wateruse_centroids_shp_id_field = str(self.ui.tab_wateruse_combo_box_wateruse_shp_id_field.currentText())

		wateruse_inputs = [
			{"Simulation Directory" : self.tab_wateruse_sim_dir},

			{"Basin Shapefile": self.tab_wateruse_basin_shp_file},
			{"Basin Shapefile Id Field": self.tab_wateruse_basin_shp_id_field},
			{"Basin Shapefile Area Field": self.tab_wateruse_basin_shp_area_field},
			{"Water Use Data Files": self.tab_wateruse_wateruse_data_files},

			{"Water Use Factor File": self.tab_wateruse_wateruse_factor_file_path},
			{"Water Use Shapefile": self.tab_wateruse_centroids_shp_path},
			{"Water Use Shapefile Id Field": self.tab_wateruse_centroids_shp_id_field}
		]

		valid_list = []
		for wateruse_input in wateruse_inputs:
			print(wateruse_input)
			if not wateruse_input.values()[0]:
				valid_list.append(False)
				error_msg = "Empty input!<br />Need the following input(s):<br /><br />{}<br /><br />Please provide proper inputs.".format(wateruse_input.keys()[0])
				self.popup_error(parent = self, msg = error_msg)
			else:
				valid_list.append(True)

		if False in valid_list:
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)
		else:
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(True)

	def display_text(self):
		""" Display text in text edit area """

		info_dir = settings["info_directory_name"]
		info_file = info_dir + "/" + settings["wateruse_info_file_name"]
		ecoflow_dir = settings["ecoflow_directory_name"]
		oasis_dir = settings["oasis_directory_name"]

		msg = "Please see output directories and files located in chosen simulation directory:<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />Additional output is located in each respective basin directory within the chosen simulation directory".format(self.tab_wateruse_sim_dir, info_dir, info_file, ecoflow_dir, oasis_dir)

		self.ui.tab_wateruse_text_edit.setHtml(msg)
		self.ui.tab_wateruse_text_edit.toHtml()

	def apply_wateruse(self):
		""" Apply water use using data provided on water use tab """

		try:

			settings = user_settings.settings 

			# over write the settings in user_settings.py with values from gui
			settings["simulation_directory"] = self.tab_wateruse_sim_dir			
			settings["is_batch_simulation"] = self.is_batch_simulation

			settings["basin_shapefile_name"] = self.tab_wateruse_basin_shp_file
			settings["basin_shapefile_id_field"] = self.tab_wateruse_basin_shp_id_field			
			settings["basin_shapefile_area_field"] = self.tab_wateruse_basin_shp_area_field

			settings["wateruse_files"] = self.tab_wateruse_wateruse_data_files
			settings["wateruse_factor_file"] = self.tab_wateruse_wateruse_factor_file_path
			settings["wateruse_centroids_shapefile"] = self.tab_wateruse_centroids_shp_path
			settings["wateruse_centroids_shapefile_id_field"] = self.tab_wateruse_centroids_shp_id_field

			# wateruse_processing.apply_wateruse(settings = settings)

			# reset button
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

			# display text in text edit
			self.display_text()

		except (IOError, AssertionError, ValueError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

	def select_water_sim(self):
		""" Open a QtDialog to select a WATER simulation directory and show the directory in the line edit widget """

		try:

			dirpath = QtGui.QFileDialog.getExistingDirectory(self, caption = "Please select a WATER simulation directory", directory = "../data/sample-water-simulations/")

			if dirpath:
				self.tab_wateruse_sim_dir = str(dirpath)
				self.ui.tab_wateruse_line_edit_open_sim.setText(self.tab_wateruse_sim_dir)
				self.populate_sim_info(sim_dirpath = self.tab_wateruse_sim_dir)

		except IOError as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_wateruse_line_edit_open_sim.clear()

	def populate_sim_info(self, sim_dirpath):
		""" Populate the widgets in simulation info group box"""

		tmp_shp_file = None

		if self.ui.tab_wateruse_radio_button_batch.isChecked():
			self.is_batch_simulation = True
			tmp_shp_file = "Watersheds.shp"

		elif self.ui.tab_wateruse_radio_button_single.isChecked():
			self.is_batch_simulation = False
			tmp_shp_file = "basinMask.shp"

		# find the basin shapefile before populating widgets
		if tmp_shp_file:
			self.tab_wateruse_basin_shp_path = helpers.find_file(name = tmp_shp_file, path = sim_dirpath)
			
			self.tab_wateruse_basin_shp_dir, self.tab_wateruse_basin_shp_file = helpers.get_file_info(self.tab_wateruse_basin_shp_path) 
			self.ui.tab_wateruse_line_edit_basin_shp.setText(self.tab_wateruse_basin_shp_file)

			# get fields
			basin_shapefile = osgeo.ogr.Open(self.tab_wateruse_basin_shp_path)  
			self.tab_wateruse_basin_shp_dict = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

			fields_str = " ".join(self.tab_wateruse_basin_shp_dict["fields"])
			self.ui.tab_wateruse_combo_box_shp_id_field.addItems(fields_str.split())
			self.ui.tab_wateruse_combo_box_shp_area_field.addItems(fields_str.split())

	def select_wateruse_files(self):
		""" Open a QtDialog to select water use files and show the files in the list widget """

		wateruse_files_qtstr_list = QtGui.QFileDialog.getOpenFileNames(self, caption = "Please select 4 seasonal water use files", directory = "../data/wateruse-datafiles", filter = "Text files (*.txt);; All files (*.*)")
		wateruse_files_str = str(wateruse_files_qtstr_list.join(","))
		self.tab_wateruse_wateruse_data_files = wateruse_files_str.split(",")		# convert QtStringList to a Python list
	
		if len(self.tab_wateruse_wateruse_data_files) != 4:
			error_msg = "Need 4 seasonal water use files! <br />Number of files selected: {}.<br />{}<br />Please select 4 seasonal water use files.".format(len(self.tab_wateruse_wateruse_data_files), self.tab_wateruse_wateruse_data_files)
			self.popup_error(parent = self, msg = error_msg)
		else:
			self.add_to_list_widgets(widget_names = ["tab_wateruse_list_widget_wateruse_files"], items = self.tab_wateruse_wateruse_data_files)

	def select_wateruse_factor_file(self):
		""" Open a QtDialog to select water use factor file and show the files in the line edit widget"""

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a water use factor file", directory = "../data/wateruse-datafiles/", filter = "Text files (*.txt);; All files (*.*)")	

		if filepath:
			self.tab_wateruse_wateruse_factor_file_path = str(filepath)
			self.ui.tab_wateruse_line_edit_wateruse_factor_file.setText(self.tab_wateruse_wateruse_factor_file_path)		

	def select_wateruse_shp_file(self):
		""" Open a QtDialog to select water use shapefile"""

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a water use shapefile", directory = "../data/spatial-datafiles/wateruse-centroids", filter = "Shapefile (*.shp)")	

		if filepath:
			self.ui.tab_wateruse_line_edit_wateruse_shp.setText(filepath)
			self.tab_wateruse_centroids_shp_path = str(filepath)
			self.tab_wateruse_centroids_shp_dir, self.tab_wateruse_centroids_shp_file = helpers.get_file_info(self.tab_wateruse_centroids_shp_path) 

			# get fields
			wateruse_shapefile = osgeo.ogr.Open(self.tab_wateruse_centroids_shp_path)  
			self.tab_wateruse_centroids_shp_dict = spatialvectors.fill_shapefile_dict(shapefile = wateruse_shapefile)

			fields_str = " ".join(self.tab_wateruse_centroids_shp_dict["fields"])
			self.ui.tab_wateruse_combo_box_wateruse_shp_id_field.addItems(fields_str.split())


	def handleActivated(self, text):
		print('handleActivated: %s' % text)

	def handleChanged(self, text):
		print('handleChanged: %s' % text)


	#-------------------------------- Tab Independent Methods ------------------------------------

	def read_watertxt_file(self, filepath):
		""" Read a WATER.txt file """

		watertxt_data = watertxt.read_file(filepath = filepath)
		self.validate_watertxt_data(watertxt_data = watertxt_data, filepath = filepath)

		return watertxt_data

	def add_to_table_widgets(self, widget_names, data_list):
		""" Add first WATER output text file to table widget """

		for i in range(len(widget_names)):
			# get the widget object by finding the child object of the main QWidget
			table_widget = self.findChild(QtGui.QWidget, widget_names[i])								
			data_values = self.format_data_for_table(watertxt_data = data_list[i])

			nrows = len(data_values)
			ncols = len(data_values[0])

			table_widget.setRowCount(nrows)
			table_widget.setColumnCount(ncols)
			table_widget.setHorizontalHeaderLabels(["Date"] + data_list[i]["column_names"])

			for row in range(nrows):
				for col in range(ncols):
					table_widget.setItem(row, col, QtGui.QTableWidgetItem(data_values[row][col]))

	def add_to_list_widgets(self, widget_names, items):
		""" Add first WATER output text file to table widget """

		for i in range(len(widget_names)):
			# get the widget object by finding the child object of the main QWidget
			list_widget = self.findChild(QtGui.QWidget, widget_names[i])								
			list_widget.clear()
			list_widget.addItems(items)

	def format_data_for_table(self, watertxt_data):
		""" Format the watertxt data into a list of lists with string elements for the table """

		# get the dates and all the values
		dates = watertxt_data["dates"]
		values_all = watertxt.get_all_values(watertxt_data = watertxt_data)

		nrows = len(dates)
		ncols = len(values_all)

		# format the dates to strings of mm/dd/yyyy
		dates_fmt = []
		for i in range(nrows):
			date_str = dates[i].strftime("%m/%d/%Y")
			dates_fmt.append(date_str)

		# format the data into a list of lists [[row1], [row2], ...]
		data_fmt = []
		for i in range(nrows):
			row = []
			for j in range(ncols):
				data_str = "{:.2f}".format((values_all[j][i]))		# convert value to a formatted string of 2 decimals
				row.append(data_str)							
			data_fmt.append(row)

		# merge dates and data values into a single list
		data_all = []
		for i in range(nrows):
			new_row = [dates_fmt[i]] + data_fmt[i]
			data_all.append(new_row)

		return data_all


	def validate_watertxt_data(self, watertxt_data, filepath):
		""" Check and make sure that watertxt_data is valid """ 

		error_msg = "Invalid file! <br />{}<br />Please choose a valid WATER output text file.".format(filepath)

		if watertxt_data["parameters"] == [] or watertxt_data["column_names"] == None:
			self.raise_error_clear_widgets(parent = self, msg = error_msg)

	def validate_column_names(self, parent, column_names, filepaths):
		""" Validate the equality between column_names """

		error_msg = \
		"""
		Column names do not match between files! <br />
		<br />
		{}:<br />
		<br />
		{}<br />
		<br />
		{}:<br />
		<br />
		{}<br />
		<br />
		Please choose valid WATER output text files.		
		""".format(filepaths[0], column_names[0], filepaths[1], column_names[1])

		# check column names
		if not column_names[0] == column_names[1]:
			self.raise_error_clear_widgets(parent = self, msg = error_msg)

	def validate_dates(self, parent, dates, filepaths):
		""" Validate the equality between column_names """

		# check dates
		start_dates = [dates[0][0], dates[1][0]]
		end_dates = [dates[1][-1], dates[1][-1]]

		error_msg = \
		"""
		Dates do not match between files! <br />
		<br />
		{}:<br />
		<br />
		Start date: {}<br />
		End date: {}<br />
		<br />
		{}:<br />
		<br />
		Start date: {}<br />
		End date: {}<br />
		<br />
		Please choose valid WATER output text files.		
		""".format(filepaths[0], start_dates[0], end_dates[0], filepaths[1], start_dates[1], end_dates[1])

		# check column names
		if not set(dates[0]) == set(dates[1]):
			self.raise_error_clear_widgets(parent = self, msg = error_msg)			

	def validate_watertxt_data_for_comparison(self, data_list, filepaths):
		""" Check and make sure that both watertxt_data dictionaries can be compared """ 

		column_names = [data_list[0]["column_names"], data_list[1]["column_names"]]
		dates = [data_list[0]["dates"], data_list[1]["dates"]]

		# check column names
		self.validate_column_names(parent = self, column_names = column_names, filepaths = filepaths)

		# check dates
		self.validate_dates(parent = self, dates = dates, filepaths = filepaths)


	def raise_error_clear_widgets(self, parent, msg):
		""" Raise the error """

		self.popup_error(parent, msg)

		sender = self.sender()
		sender_object_name = sender.objectName()
		self.clear_widgets(sender_name = sender_object_name)

		raise IOError(msg)

	def popup_error(self, parent, msg):
		""" Display an error message box """

		title = "ERROR"
		QtGui.QMessageBox.critical(parent, title, msg, QtGui.QMessageBox.Close)

	def clear_widgets(self, sender_name):
		""" Clear the appropriate widgets """

		if sender_name == "tab_watertxt_push_button_open_file":
			self.clear_tab_watertxt_widgets()

		elif sender_name == "tab_watertxtcmp_push_button_compare":
			self.clear_tab_watertxtxmp_widgets()

	def clear_tab_watertxt_widgets(self):
		""" Clear widgets on watertxt tab """

		self.ui.tab_watertxt_list_widget.clear()
		self.ui.tab_watertxt_table_widget.clear()
		self.ui.tab_watertxt_matplotlib_widget.clear_watertxt_plot()			
		self.ui.tab_watertxt_matplotlib_widget.setEnabled(False)

	def clear_tab_watertxtxmp_widgets(self):
		""" Clear widgets on watertxtcmp tab """

		self.ui.tab_watertxtcmp_list_widget.clear()
		self.ui.tab_watertxtcmp_table_widget1.clear()
		self.ui.tab_watertxtcmp_table_widget2.clear()
		self.ui.tab_watertxtcmp_matplotlib_widget.clear_watertxtcmp_plot()			
		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(False)
		self.ui.tab_watertxtcmp_push_button_compare.setEnabled(False)

	def about(self):
		""" Show an message box about the gui."""
		
		msg = \
		"""
		The waterapputils gui can be used to process and interact with output <br /> 
		and database files from the WATER application. In addition, water use can <br />
		be applied to WATER output text files and global climate change factors can <br />
		be applied to WATER database xml files.  More help and information <br />
		can be found at the <a href="https://github.com/jlant-usgs/waterapputils/">GitHub site for waterapputils</a>. 
		"""

		QtGui.QMessageBox.about(self, "About the waterapputils gui", msg.strip())

	def update_status_bar(self, msg = ""):
		""" Update the status bar """

		self.ui.statusbar.clearMessage()
		self.ui.statusbar.showMessage(msg)

def main():
	""" Run application """

	app = QtGui.QApplication(sys.argv)		# create application object
	main_window = MainWindow()				# create main window object
	main_window.show()			
	main_window.raise_()					# raise window to top of stack						
	sys.exit(app.exec_())					# monitor application for events


if __name__ == "__main__":
	main()
