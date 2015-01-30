# -*- coding: utf-8 -*-
"""
:Module: wateruse_processing.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles specific output file processing for external OASIS and Ecoflow programs.
"""

__version__   = "1.0.0"
__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os
import sys
import osgeo.ogr
import logging

# my modules
import helpers
import watertxt
import waterxml
import spatialvectors
import wateruse
import waterapputils_logging
import water_files_processing


def write_oasis_file(file_list, dir_name, file_name):

    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        oasis_dir = helpers.make_directory(path = filedir, directory_name = dir_name)

        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": oasis_dir})

        waterapputils_logging.initialize_loggers(output_dir = oasis_dir) 

        watertxt_data = watertxt.read_file(f)      

        # write timeseries of discharge + water use for OASIS
        watertxt.write_timeseries_file(watertxt_data = watertxt_data, name = "Discharge + Water Use", save_path = oasis_dir, filename = "-".join([watertxt_data["stationid"], file_name]))
                
        waterapputils_logging.remove_loggers()

def write_ecoflow_file_stationid(file_list, dir_name, file_name, parameter_name = "Discharge + Water Use"):
    """    
    Write a csv file containing a timeseries for a particular parameter contained in a WATER.txt file

    Parameters
    ----------
    file_list : list
        List of WATER.txt files to process
    dir_name : string
        String name for output directory
    file_name : string
        String name for output file
    parameter_name : string
        String name for a parameter contained in a WATER.txt file
    """   

    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        ecoflow_dir = helpers.make_directory(path = filedir, directory_name = dir_name)

        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": ecoflow_dir})

        waterapputils_logging.initialize_loggers(output_dir = ecoflow_dir) 

        watertxt_data = watertxt.read_file(f)      

        # write timeseries of discharge + water use for ecoflow program
        watertxt.write_timeseries_file_stationid(watertxt_data, name = parameter_name, save_path = ecoflow_dir, filename = file_name, stationid = watertxt_data["stationid"])
                
        waterapputils_logging.remove_loggers()

def write_ecoflow_file_drainageareaxml(file_list, dir_name, file_name):
    """    
    Write a csv file containing a label (basin id number) and its corresponding area.

    Parameters
    ----------
    file_list : list
        List of WATERSimulation.xml files to process
    dir_name : string
        String name for output directory
    file_name : string
        String name for output file
    """   
    area_data = {}
    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        ecoflow_dir = helpers.make_directory(path = filedir, directory_name = dir_name)

        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": ecoflow_dir})

        waterapputils_logging.initialize_loggers(output_dir = ecoflow_dir) 

        # read xml file
        waterxml_tree = waterxml.read_file(f)       

        # get area from each region from the xml file and sum for a total area
        project, study, simulation = waterxml.get_xml_data(waterxml_tree = waterxml_tree)

        # get the project name which is the same as the stationid
        stationid = project["ProjName"]

        # get the area means for each region
        areas = waterxml.get_study_unit_areas(simulation_dict = simulation)

        # calculate total area
        total_area = waterxml.calc_total_study_unit_areas(areas)

        # fill area_data with total area
        area_data[stationid] = total_area

    # convert from km**2 to mi**2
    area_data = helpers.convert_area_values(area_data, in_units = "km2", out_units = "mi2")

    # write timeseries of dishcarge + water use for ecoflow program
    watertxt.write_drainagearea_file(area_data = area_data, save_path = ecoflow_dir, filename = file_name)
            
    waterapputils_logging.remove_loggers()


def write_ecoflow_file_drainageareashp(file_list, dir_name, file_name, label_field, query_field):
    """    
    Write a csv file containing a label (basin id number) and its corresponding area.
    Two methods to get the area from each respective shapefile:

        1. if shapefile(s) has an area field and user specifies it in user_settings.py 
        under the *basin_shapefile_area_field* variable then get the area for each
        basin using the specified area field name (query_field)
        
        2. if shapefile(s) do not have an area field or user does not specify is in
        user_settings.py, then calculate it using osgeo and label each basin according
        to *basin_shapefile_id_field* in user_settings.py 

    Parameters
    ----------
    file_list : list
        List of files to process; files are shapefiles
    settings : dictionary
        Dictionary of user settings
    label_field : string
        String name of an id field (basin id number) to associate with a basin
    query_field : string
        String name of an area field

    Notes
    -----
    Uses settings set in user_settings.py  
    """   
    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        ecoflow_dir = helpers.make_directory(path = filedir, directory_name = dir_name)

        waterapputils_logging.initialize_loggers(output_dir = ecoflow_dir) 
 
        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": ecoflow_dir})

        basin_shapefile = osgeo.ogr.Open(f)  

        # get the areas for each region
        areas = spatialvectors.get_areas_dict(shapefile = basin_shapefile, id_field = label_field, query_field = query_field)

        # write timeseries of dishcarge + water use for ecoflow program
        watertxt.write_drainagearea_file(area_data = areas, save_path = ecoflow_dir, filename = file_name)
            
    waterapputils_logging.remove_loggers()
 

 