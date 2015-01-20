# -*- coding: utf-8 -*-
"""
:Module: wateruse_processing.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles the WATER application file processing using settings from the user_settings.py file
"""

__version__   = "1.0.0"
__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os

import watertxt
import waterxml
import watertxt_viewer
import waterxml_viewer
import helpers
import waterapputils_logging

def process_water_files(file_list, settings, print_data = True):
    """    
    Process a list of WATER xml files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """ 
    print("Processing WATER files ...\n")

    for f in file_list:
        
        ext = os.path.splitext(f)[1]       
        assert ext == ".txt" or ext == ".xml", "Can not process file {}. File extension {} is not .txt or .xml".format(f, ext)
        
        filedir, filename = helpers.get_file_info(f)       
 
        if ext == ".txt":
            output_dir = helpers.make_directory(path = filedir, directory_name = settings["watertxt_directory_name"])
            helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": output_dir})
            waterapputils_logging.initialize_loggers(output_dir = output_dir) 

            data = watertxt.read_file(f)                   
            watertxt_viewer.plot_watertxt_data(data, save_path = output_dir)
            if print_data: 
                watertxt_viewer.print_watertxt_data(data) 
                
        elif ext == ".xml":
            output_dir = helpers.make_directory(path = filedir, directory_name = settings["waterxml_directory_name"])
            waterapputils_logging.initialize_loggers(output_dir = output_dir) 
            helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": output_dir})

            data = waterxml.read_file(f)                           
            waterxml_viewer.plot_waterxml_timeseries_data(data, save_path = output_dir)             
            waterxml_viewer.plot_waterxml_topographic_wetness_index_data(data, save_path = output_dir) 
            if print_data: 
                waterxml_viewer.print_waterxml_data(data)  

        waterapputils_logging.remove_loggers()

def process_cmp(file_list, settings, print_data = True):
    """
    Compare two WATER text files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.    
    """

    print("Comparing WATER files ...\n")

    water_file1 = file_list[0]
    water_file2 = file_list[1]

    filedir1, filename1 = helpers.get_file_info(water_file1)
    filedir2, filename2 = helpers.get_file_info(water_file2)

    ext1 = os.path.splitext(filename1)[1]
    ext2 = os.path.splitext(filename2)[1]

    assert ext1 == ".txt" or ext1 == ".xml", "Can not process file {}. File extension {} is not .txt or .xml".format(filename1, ext1)
    assert ext2 == ".txt" or ext2 == ".xml", "Can not process file {}. File extension {} is not .txt or .xml".format(filename2, ext2)

    if ext1 == ".txt" and ext2 == ".txt":
        output_dir = helpers.make_directory(path = filedir1, directory_name = settings["watertxt_directory_name"])
        helpers.print_input_output_info(input_dict = {"input_file_1": water_file1, "input_file_2": water_file2}, output_dict = {"output_directory": output_dir})
        waterapputils_logging.initialize_loggers(output_dir = output_dir) 

        watertxt_data1 = watertxt.read_file(water_file1)  
        watertxt_data2 = watertxt.read_file(water_file2)         
        watertxt_viewer.plot_watertxt_comparison(watertxt_data1, watertxt_data2, save_path = output_dir)         
        if print_data:
            watertxt_viewer.print_watertxt_data(watertxt_data1)  
            watertxt_viewer.print_watertxt_data(watertxt_data2)   

    elif ext1 == ".xml" and ext2 == ".xml":
        output_dir = helpers.make_directory(path = filedir1, directory_name = settings["waterxml_directory_name"])
        helpers.print_input_output_info(input_dict = {"input_file_1": water_file1, "input_file_2": water_file2}, output_dict = {"output_directory": output_dir})
        waterapputils_logging.initialize_loggers(output_dir = output_dir) 

        waterxml_data1 = waterxml.read_file(water_file1)  
        waterxml_data2 = waterxml.read_file(water_file2)         
        waterxml_viewer.plot_waterxml_timeseries_comparison(waterxml_data1, waterxml_data2, save_path = output_dir)         
        if print_data: 
            waterxml_viewer.print_waterxml_data(waterxml_data1)  
            waterxml_viewer.print_waterxml_data(waterxml_data2)   

    else:
        print("Can not process files {} and {}. File extensions {} and {} both need to be .txt or .xml".format(filename1, filename2, ext1, ext2))

    waterapputils_logging.remove_loggers()
