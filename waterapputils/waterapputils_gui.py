import sys
from PyQt4 import QtGui, QtCore
from gui.user_interface import Ui_MainWindow
from modules import watertxt
# from gui.table_class import Table

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

		# connections
		self.ui.actionExit.triggered.connect(self.close)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.tab_watertxt_push_button_open_file.clicked.connect(self.process_watertxt_file)
		self.ui.tab_watertxt_list_widget.itemSelectionChanged.connect(self.plot_list_item)

		self.ui.tab_watertxtcmp_push_button_open_file1.clicked.connect(self.select_watertxt_file_cmp)
		self.ui.tab_watertxtcmp_push_button_open_file2.clicked.connect(self.select_watertxt_file_cmp)
		self.ui.tab_watertxtcmp_push_button_compare.clicked.connect(self.compare_watertxt_files)
		self.ui.tab_watertxtcmp_list_widget.itemSelectionChanged.connect(self.plot_list_item)

		# disble the plot area until a file is opened 
		self.ui.tab_watertxt_matplotlib_widget.setEnabled(False)
		self.ui.tab_watertxtcmp_matplotlib_widget.setEnabled(False)

		# disable compare button until both line edit boxes have text
		self.ui.tab_watertxtcmp_push_button_compare.setEnabled(False)

	def about(self):
		""" Show an message box about the gui."""
		
		msg = \
		"""
		The waterapputils gui can be used to process and interact with output
		and database files from the WATER application.  More help and information
		can be found at https://github.com/jlant-usgs/waterapputils
		"""

		QtGui.QMessageBox.about(self, "About the waterapputils gui", msg.strip())

	#-------------------------------- Tab: Process WATER output text file ------------------------------------

	def process_watertxt_file(self):
		""" Open a file dialog to select, read, display column names, and plot a WATER.txt file."""
		try:
			sender_object_name = get_sender_name()
			filepath = self.select_watertxt_file()
			if filepath:
				self.tab_watertxt_data = self.read_watertxt_file(filepath)
				self.add_to_list_widget(column_names = self.tab_watertxt_data["column_names"], sender_object_name)
				self.add_to_table_widget()
				self.ui.tab_watertxt_matplotlib_widget.setEnabled(True)
				self.plot_watertxt_file(parameter_name = self.tab_watertxt_data["column_names"][0])

		except IOError as error:
			print("Error: {}".format(error.message))

	def select_watertxt_file(self):
		""" Open a QtDialog to select a WATER.txt file and show the file in the line edit widget """

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a WATER.txt file", directory = "../data/watertxt-datafiles/", filter = "Text files (*.txt);; All files (*.*)")	
		if filepath:
			self.ui.tab_watertxt_line_edit_open_file.setText(filepath)

		return filepath

	def add_to_list_widget(self, column_names, sender_object_name):
		""" Add column_names to list widget """

		if sender_object_name == "tab_watertxt_push_button_open_file":
			self.ui.tab_watertxt_list_widget.addItems(column_names)

	def add_to_table_widget(self):
		""" Add data to table widget """

		data = self.format_table_data(watertxt_data = self.tab_watertxt_data)

		self.ui.tab_watertxt_table_widget.setRowCount(len(data))
		self.ui.tab_watertxt_table_widget.setColumnCount(len(data[0]))
		self.ui.tab_watertxt_table_widget.setHorizontalHeaderLabels(["Date"] + self.tab_watertxt_data["column_names"])

		for row in range(len(data)):
			for col in range(len(data[row])):
				self.ui.tab_watertxt_table_widget.setItem(row, col, QtGui.QTableWidgetItem(data[row][col]))

	def plot_watertxt_file(self, parameter_name):
		""" Plot a WATER.txt file """ 
		self.ui.tab_watertxt_matplotlib_widget.plot_watertxt_parameter(watertxt_data = self.tab_watertxt_data, name = parameter_name)

	def plot_list_item(self):
		""" Plot the item selected in the list widget """
		
		item_type = str(self.ui.tab_watertxt_list_widget.currentItem().text())
		self.plot_watertxt_file(parameter_name = item_type)

	def format_table_data(self, watertxt_data):
		""" Format the watertxt data into a list of lists with string elements for the table """

		# get the dates and all the values
		dates = self.tab_watertxt_data["dates"]
		values_all = watertxt.get_all_values(watertxt_data = self.tab_watertxt_data)

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
				row.append("{:.2f}".format((values_all[j][i])))
			data_fmt.append(row)

		# merge dates and data values into a single list
		data_all = []
		for i in range(nrows):
			new_row = [dates_fmt[i]] + data_fmt[i]
			data_all.append(new_row)

		return data_all

	#-------------------------------- Tab: Compare 2 WATER output text files ------------------------------------

	def compare_watertxt_files(self):
		""" Compare two WATER output text files """


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

		print("Compare!")
		self.read_watertxt_file()
		# self.add_to_list_widget()
		# self.add_to_table_widget()
		# self.ui.tab_watertxt_matplotlib_widget.setEnabled(True)
		# self.plot_watertxt_file(parameter_name = self.tab_watertxt_data["column_names"][0])

	#-------------------------------- Independent methods ------------------------------------
	def get_sender_name(self):
		""" Get the current name of the sender object """

		sender = self.sender()
		sender_object_name = sender.objectName()

		return sender_object_name

	def read_watertxt_file(self, filepath):
		""" Read a WATER.txt file """

		watertxt_data = watertxt.read_file(filepath = filepath)
		
		if self.validate_watertxt_data(watertxt_data = watertxt_data)

		else:
			return watertxt_data

	def validate_watertxt_data(self, watertxt_data):
		""" Check and make sure that watertxt_data is valid """ 

		sender_object_name = get_sender_name()

		if watertxt_data["parameters"] == [] or watertxt_data["column_names"] == None:
			isvalid = False
			error_msg = "Invalid File! Please choose a valid file."
			self.popup_error(self, error_msg)
			self.clear_widgets(sender_object_name = sender_object_name)
			raise IOError(error_msg)

		else:
			isvalid = True

		return isvalid

	def clear_widgets(self, sender_object_name):
		""" Clear all the widgets """

		if sender_object_name == "tab_watertxt_push_button_open_file":

			# clear widget on tab_watertxt
			self.ui.tab_watertxt_list_widget.clear()
			self.ui.tab_watertxt_table_widget.clear()
			self.ui.tab_watertxt_matplotlib_widget.clear_plot()			
			self.ui.tab_watertxt_matplotlib_widget.setEnabled(False)

	def popup_error(self, parent, msg):
		""" Display an error message box """

		title = "ERROR"
		QtGui.QMessageBox.critical(parent, title, msg, QtGui.QMessageBox.Close)

def main():
	""" Run application """

	app = QtGui.QApplication(sys.argv)		# create application object
	main_window = MainWindow()				# create main window object
	main_window.show()			
	main_window.raise_()					# raise window to top of stack						
	sys.exit(app.exec_())					# monitor application for events


if __name__ == "__main__":
	main()
