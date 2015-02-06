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
		self.watertxt_data = None

		# set up the ui
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) # method in *_ui.py file of the Ui_MainWindow class

		# connections
		self.ui.actionExit.triggered.connect(self.close)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.push_button_open_file.clicked.connect(self.process_watertxt_file)
		self.ui.list_widget.itemSelectionChanged.connect(self.plot_list_item)

		# disble the plot area until a file is opened 
		self.ui.matplotlib_widget.setEnabled(False)

	def about(self):
		""" Show an message box about the gui."""
		
		msg = \
		"""
		The waterapputils gui can be used to process and interact with output
		and database files from the WATER application.  More help and information
		can be found at https://github.com/jlant-usgs/waterapputils
		"""

		QtGui.QMessageBox.about(self, "About the waterapputils gui", msg.strip())

	def select_watertxt_file(self):
		""" Open a QtDialog to select a WATER.txt file and show the file in the line edit widget """

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a WATER.txt file", directory = "../data/watertxt-datafiles/", filter = "Text files (*.txt);; All files (*.*)")
		if filepath:
			self.ui.line_edit_open_file.setText(filepath)

	def popup_error(self, parent, msg):
		title = "ERROR"
		QtGui.QMessageBox.critical(parent, title, msg, QtGui.QMessageBox.Close)

	def read_watertxt_file(self):
		""" Read a WATER.txt file """
		self.watertxt_data = watertxt.read_file(filepath = self.ui.line_edit_open_file.text())

		if self.watertxt_data["column_names"] == None:
			self.popup_error(self, 'Invalid File! Please open a valid file.')
			self.clear_widgets()
		else:
			print "OK"

	def clear_widgets(self):
		""" Clear all the widgets """
		self.ui.list_widget.clear()
		self.ui.line_edit_open_file.clear()
		self.ui.table_widget.clear()
		self.ui.matplotlib_widget.clear_plot()			# fixme, not working
		self.ui.matplotlib_widget.setEnabled(False)

	def add_to_list_widget(self):
		""" Add column_names to list widget """
		self.ui.list_widget.addItems(self.watertxt_data["column_names"])

	def plot_watertxt_file(self, parameter_name):
		""" Plot a WATER.txt file """ 
		self.ui.matplotlib_widget.plot_watertxt_parameter(watertxt_data = self.watertxt_data, name = parameter_name)

	def format_table_data(self, watertxt_data):
		""" Format the watertxt data into a list of lists with string elements for the table """

		# get the dates and all the values
		dates = self.watertxt_data["dates"]
		values_all = watertxt.get_all_values(watertxt_data = self.watertxt_data)

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

	def add_to_table_widget(self):
		""" Add data to table widget """

		data = self.format_table_data(watertxt_data = self.watertxt_data)

		self.ui.table_widget.setRowCount(len(data))
		self.ui.table_widget.setColumnCount(len(data[0]))
		self.ui.table_widget.setHorizontalHeaderLabels(["Date"] + self.watertxt_data["column_names"])

		for row in range(len(data)):
			for col in range(len(data[row])):
				self.ui.table_widget.setItem(row, col, QtGui.QTableWidgetItem(data[row][col]))

	def process_watertxt_file(self):
		""" Open a file dialog to select, read, display column names, and plot a WATER.txt file."""

		self.select_watertxt_file()
		self.read_watertxt_file()
		self.add_to_list_widget()
		self.add_to_table_widget()
		self.ui.matplotlib_widget.setEnabled(True)
		self.plot_watertxt_file(parameter_name = self.watertxt_data["column_names"][0])

	def plot_list_item(self):
		""" Plot the item selected in the list widget """
		
		item_type = str(self.ui.list_widget.currentItem().text())
		self.plot_watertxt_file(parameter_name = item_type)
	

def main():
	""" Run application """
	app = QtGui.QApplication(sys.argv)		# create application object
	main_window = MainWindow()				# create main window object
	main_window.show()			
	main_window.raise_()					# raise window to top of stack						
	sys.exit(app.exec_())					# monitor application for events


if __name__ == "__main__":
	main()
