# -*- coding: utf-8 -*-
"""
:Module: waterxml.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Read, parse, plot, and print information about the WATERSimulation.xml output 
file created by the WATER application developed by Williamson, T., Ulery, R.
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

# my module
import helpers
import deltas

# xml.etree.cElementTree is parses xml files faster than xml.etree.ElementTree
try:    
    import xml.etree.cElementTree as ET
except ImportError:    
    import xml.etree.ElementTree as ET


def fill_info(tree, data_dict, element_str, key_list):
    """
    Fills a dictionary with information of interest contained in a 
    particular xml element.
    
    *Parameters:*
        tree : ElementTree object of entire xml file
        data_dict : dictionary containing keys that match particular children in an element
        element_str : string of a particular element of interest
        key_list: list of keys to get information for
    
    *Return:*
        data_dict : dictionary containing data found in the element of interest  
    """
    for elem in tree.iter(tag = element_str):
        for child in elem:
            for key in data_dict:
                if child.tag == key and key in key_list:
                    if type(data_dict[key]) is list:
                        data_dict[key].append(child.text)
                    else:
                        data_dict[key] = child.text

    return data_dict


def fill_study_simulation(tree, study_simulation, key_list):
    """
    Fills study simulation dictionary with climate, feature, and twi data.   
    
    *Parameters:*
        tree : ElementTree object of entire xml file
        study_simulation : dictionary containing information about the study simulations
        key_list: list of keys to fill
    
    *Return:*
        study_simulation : updated dictionary containing climate, feature, and twi data
    """
    
    # get data of interest for all simulations and add to study_simulation dictionary
    for string in key_list:
        for i in range(len(study_simulation['SimulID'])):                
            data = get_data(tree = tree, element_str = string, sim_id_num = study_simulation['SimulID'][i])
            study_simulation[string].append(data)
    
    return study_simulation
    
def get_data(tree, element_str, sim_id_num):
    """
    Get all data parameters for an xml element for a particular simulation 
    id number, and return a list of dictionaries each containing the data 
    parameters found for the xml element.
    Done this way due to the struture of the WATERSimulation.xml file; repeated
    xml elements for different simulation id numbers.
    
    *Parameters:*
        tree : ElementTree object of entire xml file
        element_str : string of a particular element of interest
        sim_id_num : integer of the simulation id of interest
    
    *Return:*
        data : list of dictionaries each containing data found in the element of interest  
    """        
    data = []
    for elem in tree.iter(tag = element_str):
        simid = int(elem.find('SimulID').text)
        if simid == int(sim_id_num):
            data_dict = {}            
            for child in elem:
                data_dict[child.tag] = child.text
        
            data.append(data_dict)    
            
    return data

def get_climate_data(climate_parameter):
    """   
    Get dates, values, and units from a climate parameter contained in the 
    study simulation dictionary. Valid climate parameters include:
    'StudyUnitDischargeSeries', 'ClimaticPrecipitationSeries',
    and 'ClimaticTemperatureSeries.'
    
    Each climate parameter has the following xml elements:
        'SeriesID'
        'SimulID'
        'SeriesDate'
        'SeriesValue'
        'SeriesUnitCode'
        'SeriesUnit'
    
    *Parameters*:
        climate_parameter : list of dictionaries containing climate data 
        
    *Return*:
        dates : numpy array of dates
        values : numpy array of floats
        units : string of unit for a particular climate parameter
        
    """
    dates = []
    values = []
    units = []
    for i in range(len(climate_parameter)):
        datestr = climate_parameter[i]['SeriesDate'].split('T')[0]
        year = datestr.split('-')[0]
        month = datestr.split('-')[1]
        day = datestr.split('-')[2]
        date = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
        
        value = climate_parameter[i]['SeriesValue']
        unit = climate_parameter[i]['SeriesUnit']
        
        dates.append(date)
        values.append(value)            
        units.append(unit)
    
    dates = np.array(dates)    
    values = np.array(values, dtype = float)
    units = units[0]
    
    return dates, values, units

def get_general_info(tree):
    """
    Get information of interest contained in the 'Project', 'Study', and 
    'StudySimulation' xml elements. Return three dictionaries containing 
    information of interest:
    
        project = {
            'ProjID': None,
            'UserName': None,
            'DateCreated': None,
            'ProjName': None
        }
        
        study = {
            'StudyID': None,
            'StudyLocDecDeg': None,
            'StudyDescription': None
        }
        
        study_simulation = {
            'SimulID': [],
            'StudyID': [],
            'RegionType': [],
        }    
    
    *Parameters:*
        tree : ElementTree object of entire xml file 
    
    *Return:*
        project : dictionary containing information found in the 'Project' element
        study : dictionary containing information found in the 'Study' element
        study_simulation : dictionary containing information found in the 'StudySimulation' element
    """
    
    project = {
        'ProjID': None,
        'UserName': None,
        'DateCreated': None,
        'ProjName': None
    }
    
    study = {
        'StudyID': None,
        'StudyLocDecDeg': None,
        'StudyDescription': None
    }
    
    study_simulation = {
        'SimulID': [],
        'StudyID': [],
        'RegionType': [],
        'SimulationFeatures': [],
        'SimulationTopographicWetnessIndex': [],
        'StudyUnitDischargeSeries': [],
        'ClimaticPrecipitationSeries': [],
        'ClimaticTemperatureSeries': []
    }
  
    # get information for elements of interest and fill respective dictionaries
    project = fill_info(tree = tree, data_dict = project, element_str = 'Project', key_list = project.keys())
    study = fill_info(tree = tree, data_dict = study, element_str = 'Study', key_list = study.keys())
    study_simulation = fill_info(tree = tree, data_dict = study_simulation, element_str = 'StudySimulation', key_list = ['SimulID',
                                                                                                                         'StudyID',
                                                                                                                         'RegionType'])
                                                                                                                         
    return project, study, study_simulation

def plot_climate_parameter(parameter_name, climate_parameter, region_type, sim_id_num, is_visible = True, save_path = None):
    """   
    Plot a climate parameter contained in the study simulation dictionary. Valid
    climate parameters include 'StudyUnitDischargeSeries', 'ClimaticPrecipitationSeries',
    and 'ClimaticTemperatureSeries.' Save plots to a particular path.
    
    *Parameters*:
        parameter_name : string of climate parameter
        climate_parameter: list of dictionaries containing climate data
        region_type : string of region type; i.e. 4, 6, or 1
        sim_id_num : string of sim id numbers; i.e. 1, 2, or 3
        is_visible : boolean to show plots
        save_path: string path to save plot(s) 

    *Return*:
        no return
        
    """

    dates, values, units = get_climate_data(climate_parameter)

    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title('Region Type: ' + region_type + ' Sim ID: ' + sim_id_num + ' Parameter: ' + parameter_name)
    ax.set_xlabel('Date')
    ax.set_ylabel(parameter_name + ' (' + units + ')')
    plt.plot(dates, values, color = 'b', label = parameter_name)

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
    text = 'mean = %.2f\nmax = %.2f\nmin = %.2f' % (np.mean(values), np.max(values), np.min(values))
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
        plt.savefig(save_path + '/' + 'regiontype_' + region_type + '_' + 'simid_' + sim_id_num + '_' + parameter_name +'.png', dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()

def plot_climate_parameter_comparison(parameter_name, climate_parameter_a, climate_parameter_b, region_type, sim_id_num, is_visible = True, save_path = None, xml_filenames = None):
    """   
    Plot a comparison of climate parameters contained in two the study simulation 
    dictionaries.  Valid climate parameters include 'ClimaticPrecipitationSeries'
    and 'ClimaticTemperatureSeries.' Save plots to a particular path.
    
    *Parameters*:
        parameter_name : string of climate parameter
        climate_parameter_a: list of dictionaries containing climate data
        climate_parameter_b: list of dictionaries containing climate data
        region_type : string of region type; i.e. 4, 6, or 1
        sim_id_num : string of sim id numbers; i.e. 1, 2, or 3
        is_visible : boolean to show plots
        save_path : string path to save plot(s) 
        xml_filenames : list of two xml filenames

    *Return*:
        no return
        
    """

    dates_a, values_a, units_a = get_climate_data(climate_parameter_a)
    dates_b, values_b, units_b = get_climate_data(climate_parameter_b)

    fig = plt.figure(figsize = (12,10))
    
    # plot original vs. updated
    ax1 = fig.add_subplot(211)
    ax1.grid(True)
    ax1.set_title('Region Type: ' + region_type + ' Sim ID: ' + sim_id_num + ' Parameter: ' + parameter_name)
    ax1.set_xlabel('Date')
    ax1.set_ylabel(parameter_name + ' (' + units_a + ')')
    ax1.plot(dates_a, values_a, color = 'b', label = xml_filenames[0], linewidth = 2)
    ax1.hold(True)
    ax1.plot(dates_b, values_b, color = 'r', label = xml_filenames[1], linewidth = 2, alpha = 0.6)
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
    text = 'mean = %.2f\nmax = %.2f\nmin = %.2f\n---\nmean = %.2f\nmax = %.2f\nmin = %.2f' % (np.mean(values_a), np.max(values_a), np.min(values_a),
                                                                                                                                np.mean(values_b), np.max(values_b), np.min(values_b))
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
        plt.savefig(save_path + '/' + 'comparison_' + 'regiontype_' + region_type + '_' + 'simid_' + sim_id_num + '_' + parameter_name +'.png', dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()

def print_info(data_dict, key_list):
    """   
    Print information contained in particular keys in a data dictionary
    
    *Parameters*:
        data_dict: dictionary holding data from WATERSimulation.xml file
        key_list: list of keys to print key value pairs
        
    *Return*:
        no return
        
    """   

    # print information
    for key, value in data_dict.iteritems():
        if key in key_list:
            print key, value

def set_data(tree, element_str, element_tag_str, sim_id_num, factor):
    """
    Set new data for a particular element tag in a particular xml element for
    a particular simulation id number using a additive or multiplicative factor.  
    The factor is applied to the particular element tag and is additive if 
    the element string (element_str) is ClimaticTemperatureSeries otherwise
    the factor is multiplicative.
    
    *Parameters:*
        tree : ElementTree object of entire xml file
        element_str : string of a particular element of interest
        element_tag_str : string of a particular element tag of interest
        sim_id_num : integer of the simulation id of interest
        factor : float factor
    
    *Return:*
        No return
    """        
    for elem in tree.iter(tag = element_str):
        simid = int(elem.find('SimulID').text)
        if simid == int(sim_id_num):
            for child in elem:
                if child.tag == element_tag_str:
                    if element_str == 'ClimaticTemperatureSeries':
                        new_num = float(child.text) + factor    # additive
                    else:
                        new_num = float(child.text) * factor    # multiplicative
                        child.text = str(new_num)

def set_factors(tree, element_str, factors):
    """
    Set new data for a particular xml element for using a timeseries of factor  
    values. The factors are applied to the particular element tag.  
    If the element string (element_str) is 'ClimaticTemperatureSeries'
     otherwise the factor is multiplicative.
    
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
   
    for elem in tree.iter(tag = element_str):
        # get element date and match the appropriate factor fraom factors
        elem_date = elem.find('SeriesDate')
        datestr = elem_date.text.split('T')[0]
        year = datestr.split('-')[0]
        month = datestr.split('-')[1]
        day = datestr.split('-')[2]
        date = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
        # get the month name to match the delta_factor dictionary keys
        month_name = date.strftime('%B')
        factor = factors[month_name]
        
        # get element value
        elem_value = elem.find('SeriesValue')
        
        if element_str == 'ClimaticTemperatureSeries':
            new_value = float(elem_value.text) + factor
        else:
            new_value = float(elem_value.text) * factor
        
        # set new value
        elem_value.text = str(new_value)          

