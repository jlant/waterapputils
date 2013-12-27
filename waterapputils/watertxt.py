# -*- coding: utf-8 -*-
"""
:Module: watertxt.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Read, process, plot, and print information about the WATER.txt output file 
created by the WATER application developed by Williamson, T., Ulery, R.and 
Newson, J.

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
import deltas

def get_parameter_data(water_data, parameter_name):
    """   
    Get dates, values, and units from a particular parameter contained in the 
    water_data dictionary. 
    
    *Parameters*:
        water_data : dictionary holding data from WATER *.txt file 
        parameter_name : string of parameter of interest

    *Return*:
        dates : numpy array of dates
        values : numpy array of floats
        units : string of unit for a particular parameter
        
    """
    
    dates = water_data['dates']    
    
    for parameter in water_data['parameters']:
        parameter_str = parameter['name'].split('(')[0].strip()
        parameter_name_str = parameter_name.split('(')[0].strip()
        if parameter_str == parameter_name_str :
            values = parameter['data']
            units = parameter['name'].split('(')[1].split(')')[0]
            mean_val = parameter['mean']
            max_val = parameter['max']
            min_val = parameter['min']
    
    return dates, values, units, mean_val, max_val, min_val

def print_info(water_data):
    """   
    Print relevant information contained in the water data file.
    
    *Parameters*:
        water_data : dictionary holding data from WATER *.txt file
        
    *Return*:
        no return
        
    """   
    
    # print relevant information
    print 'User: ', water_data['user']
    print 'Date and time created: ', water_data['date_created']
    print 'StationID: ', water_data['stationid']
    
    print 'The following are the parameters available in the file:'
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
        ax.set_title('Parameter: ' + parameter['name'] + ' Stationid: ' + water_data['stationid'])
        ax.set_xlabel('Date')
        ax.set_ylabel(parameter['name'])
        plt.plot(water_data['dates'], parameter['data'], color = 'b', linewidth = 2, label = parameter['name'])
    
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

def plot_parameter_comparison(parameter_name, water_data_a, water_data_b, is_visible = True, save_path = None, txt_filenames = None):
    """   
    Plot a comparison of two parameters contained in WATER.txt data file. Save 
    plots to a particular path.
    
    *Parameters*:
        parameter_name : string of parameter
        water_data_a: dictionary holding data found in WATER *.txt data file
        water_data_b: dictionary holding data found in WATER *.txt data file
        is_visible : boolean to show plots
        save_path : string path to save plot(s) 
        txt_filenames : list of two txt filenames

    *Return*:
        no return
    
    * Note: fig.autofmt_xdate() sets and rotates the axes properly; do not need
    to set them individually as:
        # rotate and align the tick labels so they look better; do not      
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation = 30)    
        
        # rotate and align the tick labels so they look better 
        #plt.xticks(rotation = 30) # same thing as plt.setp(...)
        #ax2.xticks(rotation = 30) # same thing as plt.setp(...)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation = 30)
        
    """
    
    dates_a, values_a, units_a, mean_a, max_a, min_a = get_parameter_data(parameter_name = parameter_name, water_data = water_data_a)
    dates_b, values_b, units_b, mean_b, max_b, min_b = get_parameter_data(parameter_name = parameter_name, water_data = water_data_b)

    fig = plt.figure(figsize = (12,10))
    
    # plot original vs. updated
    ax1 = fig.add_subplot(211)
    ax1.grid(True)
    ax1.set_title(' Parameter: ' + parameter_name)
    ax1.set_xlabel('Date')
    ax1.set_ylabel(parameter_name  + ' (' + units_a + ')')
    ax1.plot(dates_a, values_a, color = 'b', label = txt_filenames[0], linewidth = 2)
    ax1.hold(True)
    ax1.plot(dates_b, values_b, color = 'r', label = txt_filenames[1], linewidth = 2, alpha = 0.6)
    # increase y axis to have text and legend show up better
    curr_ylim = ax1.get_ylim()
    ax1.set_ylim((curr_ylim[0], curr_ylim[1] * 1.5))

    # use a more precise date string for the x axis locations in the toolbar
    ax1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    # legend; make it transparent    
    handles1, labels1 = ax1.get_legend_handles_labels()
    legend1 = ax1.legend(handles1, labels1, fancybox = True)
    legend1.get_frame().set_alpha(0.5)
    legend1.draggable(state=True)
    
    # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
    text = 'mean = %.2f\nmax = %.2f\nmin = %.2f\n---\nmean = %.2f\nmax = %.2f\nmin = %.2f' % (mean_a, max_a, min_a,
                                                                                              mean_b, max_b, min_b)
    patch_properties = {'boxstyle': 'round',
                        'facecolor': 'wheat',
                        'alpha': 0.5
                        }
                   
    ax1.text(0.05, 0.95, text, transform = ax1.transAxes, fontsize = 14, 
            verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
            
    # plot difference = values_b - values_a
    ax2 = fig.add_subplot(212, sharex = ax1)
    ax2.grid(True)
    ax2.set_title('Difference: ' + parameter_name)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Difference' + ' (' + units_a + ')')
    diff = values_b - values_a
    ax2.plot(dates_a, diff, color = 'k', linewidth = 2)  
    
    # use a more precise date string for the x axis locations in the toolbar
    ax2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    # rotate and align the tick labels so they look better; note that ax2 will 
    # have the dates, but ax1 will not. do not need to rotate each individual axis
    # because this method does it
    fig.autofmt_xdate()
    
    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        plt.savefig(save_path + '/' + 'comparison_' + parameter_name +'.png', dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()


def read_file(filename):
    """    
    Open WATER.txt file, create a file object for read_file_in(filestream) to process.
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
    

