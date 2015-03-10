from PyQt4 import QtGui
from PyQt4 import QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.widgets import RadioButtons
from scipy.stats import nanmean 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

import os
import numpy as np
from textwrap import wrap
import matplotlib.dates as mdates 
import datetime

from modules import watertxt

class MatplotlibWidget(QtGui.QWidget):
    """ This subclass of QtWidget will manage the widget drawing; name matches the class in the *_ui.py file"""    
 
    # Global colors dictionary
    colors_dict = {
        "Discharge": "b",
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

    def __init__(self, parent = None):
        super(MatplotlibWidget, self).__init__(parent)

        # create object scope variables for watertxt data plot; used by radio buttons and span selector
        self.watertxt_data = None
        self.parameter = None
        self.color_str = None
        self.axes_text = None
        self.axes_radio = None
               
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
        self.ax = self.figure.add_subplot(111) 
        self.ax.grid(True)

        # create toolbar  
        self.matplotlib_toolbar = NavigationToolbar(self.canvas, parent) # the matplotlib toolbar object

        # create the layout
        self.layout = QtGui.QVBoxLayout()

        # add the widgets to the layout
        self.layout.addWidget(self.matplotlib_toolbar)
        self.layout.addWidget(self.canvas)

        # set the layout
        self.setLayout(self.layout)

    #-------------------------------- WATER.txt Parameter Plot ------------------------------------ 

    def setup_watertxt_plot(self):
        """ Setup the watertxt plot """

        self.clear_watertxt_plot()

        # set up axes and its properties
        self.axes = self.figure.add_subplot(111) 
        self.axes.grid(True)

        # create radio buttons
        self.axes_radio = self.figure.add_axes([0.01, 0.02, 0.10, 0.15])        # [left, bottom, width, height] = fractions of figure width and height
        self.figure.subplots_adjust(bottom=0.2)
        self.radio_buttons = RadioButtons(ax = self.axes_radio, labels = ("Span On", "Span Off"), active = 1, activecolor= "r")
        self.radio_buttons.on_clicked(self.toggle_selector)

        # create SpanSelector; invisble at first unless activated with toggle selector        
        self.span_selector = SpanSelector(self.axes, self.on_select_axes, 'horizontal', useblit = True, rectprops = dict(alpha=0.5, facecolor='red'))
        self.span_selector.visible = False

    def plot_watertxt_parameter(self, watertxt_data, name): 
        """ Plot a parameter from a WATER.txt file """

        self.reset_watertxt_plot()

        self.dates = watertxt_data["dates"]
        self.watertxt_data = watertxt_data
        self.parameter = watertxt.get_parameter(watertxt_data, name = name)     

        assert self.parameter is not None, "Parameter name {} is not in watertxt_data".format(name)

        self.axes.set_title("Parameter: {}".format(self.parameter["name"]))
        self.axes.set_xlabel("Date")
        ylabel = "\n".join(wrap(self.parameter["name"], 60))
        self.axes.set_ylabel(ylabel)

        # get proper color that corresponds to parameter name
        self.color_str = self.colors_dict[name.split('(')[0].strip()]

        # plot parameter    
        self.axes.plot(self.dates, self.parameter["data"], color = self.color_str, label = self.parameter["name"], linewidth = 2)   

        # legend; make it transparent    
        handles, labels = self.axes.get_legend_handles_labels()
        legend = self.axes.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)

        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "mean = {:.2f}\nmax = {:.2f}\nmin = {:.2f}".format(self.parameter["mean"], self.parameter["max"], self.parameter["min"])

        patch_properties = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
                       
        self.axes_text = self.axes.text(0.05, 0.95, text, transform = self.axes.transAxes, fontsize = 14, 
                                        verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)    

        # use a more precise date string for the x axis locations in the toolbar and rotate labels
        self.axes.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

        # rotate and align the tick labels so they look better; note that self.figure.autofmt_xdate() does not work because of the radio button axes 
        for label in self.axes.get_xticklabels():
            label.set_ha("right")
            label.set_rotation(30)

        # draw the plot
        self.canvas.draw()

    def on_select_helper(self, xmin, xmax):
        """ Helper for on_select methods """

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

        return selected_dates, selected_values, selected_values_mean, selected_value_max, selected_value_min

    def on_select_axes(self, xmin, xmax):
        """ A select handler for SpanSelector that updates axes with the new x and y limits selected by user """

        selected_dates, selected_values, selected_values_mean, selected_value_max, selected_value_min = self.on_select_helper(xmin, xmax)

        # plot the selected values and update plots limits and text
        self.axes.plot(selected_dates, selected_values, self.color_str)
        self.axes.set_xlim(selected_dates[0], selected_dates[-1])
        self.axes.set_ylim(selected_values.min(), selected_values.max())

        text = 'mean = %.2f\nmax = %.2f\nmin = %.2f' % (selected_values_mean, selected_value_max, selected_value_min)           
        self.axes_text.set_text(text)

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

    def clear_watertxt_plot(self):
        """ Clear the plot axes """ 

        self.figure.clear()
        self.canvas.draw()

    def reset_watertxt_plot(self):
        """ Clear the plot axes """ 

        self.axes.clear()
        self.canvas.draw()
        self.axes.grid(True)

    #-------------------------------- WATER.txt Parameter Comparison Plot ------------------------------------        

    def setup_watertxtcmp_plot(self):
        """ Setup the watertxt plot """

        self.clear_watertxtcmp_plot()

        # set up axes and its properties
        self.axes1 = self.figure.add_subplot(211)
        self.axes2 = self.figure.add_subplot(212, sharex = self.axes1)

        self.axes1.grid(True)
        self.axes2.grid(True)

    def plot_watertxtcmp_parameter(self, watertxt_data1, watertxt_data2, filename1, filename2, name): 
        """ Plot a parameter from a WATER.txt file """

        self.reset_watertxtcmp_plot()

        dates = watertxt_data1["dates"]

        parameter1 = watertxt.get_parameter(watertxt_data = watertxt_data1, name = name)     
        parameter2 = watertxt.get_parameter(watertxt_data = watertxt_data2, name = name)  

        assert parameter1 is not None, "Parameter name {} is not in watertxt_data".format(name)
        assert parameter2 is not None, "Parameter name {} is not in watertxt_data".format(name)

        # calculate the difference
        diff = parameter2["data"] - parameter1["data"]

        # plot parameters on axes1  
        self.axes1.plot(dates, parameter1["data"], color = "b", label = filename1 + ": " + parameter1["name"], linewidth = 2)   
        self.axes1.hold(True)
        self.axes1.plot(dates, parameter2["data"], color = "r", label = filename2 + ": " + parameter2["name"], linewidth = 2)   

        # plot the difference on axes2
        self.axes2.plot(dates, diff, color = "k", linewidth = 2)

        # add title, labels, legend
        self.axes1.set_title(parameter1["name"])

        self.axes2.set_xlabel("Date")
        self.axes2.set_ylabel("Difference")
 
        handles1, labels1 = self.axes1.get_legend_handles_labels()
        legend1 = self.axes1.legend(handles1, labels1, fancybox = True)
        legend1.get_frame().set_alpha(0.5)
        legend1.draggable(state=True)

        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text1 = "mean = {:.2f}\nmax = {:.2f}\nmin = {:.2f}".format(parameter1["mean"], parameter1["max"], parameter1["min"])
        text2 = "mean = {:.2f}\nmax = {:.2f}\nmin = {:.2f}".format(parameter2["mean"], parameter2["max"], parameter2["min"])

        text_diff = "mean = {:.2f}\nmax = {:.2f}\nmin = {:.2f}".format(nanmean(diff), np.max(diff), np.min(diff))

        patch_properties1 = {"boxstyle": "round", "facecolor": "b", "alpha": 0.5}
        patch_properties2 = {"boxstyle": "round", "facecolor": "r", "alpha": 0.5}
        patch_properties_diff = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
                       
        self.axes1.text(0.02, 0.95, text1, transform = self.axes1.transAxes, fontsize = 12, verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties1)
        self.axes1.text(0.02, 0.45, text2, transform = self.axes1.transAxes, fontsize = 12, verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties2)
        self.axes2.text(0.02, 0.95, text_diff, transform = self.axes2.transAxes, fontsize = 12, verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties_diff)

        # use a more precise date string for the x axis locations in the toolbar and rotate labels
        self.axes2.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

        # rotate and align the tick labels so they look better
        self.figure.autofmt_xdate()

        # draw the plot
        self.canvas.draw()

    def clear_watertxtcmp_plot(self):
        """ Clear the plot axes """ 

        self.figure.clear()
        self.canvas.draw()

    def reset_watertxtcmp_plot(self):
        """ Clear the plot axes """ 

        self.axes1.clear()
        self.axes2.clear()
        self.canvas.draw()
        self.axes1.grid(True)
        self.axes2.grid(True)


    #-------------------------------- Basemap Plot ------------------------------------

    def setup_basemap_plot(self):
        """ Setup the watertxt plot """

        self.clear_basemap_plot()

        # set up axes and its properties
        self.basemap_axes = self.figure.add_subplot(111) 
        self.basemap_axes.grid(True)

    def get_map_extents(self, shapefiles, shp_name = None):
        """   
        Get max and min extent coordinates from a list of shapefiles to use as the 
        extents on the map. Use the map extents to calculate the map center and the 
        standard parallels.

        Parameters
        ----------
        shapefiles : list 
            List of shapefile_data dictionaries 
        shp_name : string
            String name of shapefile to use for getting map extents 

        Returns
        -------
        extent_coords : dictionary 
            Dictionary containing "lon_min", "lon_max", "lat_max", "lat_min" keys with respective calculated values
        center_coords : dictionary 
            Dictionary containing "lon", "lat" keys with respective calculated values
        standard_parallels : dictionary 
            Dictionary containing "first", "second" keys with respective calculated values (first = min(lat), second = max(lat))   
        """
        extent_coords = {}    
        center_coords = {}
        standard_parallels = {}

        lons = []
        lats = []

        if shp_name:
            for shapefile_data in shapefiles:            
                if shp_name in shapefile_data["name"].split("_")[0]:
                    lons.append(shapefile_data["extents"][0:2])
                    lats.append(shapefile_data["extents"][2:])
            
        else:
            for shapefile_data in shapefiles:
                lons.append(shapefile_data["extents"][0:2])
                lats.append(shapefile_data["extents"][2:])

        extent_coords["lon_min"] = np.min(lons)
        extent_coords["lon_max"] = np.max(lons)
        extent_coords["lat_min"] = np.min(lats)
        extent_coords["lat_max"] = np.max(lats)

        center_coords["lon"] = np.mean([extent_coords["lon_min"], extent_coords["lon_max"]])
        center_coords["lat"] = np.mean([extent_coords["lat_min"], extent_coords["lat_max"]])

        standard_parallels["first"] = extent_coords["lat_min"]
        standard_parallels["second"] = extent_coords["lat_max"]
            
        return extent_coords, center_coords, standard_parallels

    def plot_shapefiles_map(self, shapefiles, display_fields = [], colors = [], title = None, shp_name = None, buff = 1.0):
        """   
        Generate a map showing all the shapefiles in the shapefile_list.  
        Shapefiles should be in a Geographic Coordinate System (longitude and 
        latitude coordinates) such as World WGS84; Matplotlib"s basemap library 
        does the proper transformation to a projected coordinate system.  The projected
        coordinate system used is Albers Equal Area.
        
        Parameters
        ----------
        shapefiles : list 
            List of dictionaries containing shapefile information
        title : string 
            String title for plot
        display_fields : list 
            List of strings that correspond to a shapefile field where the corresponding value(s) will be displayed.
        colors : list
            List of strings that correspond to colors to be displayed
        shp_name : string
            String name of shapefile to use for getting map extents 
        buff : float
            Float value in coordinate degrees to buffer the map with
        """  

        self.setup_basemap_plot()

        extent_coords, center_coords, standard_parallels = self.get_map_extents(shapefiles, shp_name = shp_name)     

        # create the basemap object with Albers Equal Area Conic Projection
        bmap = Basemap(projection = "aea", 
                       llcrnrlon = extent_coords["lon_min"] - buff, llcrnrlat = extent_coords["lat_min"] - buff, 
                       urcrnrlon = extent_coords["lon_max"] + buff, urcrnrlat = extent_coords["lat_max"] + buff, 
                       lat_1 = standard_parallels["first"], lat_2 = standard_parallels["second"],
                       lon_0 = center_coords["lon"], lat_0 = center_coords["lat"],
                       resolution = "h", area_thresh = 10000, ax = self.basemap_axes)    
        
        # have basemap object plot background stuff
        bmap.drawcoastlines()
        bmap.drawcountries()
        bmap.drawrivers(linewidth = 1, color = "blue")
        bmap.drawstates()
        bmap.drawmapboundary(fill_color = "aqua")
        bmap.fillcontinents(color = "coral", lake_color = "aqua")
        bmap.drawparallels(np.arange(-80., 81., 1.), labels = [1, 0, 0, 0], linewidth = 0.5)
        bmap.drawmeridians(np.arange(-180., 181., 1.), labels = [0, 0, 0, 1], linewidth = 0.5)
         
        # plot each shapefile on the basemap    
        legend_handles = []
        legend_labels = []
        colors_index = 0
        colors_list = ["b", "g", "y", "r", "c", "y", "m", "orange", "aqua", "darksalmon", "gold", "k"]
        for shapefile_data in shapefiles:
            
            # set up colors to use
            if colors:
                color = colors[colors_index]        
            elif colors_index > len(colors_list) - 1:
                color = np.random.rand(3,)
            else:
                color = colors_list[colors_index]         
            
            full_path = os.path.join(shapefile_data["path"], shapefile_data["name"].split(".")[0])
            
            shp_tuple = bmap.readshapefile(full_path, "shp", drawbounds = False)                            # use basemap shapefile reader for ease of plotting
            for shape_dict, shape in zip(bmap.shp_info, bmap.shp):                                          # zip the shapefile information and its shape as defined by basemap

                if shapefile_data["type"] == "POLYGON":
                    p1 = Polygon(shape, facecolor = color, edgecolor = "k",
                                             linewidth = 1, alpha = 0.7, label = shapefile_data["name"])            
                    self.basemap_axes.add_patch(p1)
                    xx, yy = zip(*shape)
                    txt_x = str(np.mean(xx))
                    txt_y = str(np.mean(yy))
                    
                elif shapefile_data["type"] == "POINT":
                    x, y = shape

                    if "usgsgages" in shapefile_data["name"].split("_")[0]:
                        p1 = bmap.plot(x, y, color = color, marker = "^", markersize = 10, label = shapefile_data["name"])
                    elif "wateruse" in shapefile_data["name"].split("_")[0]:
                        p1 = bmap.plot(x, y, color = color, marker = "o", markersize = 5, label = shapefile_data["name"])
                    else:
                        print("what!!")
                        p1 = bmap.plot(x, y, color = color, marker = "o", markersize = 10, label = shapefile_data["name"])

                    txt_x = str(x)
                    txt_y = str(y)
                    
                else:
                    xx, yy = zip(*shape)
                    p1 = bmap.plot(xx, yy, linewidth = 1, color = color, label = shapefile_data["name"])
                    txt_x = str(np.mean(xx))
                    txt_y = str(np.mean(yy))
                
                
                if isinstance(p1, list):
                    p1 = p1[0]

                # control text display of shapefile fields
                for display_field in display_fields:
                    if display_field in shape_dict.keys():
                        self.basemap_axes.text(txt_x, txt_y, shape_dict[display_field], color = "k", fontsize = 12, fontweight = "bold")

            colors_index += 1    
            legend_handles.append(p1)    
            legend_labels.append(shapefile_data["name"].split("_")[0])

        handles, labels = self.basemap_axes.get_legend_handles_labels()
        
        # edit the contents of handles and labels to only show 1 legend per shape
        handles = legend_handles
        labels = legend_labels
        legend = self.basemap_axes.legend(handles, labels, fancybox = True, numpoints = 1)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state = True)

        # draw the plot
        self.canvas.draw()

        # get background to use blit while plotting; makes plotting faster
        # background = self.canvas.copy_from_bbox(self.basemap_axes.bbox)
        self.canvas.blit(self.basemap_axes.bbox)


    def clear_basemap_plot(self):
        """ Clear the plot axes """ 

        self.figure.clear()
        self.canvas.draw()

    def reset_basemap_plot(self):
        """ Clear the plot axes """ 

        self.basemap_axes.clear()
        self.canvas.draw()