def main_singlefile():  
    """
    Run as a script. Prompt user for WATERSimulation.xml file, process the file, 
    print information, and plot data. Information is printed to the screen.  
    Plots are saved to a directory called 'figs/xml-figs/' which is created in the  
    same directory as the data file. 
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('XML file','*.xml')]  
    water_file = tkFileDialog.askopenfilename(title = 'Select WATER.xml file to process', filetypes = file_format)
    root.destroy()
    
    if water_file:
        
        try:
            
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(water_file))
            
            # make a directory to hold the plots            
            figs_path = dirname + '/figs' + '/xml-figs/' + filename 
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
                       
            # process file
            print ''
            print '** Processing **'
            print water_file
            water_tree = ET.parse(water_file)

            project, study, study_simulation = get_general_info(water_tree)            
            
            # print 'Project' information
            print ''
            print '** WATER Project Information **'
            print_info(data_dict = project, key_list = project.keys())
            
            # print 'Study' information
            print ''
            print '** WATER Study Information **'
            print_info(data_dict = study, key_list = study.keys())
            
            # print 'StudySimulation' information
            print ''
            print '** WATER StudySimulation Information **'
            print_info(data_dict = study_simulation, key_list = ['SimulID', 'StudyID', 'RegionType'])

            # fill climate, feature, and twi information into study simulation dictionary
            study_simulation = fill_study_simulation(tree = water_tree, study_simulation = study_simulation, key_list = ['SimulationFeatures',
                                                                                                                         'SimulationTopographicWetnessIndex',
                                                                                                                         'StudyUnitDischargeSeries',
                                                                                                                         'ClimaticPrecipitationSeries',
                                                                                                                         'ClimaticTemperatureSeries'])
                                                                                                                         
            print ''                                                                                                             
            print '** Plotting **'
            # plot climate data contained in study simulation dictionary
            climate_parameters = ['StudyUnitDischargeSeries', 'ClimaticPrecipitationSeries', 'ClimaticTemperatureSeries']     
            for parameter in climate_parameters:
                for i in range(len(study_simulation['SimulID'])):
                    plot_climate_parameter(parameter_name = parameter,
                                           climate_parameter = study_simulation[parameter][i], 
                                           region_type = study_simulation['RegionType'][i], 
                                           sim_id_num = study_simulation['SimulID'][i], 
                                           is_visible = False, 
                                           save_path = figs_path)                
                 
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

    
def main_comparexmlfiles():  
    """
    Run as a script. Prompt user for 2 WATERSimulation.xml files to compare.
    Process the file, print information, and plot data. Information is printed
    to the screen.  Plots are saved to a directory called 'figs/xml-figs/'
    which is created in the same directory as the *.xml data file. 
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('XML file','*.xml')]  
    water_files = tkFileDialog.askopenfilenames(title = 'Select 2 WATER.xml files to compare', filetypes = file_format)
    water_files = water_files.split()
    root.destroy()
    
    study_simulations = []
    for water_file in water_files:
        if water_file:
            
            try:
                
                # get directory and filename from data file
                dirname, filename = os.path.split(os.path.abspath(water_file))
                
                # process file
                print ''
                print '** Processing **'
                print water_file
                water_tree = ET.parse(water_file)
    
                project, study, study_simulation = get_general_info(water_tree)            
                
                # print 'Project' information
                print ''
                print '** WATER Project Information **'
                print_info(data_dict = project, key_list = project.keys())
                
                # print 'Study' information
                print ''
                print '** WATER Study Information **'
                print_info(data_dict = study, key_list = study.keys())
                
                # print 'StudySimulation' information
                print ''
                print '** WATER StudySimulation Information **'
                print_info(data_dict = study_simulation, key_list = ['SimulID', 'StudyID', 'RegionType'])
    
                # fill climate, feature, and twi information into study simulation dictionary
                study_simulation = fill_study_simulation(tree = water_tree, study_simulation = study_simulation, key_list = ['SimulationFeatures',
                                                                                                                             'SimulationTopographicWetnessIndex',
                                                                                                                             'StudyUnitDischargeSeries',
                                                                                                                             'ClimaticPrecipitationSeries',
                                                                                                                             'ClimaticTemperatureSeries'])
                                                                                                                                 
                study_simulations.append(study_simulation)                                                                                                              
                      
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
            
    figs_path = dirname + '/figs' + '/xml-figs/' + filenames[0] + '_vs_' + filenames[1]
    if not os.path.exists(figs_path):
        os.makedirs(figs_path)  
        
    # plot data                
    print ''                                                                                                             
    print '** Plotting **'
    # plot climate data contained in study simulation dictionary
    climate_parameters = ['ClimaticPrecipitationSeries', 'ClimaticTemperatureSeries'] 
    for parameter in climate_parameters:
        for i in range(len(study_simulations[0]['SimulID'])):
            plot_climate_parameter_comparison(parameter_name = parameter,
                                              climate_parameter_a = study_simulations[0][parameter][i], 
                                              climate_parameter_b = study_simulations[1][parameter][i],
                                              region_type = study_simulations[0]['RegionType'][i], 
                                              sim_id_num = study_simulations[0]['SimulID'][i], 
                                              is_visible = True, 
                                              save_path = figs_path,
                                              xml_filenames = filenames)                


