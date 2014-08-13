# -*- coding: utf-8 -*-
"""
:Module: waterapputils.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Main controller that handles user input options for processing WATER application output filesb
"""

__version__   = "1.0.0"
__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os, sys
import argparse
import Tkinter, tkFileDialog
import logging
import osgeo.ogr

# my modules
import helpers
import watertxt
import waterxml
import watertxt_viewer
import waterxml_viewer
import waterapputils_logging
import deltas
import spatialvectors
import wateruse

# editable files containing path
import wateruse_batch_variables
import waterdeltas_batch_variables

def process_txt_files(file_list, arguments):
    """    
    Process a list of WATER text files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """
    for f in file_list:
                
        filedir, filename = helpers.get_file_info(f)
          
        # create output directory     
        outputdirpath = helpers.make_directory(path = filedir, directory_name = "_".join(["_waterapputils", filename.split(".txt")[0], "output"]))      
        
        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = outputdirpath)        
        
        # read data
        data = watertxt.read_file(f)  

        # plot data                            
        watertxt_viewer.plot_watertxt_data(data, is_visible = arguments.showplot, save_path = outputdirpath)             

        # print data
        if arguments.verbose: 
            watertxt_viewer.print_watertxt_data(data)  

        # close error logging
        waterapputils_logging.remove_loggers()

def process_xml_files(file_list, arguments):
    """    
    Process a list of WATER xml files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """
    for f in file_list:
                
        filedir, filename = helpers.get_file_info(f)
          
        # create output directory     
        outputdirpath = helpers.make_directory(path = filedir, directory_name = "-".join([filename.split(".xml")[0], "output"]))      
        
        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = outputdirpath)        
        
        # read data
        data = waterxml.read_file(f)  

        # plot data                            
        waterxml_viewer.plot_waterxml_timeseries_data(data, is_visible = arguments.showplot, save_path = outputdirpath)             
        waterxml_viewer.plot_waterxml_topographic_wetness_index_data(data, is_visible = arguments.showplot, save_path = outputdirpath) 
        
        # print data
        if arguments.verbose: 
            waterxml_viewer.print_waterxml_data(data)  

        # close error logging
        waterapputils_logging.remove_loggers()

def process_txtcmp(file_list, arguments):
    """    
    Compare two WATER text files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """
    watertxt_file1 = file_list[0]
    watertxt_file2 = file_list[1]
                
    filedir1, filename1 = helpers.get_file_info(watertxt_file1)
    filedir2, filename2 = helpers.get_file_info(watertxt_file2)
      
    # create output directory     
    outputdirpath = helpers.make_directory(path = filedir1, directory_name = "-".join([filename1.split(".txt")[0], filename2.split(".txt")[0] , "comparison", "output"]))      
    
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = outputdirpath)        
    
    # read data
    watertxt_data1 = watertxt.read_file(watertxt_file1)  
    watertxt_data2 = watertxt.read_file(watertxt_file2) 
    
    # plot data                            
    watertxt_viewer.plot_watertxt_comparison(watertxt_data1, watertxt_data2, is_visible = arguments.showplot, save_path = outputdirpath)             
            
    # print data
    if arguments.verbose: 
        watertxt_viewer.print_watertxt_data(watertxt_data1)  
        watertxt_viewer.print_watertxt_data(watertxt_data2)  

    # close error logging
    waterapputils_logging.remove_loggers()

def process_xmlcmp(file_list, arguments):
    """    
    Compare two WATER XML files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """
    waterxml_file1 = file_list[0]
    waterxml_file2 = file_list[1]
                
    filedir1, filename1 = helpers.get_file_info(waterxml_file1)
    filedir2, filename2 = helpers.get_file_info(waterxml_file2)
      
    # create output directory     
    outputdirpath = helpers.make_directory(path = filedir1, directory_name = "-".join([filename1.split(".xml")[0], "vs", filename2.split(".xml")[0], "output"]))         
    
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = outputdirpath)        
    
    # read data
    waterxml_data1 = waterxml.read_file(waterxml_file1)  
    waterxml_data2 = waterxml.read_file(waterxml_file2) 
   
    # plot data                            
    waterxml_viewer.plot_waterxml_timeseries_comparison(waterxml_data1, waterxml_data2, is_visible = arguments.showplot, save_path = outputdirpath) 
            
    # print data
    if arguments.verbose: 
        waterxml_viewer.print_watertxt_data(waterxml_data1)  
        waterxml_viewer.print_watertxt_data(waterxml_data2)  

    # close error logging
    waterapputils_logging.remove_loggers()

