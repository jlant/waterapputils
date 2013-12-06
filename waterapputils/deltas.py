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


def read_deltafile(filename):
    """    
    Open delta.txt file, create a file object for read_deltafile_in(filestream) to process.
    This function is responsible to opening the file, removing the file opening  
    responsibility from read_deltafile_in(filestream) so that read_deltafile_in(filestream)  
    can be unit tested.
    
    *Parameters:*
		filename : string path to water text file
    
    *Return:*
        data : dictionary holding data found in delta text file  
        
    """
    
    filestream = open(filename, 'r')
    data = read_deltafile_in(filestream)
    filestream.close()
    
    return data

def read_deltafile_in(filestream):
    
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file 
    patterns = {
        'column_names': '([a-zA-Z].+)',
        'data_row': '([0-9].+)'
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
            data['column_names'] = match_column_names.group(0).split(',') 
            
            for name in data['column_names']:
                data['parameters'].append({
                    'name': name,
                    'index': data['column_names'].index(name),
                    'data': []
                })
                
        if match_data_row:
             for parameter in data['parameters']:
                value = match_data_row.group(0).split(',')[parameter['index']]
                
                if not helpers.is_float(value):
                    error_str = '**ERROR on ' + parameter['name'] +' Value can not be converted to a float: ' + value + '**Exiting. Bad data in file!'
                    raise ValueError(error_str)
                    sys.exit('**Exiting. Bad data in file!')
                        
                parameter['data'].append(float(value)) 
                
    
    return data

def write_deltafile(study_simulation, output_path, filename, delta_headers):
    """   
    Write a comma separated text file for a user to edit.
    
    *Parameters*:
        study_simulation: dictionary holding data from WATERSimulation.xml file
        output_path: string path for output text file
        delta_headers: list of strings for the avaiable deltas
        
    *Return*:
        no return
        
    """  
    output_file = open(output_path + filename, 'w')
    
    header = ['RegionType', 'SimulID'] + delta_headers
    txt = []
    txt.append(header)
    for i in range(len(study_simulation['SimulID'])):
        region_type_str = str(study_simulation['RegionType'][i])
        sim_id_num_str = str(study_simulation['SimulID'][i])
        txt.append([region_type_str, sim_id_num_str, 'fillme', 'fillme'])
    
    for str_line in txt:
        output_file.writelines(','.join(str_line) + '\n')
    
    output_file.close()