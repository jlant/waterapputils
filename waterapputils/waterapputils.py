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
import pdb
# my modules
import helpers
import watertxt
import waterxml
import waterapputils_viewer
import waterapputils_logging
import deltas

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

        # print data
        if arguments.verbose: 
            waterapputils_viewer.print_watertxt_data(data)  

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

def apply_deltas(file_list, arguments):
    """    
    Apply delta factors to a WATER *.txt file

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
      
    # create output directory     
    outputdirpath = helpers.make_directory(path = water_filedir, directory_name = "-".join([water_filename.split(".txt")[0], "with", delta_filename.split(".txt")[0] , "applied", "output"]))      
    
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

    group.add_argument("-waterxml", "--waterxmlfiles", nargs = "+", help = "List WATER xml data file(s) to be processed")
    group.add_argument("-waterxmlfd", "--waterxmlfiledialog", action = "store_true", help = "Open a file dialog window to select WATER xml data file(s).")



    group.add_argument("-applydeltas", "--applydeltasdata", nargs = 2, help = "List WATER text data file followed by delta file to be applied.")

    parser.add_argument("-v", "--verbose", action = "store_true",  help = "Print general information about data file(s)")
    parser.add_argument("-p", "--showplot", action = "store_true",  help = "Show plots of parameters contained in data file(s)")
    args = parser.parse_args()  

    try:
        
        # get files from command line arguments and process
        if args.watertxtfiles:
            process_txt_files(file_list = args.watertxtfiles, arguments = args)
            sys.exit()
        
        # get files from file dialog and process
        elif args.watertxtfiledialog:
            root = Tkinter.Tk() 
            files = tkFileDialog.askopenfilenames(title = "Select WATER Text File(s)", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()          
            process_txt_files(file_list = root.tk.splitlist(files), arguments = args)
        
        elif args.watertxtcompare:
            process_txtcmp(file_list = args.watertxtcompare, arguments = args)

        if args.waterxmlfiles:
            process_xml_files(file_list = args.waterxmlfiles, arguments = args)
            sys.exit()
        
        # get files from file dialog and process
        elif args.waterxmlfiledialog:
            root = Tkinter.Tk() 
            files = tkFileDialog.askopenfilenames(title = "Select WATER XML File(s)", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy()          
            process_xml_files(file_list = root.tk.splitlist(files), arguments = args)

        elif args.applydeltasdata:
            apply_deltas(file_list = args.applydeltasdata, arguments = args)
                 
        # process file(s) using standard input
        else:
            data = watertxt.read_file_in(sys.stdin) 
            outputdirpath = helpers.make_directory(path = os.getcwd(), directory_name = args.outputdir)
            waterapputils_viewer.plot_data(data, is_visible = args.showplot, save_path = outputdirpath) 
                    
            if args.verbose: 
                waterapputils_viewer.print_info(data)
            
    except IOError as error:
        logging.exception("IO error: {0}".format(error.message))
        sys.exit(1)
        
    except ValueError as error:
        logging.exception("Value error: {0}".format(error.message))
        sys.exit(1)

    except IndexError as error:
        logging.exception("Index: {0}".format(error.message))
        sys.exit(1)
        
if __name__ == "__main__":
    main()    

  
