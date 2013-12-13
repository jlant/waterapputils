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
import logging

# my modules
import helpers

def main():  
    """
    Run as a script. Prompt user for delta *.txt file, process the file, 
    print information, and plot data. Information is printed to the screen.  
    Plots are saved to a directory called 'figs' which is created in the same 
    directory as the data file. A log file called 'delta_error.log' is created 
    if any errors are found in the data file.
    
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
            
            # make a directory called updated_xml to hold the updated xml file             
            deltas_path = dirname + '/deltas'
            if not os.path.exists(deltas_path):
                os.makedirs(deltas_path) 
                
            # log any errors or warnings found in file; save to data file directory
            logging.basicConfig(filename = dirname + '/delta_error.log', filemode = 'w', level=logging.DEBUG)
            
            # process file
            print ''
            print '** Processing **'
            print delta_file
            delta_data = read_file(delta_file)         
            
            # print 'Project' information
            print ''
            print '** Delta Data Information **'
            print_info(data_dict = delta_data)
            
              
            
            # example delta dataset
            delta_values = {
                'ClimaticTemperatureSeries': {
                    'January': 2.0,
                    'February': 0.98,
                    'March': 0.97,
                    'April': 1.04,
                    'May': 1.10,
                    'June': 0.99,
                    'July': 0.97,
                    'August': 1.25,
                    'September': 1.21,
                    'October': 1.11,
                    'November': 1.10,
                    'December': 2.0
                },
                'ClimaticPrecipitationSeries': {
                    'January': 2.0,
                    'February': 0.98,
                    'March': 0.97,
                    'April': 1.04,
                    'May': 1.10,
                    'June': 0.99,
                    'July': 0.97,
                    'August': 1.25,
                    'September': 1.21,
                    'October': 1.11,
                    'November': 1.10,
                    'December': 2.0
                },
            }            
            
            # shutdown the logging system
            logging.shutdown()

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
    
    *Parameters:*
        filestream: file object
    
    *Return:*
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
       
    # fix duplicates for particular keys
    key_list = ['Model', 'Scenario', 'Target', 'Variable']
    for parameter in data['parameters']:
        if parameter['name'] in key_list:
            parameter['data'] = parameter['data'][0]
        elif parameter['name'] == 'Tile':
            pass
        else:
            parameter['data'] = np.array(parameter['data'], dtype = float)
    
    return data

    

if __name__ == "__main__":
    
    # read file, print results, and plot 
    main() 

