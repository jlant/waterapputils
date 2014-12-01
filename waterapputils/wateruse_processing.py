import osgeo.ogr

import helpers
import water_files_processing
import watertxt


def write_oasis_file(file_list, settings):

    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        oasis_dir = helpers.make_directory(path = filedir, directory_name = settings["oasis_directory_name"])

        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": oasis_dir})

        waterapputils_logging.initialize_loggers(output_dir = oasis_dir) 

        watertxt_data = watertxt.read_file(f)      

        # write timeseries of discharge + water use for OASIS
        watertxt.write_timeseries_file(watertxt_data = watertxt_data, name = "Discharge + Water Use", save_path = oasis_dir, filename = "-".join([watertxt_data["stationid"], settings["oasis_file_name"]]))
                
        waterapputils_logging.remove_loggers()

def write_ecoflow_file_stationid(file_list, settings):

    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       
 
        print("Processing: \n    {}\n".format(f))

        ecoflow_dir = helpers.make_directory(path = filedir, directory_name = settings["ecoflow_directory_name"])

        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": ecoflow_dir})

        waterapputils_logging.initialize_loggers(output_dir = ecoflow_dir) 

        watertxt_data = watertxt.read_file(f)      

        # write timeseries of dishcarge + water use for ecoflow program
        watertxt.write_timeseries_file_stationid(watertxt_data, name = "Discharge + Water Use", save_path = ecoflow_dir, filename = "", stationid = watertxt_data["stationid"])

        print("Output: \n    {}\n\n".format(ecoflow_dir))
                
        waterapputils_logging.remove_loggers()

def write_ecoflow_file_drainageareaxml(file_list, settings):

    area_data = {}
    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        ecoflow_dir = helpers.make_directory(path = filedir, directory_name = settings["ecoflow_directory_name"])

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
    watertxt.write_drainagearea_file(area_data = area_data, save_path = ecoflow_dir, filename = settings["ecoflow_drainage_area_file_name"])
            
    waterapputils_logging.remove_loggers()


def write_ecoflow_file_drainageareashp(file_list, settings, label_field):

    for f in file_list:
               
        filedir, filename = helpers.get_file_info(f)       

        ecoflow_dir = helpers.make_directory(path = filedir, directory_name = settings["ecoflow_directory_name"])

        waterapputils_logging.initialize_loggers(output_dir = ecoflow_dir) 
 
        helpers.print_input_output_info(input_dict = {"input_file": f}, output_dict = {"output_directory": ecoflow_dir})

        # Open the shapefiles
        basin_shapefile = osgeo.ogr.Open(f)  

        # get the area means for each region
        if label_field:
            field = arguments.shpfield[0]
            areas = spatialvectors.get_shapefile_areas(basin_shapefile, field = field)
        else:
            areas = spatialvectors.get_shapefile_areas(basin_shapefile, field = "FID")

        # convert from m**2 to mi**2; water application uses NAD83 projection with units of meters
        area_data = helpers.convert_area_values(areas, in_units = "m2", out_units = "mi2")

        # write timeseries of dishcarge + water use for ecoflow program
        watertxt.write_drainagearea_file(area_data = area_data, save_path = ecoflow_dir, filename = settings["ecoflow_drainage_area_file_name"])
            
    waterapputils_logging.remove_loggers()


