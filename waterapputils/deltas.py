# -*- coding: utf-8 -*-
"""
:Module: deltas.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Read, parse, and retrieve delta timeseries values for temperature, precipitation,
and pet for various GCM models to be applied to temperature, precipitation, and 
pet values from the WATER application developed by Williamson, T., Ulery, R.
and Newson, J.

"""

import os
import sys
import re
import numpy as np
import datetime
import Tkinter, tkFileDialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# my modules
import helpers


def get_deltavalues(delta_data, tile_list):
    """   
    Process and return delta data values for a list of tiles of interest. Delta 
    values are averaged when there are multiple tiles.
    
    *Parameters*:
        delta_data_list: list of dictionaries holding data from many delta data files
        
    *Return*:
        delta_values: dictionary holding data for specific list of tiles; i.e.
        
            delta_values = {
                'Ppt': {
                    'January': 2.0,
                    'February': 0.98,
                    'March': 0.97,
                    'April': 1.04,
                    'May': 1.10,
                    'June': 0.99,
                    'July': 0.87,
                    'August': 0.75,
                    'September': 0.95,
                    'October': 0.98,
                    'November': 1.10,
                    'December': 2.0
                }
            } 
        
    """ 
    delta_values = {}
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']       
    
    # initialize a dictionary containing month keys and None values
    month_dict = {}
    for month in month_list:
        month_dict[month] = None
    
    # set the initialized month dictionary as a value into specific variable key
    variable = delta_data['Variable']
    delta_values[variable] = month_dict
    
    # get tile indices and values for a specific list of tiles
    values = []
    for tile in tile_list:
        if tile in delta_data['Tile']:
            monthly_values = []
            tile_index = delta_data['Tile'].index(tile)
            for month in month_list:
                value = delta_data[month][tile_index]
                monthly_values.append(value)
                
            values.append(monthly_values)

        else: 
            print tile + ' is not in delta_data[Tile] list'

    # convert delta values into a numpy array; take average (axis = 0 => along columns)
    # value for multiple tiles
    values = np.array(values, dtype = float)
    values_avg = np.average(values, axis = 0)
    
    # fill delta value dictionary with values
    month_enum_list = list(enumerate(month_list))
    for item in month_enum_list:
        index = item[0]
        month = item[1]
        delta_values[variable][month] = values_avg[index]
    
    return delta_values

def print_info(delta_data):
    """   
    Print relevant information contained in the delta data file. 
    
    *Parameters*:
        delta_data: dictionary holding data fromdelta data file
        
    *Return*:
        no return
        
    """   
    
    # print relevant information    
    print 'The following are the parameters and values in the file:'
    
    for key, value in delta_data.iteritems():
        print key, value


