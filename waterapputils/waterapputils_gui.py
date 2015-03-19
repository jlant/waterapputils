import sys, os
from PyQt4 import QtGui, QtCore
import osgeo.ogr
import osgeo.osr
from gui.user_interface import Ui_MainWindow
from modules import watertxt
from modules import helpers
from modules import spatialvectors
from modules import wateruse_processing
from modules import gcm_delta_processing
from modules import map_processing
import user_settings

import time

class Worker(QtCore.QObject):
	""" 
	Object that does the work of applying water use. 
	Note that a QPixmap warning is spawned while matplotlib plots using pyplot (plt.plot).
	This warning can be fixed by doing plots with Figure() and FigureCanvas() which are used for gui's.
	Here, using same plotting code as the command line program, so warning still occurs.  Can fix this in future if need be.
	"""
	starting = QtCore.pyqtSignal(["QString"])
	finished = QtCore.pyqtSignal(["QString"])

	@QtCore.pyqtSlot(dict)
	def process_wateruse(self, settings):
		""" Process water use """

		self.starting.emit("Processing water use ... this may take some time ... please wait.")

		# apply wateruse
		wateruse_processing.apply_wateruse(settings = settings)			

		self.finished.emit("Finished processing water use.")

	@QtCore.pyqtSlot(dict)
	def process_subwateruse(self, settings):
		""" Process substitute water use """

		self.starting.emit("Processing substitute water use ... this may take some time ... please wait.")

		# apply substitute wateruse
		wateruse_processing.apply_subwateruse(settings = settings)			

		self.finished.emit("Finished processing substitute water use.")

	@QtCore.pyqtSlot(dict)
	def process_multi_wateruse(self, settings):
		""" Process water use """

		dir_parent = settings["simulation_directory"]
		for dir_name in os.listdir(dir_parent):
			dir_path = os.path.join(dir_parent, dir_name)
			if os.path.isdir(dir_path):
				settings["simulation_directory"] = dir_path
				self.starting.emit("Processing water use ... this may take some time ... please wait.")
				wateruse_processing.apply_wateruse(settings = settings)	
				self.finished.emit("Finished processing water use.")

	@QtCore.pyqtSlot(dict)
	def process_multi_subwateruse(self, settings):
		""" Process water use """

		dir_parent = settings["simulation_directory"]
		for dir_name in os.listdir(dir_parent):
			dir_path = os.path.join(dir_parent, dir_name)
			if os.path.isdir(dir_path):
				settings["simulation_directory"] = dir_path
				wateruse_non_intersecting_file_name = os.path.join(settings["simulation_directory"], settings["info_directory_name"], settings["wateruse_non_intersecting_file_name"])
				if os.path.isfile(wateruse_non_intersecting_file_name):
					self.starting.emit("Processing substitute water use ... this may take some time ... please wait.")
					wateruse_processing.apply_subwateruse(settings = settings)
					self.finished.emit("Finished processing substitute water use.")
				else:
					error_msg = "Substitute water use file does not exist. Please make sure the the following file exists: <br /> <br />{}".format(wateruse_non_intersecting_file_name)
					self.finished.emit(error_msg)				
	
	@QtCore.pyqtSlot(dict)
	def process_gcm(self, settings):
		""" Process global climate model deltas """

		self.starting.emit("Processing global climate model deltas ... this may take some time ... please wait.")

		# apply global climate deltas
		gcm_delta_processing.apply_gcm_deltas(settings = settings)			

		self.finished.emit("Finished processing global climate model deltas.")

	@QtCore.pyqtSlot(dict)
	def process_subgcm(self, settings):
		""" Process substitute global climate model deltas """

		self.starting.emit("Processing substitute global climate model deltas ... this may take some time ... please wait.")

		# apply substitute global climate deltas
		gcm_delta_processing.apply_sub_gcm_deltas(settings = settings)			

		self.finished.emit("Finished processing substitute global climate model deltas.")

	@QtCore.pyqtSlot(dict)
	def process_multi_gcm(self, settings):
		""" Process global climate model deltas """

		dir_parent = settings["simulation_directory"]
		for dir_name in os.listdir(dir_parent):
			dir_path = os.path.join(dir_parent, dir_name)
			if os.path.isdir(dir_path):
				settings["simulation_directory"] = dir_path
				self.starting.emit("Processing global climate model deltas ... this may take some time ... please wait.")
				gcm_delta_processing.apply_gcm_deltas(settings = settings)	
				self.finished.emit("Finished processing global climate model deltas.")

	@QtCore.pyqtSlot(dict)
	def process_multi_subwateruse(self, settings):
		""" Process water use """

		dir_parent = settings["simulation_directory"]
		for dir_name in os.listdir(dir_parent):
			dir_path = os.path.join(dir_parent, dir_name)
			if os.path.isdir(dir_path):
				settings["simulation_directory"] = dir_path
				gcm_delta_non_intersecting_file_name = os.path.join(settings["simulation_directory"], settings["info_directory_name"], settings["gcm_delta_non_intersecting_file_name"])
				if os.path.isfile(gcm_non_intersecting_file_name):
					self.starting.emit("Processing substitute global climate model deltas ... this may take some time ... please wait.")
					gcm_delta_processing.apply_sub_gcm_deltas(settings = settings)
					self.finished.emit("Finished processing substitute global climate model deltas.")
				else:
					error_msg = "Substitute water use file does not exist. Please make sure the the following file exists: <br /> <br />{}".format(gcm_delta_non_intersecting_file_name)
					self.finished.emit(error_msg)	


