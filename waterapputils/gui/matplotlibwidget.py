from PyQt4 import QtGui
from PyQt4 import QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.widgets import RadioButtons
from scipy.stats import nanmean 

import numpy as np
from textwrap import wrap
import matplotlib.dates as mdates 
import datetime

from modules import watertxt

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

        # create initial values for watertxt data
        self.watertxt_data = None
        self.parameter = None
        self.color_str = None
        self.axes1_text = None

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
        self.axes1 = self.figure.add_subplot(111) 
        self.axes1.grid(True)

        # create widgets  
        self.matplotlib_toolbar = NavigationToolbar(self.canvas, parent) # the matplotlib toolbar object

        # create radio buttons
        self.axes_radio = self.figure.add_axes([0.01, 0.02, 0.10, 0.15])        # [left, bottom, width, height] = fractions of figure width and height
        self.figure.subplots_adjust(bottom=0.2)
        self.radio_buttons = RadioButtons(ax = self.axes_radio, labels = ("Span On", "Span Off"), active = 1, activecolor= "r")
        self.radio_buttons.on_clicked(self.toggle_selector)

        # create SpanSelector; invisble at first unless activated with toggle selector        
        self.span_selector = SpanSelector(self.axes1, self.on_select, 'horizontal', useblit = True, rectprops = dict(alpha=0.5, facecolor='red'))
        self.span_selector.visible = False

        # create the layout
        self.layout = QtGui.QVBoxLayout()

        # add the widgets to the layout
        self.layout.addWidget(self.matplotlib_toolbar)
        self.layout.addWidget(self.canvas)

        # set the layout
        self.setLayout(self.layout)

    def plot_watertxt_parameter(self, watertxt_data, name): 
        """ Plot a parameter from a WATER.txt file """

        self.clearplot()

        self.watertxt_data = watertxt_data
        self.parameter = watertxt.get_parameter(watertxt_data, name = name)     

        assert self.parameter is not None, "Parameter name {} is not in watertxt_data".format(name)

        self.dates = watertxt_data["dates"]
        self.axes1.set_title("Parameter: {}".format(self.parameter["name"]))
        self.axes1.set_xlabel("Date")
        ylabel = "\n".join(wrap(self.parameter["name"], 60))
        self.axes1.set_ylabel(ylabel)

        # get proper color that corresponds to parameter name
        self.color_str = COLORS[name.split('(')[0].strip()]

        # plot parameter    
        self.axes1.plot(self.dates, self.parameter["data"], color = self.color_str, label = self.parameter["name"], linewidth = 2)   

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
        text = "mean = %.2f\nmax = %.2f\nmin = %.2f" % (self.parameter["mean"], self.parameter["max"], self.parameter["min"])
        patch_properties = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
                       
        self.axes1_text = self.axes1.text(0.05, 0.95, text, transform = self.axes1.transAxes, fontsize = 14, 
            verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)    

        self.canvas.draw()
   
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
        
        # get the selected dates and values
        selected_dates = self.dates[indices]
        selected_values = self.parameter["data"][indices]

        # compute simple stats on selected values 
        selected_values_mean = nanmean(selected_values)
        selected_value_max = np.nanmax(selected_values)
        selected_value_min = np.nanmin(selected_values)

        # plot the selected values and update plots limits and text
        self.axes1.plot(selected_dates, selected_values, self.color_str)
        self.axes1.set_xlim(selected_dates[0], selected_dates[-1])
        self.axes1.set_ylim(selected_values.min(), selected_values.max())

        text = 'mean = %.2f\nmax = %.2f\nmin = %.2f' % (selected_values_mean, selected_value_max, selected_value_min)           
        self.axes1_text.set_text(text)

        # draw the updated plot
        self.canvas.draw() 

    def toggle_selector(self, radio_button_label):
        """ 
        A toggle radio buttons for the matplotlib SpanSelector widget.
        """ 

        if radio_button_label == "Span On":
            self.span_selector.visible = True
        elif radio_button_label == "Span Off":
            self.span_selector.visible = False
            self.plot_watertxt_parameter(watertxt_data = self.watertxt_data, name = self.parameter["name"])
            # self.axes1.set_xlim(self.dates[0], self.dates[-1])
            # self.axes1.set_ylim(self.parameter["min"], self.parameter["max"])

    def clearplot(self):
        """ Clear the plot axes """ 
        self.axes1.clear()
        self.axes1.grid(True)