def main_setsampledeltas():  
    """
    Run as a script. Prompt user for WATERSimulation.xml file, process the file, 
    and print information. Information is printed to the screen. Set/appply sample deltas
    in WATERSimulation.xml file and create a new WATERSimulation.xml file called
    WATERSimulation_sampledeltas.xml file
    
    Sample deltas used:
            deltas_data = {
                'ClimaticPrecipitationSeries': {
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
                'ClimaticTemperatureSeries': {
                    'January': 20.0,
                    'February': 10.0,
                    'March': 5.0,
                    'April': 6.0,
                    'May': 3.0,
                    'June': 10.0,
                    'July': 11.0,
                    'August': 12.0,
                    'September': 7.0,
                    'October': 8.0,
                    'November': 9.0,
                    'December': 20.0
                },
            }     
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('XML file','*.xml')]  
    water_file = tkFileDialog.askopenfilename(title = 'Select WATER.xml file to process and set sample deltas', filetypes = file_format)
    root.destroy()
    
    if water_file:
        
        try:
            
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(water_file))
                       
            # process file
            print ''
            print '** Processing **'
            print water_file
            water_tree = ET.parse(water_file)

            project, study, study_simulation = get_general_info(water_tree)            
            
            # print 'Project' information
            print ''
            print '** WATER Project Information **'
            print_info(data_dict = project, key_list = project.keys())
            
            # print 'Study' information
            print ''
            print '** WATER Study Information **'
            print_info(data_dict = study, key_list = study.keys())
            
            # print 'StudySimulation' information
            print ''
            print '** WATER StudySimulation Information **'
            print_info(data_dict = study_simulation, key_list = ['SimulID', 'StudyID', 'RegionType'])

            # fill climate, feature, and twi information into study simulation dictionary
            study_simulation = fill_study_simulation(tree = water_tree, study_simulation = study_simulation, key_list = ['SimulationFeatures',
                                                                                                                         'SimulationTopographicWetnessIndex',
                                                                                                                         'StudyUnitDischargeSeries',
                                                                                                                         'ClimaticPrecipitationSeries',
                                                                                                                         'ClimaticTemperatureSeries'])
                                                                                                                                                   
            # sample deltas data and apply to precipiation and temperature timeseries  
            deltas_data = {
                'ClimaticPrecipitationSeries': {
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
                'ClimaticTemperatureSeries': {
                    'January': 20.0,
                    'February': 10.0,
                    'March': 5.0,
                    'April': 6.0,
                    'May': 3.0,
                    'June': 10.0,
                    'July': 11.0,
                    'August': 12.0,
                    'September': 7.0,
                    'October': 8.0,
                    'November': 9.0,
                    'December': 20.0
                },
            }               
            
            for key in deltas_data:
                set_factors(tree = water_tree, element_str = key, factors = deltas_data[key])            
            
            # write out new xml file
            output_xmlfile = dirname + '/WATERSimulation' + '_sampledeltas.xml'
            water_tree.write(output_xmlfile) 
                
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
    Run as a script. Prompt user for WATERSimulation.xml file, process the file, 
    and print information. Information is printed to the screen. Prompt user for
    deltas file, process the file, and print information. Set/apply deltas values
    in WATERSimulation.xml file and create a new WATERSimulation.xml file called
    WATERSimulation_deltafile.xml file.
    
    """ 

    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('XML file','*.xml')]  
    water_file = tkFileDialog.askopenfilename(title = 'Select  WATER.xml ', filetypes = file_format)
    root.destroy()
    
    if water_file:
        
        try:
            
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(water_file))
                       
            # process file
            print ''
            print '** Processing **'
            print water_file
            water_tree = ET.parse(water_file)

            project, study, study_simulation = get_general_info(water_tree)            
            
            # print 'Project' information
            print ''
            print '** WATER Project Information **'
            print_info(data_dict = project, key_list = project.keys())
            
            # print 'Study' information
            print ''
            print '** WATER Study Information **'
            print_info(data_dict = study, key_list = study.keys())
            
            # print 'StudySimulation' information
            print ''
            print '** WATER StudySimulation Information **'
            print_info(data_dict = study_simulation, key_list = ['SimulID', 'StudyID', 'RegionType'])

            # fill climate, feature, and twi information into study simulation dictionary
            study_simulation = fill_study_simulation(tree = water_tree, study_simulation = study_simulation, key_list = ['SimulationFeatures',
                                                                                                                         'SimulationTopographicWetnessIndex',
                                                                                                                         'StudyUnitDischargeSeries',
                                                                                                                         'ClimaticPrecipitationSeries',
                                                                                                                         'ClimaticTemperatureSeries'])
                                                                                                                         
            # get deltas data and apply to precipiation and temperature timeseries  
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
                if delta_values.keys()[0] == 'Tmax':
                    set_factors(tree = water_tree, element_str = 'ClimaticTemperatureSeries', factors = delta_values['Tmax'])
                    
                if delta_values.keys()[0] == 'Ppt':
                    set_factors(tree = water_tree, element_str = 'ClimaticPrecipitationSeries', factors = delta_values['Ppt'])
                             
            # write out new xml file
            output_xmlfile = dirname + '/WATERSimulation' + '_deltafile.xml'
            water_tree.write(output_xmlfile) 
                
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
    #main_singlefile()
    #main_setsampledeltas()
    #main_setdeltafile()
    main_comparexmlfiles()
    