def plot_data(delta_data, is_visible = True, save_path = None):
    """   
    Plot each parameter contained in the delta data. Save plots to a particular
    path.
    
    *Parameters*:
        delta_data: dictionary holding data from delta data file
        
        save_path: string path to save plot(s) 
        
    *Return*:
        no return
        
    """

    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title('Model: ' + delta_data['Model'] + ' Scenario: ' + delta_data['Scenario'] + 
                ' Target: ' + delta_data['Target'] + ' Variable:' + delta_data['Variable'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Delta Values')
    
    colors_list = ['b', 'g', 'r', 'k', 'y', 'c', 'm', 'orange']
    colors_index = 0
    for tile in delta_data['Tile']:
        
        tile_index = delta_data['Tile'].index(tile)
        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']       
        dates = []        
        data = []
        for month in month_list:
            dates.append(datetime.datetime.strptime(month, '%B'))
            data.append(delta_data[month][tile_index])
        
        # if the number of tiles exceeds the number of colors in colors list,
        # then randomly pick an rgb color
        if colors_index > len(colors_list) - 1:
            c = np.random.rand(3,)
        else:
            c = colors_list[colors_index]
            
        plt.plot(dates, data, color = c, linestyle = '-', marker = 'o', label = tile)
        plt.hold(True)
        
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # set the x axis to display only the month; '%B' => full month name; '%b' => abreviated month name
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
        
        # legend; make it transparent    
        handles, labels = ax.get_legend_handles_labels()
        legend = ax.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = 'Model = %s\nScenario = %s\nTarget = %s\nVariable = %s' % (delta_data['Model'], delta_data['Scenario'], 
                                                                          delta_data['Target'], delta_data['Variable'])
        patch_properties = {'boxstyle': 'round',
                            'facecolor': 'wheat',
                            'alpha': 0.5
                            }
                       
        ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
        
        colors_index += 1
        
    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        filename = delta_data['Model'] + '_' + delta_data['Scenario'] + '_' + delta_data['Target'] + '_' + delta_data['Variable']
        plt.savefig(save_path + '/' + filename +'.png', dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()


def read_file(filename):
    """    
    Open delta *.txt file, create a file object for read_file_in(filestream) to process.
    This function is responsible to opening the file, removing the file opening  
    responsibility from read_file_in(filestream) so that read_file_in(filestream)  
    can be unit tested.
    
    *Parameters:*
		filename : string path to delta text file
    
    *Return:*
        data : dictionary holding data found in delta text file  
        
    """
    
    filestream = open(filename, 'r')
    data = read_file_in(filestream)
    filestream.close()
    
    return data

def read_file_in(filestream):
    """    
    Read and process a delta *.txt file. Finds any parameter and its respective data. 
    Relevant data is put into a dictionary (see Return section). 
    
        ** Note:
        data: dictionary holding data found in delta *.txt data file
        
        data = {
            
            'column_names': None,
                       
            'parameters': [], 
              
        }      
                
        ** Note: The 'parameters' key contains a list of dictionaries containing
        the parameters found in the data file; i.e.
        
        parameters[0] = {
            'name': string of parameter name,
            
            'index': integer of column index data is located in file,
            
            'data': numpy array of data values,
            
        }  
        
    *Parameters:*
        filestream: file object
    
    *Return:*
        data_formatted: formatted dictionary holding data found in delta *.txt data file
        
        data_formatted = {
            'Model': string of model name,
            
            'Scenario': string of scenario name,
            
            'Target': string of scenario name,
            
            'Variable': string of variable name,
            
            'Tile': list of tile numbers,
            
            'January': array of delta values for each tile
            
            . . .
            
            'December': array of delta values for each tile
            
        }  
        
    """ 
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file
    patterns = {
        'column_names': '(Model.+)',
        'data_row': '(\w+)\t(\w+)\t(\d+)\t(.+)'
    }        

   # initialize a dictionary to hold all the data of interest
    data = {
        'column_names': None,
        'parameters': []
    }      
    
    # process file
    for line in data_file:     
        match_column_names = re.search(pattern = patterns['column_names'], string = line)
        match_data_row = re.search(pattern = patterns['data_row'], string = line)
     
        # if match is found add it to data dictionary
        if match_column_names:
            data['column_names'] = match_column_names.group(0).split('\t') 
            
            for name in data['column_names']:
                data['parameters'].append({
                    'name': name,
                    'index': data['column_names'].index(name),
                    'data': []
                })
                
        if match_data_row:
            for parameter in data['parameters']:
                value = match_data_row.group(0).split('\t')[parameter['index']]                        
                parameter['data'].append(value) 
       
    # get first value for particular keys that contain duplicates and convert 
    # strings to floats for the delta values
    key_list = ['Model', 'Scenario', 'Target', 'Variable']
    data_formatted = {}
    for parameter in data['parameters']:
        if parameter['name'] in key_list:
            parameter['data'] = parameter['data'][0]
        elif parameter['name'] == 'Tile':
            pass
        else:
            parameter['data'] = np.array(parameter['data'], dtype = float)    

        # create formatted dictionary
        data_formatted[parameter['name']] = parameter['data']       
    
    return data_formatted

def main_singlefile():  
    """
    Run as a script. Prompt user for delta *.txt file, process the file, 
    print information, and plot data. Information is printed to the screen.  
    Plots are saved to a directory called 'figs' which is created in the same 
    directory as the data file.
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    delta_file = tkFileDialog.askopenfilename(title = 'Select Delta *.txt file', filetypes = file_format)
    root.destroy()
    
    if delta_file:
        
        try:
            
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(delta_file))
            
            # make a directory called figs to hold the plots            
            figs_path = dirname + '/figs'
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
            
            # process file
            print ''
            print '** Processing **'
            print delta_file
            delta_data = read_file(delta_file)         
            
            # print 'Project' information
            print ''
            print '** Delta Data Information **'
            print_info(delta_data)
            
            # plot data
            print ''
            print '** Plotting **'
            print 'Plots are being saved to same directory as data file.'
            plot_data(delta_data, is_visible = False, save_path = figs_path)

        except IOError as error:
            print 'Cannot read file!' + error.filename
            print error.message
            
        except IndexError as error:
            print 'Cannot read file! Bad file!'
            print error.message
            
        except ValueError as error:
            print error.message
                
    else:
        print '** Canceled **'
 

def main_multifile():  
    """
    Run as a script. Prompt user for delta *.txt files, process the files, 
    print information, and plot data. Information is printed to the screen.  
    Plots are saved to a directory called 'figs' which is created in the same 
    directory as the data file. 
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    delta_files = tkFileDialog.askopenfilenames(title = 'Select Multiple Delta *.txt files', filetypes = file_format)
    delta_files = delta_files.split()
    root.destroy()
    
    delta_data_allfiles = []
    delta_values_allfiles = []
    for delta_file in delta_files:
        if delta_file:
            
            try:
                
                # get directory and filename from data file
                dirname, filename = os.path.split(os.path.abspath(delta_file))
                
                # make a directory called figs to hold the plots            
                figs_path = dirname + '/figs'
                if not os.path.exists(figs_path):
                    os.makedirs(figs_path)            
                
                # process file
                print ''
                print '** Processing **'
                print delta_file
                delta_data = read_file(delta_file)         
                delta_data_allfiles.append(delta_data)
                
                # print 'Project' information
                print ''
                print '** Delta Data Information **'
                print_info(delta_data)
                
                # plot data
                print ''
                print '** Plotting **'
                print 'Plots are being saved to same directory as data file.'
                plot_data(delta_data, is_visible = False, save_path = figs_path)
    
                # get, process, and format data for a list of tiles
                tiles = ['11', '12', '22']
                delta_values = get_deltavalues(delta_data = delta_data, tile_list = tiles)
                delta_values_allfiles.append(delta_values)

                        
            except IOError as error:
                print 'Cannot read file!' + error.filename
                print error.message
                
            except IndexError as error:
                print 'Cannot read file! Bad file!'
                print error.message
                
            except ValueError as error:
                print error.message
                    
        else:
            print '** Canceled **'

def main_shapefile():  
    """
    Run as a script. Prompt user for delta *.txt files, process the files, and 
    print information. Information is printed to the screen. Prompt user for 
    basin shapefile and climate data deltas tiled shapefile. Get the tile numbers
    that the basin encompasses.
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    delta_files = tkFileDialog.askopenfilenames(title = 'Select Multiple Delta *.txt files', filetypes = file_format)
    delta_files = delta_files.split()
    root.destroy()
    
    delta_data_allfiles = []
    delta_values_allfiles = []
    for delta_file in delta_files:
        if delta_file:
            
            try:
                
                # get directory and filename from data file
                dirname, filename = os.path.split(os.path.abspath(delta_file))
                
                # make a directory called figs to hold the plots            
                figs_path = dirname + '/figs'
                if not os.path.exists(figs_path):
                    os.makedirs(figs_path)            
                
                # process file
                print ''
                print '** Processing **'
                print delta_file
                delta_data = read_file(delta_file)         
                delta_data_allfiles.append(delta_data)
                
                # print 'Project' information
                print ''
                print '** Delta Data Information **'
                print_info(delta_data)
                
                # plot data
                print ''
                print '** Plotting **'
                print 'Plots are being saved to same directory as data file.'
                plot_data(delta_data, is_visible = False, save_path = figs_path)
    
                # get, process, and format data for a list of tiles
                tiles = ['11', '12', '22']
                delta_values = get_deltavalues(delta_data = delta_data, tile_list = tiles)
                delta_values_allfiles.append(delta_values)

                        
            except IOError as error:
                print 'Cannot read file!' + error.filename
                print error.message
                
            except IndexError as error:
                print 'Cannot read file! Bad file!'
                print error.message
                
            except ValueError as error:
                print error.message
                    
        else:
            print '** Canceled **'


if __name__ == "__main__":
    
    # read file, print results, and plot 
    #main_singlefile() 
    main_multifile()