class MapWorker(QtCore.QObject):
	""" 
	Object that does the work of drawing map.
	"""
	starting = QtCore.pyqtSignal(["QString"])
	finished = QtCore.pyqtSignal(["QString"])

	@QtCore.pyqtSlot(dict, object)
	def draw_overview_map(self, settings, matplotlib_widget):
		""" Draw overview map """

		self.starting.emit("Drawing map ... this may take a few moments ... please wait.")

		files_list = [
			settings["water_shapefiles"]["drbbasin"]["path"],										# path to drb basin
			os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"]),		# path to basin shapefile for a simulation
		]

		# get necessary parameters for plot
		shp_info_list, display_fields, colors = map_processing.get_shps_colors_fields(files_list, settings)

		# do not display fields for basin shapefile
		display_fields[1] = ""

		# plot
		matplotlib_widget.plot_shapefiles_map(
			shapefiles = shp_info_list, 
			display_fields = display_fields, 
			colors = colors, 
			title = None, 
			shp_name = None, 
			buff = settings["map_buffer_overview"],
		)

		self.finished.emit("Finished drawing map.")

	@QtCore.pyqtSlot(dict, object)
	def draw_zoomed_map(self, settings, matplotlib_widget):
		""" Draw zoomed map """

		self.starting.emit("Drawing map ... this may take a few moments ... please wait.")

		files_list = [
			settings["water_shapefiles"]["drbbasin"]["path"],										# path to drb basin
			os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"]),		# path to basin shapefile for a simulation
			settings["water_shapefiles"]["strm"]["path"],								    		# path to streams shapefile
			settings["water_shapefiles"]["rsvr"]["path"],								    		# path to reservoir shapefile
			settings["water_shapefiles"]["usgsgages"]["path"],							    		# path to usgs gages shapefile
		]

		# get necessary parameters for plot
		shp_info_list, display_fields, colors = map_processing.get_shps_colors_fields(files_list, settings)

		# plot
		matplotlib_widget.plot_shapefiles_map(
			shapefiles = shp_info_list, 
			display_fields = display_fields, 
			colors = colors, 
			title = None, 
			shp_name = os.path.splitext(settings["basin_shapefile_name"])[0], 
			buff = settings["map_buffer_zoomed"],
		)

		self.finished.emit("Finished drawing map.")


	@QtCore.pyqtSlot(dict, object)
	def draw_gcm_overview_map(self, settings, matplotlib_widget):
		""" Draw overview map """
		print(settings["gcm_delta_tile_shapefile"])
		self.starting.emit("Drawing map ... this may take a few moments ... please wait.")

		files_list = [
			settings["water_shapefiles"]["drbbasin"]["path"],										# path to drb basin
			os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"]),		# path to basin shapefile for a simulation
			settings["gcm_delta_tile_shapefile"],													# path to chosen gcm delta tile
		]

		# get necessary parameters for plot
		shp_info_list, display_fields, colors = map_processing.get_shps_colors_fields(files_list, settings)

		# do not display fields for basin shapefile
		display_fields[1] = ""

		# plot
		matplotlib_widget.plot_shapefiles_map(
			shapefiles = shp_info_list, 
			display_fields = display_fields, 
			colors = colors, 
			title = None, 
			shp_name = None, 
			buff = settings["map_buffer_overview"],
		)

		self.finished.emit("Finished drawing map.")

class Thread(QtCore.QThread):
	"""
	Thread object.
	Note that some tutorials override the run method in the QtCore.QThread class.  
	According to a post on the Qt Blog titled "You're doing it wrong" (http://blog.qt.io/blog/2010/06/17/youre-doing-it-wrong/),
	the preferred way to use QThread is by creating a QObject and then moving it to a Qthread.  It is discouraged
	to subclass the thread and override the run method with the work you want to do.
	Other references:
	http://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt
	http://blog.debao.me/2013/08/how-to-use-qthread-in-the-right-way-part-1/
	https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/

	"""
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)

	def __del__(self):
		""" Make sure thread stops processing before it gets destroyed; does not get garbage collected until finished"""
		self.exiting = True
		self.wait()

	def start(self):
		QtCore.QThread.start(self)

	def run(self):
		QtCore.QThread.run(self)

