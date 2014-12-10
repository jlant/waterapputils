def process_intersecting_tiles(intersecting_tiles, files_dict):
    """    
    Apply delta factors to a WATER \*.xml file. The new file created is saved to a directory
    chosen by the user.

    Parameters
    ----------
    intersecting_tiles : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.  
    files_dict : dictionary
        Dictionary of user file paths to necessary datasets.
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {

        "delta_files": list of delta text files,

        "delta_shapefile": shapefile corresponding to delta files,

        "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with delta shapefile

        "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files

        "waterxml_directory": path to directory containing xml file or files

    }   
    """ 
    for featureid, tiles in intersecting_tiles.iteritems():                    

        print("FeatureId: {}\n".format(featureid))  
        print("\tTiles: {}\n".format(tiles))  
        print("\tAverage Deltas: \n")
        
        # get average values for a list of delta files
        avg_deltas = deltas.get_avg_deltas(delta_files = files_dict["delta_files"], tiles = tiles)  

        print("\t  Tmax\n")
        helpers.print_monthly_dict(monthly_dict = avg_deltas["Tmax"])

        print("\t  Ppt\n")
        helpers.print_monthly_dict(monthly_dict = avg_deltas["Ppt"])

        # get the xml data file that has a parent directory matching the current featureid
        path = os.path.join(files_dict["waterxml_directory"], featureid)
        waterxml_file = helpers.find_file(name = "WATERSimulation.xml", path = path)

        # get file info
        waterxml_filedir_path, waterxml_filename = helpers.get_file_info(waterxml_file)

        # create an output directory
        output_dir = helpers.make_directory(waterxml_filedir_path, GCMDELTA_DIRNAME)

        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = output_dir)

        # read the xml
        waterxml_tree = waterxml.read_file(waterxml_file)            

        # apply deltas
        for key, value in avg_deltas.iteritems():
            if key == "Ppt":
                waterxml.apply_factors(waterxml_tree = waterxml_tree, element = "ClimaticPrecipitationSeries", factors = avg_deltas[key])

            elif key == "Tmax":
                waterxml.apply_factors(waterxml_tree = waterxml_tree, element = "ClimaticTemperatureSeries", factors = avg_deltas[key])

        # write updated xml
        xml_output_filename = "-".join([waterxml_filename.split(".xml")[0], "updated", files_dict["basin_field"], featureid]) + ".xml"                
        waterxml.write_file(waterxml_tree = waterxml_tree, save_path = output_dir, filename = xml_output_filename)

        # plot comparison
        updated_waterxml_file = os.path.join(output_dir, xml_output_filename)
        process_cmp(file_list = [updated_waterxml_file, waterxml_file], arguments = arguments)


def apply_deltas_to_xml_files(files_dict, arguments):
    """    
    Apply delta factors to a WATER \*.xml file. The new file created is saved to a directory
    chosen by the user.

    Parameters
    ----------
    files_dict : dictionary
        Dictionary of user file paths to necessary datasets.
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {

        "delta_files": list of delta text files,

        "delta_shapefile": shapefile corresponding to delta files,

        "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with delta shapefile

        "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files

        "waterxml_directory": path to directory containing xml file or files

    } 
    """    
   
    info_dir = helpers.make_directory(path = files_dict["waterxml_directory"], directory_name = BATCH_INFO_DIR) 

    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    info_file = os.path.join(info_dir, GCMDELTA_INFO_FILE)

    print("Using the following data files:\n")
    
    for key, value in files_dict.iteritems():
        print("    {} : {}".format(key, value))

    print("")
    print("Batch Run Information:\n    {}\n".format(info_dir))

    print("GCM Delta Information and Values:\n    {}\n".format(info_file))

    sys.stdout = open(info_file, "w")    

    # open shapefiles
    delta_shapefile = osgeo.ogr.Open(files_dict["delta_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(files_dict["basin_shapefile"]) 

    # find intersecting tiles based on water basin supplied
    intersecting_tiles_all = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = delta_shapefile, intersectee_field = "Tile", intersector_field = files_dict["basin_field"])
       
    intersecting_tiles, nonintersecting_tiles = spatialvectors.validate_field_values(field_values_dict = intersecting_tiles_all)     

    if intersecting_tiles:    
        process_intersecting_tiles(intersecting_tiles, files_dict, arguments)

    if nonintersecting_tiles:
        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = files_dict["waterxml_directory"]) 
        
        logging.warn("The following are basins that do not intersect with the centroids for water use:\n    {}\n".format(nonintersecting_tiles)) 
        
        outfilename = GCMDELTA_NON_INTERSECT_FILE
        spatialvectors.write_field_values_file(filepath = files_dict["waterxml_directory"], filename = outfilename, field_values_dict = nonintersecting_tiles)
        outfilepath = os.path.join(files_dict["watertxt_directory"], outfilename)
        
        logging.warn("Writing file:\n    {}\n\n    Please add the tiles (separated by commas) that you would like to use for each non-intersecting basin".format(outfilepath))

    # close error logging
    waterapputils_logging.remove_loggers()


def apply_subwaterdeltas_to_xml_files(files_dict, arguments):

    info_dir = os.path.join(files_dict["waterxml_directory"], BATCH_INFO_DIR)    
    
    waterapputils_logging.initialize_loggers(output_dir = info_dir) 

    info_file = os.path.join(info_dir, SUBGCMDELTA_INFO_FILE)

    print("Using the following data files:\n")
    
    for key, value in files_dict.iteritems():
        print("    {} : {}".format(key, value))

    print("")
    print("Batch Run Information:\n    {}\n".format(info_dir))

    print("GCM Deltas Information and Values:\n    {}\n".format(info_file))

    intersecting_tiles = spatialvectors.read_field_values_file(filepath = files_dict["non_intersecting_basin_tiles_file"])

    process_intersecting_tiles(intersecting_tiles, files_dict, arguments) 

    waterapputils_logging.remove_loggers()