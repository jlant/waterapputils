# Python built-in
import sys
import random

# PyQt modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# ui
from my_ui import Ui_MainWindow

# my classes
from parser_class import Parser

class MainWindow(QtGui.QMainWindow):
    """ this subclass of QMainWindow creates a main window to observe the growth of a simulated animal"""
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("My Simulation")
        
        # set up the ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) # method in *_ui.py file of the Ui_MainWindow class
        
        # connections
        self.ui.plot_button.clicked.connect(self.parse)
        self.ui.actionOpen.triggered.connect(self.select_file)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)

    def about(self):
        msg =   """ A demo of using PyQt with matplotlib:
                
                 * Use the File -> Open to select tab delimited text file of values
                 * Click "Plot" to plot the values
                 * Use Matplotlib Navigation Bar to query
                 """
        
        QtGui.QMessageBox.about(self, "About the demo", msg.strip())
    
    
    def _plot_random(self):
        """ method to plot random data """
#        random_numbers = random.sample(range(0, 10), 10)
#        self.ui.matplotlib_widget.axes2.clear()
#        self.ui.matplotlib_widget.axes2.set_title("Random Numbers")
#        self.ui.matplotlib_widget.axes2.plot(random_numbers, '*-')
#        self.ui.matplotlib_widget.canvas.draw()
        
        axes2 = self.ui.matplotlib_widget.axes2
        self.ui.matplotlib_widget.plot_rand(axes2)

    def _plot(self, x, y):
#        self.ui.matplotlib_widget.axes1.clear()
#        self.ui.matplotlib_widget.axes1.set_title("Simple x vs y Plot")
#        self.ui.matplotlib_widget.axes1.set_xlabel("x")
#        self.ui.matplotlib_widget.axes1.set_ylabel("y")
#        self.ui.matplotlib_widget.axes1.plot(x, y)
#        self.ui.matplotlib_widget.canvas.draw()
        axes1 = self.ui.matplotlib_widget.axes1
        axes2 = self.ui.matplotlib_widget.axes2
        self.ui.matplotlib_widget.plot(x, y)
        #self.ui.matplotlib_widget.plot(axes2, x, y)
    
    def parse(self):
        """ method to parse a file """
        parser = Parser()
        x, y = parser.parse(filename = self.ui.file_line_edit.text())
        self._plot(x, y)
        #self._plot_random()
        

    def select_file(self):
        """ method to open a QtDialog to select a file """
        filepath = QtGui.QFileDialog.getOpenFileName(self, caption = "Please select a text file", directory = "", filter = "Text files (*.txt);; All files (*.*)")
        if filepath:
            self.ui.file_line_edit.setText(filepath) # set the path string in the line edit widget
            

def main():
    main_simulation = QtGui.QApplication(sys.argv) # create main window
    main_window = MainWindow() # create instance of (main) window
    main_window.show() # show the window
    main_window.raise_() # raise the window to the top of the stack
    main_simulation.exec_() # monitor window for events
    

if __name__ == "__main__":
    main()