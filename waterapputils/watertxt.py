# -*- coding: utf-8 -*-
"""
:Module: watertxt.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Read, process, plot, and print information about an output file created 
by the WATER application.

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


def read_file(filename):
    """    
    Open WATER file, create a file object for read_file_in(filestream) to process.
    This function is responsible to opening the file, removing the file opening  
    responsibility from read_file_in(filestream) so that read_file_in(filestream)  
    can be unit tested.
    
    *Parameters:*
		filename : string path to water text file
    
    *Return:*
        data : dictionary holding data found in water text file  
        
    """
    
    filestream = open(filename, 'r')
    data = read_file_in(filestream)
    filestream.close()
    
    return data

def read_file_in(filestream):
    """    
    Read and process a WATER *.txt file. Finds any parameter and its respective data. 
    Relevant data is put into a dictionary (see Return section).  Missing data values
    are replaced with a NAN value. 
    
    *Parameters:*
        filestream: file object
    
    *Return:*
        data: dictionary holding data found in WATER *.txt data file
        
        data = {
            'user': None,
            
            'date_created': None,
            
            'stationid': None,
            
            'column_names': None,
            
            'dates': [],
            
            'parameters': [], 
              
        }      
                
        ** Note: The 'parameters' key contains a list of dictionaries containing
        the parameters found in the data file; i.e.
        
        parameters[0] = {
            'name': string of parameter name,
            
            'index': integer of column index data is located,
            
            'data': numpy array of data values,
            
            'mean': mean of data values,
            
            'max': max of data values,
            
            'min': min of data values
        }        
        
    """  
    
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file 
    patterns = {
        'user': '(User:)\t(.+)',
        'date_created': '(Date:)\t(.+)',
        'stationid': '(StationID:)\t(.+)',
        'column_names': '(Date)\t(.+)',
        'data_row': '([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\t(.+)'
    }        

   # initialize a dictionary to hold all the data of interest
    data = {
        'user': None,
        'date_created': None,
        'stationid': None,
        'column_names': None,
        'dates': [],
        'parameters': []
    }      
    
    # process file
    for line in data_file: 
        # find match
        match_user = re.search(pattern = patterns['user'], string = line)
        match_date_created = re.search(pattern = patterns['date_created'], string = line)
        match_stationid = re.search(pattern = patterns['stationid'], string = line)       
        match_column_names = re.search(pattern = patterns['column_names'], string = line)
        match_data_row = re.search(pattern = patterns['data_row'], string = line)
     
        # if match is found add it to data dictionary
        if match_user:
            data['user'] = match_user.group(2) 
        if match_date_created:
            data['date_created'] = match_date_created.group(2)
        if match_stationid:
            data['stationid'] = match_stationid.group(2)
        if match_column_names:
            # group(2) does not include dates which are added during data row match
            data['column_names'] = match_column_names.group(2).split('\t')
            # create a dictionary for each column_name (excluding 'Date')
            for name in data['column_names']:
                data['parameters'].append({
                    'name': name,
                    'index': data['column_names'].index(name) ,
                    'data': [],
                    'mean': None,
                    'max': None,
                    'min': None
                })
            
#            for parameter in data['parameters']:
#                parameter['index'] = data['column_names'].index(parameter['name'])           

        if match_data_row:
            # add date to data dictionary
            year = match_data_row.group(1).split('/')[2]
            month = match_data_row.group(1).split('/')[0]
            day = match_data_row.group(1).split('/')[1]
            date = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
            data['dates'].append(date)            
            
            for parameter in data['parameters']:
                value = match_data_row.group(2).split('\t')[parameter['index']]
                
                if not helpers.is_float(value):
                    if value == "":
                        error_str = '**Missing value on ' + str(date) + ' *Filling with Not A Number (NAN)'
                        print error_str
                        logging.info(error_str)
                        value = np.nan
                                       
                    else:
                        error_str = '**ERROR on ' + str(date) +' Value can not be converted to a float: ' + value + '**Exiting. Bad data in file!'
                        raise ValueError(error_str)
                        sys.exit('**Exiting. Bad data in file!')
                        
                parameter['data'].append(float(value)) 
                
            
    # convert the date list to a numpy array
    data['dates'] = np.array(data['dates']) 
    
    # convert each parameter data list in data['parameter'] convert to a numpy array and
    # compute mean, max, and min 
    for parameter in data['parameters']:
        parameter['data'] = np.array(parameter['data'])
        parameter['mean'] = np.mean(parameter['data'])
        parameter['max'] = np.max(parameter['data'])
        parameter['min'] = np.min(parameter['data'])
    
    # return data
    return data

def print_info(water_data):
    """   
    Print relevant information and contained in the water data 
    
    *Parameters*:
        water_data: dictionary holding data from WATER *.txt file
        
    *Return*:
        no return
        
    """   
    
    # print relevant information
    print 'User: ', water_data['user']
    print 'Date and time created: ', water_data['date_created']
    print 'StationID: ', water_data['stationid']
    
    print 'The following are the parameters avaiable in the file:'
    # print each parameter
    for parameter in water_data['parameters']:
        print parameter['name']

def plot_data(water_data, is_visible = True, save_path = None):
    """   
    Plot each parameter contained in the water data. Save plots to a particular
    path.
    
    *Parameters*:
        water_data: dictionary holding data from WATER *.txt file
        
        save_path: string path to save plot(s) 
        
    *Return*:
        no return
        
    """
    
    for parameter in water_data['parameters']:
        
        fig = plt.figure(figsize=(12,10))
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_title(parameter['name'] + ' (' + water_data['stationid'] + ')')
        ax.set_xlabel('Date')
        ax.set_ylabel(parameter['name'])
        plt.plot(water_data['dates'], parameter['data'], color = 'b', marker = 'o', label = parameter['name'])
    
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
     
        # legend; make it transparent    
        handles, labels = ax.get_legend_handles_labels()
        legend = ax.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = 'mean = %.2f\nmax = %.2f\nmin = %.2f' % (parameter['mean'], parameter['max'], parameter['min'])
        patch_properties = {'boxstyle': 'round',
                            'facecolor': 'wheat',
                            'alpha': 0.5
                            }
                       
        ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
        
        # save plots
        if save_path:        
            # set the size of the figure to be saved
            curr_fig = plt.gcf()
            curr_fig.set_size_inches(12, 10)
            parameter_name = parameter['name'].split('(')[0].strip()
            plt.savefig(save_path + '/' + water_data['stationid'] + ' - ' + parameter_name +'.png', dpi = 100)
            
        # show plots
        if is_visible:
            plt.show()
        else:
            plt.close()

def main():  
    """
    Run as a script. Prompt user for WATER text file, process the file, print information, 
    and plot data. Information is printed to the screen.  Plots are saved to a directory 
    called 'figs' which is created in the same directory as the data file. A
    log file called 'water_error.log' is created if any errors are found in the 
    data file.
    
    """ 
    
    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    water_file = tkFileDialog.askopenfilename(title = 'Select WATER.txt file', filetypes = file_format)
    root.destroy()
    
    if water_file:
        
        try:
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(water_file))
            
            # make a directory called figs to hold the plots            
            figs_path = dirname + '/figs'
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
            
            # log any errors or warnings found in file; save to data file directory
            logging.basicConfig(filename = dirname + '/water_error.log', filemode = 'w', level=logging.DEBUG)
            
            # process file
            print ''
            print '** Processing **'
            print water_file
            water_data = read_file(water_file)
            
            
            # print information
            print ''
            print '** USGS WATER text file Information **'
            print_info(water_data)
            
            # plot parameters
            print ''
            print '** Plotting **'
            print 'Plots are being saved to same directory as WATER text file.'
            plot_data(water_data, is_visible = False, save_path = figs_path)

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
    

if __name__ == "__main__":
    
    # read file, print results, and plot 
    main()
