import sys
from PyQt4 import QtGui, QtCore
from gui.user_interface import Ui_MainWindow
from modules import watertxt
from modules import helpers

# my modules
class MainWindow(QtGui.QMainWindow):
	""" Subclass of QMainWindow that creates the main window """

	def __init__(self, parent = None):

		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("WATERAPPUTILS GUI")

		# initialize variables
		self.tab_watertxt_data = None
		self.tab_watertxtcmp_data1 = None
		self.tab_watertxtcmp_data2 = None

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
		# self.ui.tab_watertxtcmp_list_widget.itemSelectionChanged.connect(self.plot_tab_watertxtcmp_list_item)

		# disble the plot area until a file is opened 
		self.ui.tab_watertxt_matplotlib_widget.setEnabled(False)
		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(False)

		# disable compare button until both line edit boxes have text
		self.ui.tab_watertxtcmp_push_button_compare.setEnabled(False)

	#-------------------------------- Tab: Process WATER output text file ------------------------------------

	def process_watertxt_file(self):
		""" Open a file dialog to select, read, display column names, and plot a WATER.txt file."""
		try:
			filepath = self.select_watertxt_file()
			if filepath:
				self.tab_watertxt_data = self.read_watertxt_file(filepath)
				self.add_to_tab_watertxt_list_widget()
				self.add_to_tab_watertxt_table_widget()
				self.setup_tab_watertxt_matplotlib_widget()
				self.plot_on_tab_watertxt_matplotlib_widget(parameter_name = self.tab_watertxt_data["column_names"][0])		# plot the first parameter in column names

		except IOError as error:
			print("Error: {}".format(error.message))

	def select_watertxt_file(self):
		""" Open a QtDialog to select a WATER.txt file and show the file in the line edit widget """

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a WATER.txt file", directory = "../data/watertxt-datafiles/", filter = "Text files (*.txt);; All files (*.*)")	
		if filepath:
			self.ui.tab_watertxt_line_edit_open_file.setText(filepath)

		return filepath

	def add_to_tab_watertxt_list_widget(self):
		""" Add column names from self.tab_watertxt_data to list widget on the watertxt tab """

		self.ui.tab_watertxt_list_widget.addItems(self.tab_watertxt_data["column_names"])

	def add_to_tab_watertxt_table_widget(self):
		""" Add data from self.tab_watertxt_data to table widget on the watertxt tab """

		data = self.format_data_for_table(watertxt_data = self.tab_watertxt_data)

		self.ui.tab_watertxt_table_widget.setRowCount(len(data))
		self.ui.tab_watertxt_table_widget.setColumnCount(len(data[0]))
		self.ui.tab_watertxt_table_widget.setHorizontalHeaderLabels(["Date"] + self.tab_watertxt_data["column_names"])

		for row in range(len(data)):
			for col in range(len(data[row])):
				self.ui.tab_watertxt_table_widget.setItem(row, col, QtGui.QTableWidgetItem(data[row][col]))

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
			
			filepath1 = self.ui.tab_watertxtcmp_line_edit_open_file1.text()
			filepath2 = self.ui.tab_watertxtcmp_line_edit_open_file2.text()

			filedir1, filename1 = helpers.get_file_info(str(filepath1))
			filedir2, filename2 = helpers.get_file_info(str(filepath2))

			self.tab_watertxtcmp_data1 = self.read_watertxt_file(filepath = filepath1)
			self.tab_watertxtcmp_data2 = self.read_watertxt_file(filepath = filepath2)
			self.validate_watertxt_data_for_comparison(self.tab_watertxtcmp_data1, self.tab_watertxtcmp_data2, filepath1, filepath2)
			self.add_to_tab_watertxtcmp_list_widget()

			self.add_to_tab_watertxtcmp_table_widgets()
			# self.setup_tab_watertxt_matplotlib_widget()
			# self.plot_on_tab_watertxt_matplotlib_widget(parameter_name = self.tab_watertxt_data["column_names"][0])		# plot the first parameter in column names

		except IOError as error:
			print("Error: {}".format(error.message))

		except AssertionError as error:
			print("Error: {}".format(error.message))


	def add_to_tab_watertxtcmp_list_widget(self):
		""" Add column names from self.tab_watertxt_data to list widget on the watertxt tab """

		self.ui.tab_watertxtcmp_list_widget.addItems(self.tab_watertxtcmp_data1["column_names"])

	def add_to_tab_watertxtcmp_table_widgets(self):
		""" Add first WATER output text file to table widget """

		data1 = self.format_data_for_table(watertxt_data = self.tab_watertxtcmp_data1)
		data2 = self.format_data_for_table(watertxt_data = self.tab_watertxtcmp_data2)

		self.ui.tab_watertxtcmp_table_widget1.setRowCount(len(data1))
		self.ui.tab_watertxtcmp_table_widget1.setColumnCount(len(data1[0]))
		self.ui.tab_watertxtcmp_table_widget1.setHorizontalHeaderLabels(["Date"] + self.tab_watertxtcmp_data1["column_names"])

		self.ui.tab_watertxtcmp_table_widget2.setRowCount(len(data2))
		self.ui.tab_watertxtcmp_table_widget2.setColumnCount(len(data2[0]))
		self.ui.tab_watertxtcmp_table_widget2.setHorizontalHeaderLabels(["Date"] + self.tab_watertxtcmp_data2["column_names"])

		for row in range(len(data1)):
			for col in range(len(data1[row])):
				self.ui.tab_watertxtcmp_table_widget1.setItem(row, col, QtGui.QTableWidgetItem(data1[row][col]))

		for row in range(len(data2)):
			for col in range(len(data2[row])):
				self.ui.tab_watertxtcmp_table_widget2.setItem(row, col, QtGui.QTableWidgetItem(data2[row][col]))

	#-------------------------------- Tab Independent Methods ------------------------------------

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


	def read_watertxt_file(self, filepath):
		""" Read a WATER.txt file """

		watertxt_data = watertxt.read_file(filepath = filepath)
		isvalid = self.validate_watertxt_data(watertxt_data = watertxt_data, filepath = filepath)

		if isvalid:
			return watertxt_data

	def validate_watertxt_data(self, watertxt_data, filepath):
		""" Check and make sure that watertxt_data is valid """ 

		sender = self.sender()
		sender_object_name = sender.objectName()

		if watertxt_data["parameters"] == [] or watertxt_data["column_names"] == None:
			isvalid = False
			error_msg = "Invalid file! <br />{}<br />Please choose a valid WATER output text file.".format(filepath)
			self.popup_error(self, error_msg)
			self.clear_widgets(sender_name = sender_object_name)
			raise IOError(error_msg)

		else:
			isvalid = True

		return isvalid

	def validate_watertxt_data_for_comparison(self, watertxt_data1, watertxt_data2, filepath1, filepath2):
		""" Check and make sure that both watertxt_data dictionaries can be compared """ 

		sender = self.sender()
		sender_object_name = sender.objectName()

		# check column names
		if not self.tab_watertxtcmp_data1["column_names"] == self.tab_watertxtcmp_data2["column_names"]:
			isvalid = False
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
			""".format(filepath1, self.tab_watertxtcmp_data1["column_names"], filepath2, self.tab_watertxtcmp_data2["column_names"])

			self.popup_error(self, error_msg)
			self.clear_widgets(sender_name = sender_object_name)
			raise IOError(error_msg)

		dates1_start_date = self.tab_watertxtcmp_data1["dates"][0]
		dates2_start_date = self.tab_watertxtcmp_data2["dates"][0]

		dates1_end_date = self.tab_watertxtcmp_data1["dates"][-1]
		dates2_end_date = self.tab_watertxtcmp_data2["dates"][-1]

		if not set(self.tab_watertxtcmp_data1["dates"]) == set(self.tab_watertxtcmp_data2["dates"]):
			isvalid = False
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
			""".format(filepath1, dates1_start_date, dates1_end_date, filepath2, dates2_start_date, dates2_end_date)

			self.popup_error(self, error_msg)
			self.clear_widgets(sender_name = sender_object_name)
			raise IOError(error_msg)

		else:
			isvalid = True

		return isvalid

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
		# self.ui.tab_watertxtcmp_matplotlib_widget.clear_watertxtcmp_plot()			
		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(False)
		self.ui.tab_watertxtcmp_push_button_compare.setEnabled(False)


def main():
	""" Run application """

	app = QtGui.QApplication(sys.argv)		# create application object
	main_window = MainWindow()				# create main window object
	main_window.show()			
	main_window.raise_()					# raise window to top of stack						
	sys.exit(app.exec_())					# monitor application for events


if __name__ == "__main__":
	main()