def set_factors(water_data, parameter_name, factors):
    """
    Set new data for a particular parameter using a timeseries of factor  
    values. The factors are multiplicative.
    
    Example factors:
    
        factors = {
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
        }  
        
    *Parameters:*
        tree : ElementTree object of entire xml file
        element_str : string of a particular element of interest
        delta_values : dictionary of delta values
    
    *Return:*
        No return
    """  
    
    dates, values, units, mean_val, max_val, min_val = get_parameter_data(water_data, parameter_name)
        
    new_values = []
    for i in range(len(dates)):
        date = dates[i]
        # get the month name to match the delta_factor dictionary keys
        month_name = date.strftime('%B')
        factor = factors[month_name]
        
        # appply factor
        new_value = values[i] * factor
        new_values.append(new_value)
            
    new_values = np.array(new_values)

    # set new values in water_data    
    water_data = set_parameter_data(water_data, parameter_name, new_values)

    return water_data      

def set_parameter_data(water_data, parameter_name, values):
    """   
    Set new values for a particular parameter contained in the water_data
    dictionary. 
    
    *Parameters*:
        water_data : dictionary holding data from WATER *.txt file
        parameter_name : string of parameter of interest
        values : numpy array of floats
        
    *Return*:
        water_data : updated dictionary holding data from WATER *.txt file
        
    """  
    
    for parameter in water_data['parameters']:
        parameter_str = parameter['name'].split('(')[0].strip()
        parameter_name_str = parameter_name.split('(')[0].strip()
        if parameter_str == parameter_name_str:
            parameter['data'] = values

    return water_data
    

def write_txtfile(water_data, save_path = None, output_filename = None):
    """   
    Write data contained in 4the water data dictionary to an output file formatted
    the same as the original WATER.txt file.
    
    *Parameters*:
        water_data : dictionary holding data found in WATER *.txt data file
        save_path : string of directory path to save file
        output_filename : string of output filename
    
    *Return*:
        No return
        
    """ 
    
    header = " ------------------------------------------------------------------------------\n\
 ----- WATER ------------------------------------------------------------------\n\
 ------------------------------------------------------------------------------\n"
 
    output_fullpath = save_path + '/' + output_filename
    output_file = open(output_fullpath, 'w')
    output_file.write(header)
    output_file.write('User:' + '\t' + water_data['user'] + '\n')
    output_file.write('Date:' + '\t' + water_data['date_created'] + '\n')
    output_file.write('StationID:' + '\t' + water_data['stationid'] + '\n')
    output_file.write('Date' + '\t' + '\t'.join(water_data['column_names']) + '\n')
    
    values_all = []
    for column_name in water_data['column_names']:
        dates, values, units, mean_val, max_val, min_val = get_parameter_data(water_data, column_name)
        values_all.append(values)

    values_all = np.array(values_all)
    values_all = np.transpose(values_all)
    num_rows = np.shape(values_all)[0]
    num_columns = np.shape(values_all)[1]
    for i in range(num_rows):
        date = dates[i]
        year = date.year
        month = date.month
        day = date.day
        date_str = '/'.join([str(month), str(day), str(year)])
        output_file.write(date_str + '\t')
        
        row = []
        for j in range(num_columns):
            row.append(str(values_all[i][j]))
        
        output_file.write('\t'.join(row) + '\n')
            
    output_file.close()
    

