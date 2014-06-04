# -*- coding: utf-8 -*-
"""
:Module: deltas_viewer.py

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
import deltas


def print_deltas_data(deltas_data):
    """   
    Print information contained in the delta data dictionary. 
    
    Parameters
    ----------
    watertxt_data : dictionary 
        A dictionary containing data found in WATER output text file.
    """   
   
    print("The following are the parameters and values in the file:")
    
    for key, value in deltas_data.iteritems():
        print("{}: {}".format(key, value))
            
def plot_deltas_data(deltas_data, is_visible = True, save_path = None):
    """   
    Plot each parameter contained in the nwis data. Save plots to a particular
    path.
    
    Parameters
    ----------
    deltasdata_data : dictionary 
        A dictionary containing data found in deltas data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s)
    """

    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Model: " + deltas_data["Model"] + " Scenario: " + deltas_data["Scenario"] + 
                " Target: " + deltas_data["Target"] + " Variable:" + deltas_data["Variable"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Delta Values")
    
    colors_list = ["b", "g", "r", "k", "y", "c", "m", "orange"]
    colors_index = 0
    for tile in deltas_data["Tile"]:        
        tile_index = deltas_data["Tile"].index(tile)
        month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]       
        dates = []        
        data = []
        for month in month_list:
            dates.append(datetime.datetime.strptime(month, "%B"))
            data.append(deltas_data[month][tile_index])
        
        # if the number of tiles exceeds the number of colors in colors list,
        # then randomly pick an rgb color
        if colors_index > len(colors_list) - 1:
            c = np.random.rand(3,)
        else:
            c = colors_list[colors_index]
            
        plt.plot(dates, data, color = c, linestyle = "-", marker = "o", label = tile)
        plt.hold(True)
        
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # set the x axis to display only the month; "%B" => full month name; "%b" => abreviated month name
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%B"))
        
        # legend; make it transparent    
        handles, labels = ax.get_legend_handles_labels()
        legend = ax.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "Model = %s\nScenario = %s\nTarget = %s\nVariable = %s" % (deltas_data["Model"], deltas_data["Scenario"], 
                                                                          deltas_data["Target"], deltas_data["Variable"])
        patch_properties = {"boxstyle": "round",
                            "facecolor": "wheat",
                            "alpha": 0.5
                            }
                       
        ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
        
        colors_index += 1
        
    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        filename = deltas_data["Model"] + "_" + deltas_data["Scenario"] + "_" + deltas_data["Target"] + "_" + deltas_data["Variable"]
        plt.savefig(save_path + "/" + filename +".png", dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()

def _create_test_data():
    """ Create a delta data dictionary for tests """

    data = {"Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", "Tile": ["11", "12", "21", "22", "31", "32"],
            "January": [1.3, 1.2, 1.3, 1.4, 1.5, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
            "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
            "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
            "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]           
    }

    return data

def test_print_deltas_data():
    """ Test print_deltas_data() """
    
    print("---Testing print_deltas_data() ---")
    
    data = _create_test_data()
    print_deltas_data(deltas_data = data)
    
    print("")
    
def test_plot_deltas_data():
    """ Test plot_deltas_data() """
    
    print("--- Testing plot_deltas_data() ---")    
    
    data = _create_test_data()
    plot_deltas_data(deltas_data = data, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")


def main():
    """ Test functionality of deltas_viewer() """

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_print_deltas_data() 
    
    test_plot_deltas_data() 

if __name__ == "__main__":
    main() 