def process_intersecting_centroids(intersecting_centroids, settings, ecoflow_dir, oasis_dir):
    """    
    Apply water use data to a WATER \*.txt file. The new file created is saved to the same
    directory as the \*.xml file.

    Parameters
    ----------
    intersecting_centroids : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.  
    files_dict : dictionary
        Dictionary of user file paths to necessary datasets.
    arguments : argparse object
        An argparse object containing user options. 
    ecoflow_dir : string
        String path to directory that will contain output specific for ecoflow program
    oasis_dir : string
        String path to directory that will contain output specific for oasis

    Notes
    -----
    files_dict = {

        "wateruse_files": list of water use text files,
        
        "wateruse_factor_file": path to water use factor file 
        
        "basin_centroids_shapefile": shapefile corresponding to basin centroids,
        
        "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with basin centroid shapefile
        
        "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files
        
        "watertxt_directory": path to directory containing txt file or files

    }    
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
        water_files_processing.process_water_files(file_list = [updated_watertxt_file], arguments = arguments)

        # write timeseries of discharge + water use for OASIS
        watertxt.write_timeseries_file(watertxt_data = watertxt_data, name = "Discharge + Water Use", save_path = oasis_dir, filename = "-".join([watertxt_data["stationid"], settings["oasis_file_name"]]))

        # write timeseries of dishcarge + water use for ecoflow program
        watertxt.write_timeseries_file_stationid(watertxt_data, name = "Discharge + Water Use", save_path = ecoflow_dir, filename = "", stationid = watertxt_data["stationid"])


def apply_wateruse(settings):
    """    
    Apply water use data to a WATER \*.txt file. The new file created is saved to the same
    directory as the \*.xml file.

    Parameters
    ----------
    files_dict : dictionary
        Dictionary of user file paths to necessary datasets.
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {

        "wateruse_files": list of water use text files,
        
        "wateruse_factor_file": path to water use factor file 
        
        "basin_centroids_shapefile": shapefile corresponding to basin centroids,
        
        "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with basin centroid shapefile
        
        "basin_field": string name of field of used in WATER batch run; used to find the WATER.txt files in the WATER batch output directory structure
        
        "watertxt_directory": path to directory containing txt file or files

    }    
    """   

	# create output directories   
    info_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["info_directory_name"])    
    ecoflow_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["ecoflow_directory_name"])
    oasis_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["oasis_directory_name"])
    
    # initialize error logging in info_dir
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    # create full path to info_file
    wateruse_info_file = os.path.join(info_dir, settings["wateruse_info_file_name"])

    # print input and output information
    helpers.print_input_output_info(setting_dict = settings, output_dict = {"info_dir": info_dir, "info_file": wateruse_info_file, "ecoflow_dir": ecoflow_dir, "oasis_dir": oasis_dir})

    # write all future print strings to the info_file
    sys.stdout = open(info_file, "w")  
    
    # open shapefiles
    centroids_shapefile = osgeo.ogr.Open(settings["wateruse_centroids_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"])) 

    # find intersecting points (centroids) based on water basin supplied
    intersecting_centroids_all = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = centroids_shapefile, intersectee_field = settings["wateruse_centroids_shapefile_id_field"], intersector_field = settings["basin_shapefile_id_field"])

    intersecting_centroids, nonintersecting_centroids = spatialvectors.validate_field_values(field_values_dict = intersecting_centroids_all)     

    if intersecting_centroids:    
        process_intersecting_centroids(intersecting_centroids, ecoflow_dir, oasis_dir)

    if nonintersecting_centroids:
        
        logging.warn("The following basins do not intersect with the water use centroids for water use:\n    {}\n".format(nonintersecting_centroids)) 
              
        spatialvectors.write_field_values_file(filepath = info_dir, filename = settings["wateruse_non_intersecting_file_name"], field_values_dict = nonintersecting_centroids)
        
        logging.warn("Writing file:\n    {}\n\n    Please add centroids (separated by commas) that you would like to use for each non-intersecting basin".format(os.path.join(info_dir, settings["wateruse_non_intersecting_file_name"])))

    # get drainage areas for ecoflow program; if shapefile has an area field, then use that otherwise calculate area
    if settings["basin_shapefile_area_field"]:
    	area_values_dict = spatialvectors.get_field_values(shapefile = basin_shapefile, id_field = settings["basin_shapefile_id_field"], query_field = settings["basin_shapefile_area_field"])    

    else:
    	area_values_dict = spatialvectors.get_shapefile_areas(shapefile = basin_shapefile, field = settings["basin_shapefile_id_field"])

    # write the drainage area csv file for ecoflow program
    watertxt.write_drainagearea_file(area_data = area_values_dict, save_path = ecoflow_dir, filename = settings["ecoflow_drainage_area_file_name"])

    # remove error logger
    waterapputils_logging.remove_loggers()


def apply_subwateruse_to_txt_files(files_dict, arguments):

    info_dir = os.path.join(files_dict["watertxt_directory"], BATCH_INFO_DIR)    
    ecoflow_dir = helpers.make_directory(path = files_dict["watertxt_directory"], directory_name = ECOFLOW_DIR)

    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    info_file = os.path.join(info_dir, SUBWATERUSE_INFO_FILE)

    print("Using the following data files:\n")
    
    for key, value in files_dict.iteritems():
        print("    {} : {}".format(key, value))

    print("")
    print("Batch Run Information:\n    {}\n".format(info_dir))

    print("Water Use Information and Values:\n    {}\n".format(info_file))

    sys.stdout = open(info_file, "a")  

    intersecting_centroids = spatialvectors.read_field_values_file(filepath = files_dict["non_intersecting_basin_centroids_file"])

    process_intersecting_centroids(intersecting_centroids, files_dict, arguments, ecoflow_dir)

    waterapputils_logging.remove_loggers()