# main class
class MainWindow(QtGui.QMainWindow):
	""" Subclass of QMainWindow that creates the main window """

	def __init__(self, parent = None):

		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("WATERAPPUTILS GUI")

		# water text file tab
		self.watertxt_data = None
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

		# gcm tab
		self.tab_gcm_sim_dir = None
		self.is_batch_simulation = None

		self.tab_gcm_basin_shp_path = None
		self.tab_gcm_basin_shp_dir = None		
		self.tab_gcm_basin_shp_file = None		
		self.tab_gcm_basin_shp_id_field = None
		self.tab_gcm_basin_shp_area_field = None
		self.tab_gcm_basin_shp_dict = None

		self.tab_gcm_gcm_data_files = None

		self.tab_gcm_tiles_shp_path = None
		self.tab_gcm_tiles_shp_dir = None
		self.tab_gcm_tiles_shp_file = None
		self.tab_gcm_tiles_shp_id_field = None
		self.tab_gcm_tiles_shp_dict = None

		# user settings
		self.tab_wateruse_settings = user_settings.settings
		self.tab_gcm_settings = user_settings.settings

		# set up the ui
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) # method in *_ui.py file of the Ui_MainWindow class

		# connections for tab - process WATER output text file 
		self.ui.actionExit.triggered.connect(self.close)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.tab_watertxt_push_button_open_file.clicked.connect(self.process_watertxt_file)
		self.ui.tab_watertxt_list_widget.itemSelectionChanged.connect(self.plot_tab_watertxt_list_item)

		# connections for tab - compare 2 WATER output text files
		self.ui.tab_watertxtcmp_push_button_open_file1.clicked.connect(self.select_watertxt_file_cmp)
		self.ui.tab_watertxtcmp_push_button_open_file2.clicked.connect(self.select_watertxt_file_cmp)
		self.ui.tab_watertxtcmp_push_button_compare.clicked.connect(self.compare_watertxt_files)
		self.ui.tab_watertxtcmp_list_widget.itemSelectionChanged.connect(self.plot_tab_watertxtcmp_list_item)

		# connections for tab - apply water use to WATER simulations
		self.ui.tab_wateruse_push_button_open_sim.clicked.connect(self.select_wateruse_sim)
		self.ui.tab_wateruse_push_button_wateruse_files.clicked.connect(self.select_wateruse_files)
		self.ui.tab_wateruse_push_button_wateruse_factor_file.clicked.connect(self.select_wateruse_factor_file)
		self.ui.tab_wateruse_push_button_wateruse_shp.clicked.connect(self.select_wateruse_shp_file)
		self.ui.tab_wateruse_push_button_apply_wateruse.clicked.connect(self.apply_wateruse)
		self.ui.tab_wateruse_push_button_check_inputs.clicked.connect(self.check_wateruse_inputs)
		self.ui.tab_wateruse_push_button_plot_overview_map.clicked.connect(self.plot_wateruse_overview_map)
		self.ui.tab_wateruse_push_button_plot_zoomed_map.clicked.connect(self.plot_wateruse_zoomed_map)

		# connections for tab - apply global climate model deltas to WATER simulations
		self.ui.tab_gcm_push_button_open_sim.clicked.connect(self.select_gcm_sim)
		self.ui.tab_gcm_push_button_gcm_files.clicked.connect(self.select_gcm_files)
		self.ui.tab_gcm_push_button_gcm_shp.clicked.connect(self.select_gcm_shp_file)
		self.ui.tab_gcm_push_button_apply_gcm.clicked.connect(self.apply_gcm)
		self.ui.tab_gcm_push_button_check_inputs.clicked.connect(self.check_gcm_inputs)
		self.ui.tab_gcm_push_button_plot_overview_map.clicked.connect(self.plot_gcm_overview_map)
		self.ui.tab_gcm_push_button_plot_zoomed_map.clicked.connect(self.plot_gcm_zoomed_map)

		# disble the plot area until a file is opened 
		self.ui.tab_watertxt_matplotlib_widget.setEnabled(False)
		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(False)
		self.ui.tab_wateruse_matplotlib_widget.setEnabled(False)
		self.ui.tab_gcm_matplotlib_widget.setEnabled(False)

		# disable compare button until both line edit boxes have text
		self.ui.tab_watertxtcmp_push_button_compare.setEnabled(False)

		# disable apply wateruse button until all proper input exists
		self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)
		self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(False)
		self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(False)

		self.ui.tab_gcm_push_button_apply_gcm.setEnabled(False)
		self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(False)
		self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(False)

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


	#-------------------------------- Tab: Apply water use to WATER simulations ------------------------------------

	def check_wateruse_inputs(self):
		""" validate water use inputs """

		self.ui.tab_wateruse_text_edit.clear()

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
			if not wateruse_input.values()[0]:
				valid_list.append(False)
				error_msg = "Empty input!<br />Need the following input:<br /><br />{}<br /><br />Please provide proper input.".format(wateruse_input.keys()[0])
				self.popup_error(parent = self, msg = error_msg)
			else:
				valid_list.append(True)

		if False in valid_list:
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)
			self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(False)
			self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(False)
		else:
			# over write the settings in user_settings.py with values from gui
			self.tab_wateruse_settings["simulation_directory"] = self.tab_wateruse_sim_dir			
			self.tab_wateruse_settings["is_batch_simulation"] = self.is_batch_simulation

			self.tab_wateruse_settings["basin_shapefile_name"] = self.tab_wateruse_basin_shp_file
			self.tab_wateruse_settings["basin_shapefile_id_field"] = self.tab_wateruse_basin_shp_id_field			
			self.tab_wateruse_settings["basin_shapefile_area_field"] = self.tab_wateruse_basin_shp_area_field

			self.tab_wateruse_settings["wateruse_files"] = self.tab_wateruse_wateruse_data_files
			self.tab_wateruse_settings["wateruse_factor_file"] = self.tab_wateruse_wateruse_factor_file_path
			self.tab_wateruse_settings["wateruse_centroids_shapefile"] = self.tab_wateruse_centroids_shp_path
			self.tab_wateruse_settings["wateruse_centroids_shapefile_id_field"] = self.tab_wateruse_centroids_shp_id_field

			# for single simulations, overwrite the basin shapefile field values to empty strings
			if not self.tab_wateruse_settings["is_batch_simulation"]:
				self.tab_wateruse_settings["basin_shapefile_id_field"] = ""			
				self.tab_wateruse_settings["basin_shapefile_area_field"] = ""

			# enable buttons
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(True)

			if self.ui.tab_wateruse_radio_button_one_sim.isChecked():					# if single sim, enable map plot
				self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(True)
				self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(True)
			else:																		# if multi sims, disable map plot
				self.ui.tab_wateruse_matplotlib_widget.clear_basemap_plot()
				self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(False)
				self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(False)


	def display_wateruse_text(self, settings):
		""" Display text in text edit area """

		info_dir = settings["info_directory_name"]
		info_file = info_dir + "/" + settings["wateruse_info_file_name"]
		ecoflow_dir = settings["ecoflow_directory_name"]
		oasis_dir = settings["oasis_directory_name"]

		msg = "Please see output directories and files located in chosen simulation directory:<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />Additional output is located in each respective basin directory within the chosen simulation directory".format(self.tab_wateruse_sim_dir, info_dir, info_file, ecoflow_dir, oasis_dir)

		self.ui.tab_wateruse_text_edit.setHtml(msg)
		self.ui.tab_wateruse_text_edit.toHtml()

	def apply_wateruse_to_sim(self, settings):
		""" Apply water use to a simulation. Processing is completed in a separate thread from the main gui thread. """

		# initiate the thread and worker
		thread, worker = self.initiate_thread(worker_type = "wateruse")

		# start the thread
		thread.start()

		# if sub water use is checked, then apply substitute water use if proper file exists, otherwise apply water use as normal
		if self.ui.tab_wateruse_checkbox_subwateruse.isChecked():

			wateruse_non_intersecting_file_name = os.path.join(settings["simulation_directory"], settings["info_directory_name"], settings["wateruse_non_intersecting_file_name"])

			if os.path.isfile(wateruse_non_intersecting_file_name):
				# invoke / call the process method on the worker object and send it the current settings
				QtCore.QMetaObject.invokeMethod(worker, "process_subwateruse", QtCore.Qt.QueuedConnection, 
					QtCore.Q_ARG(dict, settings))

				# display text in text edit
				self.display_wateruse_text(settings = settings)

			else:
				error_msg = "Substitute water use file does not exist. Please make sure the the following file exists: <br /> <br />{}".format(wateruse_non_intersecting_file_name)
				self.popup_error(parent = self, msg = error_msg)

		else:
			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "process_wateruse", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, settings))

			# reset button
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

			# display text in text edit
			self.display_wateruse_text(settings = settings)

		# reset button
		self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

	
	def apply_multi_wateruse_sim(self, settings):
		""" Apply water use to multiple simulations """

		# initiate the thread and worker
		thread, worker = self.initiate_thread(worker_type = "wateruse")

		# start the thread
		thread.start()

		# if sub water use is checked, then apply substitute water use if proper file exists, otherwise apply water use as normal
		if self.ui.tab_wateruse_checkbox_subwateruse.isChecked():

			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "process_multi_subwateruse", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, settings))

			# reset button
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

			# display text in text edit
			self.display_wateruse_text(settings = settings)

		else:
			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "process_multi_wateruse", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, settings))

			# reset button
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

			# display text in text edit
			self.display_wateruse_text(settings = settings)

		# reset button
		self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)


	def check_multi_wateruse_sim_dir(self, settings):
		""" Check that user clicked a valid multi simulations directory """

		for dir_name in os.listdir(settings["simulation_directory"]):
			dir_path = os.path.join(settings["simulation_directory"], dir_name)
			filename, fileext = os.path.splitext(dir_path)
			if fileext:
				error_msg = "When running multiple simulations, the simulation directory can only contain WATER simulations and no other files! The following file was found in the simulation directory:<br /><br />{}".format(filename + fileext)
				self.popup_error(parent = self, msg = error_msg)
				self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

	def apply_wateruse(self):
		""" Apply water use using data provided on water use tab """

		try:

			if self.ui.tab_wateruse_radio_button_one_sim.isChecked():
				self.apply_wateruse_to_sim(settings = self.tab_wateruse_settings)

			elif self.ui.tab_wateruse_radio_button_multi_sims.isChecked():
				self.check_multi_wateruse_sim_dir(settings = self.tab_wateruse_settings)
				self.apply_multi_wateruse_sim(settings = self.tab_wateruse_settings)

		except (IOError, AssertionError, ValueError, TypeError, AttributeError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.clear_tab_wateruse_widgets()

	def select_wateruse_sim(self):
		""" Open a QtDialog to select a WATER simulation directory and show the directory in the line edit widget """

		try:

			dirpath = QtGui.QFileDialog.getExistingDirectory(self, caption = "Please select a WATER simulation directory", directory = "../data/sample-water-simulations/")

			if dirpath:
				self.clear_tab_wateruse_widgets()
				self.tab_wateruse_sim_dir = str(dirpath)
				self.ui.tab_wateruse_line_edit_open_sim.setText(self.tab_wateruse_sim_dir)
				self.populate_wateruse_sim_info(sim_dirpath = self.tab_wateruse_sim_dir)

		except IOError as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_wateruse_line_edit_open_sim.clear()

	def populate_wateruse_sim_info(self, sim_dirpath):
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
			self.ui.tab_wateruse_combo_box_shp_id_field.clear()
			self.ui.tab_wateruse_combo_box_shp_area_field.clear()
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

	def plot_wateruse_overview_map(self):
		""" Plot overview map """

		try:
			self.setup_tab_wateruse_matplotlib_widget()

			# initialize thread and worker
			thread, worker = self.initiate_thread(worker_type = "map_wateruse")

			# start the thread
			thread.start()

			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "draw_overview_map", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, self.tab_wateruse_settings),
				QtCore.Q_ARG(object, self.ui.tab_wateruse_matplotlib_widget)
			)

			# display text in text edit
			self.update_status_bar(msg = "Drawing map ... this may take a few moments ... please wait.")

		except (IOError, TypeError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_wateruse_matplotlib_widget.clear_basemap_plot()

	def plot_wateruse_zoomed_map(self):
		""" Plot overview map """

		try:
			self.setup_tab_wateruse_matplotlib_widget()

			# initialize thread and worker
			thread, worker = self.initiate_thread(worker_type = "map_wateruse")

			# start the thread
			thread.start()

			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "draw_zoomed_map", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, self.tab_wateruse_settings),
				QtCore.Q_ARG(object, self.ui.tab_wateruse_matplotlib_widget)
			)

			# display text in text edit
			self.update_status_bar(msg = "Drawing map ... this may take a few moments ... please wait.")

		except (IOError, TypeError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_wateruse_matplotlib_widget.clear_basemap_plot()


	def setup_tab_wateruse_matplotlib_widget(self):
		""" Setup the matplotlib widget """
		self.ui.tab_wateruse_matplotlib_widget.setup_basemap_plot()

	def enable_tab_wateruse_map_buttons(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(True)
		self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(True)

	def enable_tab_wateruse_checkinput_button(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_wateruse_push_button_check_inputs.setEnabled(True)

	def enable_tab_wateruse_wateruse_group_boxes(self):
		""" Disable group boxes when thread starts """
		self.ui.tab_wateruse_group_box_sim_info.setEnabled(True)
		self.ui.tab_wateruse_group_box_wateruse_info.setEnabled(True)

	def disable_tab_wateruse_map_buttons(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(False)
		self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(False)

	def disable_tab_wateruse_checkinput_button(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_wateruse_push_button_check_inputs.setEnabled(False)

	def disable_tab_wateruse_wateruse_group_boxes(self):
		""" Disable group boxes when thread starts """
		self.ui.tab_wateruse_group_box_sim_info.setEnabled(False)
		self.ui.tab_wateruse_group_box_wateruse_info.setEnabled(False)


	#-------------------------------- Tab: Apply global climate deltas to WATER simulations ------------------------------------

	def check_gcm_inputs(self):
		""" validate water use inputs """

		self.tab_gcm_basin_shp_id_field = str(self.ui.tab_gcm_combo_box_shp_id_field.currentText())
		self.tab_gcm_basin_shp_area_field = str(self.ui.tab_gcm_combo_box_shp_area_field.currentText())
		self.tab_gcm_tiles_shp_id_field = str(self.ui.tab_gcm_combo_box_gcm_shp_id_field.currentText())

		gcm_inputs = [
			{"Simulation Directory" : self.tab_gcm_sim_dir},

			{"Basin Shapefile": self.tab_gcm_basin_shp_file},
			{"Basin Shapefile Id Field": self.tab_gcm_basin_shp_id_field},
			{"Basin Shapefile Area Field": self.tab_gcm_basin_shp_area_field},
			{"GCM Data Files": self.tab_gcm_gcm_data_files},

			{"GCM Shapefile": self.tab_gcm_tiles_shp_path},
			{"GCM Shapefile Id Field": self.tab_gcm_tiles_shp_id_field}
		]

		valid_list = []
		for gcm_input in gcm_inputs:
			if not gcm_input.values()[0]:
				valid_list.append(False)
				error_msg = "Empty input!<br />Need the following input:<br /><br />{}<br /><br />Please provide proper input.".format(gcm_input.keys()[0])
				self.popup_error(parent = self, msg = error_msg)
			else:
				valid_list.append(True)

		if False in valid_list:
			self.ui.tab_gcm_push_button_apply_gcm.setEnabled(False)
			self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(False)
			self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(False)
		else:
			# over write the settings in user_settings.py with values from gui
			self.tab_gcm_settings["simulation_directory"] = self.tab_gcm_sim_dir			
			self.tab_gcm_settings["is_batch_simulation"] = self.is_batch_simulation

			self.tab_gcm_settings["basin_shapefile_name"] = self.tab_gcm_basin_shp_file
			self.tab_gcm_settings["basin_shapefile_id_field"] = self.tab_gcm_basin_shp_id_field			
			self.tab_gcm_settings["basin_shapefile_area_field"] = self.tab_gcm_basin_shp_area_field

			self.tab_gcm_settings["gcm_delta_files"] = self.tab_gcm_gcm_data_files
			self.tab_gcm_settings["gcm_delta_tile_shapefile"] = self.tab_gcm_tiles_shp_path
			self.tab_gcm_settings["gcm_delta_tile_shapefile_id_field"] = self.tab_gcm_tiles_shp_id_field

			# for single simulations, overwrite the basin shapefile field values to empty strings
			if not self.tab_gcm_settings["is_batch_simulation"]:
				self.tab_gcm_settings["basin_shapefile_id_field"] = ""			
				self.tab_gcm_settings["basin_shapefile_area_field"] = ""

			# enable buttons
			self.ui.tab_gcm_push_button_apply_gcm.setEnabled(True)

			if self.ui.tab_gcm_radio_button_one_sim.isChecked():						# if single sim, enable map plot
				self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(True)
				self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(True)
			else:																		# if multi sims, disable map plot
				self.ui.tab_gcm_matplotlib_widget.clear_basemap_plot()
				self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(False)
				self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(False)


	def display_gcm_text(self, settings):
		""" Display text in text edit area """

		info_dir = settings["info_directory_name"]
		info_file = info_dir + "/" + settings["gcm_delta_info_file_name"]
		ecoflow_dir = settings["ecoflow_directory_name"]
		oasis_dir = settings["oasis_directory_name"]

		msg = "Please see output directories and files located in chosen simulation directory:<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />{}<br /><br />Additional output is located in each respective basin directory within the chosen simulation directory".format(self.tab_gcm_sim_dir, info_dir, info_file, ecoflow_dir, oasis_dir)

		self.ui.tab_gcm_text_edit.setHtml(msg)
		self.ui.tab_gcm_text_edit.toHtml()

	def apply_gcm_to_sim(self, settings):
		""" Apply water use to a simulation. Processing is completed in a separate thread from the main gui thread. """

		# initiate the thread and worker
		thread, worker = self.initiate_thread(worker_type = "gcm")

		# start the thread
		thread.start()

		# if sub water use is checked, then apply substitute water use if proper file exists, otherwise apply water use as normal
		if self.ui.tab_gcm_checkbox_subgcm.isChecked():

			sub_water_use_file = os.path.join(settings["simulation_directory"], settings["info_directory_name"], settings["gcm_delta_non_intersecting_file_name"])

			if os.path.isfile(sub_water_use_file):
				# invoke / call the process method on the worker object and send it the current settings
				QtCore.QMetaObject.invokeMethod(worker, "process_subgcm", QtCore.Qt.QueuedConnection, 
					QtCore.Q_ARG(dict, settings))

				# display text in text edit
				self.display_gcm_text(settings = settings)

			else:
				error_msg = "Substitute global climate delta file does not exist. Please make sure the the following file exists: <br /> <br />{}".format(sub_water_use_file)
				self.popup_error(parent = self, msg = error_msg)

		else:
			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "process_gcm", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, settings))

			# reset button
			self.ui.tab_gcm_push_button_apply_gcm.setEnabled(False)

			# display text in text edit
			self.display_gcm_text(settings = settings)

		# reset button
		self.ui.tab_gcm_push_button_apply_gcm.setEnabled(False)


	def apply_multi_gcm_sim(self, settings):
		""" Apply global climate model deltas to multiple simulations """

		# initiate the thread and worker
		thread, worker = self.initiate_thread(worker_type = "wateruse")

		# start the thread
		thread.start()

		# if sub water use is checked, then apply substitute water use if proper file exists, otherwise apply water use as normal
		if self.ui.tab_wateruse_checkbox_subwateruse.isChecked():

			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "process_multi_subgcm", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, settings))

			# reset button
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

			# display text in text edit
			self.display_wateruse_text(settings = settings)

		else:
			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "process_multi_gcm", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, settings))

			# reset button
			self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)

			# display text in text edit
			self.display_wateruse_text(settings = settings)

		# reset button
		self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)


	def check_multi_gcm_sim_dir(self, settings):
		""" Check that user clicked a valid multi simulations directory """

		valid_list = []
		for dir_name in os.listdir(settings["simulation_directory"]):
			dir_path = os.path.join(settings["simulation_directory"], dir_name)
			filename, fileext = os.path.splitext(dir_path)
			if fileext:
				error_msg = "When running multiple simulations, the simulation directory can only contain WATER simulations and no other files! The following file was found in the simulation directory:<br /><br />{}".format(filename + fileext)
				self.popup_error(parent = self, msg = error_msg)
				self.ui.tab_gcm_push_button_apply_gcm.setEnabled(False)

	def apply_gcm(self):
		""" Apply water use using data provided on water use tab """

		try:

			if self.ui.tab_gcm_radio_button_one_sim.isChecked():
				self.apply_gcm_to_sim(settings = self.tab_gcm_settings)

			elif self.ui.tab_gcm_radio_button_multi_sims.isChecked():
				self.check_multi_gcm_sim_dir(settings = self.tab_gcm_settings)
				self.apply_multi_gcm_sim(settings = self.tab_gcm_settings)


		except (IOError, AssertionError, ValueError, TypeError, AttributeError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.clear_tab_gcm_widgets()

	def select_gcm_sim(self):
		""" Open a QtDialog to select a WATER simulation directory and show the directory in the line edit widget """

		try:

			dirpath = QtGui.QFileDialog.getExistingDirectory(self, caption = "Please select a WATER simulation directory", directory = "../data/sample-water-simulations/")

			if dirpath:
				self.clear_tab_gcm_widgets()
				self.tab_gcm_sim_dir = str(dirpath)
				self.ui.tab_gcm_line_edit_open_sim.setText(self.tab_gcm_sim_dir)
				self.populate_gcm_sim_info(sim_dirpath = self.tab_gcm_sim_dir)

		except IOError as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_gcm_line_edit_open_sim.clear()

	def populate_gcm_sim_info(self, sim_dirpath):
		""" Populate the widgets in simulation info group box"""

		tmp_shp_file = None

		if self.ui.tab_gcm_radio_button_batch.isChecked():
			self.is_batch_simulation = True
			tmp_shp_file = "Watersheds.shp"

		elif self.ui.tab_gcm_radio_button_single.isChecked():
			self.is_batch_simulation = False
			tmp_shp_file = "basinMask.shp"

		# find the basin shapefile before populating widgets
		if tmp_shp_file:
			self.tab_gcm_basin_shp_path = helpers.find_file(name = tmp_shp_file, path = sim_dirpath)
			
			self.tab_gcm_basin_shp_dir, self.tab_gcm_basin_shp_file = helpers.get_file_info(self.tab_gcm_basin_shp_path) 
			self.ui.tab_gcm_line_edit_basin_shp.setText(self.tab_gcm_basin_shp_file)

			# get fields
			basin_shapefile = osgeo.ogr.Open(self.tab_gcm_basin_shp_path)  
			self.tab_gcm_basin_shp_dict = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

			fields_str = " ".join(self.tab_gcm_basin_shp_dict["fields"])
			self.ui.tab_gcm_combo_box_shp_id_field.clear()
			self.ui.tab_gcm_combo_box_shp_area_field.clear()
			self.ui.tab_gcm_combo_box_shp_id_field.addItems(fields_str.split())
			self.ui.tab_gcm_combo_box_shp_area_field.addItems(fields_str.split())

	def select_gcm_files(self):
		""" Open a QtDialog to select global climate delta files and show the files in the list widget """

		gcm_files_qtstr_list = QtGui.QFileDialog.getOpenFileNames(self, caption = "Please select 3 global climate files - PET.txt, Ppt.txt, Tmax.txt", directory = "../data/deltas-gcm", filter = "Text files (*.txt);; All files (*.*)")
		gcm_files_str = str(gcm_files_qtstr_list.join(","))
		self.tab_gcm_gcm_data_files = gcm_files_str.split(",")		# convert QtStringList to a Python list
	
		if len(self.tab_gcm_gcm_data_files) != 3:
			error_msg = "Need 3 global climate files! - Ppt.txt, Tmax.txt, PET.txt <br />Number of files selected: {}.<br />{}<br />Please select 3 global climate delta files.".format(len(self.tab_gcm_gcm_data_files), self.tab_gcm_gcm_data_files)
			self.popup_error(parent = self, msg = error_msg)
		else:
			self.add_to_list_widgets(widget_names = ["tab_gcm_list_widget_gcm_files"], items = self.tab_gcm_gcm_data_files)

	def select_gcm_shp_file(self):
		""" Open a QtDialog to select gcm delta shapefile"""

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a global climate model tiled shapefile", directory = "../data/spatial-datafiles/gcm-tiles", filter = "Shapefile (*.shp)")	

		if filepath:
			self.ui.tab_gcm_line_edit_gcm_shp.setText(filepath)
			self.tab_gcm_tiles_shp_path = str(filepath)
			self.tab_gcm_tiles_shp_dir, self.tab_gcm_tiles_shp_file = helpers.get_file_info(self.tab_gcm_tiles_shp_path) 

			# get fields
			gcm_shapefile = osgeo.ogr.Open(self.tab_gcm_tiles_shp_path)  
			self.tab_gcm_tiles_shp_dict = spatialvectors.fill_shapefile_dict(shapefile = gcm_shapefile)

			fields_str = " ".join(self.tab_gcm_tiles_shp_dict["fields"])
			self.ui.tab_gcm_combo_box_gcm_shp_id_field.addItems(fields_str.split())

	def plot_gcm_overview_map(self):
		""" Plot overview map """

		try:
			self.setup_tab_gcm_matplotlib_widget()

			# initialize thread and worker
			thread, worker = self.initiate_thread(worker_type = "map_gcm")

			# start the thread
			thread.start()

			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "draw_gcm_overview_map", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, self.tab_gcm_settings),
				QtCore.Q_ARG(object, self.ui.tab_gcm_matplotlib_widget)
			)

			# display text in text edit
			self.update_status_bar(msg = "Drawing map ... this may take a few moments ... please wait.")

		except (IOError, TypeError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_gcm_matplotlib_widget.clear_basemap_plot()

	def plot_gcm_zoomed_map(self):
		""" Plot overview map """

		try:
			self.setup_tab_gcm_matplotlib_widget()

			# initialize thread and worker
			thread, worker = self.initiate_thread(worker_type = "map_gcm")

			# start the thread
			thread.start()

			# invoke / call the process method on the worker object and send it the current settings
			QtCore.QMetaObject.invokeMethod(worker, "draw_zoomed_map", QtCore.Qt.QueuedConnection, 
				QtCore.Q_ARG(dict, self.tab_gcm_settings),
				QtCore.Q_ARG(object, self.ui.tab_gcm_matplotlib_widget)
			)

			# display text in text edit
			self.update_status_bar(msg = "Drawing map ... this may take a few moments ... please wait.")

		except (IOError, TypeError) as error:
			error_msg = "{}".format(error.message)
			print(error_msg)
			self.popup_error(parent = self, msg = error_msg)
			self.ui.tab_gcm_matplotlib_widget.clear_basemap_plot()


	def setup_tab_gcm_matplotlib_widget(self):
		""" Setup the matplotlib widget """
		self.ui.tab_gcm_matplotlib_widget.setup_basemap_plot()

	def enable_tab_gcm_map_buttons(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(True)
		self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(True)

	def enable_tab_gcm_checkinput_button(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_gcm_push_button_check_inputs.setEnabled(True)

	def enable_tab_gcm_gcm_group_boxes(self):
		""" Disable group boxes when thread starts """
		self.ui.tab_gcm_group_box_sim_info.setEnabled(True)
		self.ui.tab_gcm_group_box_gcm_info.setEnabled(True)

	def disable_tab_gcm_map_buttons(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(False)
		self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(False)

	def disable_tab_gcm_checkinput_button(self):
		""" Enable map buttons when thread finishes """
		self.ui.tab_gcm_push_button_check_inputs.setEnabled(False)

	def disable_tab_gcm_gcm_group_boxes(self):
		""" Disable group boxes when thread starts """
		self.ui.tab_gcm_group_box_sim_info.setEnabled(False)
		self.ui.tab_gcm_group_box_gcm_info.setEnabled(False)

	#-------------------------------- Tab Independent Methods ------------------------------------

	def thread_msg(self, msg):
		""" Display message box about thread """

		QtGui.QMessageBox.information(self, "Thread Message", msg)
		self.update_status_bar(msg)

	def initiate_thread(self, worker_type):
		""" Create the thread and worker. Move the worker object to the thread and make necessary connections """

		# create the thread and worker
		thread = Thread()
		if worker_type == "map_wateruse":
			worker = MapWorker()

			worker.starting.connect(self.disable_tab_wateruse_map_buttons)
			worker.starting.connect(self.disable_tab_wateruse_checkinput_button)

			worker.finished.connect(self.enable_tab_wateruse_map_buttons)
			worker.finished.connect(self.enable_tab_wateruse_checkinput_button)

		elif worker_type == "wateruse":
			worker = Worker()
			
			worker.starting.connect(self.disable_tab_wateruse_checkinput_button)
			worker.starting.connect(self.disable_tab_wateruse_wateruse_group_boxes)	
				
			worker.finished.connect(self.enable_tab_wateruse_checkinput_button)
			worker.finished.connect(self.enable_tab_wateruse_wateruse_group_boxes)

		elif worker_type == "map_gcm":
			worker = MapWorker()

			worker.starting.connect(self.disable_tab_gcm_map_buttons)
			worker.starting.connect(self.disable_tab_gcm_checkinput_button)

			worker.finished.connect(self.enable_tab_gcm_map_buttons)
			worker.finished.connect(self.enable_tab_gcm_checkinput_button)

		elif worker_type == "gcm":
			worker = Worker()
			
			worker.starting.connect(self.disable_tab_gcm_checkinput_button)
			worker.starting.connect(self.disable_tab_gcm_gcm_group_boxes)	
				
			worker.finished.connect(self.enable_tab_gcm_checkinput_button)
			worker.finished.connect(self.enable_tab_gcm_gcm_group_boxes)

		else:
			raise TypeError("worker type does not exist: {}".format(worker_type))

		# move the worker object to the thread
		worker.moveToThread(thread)

		# connect the starting signal to information dialog
		worker.starting.connect(self.thread_msg)

		# connect the finished signal to quitting the thread
		worker.finished.connect(thread.quit)
		worker.finished.connect(self.thread_msg)

		return thread, worker

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

	def clear_tab_wateruse_widgets(self):
		""" Clear widgets on wateruse tab """
		self.ui.tab_wateruse_push_button_apply_wateruse.setEnabled(False)
		self.ui.tab_wateruse_line_edit_open_sim.clear()
		self.ui.tab_wateruse_line_edit_basin_shp.clear()
		self.ui.tab_wateruse_combo_box_shp_id_field.clear()
		self.ui.tab_wateruse_combo_box_shp_area_field.clear()
		self.ui.tab_wateruse_list_widget_wateruse_files.clear()
		self.ui.tab_wateruse_line_edit_wateruse_factor_file.clear()
		self.ui.tab_wateruse_line_edit_wateruse_shp.clear()
		self.ui.tab_wateruse_combo_box_wateruse_shp_id_field.clear()
		self.ui.tab_wateruse_text_edit.clear()
		self.ui.tab_wateruse_matplotlib_widget.clear_basemap_plot()
		self.ui.tab_wateruse_matplotlib_widget.setEnabled(False)
		self.ui.tab_wateruse_push_button_plot_overview_map.setEnabled(False)
		self.ui.tab_wateruse_push_button_plot_zoomed_map.setEnabled(False)

	def clear_tab_gcm_widgets(self):
		""" Clear widgets on gcm tab """
		self.ui.tab_gcm_push_button_apply_gcm.setEnabled(False)
		self.ui.tab_gcm_line_edit_open_sim.clear()
		self.ui.tab_gcm_line_edit_basin_shp.clear()
		self.ui.tab_gcm_combo_box_shp_id_field.clear()
		self.ui.tab_gcm_combo_box_shp_area_field.clear()
		self.ui.tab_gcm_list_widget_gcm_files.clear()
		self.ui.tab_gcm_line_edit_gcm_shp.clear()
		self.ui.tab_gcm_combo_box_gcm_shp_id_field.clear()
		self.ui.tab_gcm_text_edit.clear()
		self.ui.tab_gcm_matplotlib_widget.clear_basemap_plot()
		self.ui.tab_gcm_matplotlib_widget.setEnabled(False)
		self.ui.tab_gcm_push_button_plot_overview_map.setEnabled(False)
		self.ui.tab_gcm_push_button_plot_zoomed_map.setEnabled(False)

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