def process_intersecting_tiles(intersecting_tiles, files_dict, arguments):
    """    
    Apply delta factors to a WATER *.xml file. The new file created is saved to a directory
    chosen by the user.

    Parameters
    ----------
    intersecting_tiles : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.  
    files_dict : dictionary
        Dictionary of 
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {"delta_files": list of delta text files,
                  "delta_shapefile": shapefile corresponding to delta files,
                  "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with delta shapefile
                  "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files
                  "waterxml_directory": path to directory containing xml file or files}    
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
        output_dir = helpers.make_directory(waterxml_filedir_path, "_waterapputils_waterdeltas_output")

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
        process_xmlcmp(file_list = [updated_waterxml_file, waterxml_file], arguments = arguments)


def process_intersecting_centroids(intersecting_centroids, files_dict, arguments):
    """    
    Apply water use data to a WATER *.txt file. The new file created is saved to the same
    directory as the *.xml file.

    Parameters
    ----------
    intersecting_centroids : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.  
    files_dict : dictionary
        Dictionary of user file paths to necessary datasets.
    arguments : argparse object
        An argparse object containing user options. 
                 

    Notes
    -----
    files_dict = {"wateruse_files": list of water use text files,
                  "wateruse_factor_file": path to water use factor file 
                  "basin_centroids_shapefile": shapefile corresponding to basin centroids,
                  "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with basin centroid shapefile
                  "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files
                  "watertxt_directory": path to directory containing txt file or files}    
    """      
    # create a file for the output  
    for featureid, centroids in intersecting_centroids.iteritems():
           
        print("FeatureId: {}\n".format(featureid))  
        print("\tCentroids: {}\n".format(centroids))  
        print("\tTotal Water Use: \n")
        # get sum of the water use data
        if files_dict["wateruse_factor_file"]:
            total_wateruse_dict = wateruse.get_all_total_wateruse(wateruse_files = files_dict["wateruse_files"], id_list = centroids, wateruse_factor_file = files_dict["wateruse_factor_file"], in_cfs = True)

        else:
            total_wateruse_dict = wateruse.get_all_total_wateruse(wateruse_files = files_dict["wateruse_files"], id_list = centroids, wateruse_factor_file = None, in_cfs = True)

        # print monthly output in nice format
        helpers.print_monthly_dict(monthly_dict = total_wateruse_dict)
       
        # get the txt data file that has a parent directory matching the current featureid
        path = os.path.join(files_dict["watertxt_directory"], featureid)
        watertxt_file = helpers.find_file(name = "WATER.txt", path = path)

        # get file info
        watertxt_filedir_path, watertxt_filename = helpers.get_file_info(watertxt_file)       

        # create an output directory
        output_dir = helpers.make_directory(watertxt_filedir_path, "_waterapputils_wateruse_output")

        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = output_dir)

        # read the txt
        watertxt_data = watertxt.read_file(watertxt_file)            

        # apply water use
        watertxt_data = watertxt.apply_wateruse(watertxt_data, wateruse_totals = total_wateruse_dict) 

        # write updated txt
        txt_output_filename = "-".join([watertxt_filename.split(".txt")[0], "updated", files_dict["basin_field"], featureid]) + ".txt"  

        watertxt.write_file(watertxt_data = watertxt_data, save_path = output_dir, filename = txt_output_filename)              

        # plot comparison
        updated_watertxt_file = os.path.join(output_dir, txt_output_filename)
        process_txt_files(file_list = [updated_watertxt_file, watertxt_file], arguments = arguments)


def apply_deltas_to_xml_files(files_dict, arguments):
    """    
    Apply delta factors to a WATER *.xml file. The new file created is saved to a directory
    chosen by the user.

    Parameters
    ----------
    files_dict : dictionary
        Dictionary of 
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {"delta_files": list of delta text files,
                  "delta_shapefile": shapefile corresponding to delta files,
                  "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with delta shapefile
                  "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files
                  "waterxml_directory": path to directory containing xml file or files}    
    """    
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = files_dict["waterxml_directory"]) 

    info_file = os.path.join(files_dict["waterxml_directory"], "_waterapputils_waterdeltas_batchrun_info.txt")
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
        
        logging.warn("The following are basins that do not intersect with the tiles for water deltas: {}\n".format(nonintersecting_tiles)) 
        
        outfilename = "_waterapputils_non_intersecting_basin_tiles.txt"
        spatialvectors.write_field_values_file(filepath = files_dict["waterxml_directory"], filename = outfilename, field_values_dict = nonintersecting_tiles)
        outfilepath = os.path.join(files_dict["watertxt_directory"], outfilename)
        
        logging.warn("Writing file: \n{}\n Please add the tiles (separated by commas) that you would like to use for each non-intersecting basin".format(outfilepath))

    # close error logging
    waterapputils_logging.remove_loggers()

def apply_wateruse_to_txt_files(files_dict, arguments):
    """    
    Apply water use data to a WATER *.txt file. The new file created is saved to the same
    directory as the *.xml file.

    Parameters
    ----------
    files_dict : dictionary
        Dictionary of user file paths to necessary datasets.
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {"wateruse_files": list of water use text files,
                  "wateruse_factor_file": path to water use factor file 
                  "basin_centroids_shapefile": shapefile corresponding to basin centroids,
                  "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with basin centroid shapefile
                  "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files
                  "watertxt_directory": path to directory containing txt file or files}    
    """   
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = files_dict["watertxt_directory"]) 

    info_file = os.path.join(files_dict["watertxt_directory"], "_waterapputils_wateruse_batchrun_info.txt")
    
    sys.stdout = open(info_file, "w")  
     
    # open shapefiles
    centroids_shapefile = osgeo.ogr.Open(files_dict["basin_centroids_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(files_dict["basin_shapefile"]) 

    # find intersecting points (centroids) based on water basin supplied
    intersecting_centroids_all = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = centroids_shapefile, intersectee_field = "newhydroid", intersector_field = files_dict["basin_field"])

    intersecting_centroids, nonintersecting_centroids = spatialvectors.validate_field_values(field_values_dict = intersecting_centroids_all)     

    if intersecting_centroids:    
        process_intersecting_centroids(intersecting_centroids, files_dict, arguments)

    if nonintersecting_centroids:
        # initialize error logging
        waterapputils_logging.initialize_loggers(output_dir = files_dict["watertxt_directory"]) 
        
        logging.warn("The following are basins that do not intersect with the centroids for water use: {}\n".format(nonintersecting_centroids)) 
        
        outfilename = "_waterapputils_non_intersecting_basin_centroids.txt"
        spatialvectors.write_field_values_file(filepath = files_dict["watertxt_directory"], filename = outfilename, field_values_dict = nonintersecting_centroids)
        outfilepath = os.path.join(files_dict["watertxt_directory"], outfilename)
        
        logging.warn("Writing file: \n{}\n Please add the centroids (separated by commas) that you would like to use for each non-intersecting basin".format(outfilepath))

    # close error logging
    waterapputils_logging.remove_loggers()

def apply_subwaterdeltas_to_xml_files(files_dict, arguments):

    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = files_dict["watertxt_directory"]) 

    info_file = os.path.join(files_dict["watertxt_directory"], "_waterapputils_waterdelta_batchrun_info.txt")
    sys.stdout = open(info_file, "w")  

    intersecting_tiles = spatialvectors.read_field_values_file(filepath = files_dict["non_intersecting_basin_tiles_file"])

    process_intersecting_tiles(intersecting_tiles, files_dict, arguments) 

    # close error logging
    waterapputils_logging.remove_loggers()

def apply_subwateruse_to_txt_files(files_dict, arguments):

    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = files_dict["watertxt_directory"]) 

    info_file = os.path.join(files_dict["watertxt_directory"], "_waterapputils_wateruse_batchrun_info.txt")
    sys.stdout = open(info_file, "a")  

    intersecting_centroids = spatialvectors.read_field_values_file(filepath = files_dict["non_intersecting_basin_centroids_file"])

    process_intersecting_centroids(intersecting_centroids, files_dict, arguments) 

    # close error logging
    waterapputils_logging.remove_loggers()

def main():  
    """
    Run program based on user input arguments. Program will automatically process file(s) supplied,
    log any errors found in the data file, and will save plots of every parameter. Error log and plots are saved to 
    a directory (tagged with "output") at the same level as the supplied or downloaded data files.
    """    
    # parse arguments from command line
    parser = argparse.ArgumentParser(description = "Read, process, log errors, print, and plot data from WATER  \
                                                    application output data files.") 
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-watertxt", "--watertxtfiles", nargs = "+", help = "List WATER text data file(s) to be processed")
    group.add_argument("-watertxtfd", "--watertxtfiledialog", action = "store_true", help = "Open a file dialog window to select WATER text data file(s).")
    group.add_argument("-watertxtcmp", "--watertxtcompare", nargs = 2, help = "List 2 WATER text data file(s) to be compared")
    group.add_argument("-watertxtcmpfd", "--watertxtcomparefiledialog", action = "store_true", help = "Open 2 separate file dialog windows to select WATER text data file(s) to be compared")

    group.add_argument("-waterxml", "--waterxmlfiles", nargs = "+", help = "List WATER xml data file(s) to be processed")
    group.add_argument("-waterxmlfd", "--waterxmlfiledialog", action = "store_true", help = "Open a file dialog window to select WATER xml data file(s).")
    group.add_argument("-waterxmlcmp", "--waterxmlcompare", nargs = 2, help = "List 2 WATER xml data file(s) to be compared")
    group.add_argument("-waterxmlcmpfd", "--waterxmlcomparefiledialog", action = "store_true", help = "Open 2 separate file dialog windows to select WATER XML data file(s) to be compared")
    
    group.add_argument("-applydeltas", "--applydeltas", action = "store_true", help = "Apply global climate deltas to a WATERSimulation.xml file for a WATER simulations.  Use waterdelta_batch_variables.py to enter paths to data files.")

    group.add_argument("-applywateruse", "--applywateruse", action = "store_true", help = "Apply water use data to a WATER.txt file for a WATER simulation.  Use wateruse_batch_variables.py to enter paths to data files.")

    group.add_argument("-applysubwateruse", "--applysubwateruse", action = "store_true", help = "Apply updated water use data from '_non_intersecting_basin_centroids.txt' to a WATER.txt file for a WATER simulation.  Use wateruse_batch_variables.py to enter paths to data files.")

    group.add_argument("-applysubdeltas", "--applysubdeltas", action = "store_true", help = "Apply updated water deltas data from '_non_intersecting_basin_tiles.txt' to a WaterSimulation.xml file for a WATER simulation.  Use wateruse_deltas_variables.py to enter paths to data files.")

    parser.add_argument("-v", "--verbose", action = "store_true",  help = "Print general information about data file(s)")
    parser.add_argument("-p", "--showplot", action = "store_true",  help = "Show plots of parameters contained in data file(s)")
    args = parser.parse_args()  

    # get files from command line arguments and process
    try:       
        
        # water text files
        if args.watertxtfiles:
            process_txt_files(file_list = args.watertxtfiles, arguments = args)
            sys.exit()
        
        elif args.watertxtfiledialog:
            root = Tkinter.Tk() 
            files = tkFileDialog.askopenfilenames(title = "Select WATER Text File(s)", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()          
            process_txt_files(file_list = root.tk.splitlist(files), arguments = args)
            sys.exit()

        elif args.watertxtcompare:
            process_txtcmp(file_list = args.watertxtcompare, arguments = args)
            sys.exit()

        elif args.watertxtcomparefiledialog:
            root = Tkinter.Tk() 
            file1 = tkFileDialog.askopenfilename(title = "Select First WATER Text File To Use In Comparision", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()          

            root = Tkinter.Tk() 
            file2 = tkFileDialog.askopenfilename(title = "Select Second WATER Text File To Use In Comparision", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()
            
            process_txtcmp(file_list = [file1, file2], arguments = args)
            sys.exit()
            
        # water xml files
        elif args.waterxmlfiles:
            process_xml_files(file_list = args.waterxmlfiles, arguments = args)
            sys.exit()
        
        elif args.waterxmlfiledialog:
            root = Tkinter.Tk() 
            files = tkFileDialog.askopenfilenames(title = "Select WATER XML File(s)", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy()          
            process_xml_files(file_list = root.tk.splitlist(files), arguments = args)
            sys.exit()

        elif args.waterxmlcompare:
            process_xmlcmp(file_list = args.waterxmlcompare, arguments = args)
            sys.exit()

        elif args.waterxmlcomparefiledialog:
            root = Tkinter.Tk() 
            file1 = tkFileDialog.askopenfilename(title = "Select First WATER XML File To Use In Comparision", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy()          

            root = Tkinter.Tk() 
            file2 = tkFileDialog.askopenfilename(title = "Select Second WATER XML File To Use In Comparision", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy()
            
            process_xmlcmp(file_list = [file1, file2], arguments = args)
            sys.exit()

        # apply deltas
        elif args.applydeltas:

            files_dict = {"delta_files": waterdeltas_batch_variables.delta_files,
                          "delta_shapefile": waterdeltas_batch_variables.delta_shapefile, 
                          "basin_shapefile": waterdeltas_batch_variables.basin_shapefile,
                          "basin_field": waterdeltas_batch_variables.basin_field,
                          "waterxml_directory": waterdeltas_batch_variables.waterbatch_directory
            }
            
            apply_deltas_to_xml_files(files_dict = files_dict, arguments = args)
            sys.exit() 

        elif args.applysubdeltas:
            files_dict = {"delta_files": waterdeltas_batch_variables.delta_files,
                          "delta_shapefile": waterdeltas_batch_variables.delta_shapefile, 
                          "basin_shapefile": waterdeltas_batch_variables.basin_shapefile,
                          "basin_field": waterdeltas_batch_variables.basin_field,
                          "waterxml_directory": waterdeltas_batch_variables.waterbatch_directory,
                          "non_intersecting_basin_tile_file": wateruse_batch_variables.subwaterdeltas_file,
            }
            
            apply_subwateruse_to_txt_files(files_dict = files_dict, arguments = args)

            sys.exit()

        # apply water use
        elif args.applywateruse:          

            files_dict = {"wateruse_files": wateruse_batch_variables.wateruse_files,
                          "wateruse_factor_file": wateruse_batch_variables.wateruse_factor_file,
                          "basin_centroids_shapefile": wateruse_batch_variables.basin_centroids_shapefile, 
                          "basin_shapefile": wateruse_batch_variables.basin_shapefile,
                          "basin_field": wateruse_batch_variables.basin_field,
                          "watertxt_directory": wateruse_batch_variables.waterbatch_directory
            }
            
            apply_wateruse_to_txt_files(files_dict = files_dict, arguments = args)

        elif args.applysubwateruse:
            files_dict = {"wateruse_files": wateruse_batch_variables.wateruse_files,
                          "wateruse_factor_file": wateruse_batch_variables.wateruse_factor_file,
                          "basin_centroids_shapefile": wateruse_batch_variables.basin_centroids_shapefile, 
                          "basin_shapefile": wateruse_batch_variables.basin_shapefile,
                          "basin_field": wateruse_batch_variables.basin_field,
                          "watertxt_directory": wateruse_batch_variables.waterbatch_directory,
                          "non_intersecting_basin_centroids_file": wateruse_batch_variables.subwateruse_file,
            }
            
            apply_subwateruse_to_txt_files(files_dict = files_dict, arguments = args)

            sys.exit()

    except IOError as error:
        logging.exception("IO error: {0}".format(error.message))
        sys.exit(1)
        
    except ValueError as error:
        logging.exception("Value error: {0}".format(error.message))
        sys.exit(1)

    except IndexError as error:
        logging.exception("Index error: {0}".format(error.message))
        sys.exit(1)

    except AssertionError as error:
        logging.exception("Assertion error: {0}".format(error.message))
        sys.exit(1)

        
if __name__ == "__main__":
    main() 

