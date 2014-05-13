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
import waterapputils_viewer
import waterapputils_logging
import deltas
import spatialvectors

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
        waterapputils_viewer.plot_watertxt_data(data, is_visible = arguments.showplot, save_path = outputdirpath)             

        # print data
        if arguments.verbose: 
            waterapputils_viewer.print_watertxt_data(data)  

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
        waterapputils_viewer.plot_waterxml_timeseries_data(data, is_visible = arguments.showplot, save_path = outputdirpath)             
        waterapputils_viewer.plot_waterxml_topographic_wetness_index_data(data, is_visible = arguments.showplot, save_path = outputdirpath) 
        
        # print data
        if arguments.verbose: 
            waterapputils_viewer.print_waterxml_data(data)  

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
    waterapputils_viewer.plot_watertxt_comparison(watertxt_data1, watertxt_data2, is_visible = arguments.showplot, save_path = outputdirpath)             
            
    # print data
    if arguments.verbose: 
        waterapputils_viewer.print_watertxt_data(watertxt_data1)  
        waterapputils_viewer.print_watertxt_data(watertxt_data2)  

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
    outputdirpath = helpers.make_directory(path = filedir1, directory_name = "-".join([filename1.split(".xml")[0], filename2.split(".xml")[0] , "comparison", "output"]))         
    
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = outputdirpath)        
    
    # read data
    waterxml_data1 = waterxml.read_file(waterxml_file1)  
    waterxml_data2 = waterxml.read_file(waterxml_file2) 
    
    # plot data                            
    waterapputils_viewer.plot_waterxml_timeseries_comparison(waterxml_data1, waterxml_data2, is_visible = arguments.showplot, save_path = outputdirpath) 
            
    # print data
    if arguments.verbose: 
        waterapputils_viewer.print_watertxt_data(waterxml_data1)  
        waterapputils_viewer.print_watertxt_data(waterxml_data2)  

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

    watertxt.write_file(watertxt_data = watertxt_data_with_deltas, save_path = water_filedir, filename = "-".join([water_filename.split(".txt")[0], "with", delta_filename.split(".txt")[0] , "applied.txt"]))
           
    # print data
    if arguments.verbose: 
        waterapputils_viewer.print_watertxt_data(watertxt_data)  
        waterapputils_viewer.print_watertxt_data(watertxt_data_with_deltas)  

    # close error logging
    waterapputils_logging.remove_loggers()

#def apply_deltas_to_xml(file_list, arguments):
#    """    
#    Apply delta factors to a WATER *.xml file. The new file created is saved to the same
#    directory as the *.xml file.
#
#    Parameters
#    ----------
#    file_list : list 
#        List of files to parse, process, and plot.        
#    arguments : argparse object
#        An argparse object containing user options.                    
#    """
#    waterxml_file = file_list[0]
#    delta_file = file_list[1]
#                
#    water_filedir, water_filename = helpers.get_file_info(waterxml_file)
#    delta_filedir, delta_filename = helpers.get_file_info(delta_file)
#          
#    # initialize error logging
#    waterapputils_logging.initialize_loggers(output_dir = water_filedir)        
#    
#    # read data
#    waterxml_data = waterxml.read_file(waterxml_file)  
#    deltas_data = deltas.read_file(delta_file) 
#    
#    # calculate average deltas for a list of tiles
#    avg_delta_values = deltas.calculate_avg_delta_values(deltas_data = deltas_data, tile_list = ["31", "32"])
#
#    # apply deltas
#    for key, value in avg_delta_values.iteritems():
#        if key == "Ppt":
#            waterxml.apply_factors(waterxml_tree = waterxml_data, element = "ClimaticPrecipitationSeries", factors = avg_delta_values[key])
#        elif key == "Tmax":
#            waterxml.apply_factors(waterxml_tree = waterxml_data, element = "ClimaticTemperatureSeries", factors = avg_delta_values[key])
#
#    waterxml.write_file(waterxml_tree = waterxml_data, save_path = water_filedir, filename = "-".join([water_filename.split(".xml")[0], "with", delta_filename.split(".txt")[0] , "applied.xml"]))
#           
#    # print data
#    if arguments.verbose: 
#        waterapputils_viewer.print_watertxt_data(waterxml_data)  
#
#    # close error logging
#    waterapputils_logging.remove_loggers()