def main_singlefile():  
    """
    Run as a script. Prompt user for WATER text file, process the file, print information, 
    and plot data. Information is printed to the screen.  Plots are saved to a directory 
    called 'figs/txt-figs/' which is created in the same directory as the data file.
    
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
            figs_path = dirname + '/figs' + '/txt-figs/' + filename
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
            
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

def main_comparetxtfiles():  
    """
    Run as a script. Prompt user for 2 WATER.txt files to compare.
    Process the file, print information, and plot data. Information is printed
    to the screen.  Plots are saved to a directory called 'figs/txt-figs'
    which is created in the same directory as the *.xml data file. 
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    water_files = tkFileDialog.askopenfilenames(title = 'Select 2 WATER.txt files to compare', filetypes = file_format)
    water_files = water_files.split()
    root.destroy()
    
    water_allfiles = []
    for water_file in water_files:
        if water_file:
            
            try:
                
                # get directory and filename from data file
                dirname, filename = os.path.split(os.path.abspath(water_file))
                
                # process file
                print ''
                print '** Processing **'
                print water_file
                water_data = read_file(water_file)
                water_allfiles.append(water_data)
            
                # print information
                print ''
                print '** USGS WATER text file Information **'
                print_info(water_data)                                                                                                                                                                                                                  
                      
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
        
    
    # make a directory called figs to hold the plots
    filenames = []
    for water_file in water_files:                
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(water_file)) 
            filenames.append(filename)
            
    figs_path = dirname + '/figs' + '/txt-figs/' + filenames[0] + '_vs_' + filenames[1]
    if not os.path.exists(figs_path):
        os.makedirs(figs_path)  
        
    # plot data                
    print ''                                                                                                             
    print '** Plotting **'
    # plot data comparison for parameters of interest
    parameters = ['Precipitation', 'PET'] 
    for parameter in parameters:
        plot_parameter_comparison(parameter_name = parameter,
                                  water_data_a = water_allfiles[0],
                                  water_data_b = water_allfiles[1],
                                  is_visible = True, 
                                  save_path = figs_path,
                                  txt_filenames = filenames)                     


def main_setsampledeltas():  
    """
    Run as a script. Prompt user for WATER.txt file, process the file, 
    and print information. Information is printed to the screen. Set/appply sample deltas
    in WATER.txt file and create a new text file called
    WATER_sampledeltas.txt file
    
    Sample deltas used:
            deltas_data = {
                'PET': {
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
                },
            }     
    
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
            figs_path = dirname + '/figs' + '/txt-figs/' + filename
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
            
            # process file
            print ''
            print '** Processing **'
            print water_file
            water_data = read_file(water_file)
            
            # print information
            print ''
            print '** USGS WATER text file Information **'
            print_info(water_data)
                                                                                                                                        
            # sample deltas data and apply to precipiation and temperature timeseries  
            deltas_data = {
                'PET': {
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
                },
            }             
            
            for key in deltas_data:
                water_data_updated = set_factors(water_data = water_data, parameter_name = key, factors = deltas_data[key])            
            
            # write out new text file
            write_txtfile(water_data_updated, save_path = dirname, output_filename = 'WATER_sampledeltas.txt')
                
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

def main_setdeltafile():  
    """
    Run as a script. Prompt user for WATER.txt file, process the file, 
    and print information. Information is printed to the screen. Prompt user for
    deltas file, process the file, and print information. Set/apply deltas values
    in WATER.txt file and create a new *.txt file called
    WATER_deltafile.txt file.
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    water_file = tkFileDialog.askopenfilename(title = 'Select a WATER.txt file ', filetypes = file_format)
    root.destroy()
    
    if water_file:
        
        try:
            
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(water_file))
            
            # make a directory called figs to hold the plots            
            figs_path = dirname + '/figs' + '/txt-figs/' + filename
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
            
            # process file
            print ''
            print '** Processing **'
            print water_file
            water_data = read_file(water_file)
            
            # print information
            print ''
            print '** USGS WATER text file Information **'
            print_info(water_data)
                                                                                                          
            # get deltas data and apply to pet timeseries  
            root = Tkinter.Tk() 
            file_format = [('Text file','*.txt')]  
            delta_files = tkFileDialog.askopenfilenames(title = 'Select Multiple Delta *.txt files', filetypes = file_format)
            delta_files = delta_files.split()
            root.destroy()
                
            delta_data_allfiles = []
            delta_values_allfiles = []
            tiles = ['11', '12', '22']
            for delta_file in delta_files:
                # get directory and filename from data file
                delta_dirname, delta_filename = os.path.split(os.path.abspath(delta_file))
                
                # process file
                print ''
                print '** Processing **'
                print delta_file
                delta_data = deltas.read_file(delta_file)         
                delta_data_allfiles.append(delta_data)
                
                # print 'Project' information
                print ''
                print '** Delta Data Information **'
                deltas.print_info(delta_data)
                
                # get delta values 
                delta_values = deltas.get_deltavalues(delta_data = delta_data, tile_list = tiles)
                delta_values_allfiles.append(delta_values)
            
            # set new data in xml file
            for delta_values in delta_values_allfiles:
                if delta_values.keys()[0] == 'PET':
                    water_data_updated = set_factors(water_data = water_data, parameter_name = 'PET', factors = delta_values['PET'])
                    
            # write out new text file
            write_txtfile(water_data_updated, save_path = dirname, output_filename = 'WATER_deltafile.txt')
                
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
    
    # main scripts
    main_singlefile()
    #main_setsampledeltas()
    #main_setdeltafile()
    #main_comparetxtfiles()
