# -*- coding: utf-8 -*-
"""
:Module: watertxt_viewer.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles views of the data, such as printing and plotting.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from textwrap import wrap
from StringIO import StringIO
import datetime
import numpy as np
import os

# my modules
import watertxt

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
        
def print_watertxt_data(watertxt_data):
    """   
    Print information contained in the water data dictionary. 
    
    Parameters
    ----------
    watertxt_data : dictionary 
        A dictionary containing data found in WATER output text file.
    
    Examples
    --------
    >>> import waterapputils_viewer
    >>> import datetime
    >>> import numpy as np
    >>> start_date = datetime.datetime(2014, 04, 01, 0, 0)
    >>> dates = [start_date + datetime.timedelta(i) for i in range(11)]
    >>> discharge_data = np.array([100 + i for i in range(11)])
    >>> subsurfaceflow_data = np.array([i + 2 for i in range(11)])      
    >>> parameters = [{"name": "Discharge (cfs)", "index": 0,
                   ... "data": discharge_data, "mean": np.mean(discharge_data), "max": np.b(discharge_data), 
                   ... "min": np.min(discharge_data)}, 
                      {"name": "Subsurface Flow (mm/day)", "index": 1,
                   ... "data": subsurfaceflow_data, "mean": np.mean(subsurfaceflow_data), "max": np.max(subsurfaceflow_data), 
                   ... "min": np.min(subsurfaceflow_data)}, ]
    >>> data = {user": "jlant", "date_created": "4/9/2014 15:30:00 PM", "stationid": "012345",
            ... "column_names": ["Discharge (cfs)", "Subsurface Flow (mm/day)", "Impervious Flow (mm/day)", "Infiltration Excess (mm/day)", "Initial Abstracted Flow (mm/day)", "Overland Flow (mm/day)", "PET (mm/day)", "AET(mm/day)", "Average Soil Root zone (mm)", "Average Soil Unsaturated Zone (mm)", "Snow Pack (mm)", "Precipitation (mm/day)", "Storage Deficit (mm/day)", "Return Flow (mm/day)"],
            ... "parameters": parameters, "dates": dates}
    >>> waterapputils_viewer.print_info(watertxt_data = data)
    --- DATA FILE INFORMATION ---
    User: jlant
    Date created: 4/9/2014 15:30:00 PM
    StationID: 012345
    Parameters:
      Discharge (cfs)
          mean: 105.0
          max: 100
          min: 110
      Subsurface Flow (mm/day)
          mean: 7.0
          max: 2
          min: 12
    """   
    
    # print relevant information
    print("")
    print("--- WATER TEXT FILE INFORMATION ---")
    print("User: {}".format(watertxt_data["user"]))
    print("Date created: {}".format(watertxt_data["date_created"]))
    print("StationID: {}".format(watertxt_data["stationid"]))
    
    print("Parameters:")
    for parameter in watertxt_data["parameters"]:
        print("  {}".format(parameter["name"]))
        print("      mean: {}".format(parameter["mean"]))
        print("      max: {}".format(parameter["max"]))
        print("      min: {}".format(parameter["min"]))
    print("")

def plot_watertxt_data(watertxt_data, is_visible = True, save_path = None):
    """   
    Plot each parameter contained in watertxt_data. Save plots to a particular
    path.
    
    Parameters
    ----------
    watertxt_data : dictionary 
        A dictionary containing data found in WATER *.txt output data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    """
    
    for parameter in watertxt_data["parameters"]:
        
        fig = plt.figure(figsize=(12,10))
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_title("Parameter: {}\nStationID: {}".format(parameter["name"], watertxt_data["stationid"]))
        ax.set_xlabel("Date")
        ylabel = "\n".join(wrap(parameter["name"], 60))
        ax.set_ylabel(ylabel)
        ax.grid(True)

        # get proper color that corresponds to parameter name
        color_str = COLORS[parameter["name"].split("(")[0].strip()]
                        
        plt.plot(watertxt_data["dates"], parameter["data"], color = color_str, label = ylabel) 
        
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
     
        # legend; make it transparent    
        handles, labels = ax.get_legend_handles_labels()
        legend = ax.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "mean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter["mean"], parameter["max"], parameter["min"])
        patch_properties = {"boxstyle": "round",
                            "facecolor": "wheat",
                            "alpha": 0.5
                            }
                       
        ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
        
        # save plots
        if save_path:        
            # set the size of the figure to be saved
            curr_fig = plt.gcf()
            curr_fig.set_size_inches(12, 10)
            
            # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
            filename = "-".join([watertxt_data["user"], watertxt_data["stationid"], parameter["name"].split("(")[0]])  + ".png"           
            filepath = os.path.join(save_path, filename)
            plt.savefig(filepath, dpi = 100)                        
          
        # show plots
        if is_visible:
            plt.show()
        else:
            plt.close()

def plot_watertxt_comparison(watertxt_data1, watertxt_data2, is_visible = True, save_path = None):
    """   
    Plot a comparison of two parameters contained in WATER.txt data file. Save 
    plots to a particular path.
    
    Parameters
    ----------
    watertxtdata_data : dictionary 
        A dictionary containing data found in WATER data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    """
    assert set(watertxt_data1.keys()) == set(watertxt_data2.keys()), "Parameter keys between water datasets do not match"  
    assert set(watertxt_data1["dates"]) == set(watertxt_data2["dates"]), "Lengths of dates are not equal"  

    dates = watertxt_data1["dates"]
    for parameter1, parameter2 in zip(watertxt_data1["parameters"], watertxt_data2["parameters"]):    
    
        fig = plt.figure(figsize = (12,10))
        ax1 = fig.add_subplot(211)
        ax1.grid(True)
        ax1.set_title("Parameter: {}\n{} vs {}".format(parameter1["name"], watertxt_data1["stationid"], watertxt_data2["stationid"]))
        ax1.set_xlabel("Date")
        ylabel = "\n".join(wrap(parameter1["name"], 60))
        ax1.set_ylabel(ylabel)
        
        ax1.plot(dates, parameter1["data"], color = "b", label = watertxt_data1["stationid"], linewidth = 2)
        ax1.hold(True)
        ax1.plot(dates, parameter2["data"], color = "r", label = watertxt_data2["stationid"], linewidth = 2, alpha = 0.75)     
        
        # increase y axis to have text and legend show up better
        curr_ylim = ax1.get_ylim()
        ax1.set_ylim((curr_ylim[0], curr_ylim[1] * 1.5))

        # use a more precise date string for the x axis locations in the toolbar
        ax1.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
        
        # legend; make it transparent    
        handles1, labels1 = ax1.get_legend_handles_labels()
        legend1 = ax1.legend(handles1, labels1, fancybox = True)
        legend1.get_frame().set_alpha(0.5)
        legend1.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "mean = %.2f\nmax = %.2f\nmin = %.2f\n---\nmean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter1["mean"], parameter1["max"], parameter1["min"],
                                                                                                  parameter2["mean"], parameter2["max"], parameter2["min"])
        patch_properties = {"boxstyle": "round",
                            "facecolor": "wheat",
                            "alpha": 0.5
                            }
                       
        ax1.text(0.05, 0.95, text, transform = ax1.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
                
        # plot difference = values_b - values_a
        ax2 = fig.add_subplot(212, sharex = ax1)
        ax2.grid(True)
        ax2.set_title("Difference")
        ax2.set_xlabel("Date")
        ax2.set_ylabel(ylabel)
        diff = parameter2["data"] - parameter1["data"]
        ax2.plot(dates, diff, color = "k", linewidth = 2)  
        
        # use a more precise date string for the x axis locations in the toolbar
        ax2.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
        
        # rotate and align the tick labels so they look better; note that ax2 will 
        # have the dates, but ax1 will not. do not need to rotate each individual axis
        # because this method does it
        fig.autofmt_xdate()

        # save plots
        if save_path:        
            # set the size of the figure to be saved
            curr_fig = plt.gcf()
            curr_fig.set_size_inches(12, 10)
            
            # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
            filename = "-".join([watertxt_data1["user"], watertxt_data1["stationid"], " vs ", watertxt_data2["user"], watertxt_data2["stationid"], parameter1["name"].split("(")[0]])  + ".png"           
            filepath = os.path.join(save_path, filename)
            plt.savefig(filepath, dpi = 100)                        
          
        # show plots
        if is_visible:
            plt.show()
        else:
            plt.close()

def plot_watertxt_parameter(watertxt_data, name, is_visible = True, save_path = None):
    """   
    Plot a parameter contained in WATER.txt data file. Save 
    plots to a particular path.
    
    Parameters
    ----------
    watertxtdata_data : dictionary 
        A dictionary containing data found in WATER data file.
        
    name : string
        String name of parameter

    is_visible : bool
        Boolean value to show plots   
        
    save_path : string 
        String path to save plot(s) 
    """
    parameter = watertxt.get_parameter(watertxt_data, name = name)

    assert parameter is not None, "Parameter name {} is not in watertxt_data".format(name)

    dates = watertxt_data["dates"]
    fig = plt.figure(figsize = (12,10))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Parameter: {}".format(parameter["name"]))
    ax.set_xlabel("Date")
    ylabel = "\n".join(wrap(parameter["name"], 60))
    ax.set_ylabel(ylabel)

    # get proper color that corresponds to parameter name
    color_str = COLORS[name]

    # plot parameter    
    ax.plot(dates, parameter["data"], color = color_str, label = parameter["name"], linewidth = 2)   
 
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    
    # use a more precise date string for the x axis locations in the
    # toolbar
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
 
    # legend; make it transparent    
    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, fancybox = True)
    legend.get_frame().set_alpha(0.5)
    legend.draggable(state=True)
    
    # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
    text = "mean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter["mean"], parameter["max"], parameter["min"])
    patch_properties = {"boxstyle": "round",
                        "facecolor": "wheat",
                        "alpha": 0.5
                        }
                   
    ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
            verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
    
    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        
        # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
        filename = "-".join([watertxt_data["user"], watertxt_data["stationid"], parameter["name"].split("(")[0]])  + ".png"           
        filepath = os.path.join(save_path, filename)
        plt.savefig(filepath, dpi = 100)                        
      
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()
   
def plot_watertxt_parameter_comparison(watertxt_data, name1, name2, is_visible = True, save_path = None):
    """   
    Plot a comparison of two parameters contained in WATER.txt data file. Save 
    plots to a particular path.
    
    Parameters
    ----------
    watertxtdata_data : dictionary 
        A dictionary containing data found in WATER data file.
    name1 : string
        String name of parameter
    name2 : string
        String name of parameter
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    """
    parameter1 = watertxt.get_parameter(watertxt_data, name = name1)
    parameter2 = watertxt.get_parameter(watertxt_data, name = name2)
    
    assert parameter1 is not None, "Parameter name {} is not in watertxt_data".format(name1)
    assert parameter2 is not None, "Parameter name {} is not in watertxt_data".format(name2)   
    
    dates = watertxt_data["dates"]
    fig = plt.figure(figsize = (12,10))
    ax1 = fig.add_subplot(211)
    ax1.grid(True)
    ax1.set_title("Parameter: {} vs {}".format(parameter1["name"], parameter2["name"]))
    ax1.set_xlabel("Date")
    ylabel = "\n".join(wrap(parameter1["name"], 60))
    ax1.set_ylabel(ylabel)
    
    ax1.plot(dates, parameter1["data"], color = "b", label = parameter1["name"], linewidth = 2)
    ax1.hold(True)
    ax1.plot(dates, parameter2["data"], color = "r", label = parameter2["name"], linewidth = 2, alpha = 0.75)     
    
    # increase y axis to have text and legend show up better
    curr_ylim = ax1.get_ylim()
    ax1.set_ylim((curr_ylim[0], curr_ylim[1] * 1.5))

    # use a more precise date string for the x axis locations in the toolbar
    ax1.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    
    # legend; make it transparent    
    handles1, labels1 = ax1.get_legend_handles_labels()
    legend1 = ax1.legend(handles1, labels1, fancybox = True)
    legend1.get_frame().set_alpha(0.5)
    legend1.draggable(state=True)
    
    # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
    text = "mean = %.2f\nmax = %.2f\nmin = %.2f\n---\nmean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter1["mean"], parameter1["max"], parameter1["min"],
                                                                                              parameter2["mean"], parameter2["max"], parameter2["min"])
    patch_properties = {"boxstyle": "round",
                        "facecolor": "wheat",
                        "alpha": 0.5
                        }
                   
    ax1.text(0.05, 0.95, text, transform = ax1.transAxes, fontsize = 14, 
            verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
            
    # plot difference = values_b - values_a
    ax2 = fig.add_subplot(212, sharex = ax1)
    ax2.grid(True)
    ax2.set_title("Difference")
    ax2.set_xlabel("Date")
    ax2.set_ylabel(ylabel)
    diff = parameter2["data"] - parameter1["data"]
    ax2.plot(dates, diff, color = "k", linewidth = 2)  
    
    # use a more precise date string for the x axis locations in the toolbar
    ax2.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    
    # rotate and align the tick labels so they look better; note that ax2 will 
    # have the dates, but ax1 will not. do not need to rotate each individual axis
    # because this method does it
    fig.autofmt_xdate()


    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        
        # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
        filename = "-".join([watertxt_data["stationid"], parameter1["name"].split("(")[0], " vs ", parameter2["name"].split("(")[0]])  + ".png"           
        filepath = os.path.join(save_path, filename)
        plt.savefig(filepath, dpi = 100)                        
      
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()




def _create_test_data(multiplicative_factor = 1, stationid = "012345"):
    """ Create test data for tests """

    dates = [datetime.datetime(2014, 04, 01, 0, 0), datetime.datetime(2014, 04, 02, 0, 0), datetime.datetime(2014, 04, 03, 0, 0)]
    
    discharge_data = np.array([0, 5, 10]) * multiplicative_factor
    subsurface_data = np.array([50, 55, 45]) * multiplicative_factor
    impervious_data = np.array([2, 8, 2]) * multiplicative_factor
    infiltration_data = np.array([0, 1.5, 1.5]) * multiplicative_factor
    initialabstracted_data = np.array([0.1, 0.2, 0.3]) * multiplicative_factor
    overlandflow_data = np.array([3, 9, 3]) * multiplicative_factor
    pet_data = np.array([5, 13, 3]) * multiplicative_factor
    aet_data = np.array([5, 12, 13]) * multiplicative_factor
    avgsoilrootzone_data = np.array([40, 50, 60]) * multiplicative_factor
    avgsoilunsaturatedzone_data = np.array([4, 3, 2]) * multiplicative_factor
    snowpack_data = np.array([150, 125, 25]) * multiplicative_factor
    precipitation_data = np.array([0.5, 0.4, 0.3]) * multiplicative_factor
    storagedeficit_data = np.array([300, 310, 350]) * multiplicative_factor
    returnflow_data = np.array([-5.0, -4.5, -4.0]) * multiplicative_factor
    wateruse_data = np.array([4.0, 4.0, 4.0]) * multiplicative_factor
    discharge_wateruse_data = np.array([4.0, 9.0, 14.0]) * multiplicative_factor
    
    parameters = [{"name": "Discharge (cfs)", "index": 0, "data": discharge_data,
                   "mean": np.mean(discharge_data), "max": np.max(discharge_data), "min": np.min(discharge_data)}, 
                  
                  {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data,
                   "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)},

                  {"name": "Impervious Flow (mm/day)", "index": 2, "data": impervious_data,
                   "mean": np.mean(impervious_data), "max": np.max(impervious_data), "min": np.min(impervious_data)},

                  {"name": "Infiltration Excess (mm/day)", "index": 3, "data": infiltration_data,
                   "mean": np.mean(infiltration_data), "max": np.max(infiltration_data), "min": np.min(infiltration_data)},

                  {"name": "Initial Abstracted Flow (mm/day)", "index": 4, "data": initialabstracted_data,
                   "mean": np.mean(initialabstracted_data), "max": np.max(initialabstracted_data), "min": np.min(initialabstracted_data)},

                  {"name": "Overland Flow (mm/day)", "index": 5, "data": overlandflow_data,
                   "mean": np.mean(overlandflow_data), "max": np.max(overlandflow_data), "min": np.min(overlandflow_data)},

                  {"name": "PET (mm/day)", "index": 6, "data": pet_data,
                   "mean": np.mean(pet_data), "max": np.max(pet_data), "min": np.min(pet_data)},

                  {"name": "AET (mm/day)", "index": 7, "data": aet_data,
                   "mean": np.mean(aet_data), "max": np.max(aet_data), "min": np.min(aet_data)},

                  {"name": "Average Soil Root zone (mm)", "index": 8, "data": avgsoilrootzone_data,
                   "mean": np.mean(avgsoilrootzone_data), "max": np.max(avgsoilrootzone_data), "min": np.min(avgsoilrootzone_data)},

                  {"name": "Average Soil Unsaturated Zone (mm)", "index": 9, "data": avgsoilunsaturatedzone_data,
                   "mean": np.mean(avgsoilunsaturatedzone_data), "max": np.max(avgsoilunsaturatedzone_data), "min": np.min(avgsoilunsaturatedzone_data)},

                  {"name": "Snow Pack (mm)", "index": 10, "data": snowpack_data,
                   "mean": np.mean(snowpack_data), "max": np.max(snowpack_data), "min": np.min(snowpack_data)},

                  {"name": "Precipitation (mm/day)", "index": 11, "data": precipitation_data,
                   "mean": np.mean(precipitation_data), "max": np.max(precipitation_data), "min": np.min(precipitation_data)},

                  {"name": "Storage Deficit (mm/day)", "index": 12, "data": storagedeficit_data,
                   "mean": np.mean(storagedeficit_data), "max": np.max(storagedeficit_data), "min": np.min(storagedeficit_data)},

                  {"name": "Return Flow (mm/day)", "index": 13, "data": returnflow_data,
                   "mean": np.mean(returnflow_data), "max": np.max(returnflow_data), "min": np.min(returnflow_data)},

                  {"name": "Water Use (cfs)", "index": 14, "data": wateruse_data,
                   "mean": np.mean(wateruse_data), "max": np.max(wateruse_data), "min": np.min(wateruse_data)},

                  {"name": "Discharge + Water Use (cfs)", "index": 15, "data": discharge_wateruse_data,
                   "mean": np.mean(discharge_wateruse_data), "max": np.max(discharge_wateruse_data), "min": np.min(discharge_wateruse_data)},
    ] 

    data = {"user": "jlant", "date_created": "4/9/2014 15:30:00 PM", "stationid": stationid, 
            "column_names": ["Discharge (cfs)", "Subsurface Flow (mm/day)", "Impervious Flow (mm/day)", "Infiltration Excess (mm/day)", "Initial Abstracted Flow (mm/day)", "Overland Flow (mm/day)", "PET (mm/day)", "AET(mm/day)", "Average Soil Root zone (mm)", "Average Soil Unsaturated Zone (mm)", "Snow Pack (mm)", "Precipitation (mm/day)", "Storage Deficit (mm/day)", "Return Flow (mm/day)"],
            "parameters": parameters, "dates": dates}
    
    return data

    
def test_print_watertxt_data():
    """ Test print_watertxt_data() """
    
    print("---Testing print_watertxt_data() ---")
    
    data = _create_test_data()
    print_watertxt_data(watertxt_data = data)
    
    print("")

def test_plot_watertxt_data():
    """ Test plot_watertxt_data() """
    
    print("--- Testing plot_watertxt_data() ---")    
    
    data = _create_test_data()
    plot_watertxt_data(watertxt_data = data, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")

def test_plot_watertxt_comprison():
    """ Test plot_watertxt_comprison() """
    
    print("--- Testing plot_watertxt_comprison() ---")    
    
    data1 = _create_test_data()
    data2 = _create_test_data(multiplicative_factor = 2, stationid = "00000")
    plot_watertxt_comparison(watertxt_data1 = data1, watertxt_data2 = data2, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")

def test_plot_watertxt_parameter():
    """ Test plot_watertxt_data() """
    
    print("--- Testing plot_watertxt_data() ---")    
    
    data = _create_test_data()
    plot_watertxt_parameter(watertxt_data = data, name = "Discharge", is_visible = True, save_path = None)
    plot_watertxt_parameter(watertxt_data = data, name = "Subsurface Flow", is_visible = True, save_path = None) 
    plot_watertxt_parameter(watertxt_data = data, name = "Water Use", is_visible = True, save_path = None) 
    plot_watertxt_parameter(watertxt_data = data, name = "Discharge + Water Use", is_visible = True, save_path = None)   

    print("Plotting completed")
    print("")

def test_plot_watertxt_parameter_comprison():
    """ Test plot_watertxt_parameter_comprison() """
    
    print("--- Testing plot_watertxt_parameter_comprison() ---")    
    
    data = _create_test_data()
    plot_watertxt_parameter_comparison(watertxt_data = data, name1 = "Discharge", name2 = "Discharge + Water Use", is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")

     
def main():
    """ Test functionality of waterapputils_viewer() """

    print("")
    print("RUNNING TESTS ...")
    print("")
#
#    ans_print_watertxt_data = raw_input("Do you want to test print_watertxt_data()? y/n ")
#    if ans_print_watertxt_data == "y":
#         test_print_watertxt_data()
#
#    ans_plot_watertxt_data = raw_input("Do you want to test plot_watertxt_data()? y/n ")
#    if ans_plot_watertxt_data == "y":
#         test_plot_watertxt_data()  
#
#    ans_plot_watertxt_comprison = raw_input("Do you want to test plot_watertxt_comprison()? y/n ")
#    if ans_plot_watertxt_comprison == "y":
#         test_plot_watertxt_comprison()     
#
#    ans_plot_watertxt_parameter = raw_input("Do you want to test plot_watertxt_parameter_comprison()? y/n ")
#    if ans_plot_watertxt_parameter == "y":
#         test_plot_watertxt_parameter()   
#        
#    ans_plot_watertxt_parameter_comprison = raw_input("Do you want to test plot_watertxt_parameter_comprison()? y/n ")
#    if ans_plot_watertxt_parameter_comprison == "y":
#         test_plot_watertxt_parameter_comprison()    

    test_plot_watertxt_data()  
if __name__ == "__main__":
    main() 