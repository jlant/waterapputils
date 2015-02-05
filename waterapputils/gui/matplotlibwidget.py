from PyQt4 import QtGui
from PyQt4 import QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
import numpy as np

# Global colors dictionary
COLORS = {"Discharge": "b",
          "Subsurface Flow": "g",
          "Impervious Flow": "SteelBlue",
          "Infiltration Excess": "SeaGreen",
          "Initial Abstracted Flow": "MediumBlue",
          "Overland Flow": "RoyalBlue",
          "PET": "orange",
          "AET": "DarkOrange",
          "Average Soil Root zone": "Gray",
          "Average Soil Unsaturated Zone": "DarkGray",
          "Snow Pack": "PowderBlue",
          "Precipitation": "SkyBlue",
          "Storage Deficit": "Brown",
          "Return Flow": "Aqua",
          "Water Use": "DarkCyan",
          "Discharge + Water Use": "DarkBlue"
}

class MatplotlibWidget(QtGui.QWidget):
    """ This subclass of QtWidget will manage the widget drawing; name matches the class in the *_ui.py file"""    
    
    def __init__(self, parent = None):
        super(MatplotlibWidget, self).__init__(parent)
        super(MatplotlibWidget, self).__init__(parent)

        # create initial values for watertxt data
        self.parameter = None

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
        self.layout.addWidget(self.matplotlib_toolbar)
        self.layout.addWidget(self.canvas)

        # set the layout
        self.setLayout(self.layout)

        # create SpanSelector        
        self.span = SpanSelector(self.axes1, self.on_select, 'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))

       
    def on_select(self, xmin, xmax):
        """ A select handler for SpanSelector that updates axes 2 with the new x and y limits selected by user """

        # convert matplotlib float dates to a datetime format
        date_min = mdates.num2date(xmin)
        date_max = mdates.num2date(xmax) 

        # put the xmin and xmax in datetime format to compare
        date_min = datetime.datetime(date_min.year, date_min.month, date_min.day, date_min.hour, date_min.minute)    
        date_max = datetime.datetime(date_max.year, date_max.month, date_max.day, date_max.hour, date_max.minute)

        # find the indices that were selected    
        indices = np.where((self.dates >= date_min) & (self.dates <= date_max))
        indices = indices[0]
           
        thisx = self.dates[indices]
        thisy = self.parameter["data"][indices]

        self.axes2.plot(thisx, thisy, 'r-.')
        self.axes2.set_xlim(thisx[0], thisx[-1])
        self.axes2.set_ylim(thisy.min(), thisy.max())
        self.canvas.draw() 

    def toggle_selector(self, event):
        """ 
        A toggle key event handler for the matplotlib SpanSelector widget.
        A or a actives the slider; Q or q de-activates the slider.
        """ 
        if event.key in ['Q', 'q'] and self.span.visible:
            print '**SpanSelector deactivated.**'
            self.span.visible = False
        if event.key in ['A', 'a'] and not self.span.visible:
            print '**SpanSelector activated.**'
            self.span.visible = True

    def clearplot(self):
        """ Clear the plot axes """ 
        self.axes1.clear()
        self.axes2.clear()
        self.axes1.grid(True)
        self.axes2.grid(True)

    def plot_watertxt_parameter(self, watertxt_data, name): 
        """ Plot a parameter from a WATER.txt file """

        self.clearplot()

        self.parameter = watertxt.get_parameter(watertxt_data, name = name)     

        assert parameter is not None, "Parameter name {} is not in watertxt_data".format(name)

        dates = watertxt_data["dates"]
        self.dates = watertxt_data["dates"]
        self.axes1.set_title("Parameter: {}".format(parameter["name"]))
        self.axes1.set_xlabel("Date")
        ylabel = "\n".join(wrap(parameter["name"], 60))
        self.axes1.set_ylabel(ylabel)

        # get proper color that corresponds to parameter name
        color_str = COLORS[name.split('(')[0].strip()]

        # plot parameter    
        self.axes1.plot(dates, parameter["data"], color = color_str, label = parameter["name"], linewidth = 2)   

        self.axes2.plot(dates, parameter["data"], color = "red", label = parameter["name"], linewidth = 2)

        # rotate and align the tick labels so they look better
        self.figure.autofmt_xdate()

        # use a more precise date string for the x axis locations in the
        # toolbar
        self.axes1.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

        # legend; make it transparent    
        handles, labels = self.axes1.get_legend_handles_labels()
        legend = self.axes1.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)

        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "mean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter["mean"], parameter["max"], parameter["min"])
        patch_properties = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
                       
        self.axes1.text(0.05, 0.95, text, transform = self.axes1.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)    

        self.canvas.draw()

