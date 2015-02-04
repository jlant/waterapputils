import random

from PyQt4 import QtGui
from PyQt4 import QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from matplotlib.figure import Figure

from matplotlib.widgets import SpanSelector

import numpy as np

class MatplotlibWidget(QtGui.QWidget):
    """ This subclass of QtWidget will manage the widget drawing; name matches the class in the *_ui.py file"""    
    
    def __init__(self, parent = None):
        super(MatplotlibWidget, self).__init__(parent)
        
        # create figure
        self.figure = Figure()
        
        # create canvas and set some of its properties
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(parent) 
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()
        
        # set up axes and its properties
        self.axes1 = self.figure.add_subplot(211) 
        self.axes2 = self.figure.add_subplot(212)
        #self.axes2 = self.figure.add_subplot(212, sharex = self.axes1, sharey = self.axes1)
        
        self.axes1.grid(True)
        self.axes2.grid(True)
        
        # create widgets  
        self.matplotlib_toolbar = NavigationToolbar(self.canvas, parent) # the matplotlib toolbar object
        
        # create the layout
        self.layout = QtGui.QVBoxLayout()
        
        # add the widgets to the layout
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.matplotlib_toolbar)
        
        # set the layout
        self.setLayout(self.layout)

        # create SpanSelector        
        self.span = SpanSelector(self.axes1, self.on_select, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red') )
        
    def plot_rand(self, axes):
        """ method to plot random data """
        random_numbers = random.sample(range(0, 10), 10)
        axes.clear()
        axes.set_title("Random Numbers")
        axes.plot(random_numbers, '*-')
        self.canvas.draw()

    def plot(self, x, y):
        """ method to plot data"""
        self.x = x
        self.y = y
        self.axes1.clear()
        self.axes1.grid(True)
        self.axes1.set_title("Simple x vs y Plot")
        self.axes1.set_xlabel("x")
        self.axes1.set_ylabel("y")
        self.axes1.plot(self.x, self.y, 'b-*')
        self.axes2.plot(self.x, self.y, 'r-.')
        self.canvas.draw()
        
    def on_select(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.x, (xmin, xmax))
        indmax = min(len(self.x) - 1, indmax)
    
        thisx = self.x[indmin:indmax]
        thisy = self.y[indmin:indmax]
        print(thisx)
        print(thisy)
        self.axes2.plot(thisx, thisy, 'r-.')
        self.axes2.set_xlim(thisx[0], thisx[-1])
        self.axes2.set_ylim(thisy.min(), thisy.max())
        self.canvas.draw()      

    