def _apply_deltas(waterxml_data, avg_deltas):


    import pdb
    pdb.set_trace()

    # apply deltas 
    for key, value in avg_deltas.iteritems():
        if key == "Ppt":
            waterxml_data = waterxml.apply_factors(waterxml_tree = waterxml_data, element = "ClimaticPrecipitationSeries", factors = avg_deltas[key])

        elif key == "Tmax":
            waterxml_data = waterxml.apply_factors(waterxml_tree = waterxml_data, element = "ClimaticTemperatureSeries", factors = avg_deltas[key])

    return waterxml_data

def apply_deltas_to_xml_series(files_dict, arguments):
    """    
    Apply delta factors to a WATER *.xml file. The new file created is saved to the same
    directory as the *.xml file.

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
                  "basin_shapefile": shapefile of WATER basin of interest; used in finding intersection with delta shapefile}    
    """
    # initialize error logging
    waterapputils_logging.initialize_loggers(output_dir = os.getcwd())
    
    # open shapefiles
    delta_shapefile = osgeo.ogr.Open(files_dict["delta_shapefile"]) 
    basin_shapefile = osgeo.ogr.Open(files_dict["basin_shapefile"]) 

    # find intersecting tiles based on water basin supplied
    intersecting_tiles = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = delta_shapefile, intersectee_field = "Tile")

    print("Intersecting tiles: {}".format(intersecting_tiles))        
    for featureid, tiles in intersecting_tiles.iteritems():                    
        print("FeatureId: {}".format(featureid))  
        print("Tiles: {}".format(tiles))  

        # get average values for a list of delta files
        avg_deltas = deltas.get_avg_deltas(delta_files = files_dict["delta_files"], tiles = tiles)  
        
        # get the xml data associated with the basin shapefile
#        root = Tkinter.Tk() 
#        waterxml_file = tkFileDialog.askopenfilename(title = "Select WATER XML File That Corresponds to Feature ID (FID): {}".format(featureid), filetypes = [("All files", ".*"), ("XML file","*.xml")])
#        root.destroy()       

        # get xml file information to use in writing new xml file            
#        waterxml_filedir, waterxml_filename = helpers.get_file_info(waterxml_file)
        waterxml_filedir, waterxml_filename = helpers.get_file_info("../data/waterxml-datafiles/WATERSimulation_1981_2011.xml")
        
        # read xml data
#        waterxml_tree = waterxml.read_file(waterxml_file)            
        waterxml_tree = waterxml.read_file("../data/waterxml-datafiles/WATERSimulation_1981_2011.xml")      
                   
        # apply deltas
        for key, value in avg_deltas.iteritems():
            if key == "Ppt":
                waterxml.apply_factors(waterxml_tree = waterxml_tree, element = "ClimaticPrecipitationSeries", factors = avg_deltas[key])

            elif key == "Tmax":
                waterxml.apply_factors(waterxml_tree = waterxml_tree, element = "ClimaticTemperatureSeries", factors = avg_deltas[key])

        # write updated xml                
        waterxml.write_file(waterxml_tree = waterxml_tree, save_path = waterxml_filedir, filename = "-".join([waterxml_filename.split(".xml")[0], "updated-for-FID", featureid, ".xml"]))
               
        # print data
        if arguments.verbose: 
            waterapputils_viewer.print_watertxt_data(waterxml_tree)  

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
            apply_deltas_to_txt(file_list = args.applydeltasdatatxt, arguments = args)
            sys.exit()

        elif args.applydeltasxml:
            apply_deltas_to_xml(file_list = args.applydeltasdataxml, arguments = args)
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
                          "delta_shapefile": "../data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp", 
                          "basin_shapefile": "../data/deltas-gcm/testbasin_proj_wgs/testbasin_multi_proj_wgs.shp"}
            
            apply_deltas_to_xml_series(files_dict = files_dict, arguments = args)
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

  
