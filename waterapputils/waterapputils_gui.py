import sys
from PyQt4 import QtGui, QtCore
from gui.user_interface import Ui_MainWindow

# my modules
class MainWindow(QtGui.QMainWindow):
	""" """
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("My Simulation")

		# set up the ui
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) # method in *_ui.py file of the Ui_MainWindow class

		# connections
		self.ui.actionExit.triggered.connect(self.close)

def main():
	""" """
	app = QtGui.QApplication(sys.argv)		# create application object
	main_window = MainWindow()				# create main window object
	main_window.show()			
	main_window.raise_()					# raise window to top of stack						
	sys.exit(app.exec_())					# monitor application for events


if __name__ == "__main__":
	main()
