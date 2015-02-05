import sys
from PyQt4 import QtGui, QtCore
from gui.user_interface import Ui_MainWindow
import modules.watertxt as watertxt

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

	def about(self):
		""" Show an message box about the gui."""
		
		msg = \
		"""
		The waterapputils gui can be used to process and interact with output
		and database files from the WATER application.  More help and information
		can be found at https://github.com/jlant-usgs/waterapputils
		"""

		QtGui.QMessageBox.about(self, "About the waterapputils gui", msg.strip())

	def _select_watertxt_file(self):
		""" Open a QtDialog to select a WATER.txt file and show the file in the line edit widget """

		filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a WATER.txt file", directory = "../data/watertxt-datafiles/", filter = "Text files (*.txt);; All files (*.*)")
		if filepath:
			self.ui.line_edit_open_file.setText(filepath)

	def _read_watertxt_file(self):
		""" Read a WATER.txt file """
		self.watertxt_data = watertxt.read_file(filepath = self.ui.line_edit_open_file.text())

	def _add_to_list_widget(self):
		""" Add column_names to list widget """
		self.ui.list_widget.addItems(self.watertxt_data["column_names"])

	def _plot_watertxt_file(self):
		""" Plot a WATER.txt file """ 
		self.ui.matplotlib_widget.plot_watertxt_parameter(watertxt_data = self.watertxt_data, name = self.watertxt_data["column_names"][0])

	def process_watertxt_file(self):
		""" Open a file dialog to select, read, display column names, and plot a WATER.txt file."""

		self._select_watertxt_file()
		self._read_watertxt_file()
		self._add_to_list_widget()
		# self._plot_watertxt_file()


def main():
	""" Run application """
	app = QtGui.QApplication(sys.argv)		# create application object
	main_window = MainWindow()				# create main window object
	main_window.show()			
	main_window.raise_()					# raise window to top of stack						
	sys.exit(app.exec_())					# monitor application for events


if __name__ == "__main__":
	main()
