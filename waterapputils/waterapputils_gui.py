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

		# set the table
		# self.data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}
		# self.set_table_headers()
		# self.set_table_data()

		# connections
		self.ui.actionExit.triggered.connect(self.close)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.push_button_open_file.clicked.connect(self.process_watertxt_file)
		self.ui.list_widget.itemSelectionChanged.connect(self.plot_list_item)

	def _set_table_headers(self):
		""" Set the headers in the table """
		self.column_names = ["col1", "col2", "col3"]
		self.ui.table_widget.setColumnCount(len(self.column_names))
		self.ui.table_widget.setHorizontalHeaderLabels(self.column_names)

	def _set_table_data(self):
		""" Set the data in the table """
		self.ui.table_widget.setRowCount(len(self.data["col1"]))

		for row, key in enumerate(self.column_names):
			for col, item in enumerate(self.data[key]):
				print row, col, key, item
			 	self.ui.table_widget.setItem(row, col, QtGui.QTableWidgetItem(str(item)))

		# for row, datanode in enumerate(data):
		# 	for col, header in enumerate(["dates", "discharge"]):
		# 		print row, col, data[row][col]
		# 		self.ui.table_widget.setItem(row, col, QtGui.QTableWidgetItem(str(data[row][col])))

	def add_to_table_widget(self):
		""" """

		dates = self.watertxt_data["dates"]
		values_all = watertxt.get_all_values(watertxt_data = self.watertxt_data)

		nrows = len(values_all[0])
		ncols = len(values_all)
		self.ui.table_widget.setRowCount(nrows)
		self.ui.table_widget.setColumnCount(ncols)
		self.ui.table_widget.setHorizontalHeaderLabels(["Date"] + self.watertxt_data["column_names"])

		data_fmt = []
		for i in range(nrows):
			row = []
			for j in range(ncols):
				row.append("{:.2f}".format((values_all[j][i])))
			data_fmt.append(row)

		dates_fmt = []
		for i in range(nrows):
			date_str = dates[i].strftime("%m/%d/%Y")
			dates_fmt.append(date_str)


		data_all = []
		for i in range(nrows):
			new_row = [dates_fmt[i]] + data_fmt[i]
			data_all.append(new_row)

		for row in range(len(data_all)):
			for col in range(len(data_all[row])):
				self.ui.table_widget.setItem(row, col, QtGui.QTableWidgetItem(data_all[row][col]))


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

	def read_watertxt_file(self):
		""" Read a WATER.txt file """
		self.watertxt_data = watertxt.read_file(filepath = self.ui.line_edit_open_file.text())

	def add_to_list_widget(self):
		""" Add column_names to list widget """
		self.ui.list_widget.addItems(self.watertxt_data["column_names"])

	def plot_watertxt_file(self, parameter_name):
		""" Plot a WATER.txt file """ 
		self.ui.matplotlib_widget.plot_watertxt_parameter(watertxt_data = self.watertxt_data, name = parameter_name)

	def process_watertxt_file(self):
		""" Open a file dialog to select, read, display column names, and plot a WATER.txt file."""

		self.select_watertxt_file()
		self.read_watertxt_file()
		self.add_to_list_widget()
		self.add_to_table_widget()
		# self.plot_watertxt_file(parameter_name = self.watertxt_data["column_names"][0])

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
