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
import waterapputils_viewer
import waterapputils_logging

def process_txt_files(file_list, arguments):
    """    
    Process a list of WATER text files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list of str
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

def process_txtcmp(file_list, arguments):
    """    
    Compare two WATER text files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list of str
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
    group.add_argument("-watertxtcmp", "--watertxtcmp", nargs = 2, help = "List 2 WATER text data file(s) to be compared")

    group.add_argument("-deltastxt", "--txtfiles", nargs = "+", help = "List WATER text data file(s) to be processed")
    group.add_argument("-deltastxtfd", "--txtfiledialog", action = "store_true", help = "Open a file dialog window to select WATER text data file(s).")


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
        
        if args.watertxtcmp:
            process_txtcmp(file_list = args.txtcmp, arguments = args)
                 
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

  
