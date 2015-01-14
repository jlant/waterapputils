# -*- coding: utf-8 -*-
"""
:Module: wateruse_processing.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles the global climate model delta factors processing using settings from the user_settings.py file
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
import waterxml
import spatialvectors
import deltas
import deltas_viewer
import waterapputils_logging
import water_files_processing
import map_processing

def create_output_dirs_files(settings, is_sub_gcm_delta = False):
    """    
    Create the output directories and files needed to processes wateruse.

    Parameters
    ----------
    settings : dictionary
        Dictionary of user settings

    Returns
    -------
    info_dir : string
        string path to info directory
    gcm_delta_dir : string 
        string path to ecoflow directory
    info_file : string
        string path to info file

    Notes
    -----
    Uses settings set in user_settings.py 
    """   
    # create output directories   
    info_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["info_directory_name"])    
    gcm_delta_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["gcm_delta_directory_name"])
    
    # path to info file
    if is_sub_gcm_delta:
        info_file = os.path.join(info_dir, settings["sub_gcm_delta_info_file_name"])
    else:
        info_file = os.path.join(info_dir, settings["gcm_delta_info_file_name"])

    # print input and output information
    helpers.print_input_output_info( 
        input_dict = {"simulation_directory": settings["simulation_directory"],
                      "gcm_delta_prepend_name": settings["gcm_delta_prepend_name"],
                      "gcm_delta_directory_name": settings["gcm_delta_directory_name"],
                      "gcm_delta_info_file_name": settings["gcm_delta_info_file_name"],
                      "gcm_delta_non_intersecting_file_name": settings["gcm_delta_non_intersecting_file_name"],
                      "sub_gcm_delta_info_file_name": settings["sub_gcm_delta_info_file_name"],
        },
        output_dict = {"info_dir": info_dir, "info_file": info_file, "gcm_delta_dir": gcm_delta_dir}
    )

    return info_dir, gcm_delta_dir, info_file

def process_intersecting_tiles(intersecting_tiles, settings, gcm_delta_dir):
    """    
    Apply water use data to a WATER \*.txt file. The new file created is saved to the same
    directory as the \*.xml file.

    Parameters
    ----------
    intersecting_tiles : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.  
    settings : dictionary
        Dictionary of user settings
    gcm_delta_dir : string 
        string path to ecoflow directory

    Notes
    -----
    Uses settings set in user_settings.py 
    """      
    # create a file for the output  
    for featureid, tiles in intersecting_tiles.iteritems():

        # get monthly average gcm delta values
        deltas_data_list, deltas_avg_dict = deltas.get_deltas(delta_files = settings["gcm_delta_files"], tiles = tiles) 

        # print monthly output in nice format to info file
        print("FeatureId: {}\n    Tiles: {}\n    Average GCM Deltas:\n".format(featureid, tiles))  
        for key in deltas_avg_dict.keys():
            print("    {}\n".format(key))
            helpers.print_monthly_dict(monthly_dict = deltas_avg_dict[key])
       
        # get the txt data file that has a parent directory matching the current featureid
        if settings["is_batch_simulation"]:
            path = os.path.join(settings["simulation_directory"], featureid)
        else:
            path = settings["simulation_directory"]

        # find the WATERSimulation.xml file 
        waterxml_file = helpers.find_file(name = settings["water_database_file_name"], path = path)

        # get file info
        waterxml_dir, waterxml_filename = helpers.get_file_info(waterxml_file)       

        # create an output directory
        output_dir = helpers.make_directory(path = waterxml_dir, directory_name = settings["gcm_delta_directory_name"])
        
        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = output_dir)

        # read the xml file
        waterxml_tree = waterxml.read_file(waterxml_file)            

        # apply gcm delta
        for key, value in deltas_avg_dict.iteritems():
            if key == "Ppt":
                waterxml.apply_factors(waterxml_tree = waterxml_tree, element = "ClimaticPrecipitationSeries", factors = deltas_avg_dict[key])

            elif key == "Tmax":
                waterxml.apply_factors(waterxml_tree = waterxml_tree, element = "ClimaticTemperatureSeries", factors = deltas_avg_dict[key])

        # update the project name in the updated xml
        project = waterxml.create_project_dict() 
        project = waterxml.fill_dict(waterxml_tree = waterxml_tree, data_dict = project, element = "Project", keys = project.keys())
        waterxml.change_element_value(waterxml_tree = waterxml_tree, element = "Project", child = "ProjName" , new_value = "-".join([settings["gcm_delta_prepend_name"], project["ProjName"]]))

        # write updated xml
        waterxml_with_gcm_delta_file = "-".join([settings["gcm_delta_prepend_name"], waterxml_filename])   

        waterxml.write_file(waterxml_tree = waterxml_tree, save_path = output_dir, filename = waterxml_with_gcm_delta_file)              

        # plot 
        updated_waterxml_file = os.path.join(output_dir, waterxml_with_gcm_delta_file)
        water_files_processing.process_water_files(file_list = [updated_waterxml_file ], settings = settings, print_data = False)
        water_files_processing.process_cmp(file_list = [updated_waterxml_file, waterxml_file], settings = settings, print_data = False)

    # plot the gcm deltas 
    for deltas_data in deltas_data_list:
        deltas_viewer.plot_deltas_data(deltas_data = deltas_data, save_path = helpers.make_directory(path = gcm_delta_dir, directory_name = settings["gcm_delta_directory_name"]))



def apply_gcm_deltas(settings):
    """    
    Apply global climate model delta factor data to a WATERSimulation \*.xml file(s). 

    Parameters
    ----------
    settings : dictionary
        Dictionary of user settings                 

    Notes
    -----
    Uses settings set in user_settings.py  
    """   

	# create output directories and files   
    info_dir, gcm_delta_dir, info_file = create_output_dirs_files(settings)

    # initialize error logging in info_dir
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    # write all future print strings to the info_file
    sys.stdout = open(info_file, "w")  
    
    # open shapefiles
    gcm_delta_tile_shapefile = osgeo.ogr.Open(settings["gcm_delta_tile_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"])) 

    # find intersecting points (centroids) based on water basin supplied
    intersecting_tiles_all = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gcm_delta_tile_shapefile, intersectee_field = settings["gcm_delta_tile_shapefile_id_field"], intersector_field = settings["basin_shapefile_id_field"])

    intersecting_tiles, nonintersecting_tiles = spatialvectors.validate_field_values(field_values_dict = intersecting_tiles_all)     

    # apply gcm deltas
    if intersecting_tiles:    
        process_intersecting_tiles(intersecting_tiles, settings, gcm_delta_dir)

    # if no intersecting centroids, then warn the user and ask user to supply the water use points to a text file that will be contained in the info directory with a name specified in the user_settings.py file
    if nonintersecting_tiles:
        
        spatialvectors.write_field_values_file(filepath = info_dir, filename = settings["gcm_delta_non_intersecting_file_name"], field_values_dict = nonintersecting_tiles, field_id = "Tile")

        warn_str = "The following basin(s) do not intersect with the gcm delta tile shapefile:\n    {}\n\n    gcm delta tile shapefile: {}\n    basin shapefile: {}\n".format(nonintersecting_centroids, 
                                                                                                                                                                              settings["gcm_delta_tile_shapefile"] , 
                                                                                                                                                                              os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"]))
        instruction_str1 = "Using gcm delta tile: 000. This special tile id specifies a delta factor of 0 for Tmax type (additive) and a delta factor of 1 for Ppt type (multiplicative).\n"
        instruction_str2 = "Writing the following gcm delta non intersecting file that specifies the non intersecting basin(s) with the gcm delta tiles:\n    {}\n".format(os.path.join(info_dir, settings["gcm_delta_non_intersecting_file_name"]))
        instruction_str3 = "To apply gcm delta factor(s) to the non intersecting basin(s), add tile ids (separated by commas) that you would like to use for each non intersecting basin to the gcm delta non intersecting non intersecting file."
        logging.warn("\n{}\n{}\n{}\n{}\n".format(warn_str, instruction_str1, instruction_str2, instruction_str3)) 

        # apply a delta factor of 0 for Tmax type (additive) and a delta factor of 1 for Ppt type (multiplicative)
        sub_intersecting_tiles = spatialvectors.read_field_values_file(filepath = os.path.join(info_dir, settings["gcm_delta_non_intersecting_file_name"]))

        # apply gcm deltas    
        process_intersecting_tiles(sub_intersecting_tiles, settings, gcm_delta_dir)        

    # create map of study area
    map_processing.create_simulation_map(settings = settings)

    # remove error logger
    waterapputils_logging.remove_loggers()


def apply_sub_gcm_deltas(settings):
    """    
    Apply substitute gcm delta data to a WATERSimulation \*.xml file(s).  
    User supplies the gcm tiles to a text file that will be 
    contained in the info directory with a name specified in the user_settings.py file 

    Parameters
    ----------
    settings : dictionary
        Dictionary of user settings                 

    Notes
    -----
    Uses settings set in user_settings.py  
    """   

    # create output directories and files   
    info_dir, gcm_delta_dir, info_file = create_output_dirs_files(settings, is_sub_gcm_delta = True)

    # initialize error logging in info_dir
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    # write all future print strings to the info_file
    sys.stdout = open(info_file, "w")  

    # get the intersecting points (centroids) based on wateruse non-intersecting_file
    intersecting_tiles = spatialvectors.read_field_values_file(filepath = os.path.join(info_dir, settings["gcm_delta_non_intersecting_file_name"]))

    # apply the wateruse     
    process_intersecting_centroids(intersecting_centroids, settings, gcm_delta_dir)

    waterapputils_logging.remove_loggers()


