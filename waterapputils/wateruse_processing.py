import os
import sys
import osgeo.ogr
import logging

# my modules
import helpers
import watertxt
import spatialvectors
import wateruse
import waterapputils_logging
import water_files_processing

def create_output_dirs_files(settings, is_sub_wateruse = False):
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
    ecoflow_dir : string 
        string path to ecoflow directory
    oasis_dir : string
        string path to oasis directory
    info_file : string
        string path to info file

    Notes
    -----
    Uses settings set in user_settings.py 
    """   
    # create output directories   
    info_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["info_directory_name"])    
    ecoflow_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["ecoflow_directory_name"])
    oasis_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["oasis_directory_name"])
    
    # path to info file
    if is_sub_wateruse:
        info_file = os.path.join(info_dir, settings["sub_wateruse_info_file_name"])
    else:
        info_file = os.path.join(info_dir, settings["wateruse_info_file_name"])

    # print input and output information
    helpers.print_input_output_info( 
        input_dict = {"simulation_directory": settings["simulation_directory"],
                      "wateruse_prepend_name": settings["wateruse_prepend_name"],
                      "wateruse_directory_name": settings["wateruse_directory_name"],
                      "wateruse_info_file_name": settings["wateruse_info_file_name"],
                      "wateruse_non_intersecting_file_name": settings["wateruse_non_intersecting_file_name"],
                      "sub_wateruse_info_file_name": settings["sub_wateruse_info_file_name"],
        },
        output_dict = {"info_dir": info_dir, "info_file": info_file, "ecoflow_dir": ecoflow_dir, "oasis_dir": oasis_dir}
    )

    return info_dir, ecoflow_dir, oasis_dir, info_file

def process_intersecting_centroids(intersecting_centroids, settings, ecoflow_dir, oasis_dir):
    """    
    Apply water use data to a WATER \*.txt file. The new file created is saved to the same
    directory as the \*.xml file.

    Parameters
    ----------
    intersecting_centroids : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.  
    settings : dictionary
        Dictionary of user settings
    ecoflow_dir : string
        String path to directory that will contain output specific for ecoflow program
    oasis_dir : string
        String path to directory that will contain output specific for oasis

    Notes
    -----
    Uses settings set in user_settings.py 
    """      
    # create a file for the output  
    for featureid, centroids in intersecting_centroids.iteritems():

        # get sum of the water use data
        if settings["wateruse_factor_file"]:
            total_wateruse_dict = wateruse.get_all_total_wateruse(wateruse_files = settings["wateruse_files"], id_list = centroids, wateruse_factor_file = settings["wateruse_factor_file"], in_cfs = True)

        else:
            total_wateruse_dict = wateruse.get_all_total_wateruse(wateruse_files = settings["wateruse_files"], id_list = centroids, wateruse_factor_file = None, in_cfs = True)

        # print monthly output in nice format to info file
        print("FeatureId: {}\n    Centroids: {}\n    Total Water Use:\n".format(featureid, centroids))  
        helpers.print_monthly_dict(monthly_dict = total_wateruse_dict)
       
        # get the txt data file that has a parent directory matching the current featureid
        if settings["is_batch_simulation"]:
            path = os.path.join(settings["simulation_directory"], featureid)
        else:
            path = settings["simulation_directory"]

        # find the WATER.txt file 
        watertxt_file = helpers.find_file(name = settings["water_text_file_name"], path = path)

        # get file info
        watertxt_dir, watertxt_filename = helpers.get_file_info(watertxt_file)       

        # create an output directory
        output_dir = helpers.make_directory(path = watertxt_dir, directory_name = settings["wateruse_directory_name"])
        
        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = output_dir)

        # read the txt
        watertxt_data = watertxt.read_file(watertxt_file)            

        # apply water use
        watertxt_data = watertxt.apply_wateruse(watertxt_data, wateruse_totals = total_wateruse_dict) 

        # write updated txt
        watertxt_with_wateruse_file = "-".join([settings["wateruse_prepend_name"], watertxt_filename])   

        watertxt.write_file(watertxt_data = watertxt_data, save_path = output_dir, filename = watertxt_with_wateruse_file)              

        # plot 
        updated_watertxt_file = os.path.join(output_dir, watertxt_with_wateruse_file)
        water_files_processing.process_water_files(file_list = [updated_watertxt_file], settings = settings, print_data = True)

        # write timeseries of discharge + water use for OASIS
        watertxt.write_timeseries_file(watertxt_data = watertxt_data, name = "Discharge + Water Use", save_path = oasis_dir, filename = "-".join([watertxt_data["stationid"], settings["oasis_file_name"]]))

        # write timeseries of dishcarge + water use for ecoflow program
        watertxt.write_timeseries_file_stationid(watertxt_data, name = "Discharge + Water Use", save_path = ecoflow_dir, filename = "", stationid = watertxt_data["stationid"])


def apply_wateruse(settings):
    """    
    Apply water use data to a WATER \*.txt file(s). 

    Parameters
    ----------
    settings : dictionary
        Dictionary of user settings                 

    Notes
    -----
    Uses settings set in user_settings.py  
    """   

	# create output directories and files   
    info_dir, ecoflow_dir, oasis_dir, info_file = create_output_dirs_files(settings)

    # initialize error logging in info_dir
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    # write all future print strings to the info_file
    sys.stdout = open(info_file, "w")  
    
    # open shapefiles
    centroids_shapefile = osgeo.ogr.Open(settings["wateruse_centroids_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"])) 

    # find intersecting points (centroids) based on water basin supplied
    intersecting_centroids_all = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = centroids_shapefile, intersectee_field = settings["wateruse_centroids_shapefile_id_field"], intersector_field = settings["basin_shapefile_id_field"])

    intersecting_centroids, nonintersecting_centroids = spatialvectors.validate_field_values(field_values_dict = intersecting_centroids_all)     

    # apply water use
    if intersecting_centroids:    
        process_intersecting_centroids(intersecting_centroids, settings, ecoflow_dir, oasis_dir)

    # if no intersecting centroids, then warn the user and ask user to supply the water use points to a text file that will be contained in the info directory with a name specified in the user_settings.py file
    if nonintersecting_centroids:
        
        logging.warn("The following basins do not intersect with the water use centroids for water use:\n\n    {}\n".format(nonintersecting_centroids)) 
              
        spatialvectors.write_field_values_file(filepath = info_dir, filename = settings["wateruse_non_intersecting_file_name"], field_values_dict = nonintersecting_centroids)
        
        logging.warn("\nPlease add centroids (separated by commas) that you would like to use for each non-intersecting basin to the file\n    {}".format(os.path.join(info_dir, settings["wateruse_non_intersecting_file_name"])))

    # get drainage areas for ecoflow program; if shapefile has an area field, then use that otherwise calculate area
    if settings["basin_shapefile_area_field"]:
    	area_values_dict = spatialvectors.get_field_values(shapefile = basin_shapefile, id_field = settings["basin_shapefile_id_field"], query_field = settings["basin_shapefile_area_field"])    

    else:
    	area_values_dict = spatialvectors.get_shapefile_areas(shapefile = basin_shapefile, id_field = settings["basin_shapefile_id_field"])

    # write the drainage area csv file for ecoflow program
    watertxt.write_drainagearea_file(area_data = area_values_dict, save_path = ecoflow_dir, filename = settings["ecoflow_drainage_area_file_name"])

    # remove error logger
    waterapputils_logging.remove_loggers()


def apply_subwateruse(settings):
    """    
    Apply substitute water use data to a WATER \*.txt file(s).  
    User supplies the water use points to a text file that will be 
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
    info_dir, ecoflow_dir, oasis_dir, info_file = create_output_dirs_files(settings, is_sub_wateruse = True)

    # initialize error logging in info_dir
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    # write all future print strings to the info_file
    sys.stdout = open(info_file, "w")  

    # get the intersecting points (centroids) based on wateruse non-intersecting_file
    intersecting_centroids = spatialvectors.read_field_values_file(filepath = os.path.join(info_dir, settings["wateruse_non_intersecting_file_name"]))

    # apply the wateruse     
    process_intersecting_centroids(intersecting_centroids, settings, ecoflow_dir, oasis_dir)

    waterapputils_logging.remove_loggers()


