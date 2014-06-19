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
        outputdirpath = helpers.make_directory(path = filedir, directory_name = "-".join([filename.split(".txt")[0], "output"]))      
        
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

def apply_deltas_to_txt(file_list, arguments):
    """    
    Apply delta factors to a WATER *.txt file. The new file created is saved to the same
    directory as the *.txt file.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """
    watertxt_file = file_list[0]
    delta_file = file_list[1]
                
    water_filedir, water_filename = helpers.get_file_info(watertxt_file)
    delta_filedir, delta_filename = helpers.get_file_info(delta_file)
          
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = water_filedir)        
    
    # read data
    watertxt_data = watertxt.read_file(watertxt_file)  
    deltas_data = deltas.read_file(delta_file) 
    
    # calculate average deltas for a list of tiles
    avg_delta_values = deltas.calculate_avg_delta_values(deltas_data = deltas_data, tile_list = ["31", "32"])
    
    for key, value in avg_delta_values.iteritems():
        # apply deltas
        watertxt_data_with_deltas = watertxt.apply_factors(watertxt_data = watertxt_data, name = key, factors = avg_delta_values[key])

    watertxt.write_file(watertxt_data = watertxt_data_with_deltas, save_path = water_filedir, filename = "-".join([water_filename.split(".txt")[0], "with", delta_filename.split(".txt")[0] , "applied2.txt"]))
    watertxt.write_timeseries_file(watertxt_data = watertxt_data_with_deltas, name = "PET", save_path = water_filedir)
           
    # print data
    if arguments.verbose: 
        watertxt_viewer.print_watertxt_data(watertxt_data)  
        watertxt_viewer.print_watertxt_data(watertxt_data_with_deltas)  

    # close error logging
    waterapputils_logging.remove_loggers()


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
                  "waterxml_directory": path to directory containing xml file or files
                  "outputxml_directory": path of directory to store new updated xml files}    
    """
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = files_dict["outputxml_directory"])
    
    # open shapefiles
    delta_shapefile = osgeo.ogr.Open(files_dict["delta_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(files_dict["basin_shapefile"]) 

    # find intersecting tiles based on water basin supplied
    intersecting_tiles = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = delta_shapefile, intersectee_field = "Tile", intersector_field = files_dict["basin_field"])

    print("Intersecting tiles: {}\n".format(intersecting_tiles))        
    for featureid, tiles in intersecting_tiles.iteritems():                    
        print("FeatureId: {}\n".format(featureid))  
        print("Tiles: {}\n".format(tiles))  

        # get average values for a list of delta files
        avg_deltas = deltas.get_avg_deltas(delta_files = files_dict["delta_files"], tiles = tiles)  

        print("Avg deltas: {}\n".format(avg_deltas))

        # get the xml data file that has a parent directory matching the current featureid
        path = os.path.join(files_dict["waterxml_directory"], featureid)
        waterxml_file = helpers.find_file(name = "WATERSimulation.xml", path = path)

        # get file info
        waterxml_filedir_path, waterxml_filename = helpers.get_file_info(waterxml_file)

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
        waterxml.write_file(waterxml_tree = waterxml_tree, save_path = files_dict["outputxml_directory"], filename = xml_output_filename)

        # plot comparison
        updated_waterxml_file = os.path.join(files_dict["outputxml_directory"], xml_output_filename)
        process_xmlcmp(file_list = [updated_waterxml_file, waterxml_file], arguments = arguments)

    # close error logging
    waterapputils_logging.remove_loggers()

def apply_wateruse_to_txt_files(files_dict, arguments):
    """    
    Apply water use data to a WATER *.txt file. The new file created is saved to the same
    directory as the *.xml file.

    Parameters
    ----------
    files_dict : dictionary
        Dictionary of 
    arguments : argparse object
        An argparse object containing user options.                    

    Notes
    -----
    files_dict = {"wateruse_files": list of water use text files,
                  "wateruse_factor_file": path to water use factor file 
                  "basin_centroids_shapefile": shapefile corresponding to basin centroids,
                  "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with basin centroid shapefile
                  "basin_field": string name of field of used in WATER batch run; used to find and name updated WATERSimulation.xml files
                  "watertxt_directory": path to directory containing txt file or files
                  "outputtxt_directory": path of directory to store new updated txt files}    
    """    
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = files_dict["outputtxt_directory"])
    
    # open shapefiles
    centroids_shapefile = osgeo.ogr.Open(files_dict["basin_centroids_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(files_dict["basin_shapefile"]) 

    # find intersecting points (centroids) based on water basin supplied
    intersecting_centroids = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = centroids_shapefile, intersectee_field = "newhydroid", intersector_field = files_dict["basin_field"])

    print("Intersecting centroids: {}\n".format(intersecting_centroids))        
    for featureid, centroids in intersecting_centroids.iteritems():                    
        print("FeatureId: {}\n".format(featureid))  
        print("Centroids: {}\n".format(centroids))  

        # get sum of the water use data
        if files_dict["wateruse_factor_file"]:
            total_wateruse_dict = wateruse.get_all_total_wateruse(wateruse_files = files_dict["wateruse_files"], id_list = centroids, wateruse_factor_file = files_dict["wateruse_factor_file"], in_cfs = True)

        else:
            total_wateruse_dict = wateruse.get_all_total_wateruse(wateruse_files = files_dict["wateruse_files"], id_list = centroids, wateruse_factor_file = None, in_cfs = True)

        print("Total water use dictionary: {}\n".format(total_wateruse_dict))

        # get the txt data file that has a parent directory matching the current featureid
        path = os.path.join(files_dict["watertxt_directory"], featureid)
        watertxt_file = helpers.find_file(name = "WATER.txt", path = path)

        # get file info
        watertxt_filedir_path, watertxt_filename = helpers.get_file_info(watertxt_file)

        # read the txt
        watertxt_data = watertxt.read_file(watertxt_file)            

        # apply water use
        watertxt_data = watertxt.apply_wateruse(watertxt_data, wateruse_totals = total_wateruse_dict) 

        # write updated txt
        txt_output_filename = "-".join([watertxt_filename.split(".txt")[0], "updated", files_dict["basin_field"], featureid]) + ".txt"  
        watertxt.write_file(watertxt_data = watertxt_data, save_path = files_dict["outputtxt_directory"], filename = txt_output_filename)              

        # plot comparison
        updated_watertxt_file = os.path.join(files_dict["outputtxt_directory"], txt_output_filename)
        process_txt_files(file_list = [updated_watertxt_file, watertxt_file], arguments = arguments)

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
    
    group.add_argument("-applydeltastxt", "--applydeltastxt", nargs = 2, help = "List WATER text data file followed by delta file to be applied.")
    group.add_argument("-applydeltasxml", "--applydeltasxml", nargs = 2, help = "List WATER xml data file followed by delta file to be applied.")
    group.add_argument("-applydeltasxmlfd", "--applydeltasxmlfiledialog", action = "store_true", help = "Open a series of file dialog windows to apply deltas to WATER XML data file(s)")

    group.add_argument("-applywateruse", "--applywaterusefiledialog", action = "store_true", help = "Open a series of file dialog windows to apply deltas to WATER XML data file(s)")

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
        elif args.applydeltastxt:
            apply_deltas_to_txt(file_list = args.applydeltastxt, arguments = args)
            sys.exit()

        elif args.applydeltasxml:
            apply_deltas_to_xml(file_list = args.applydeltasxml, arguments = args)
            sys.exit() 

        elif args.applydeltasxmlfiledialog:
            # get delta_files
#            root = Tkinter.Tk() 
#            delta_files = tkFileDialog.askopenfilenames(title = "Select Global Climate Model Delta Files To Apply", filetypes = [("All files", ".*"), ("Text file","*.txt")])       
#            delta_files = root.tk.splitlist(delta_files)
#            root.destroy()   
#            
#            # get delta shapefile
#            root = Tkinter.Tk() 
#            delta_shapefile = tkFileDialog.askopenfilename(title = "Select Global Climate Model Shapefile To Use", filetypes = [("All files", ".*"), ("Shapefile file","*.shp")])
#            root.destroy()   
#            
#            # get basin shapefile
#            root = Tkinter.Tk() 
#            water_shapefile = tkFileDialog.askopenfilename(title = "Select WATER Basin Shapefile To Use", filetypes = [("All files", ".*"), ("Shapefile file","*.shp")])
#            root.destroy() 

#            files_dict = {"delta_files": delta_files, "delta_shapefile": delta_shapefile, "basin_shapefile": water_shapefile}

            files_dict = {"delta_files": ["../data/deltas-gcm/CanES/RCP45/2030/Ppt.txt", "../data/deltas-gcm/CanES/RCP45/2030/Tmax.txt"], 
                          "delta_shapefile": "../data/spatial-datafiles/gcm-tiles/CanES_proj_wgs.shp", 
                          "basin_shapefile": "../data/spatial-datafiles/basins/waterbasin_multi_clean_proj_wgs.shp",
                          "basin_field": "STAID",
                          "waterxml_directory": "C:/Users/jlant/jeremiah/temp/2014-05-19_testbatch/",
                          "outputxml_directory": "../data/waterxml-datafiles/"}
            
            apply_deltas_to_xml_files(files_dict = files_dict, arguments = args)
            sys.exit() 

        elif args.applywaterusefiledialog:
            # test using test file batch and test water use data files
            files_dict = {"wateruse_files": ["../data/wateruse-datafiles/test-files/test_wateruse_JFM.txt", "../data/wateruse-datafiles/test-files/test_wateruse_AMJ.txt", "../data/wateruse-datafiles/test-files/test_wateruse_JAS.txt", "../data/wateruse-datafiles/test-files/test_wateruse_OND.txt"], 
                          "wateruse_factor_file": "../data/wateruse-datafiles/test-files/test_wateruse_factors.txt",
                          "basin_centroids_shapefile": "../data/spatial-datafiles/basins/dem_basin_centroids_tests_proj_wgs.shp", 
                          "basin_shapefile": "../data/spatial-datafiles/basins/waterbasin_multi_tests_proj_wgs.shp",
                          "basin_field": "STAID",
                          "watertxt_directory": "../data/wateruse-datafiles/test-files/wateruse_batch_test/",
                          "outputtxt_directory": "../data/wateruse-datafiles/test-files/"}

#            # test using full batch and water use data files
#            files_dict = {"wateruse_files": ["../data/wateruse-datafiles/test_JFM.txt", "../data/wateruse-datafiles/test_AMJ.txt", "../data/wateruse-datafiles/test_JAS.txt", "../data/wateruse-datafiles/test_OND.txt"], 
#                          "wateruse_factor_file": "../data/wateruse-datafiles/test_wateruse_factors.txt",
#                          "basin_centroids_shapefile": "../data/spatial-datafiles/basins/dem_basin_centroids_proj_wgs.shp", 
#                          "basin_shapefile": "../data/spatial-datafiles/basins/waterbasin_multi_clean_proj_wgs.shp",
#                          "basin_field": "STAID",
#                          "watertxt_directory": "C:/Users/jlant/jeremiah/temp/2014-06-06_testbatch_clean/",
#                          "outputtxt_directory": "../data/wateruse-datafiles/"}
            
            apply_wateruse_to_txt_files(files_dict = files_dict, arguments = args)

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

