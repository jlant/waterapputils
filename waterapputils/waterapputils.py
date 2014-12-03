# -*- coding: utf-8 -*-
"""
:Module: waterapputils.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Main controller that handles user input options for processing WATER application output files
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

# my modules
import water_files_processing
import wateruse_processing
import specific_output_file_processing
import user_settings


def main():  
    """
    Run program based on user input arguments. Program will automatically process file(s) supplied,
    log any errors found in the data file, and will save plots of every parameter. Error log and plots are saved to 
    a directory (tagged with "output") at the same level as the supplied or downloaded data files.
    """    
    # parse arguments from command line
    parser = argparse.ArgumentParser(description = "Read, process, log errors, print, and plot data from WATER capplication output data files.") 
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-watertxt", "--watertxtfiles", nargs = "+", help = "List WATER text data file(s) to be processed")
    group.add_argument("-watertxtfd", "--watertxtfiledialog", action = "store_true", help = "Open a file dialog window to select WATER text data file(s).")
    group.add_argument("-watertxtcmp", "--watertxtcompare", nargs = 2, help = "List 2 WATER text data file(s) to be compared")
    group.add_argument("-watertxtcmpfd", "--watertxtcomparefiledialog", action = "store_true", help = "Open 2 separate file dialog windows to select WATER text data file(s) to be compared")

    group.add_argument("-waterxml", "--waterxmlfiles", nargs = "+", help = "List WATER xml data file(s) to be processed")
    group.add_argument("-waterxmlfd", "--waterxmlfiledialog", action = "store_true", help = "Open a file dialog window to select WATER xml data file(s).")
    group.add_argument("-waterxmlcmp", "--waterxmlcompare", nargs = 2, help = "List 2 WATER xml data file(s) to be compared")
    group.add_argument("-waterxmlcmpfd", "--waterxmlcomparefiledialog", action = "store_true", help = "Open 2 separate file dialog windows to select WATER XML data file(s) to be compared")

    group.add_argument("-applywateruse", "--applywateruse", action = "store_true", help = "Apply water use data to a WATER.txt file for a WATER simulation.  Use wateruse_batch_variables.py to enter paths to data files.")

    group.add_argument("-applydeltas", "--applydeltas", action = "store_true", help = "Apply global climate deltas to a WATERSimulation.xml file for a WATER simulations.  Use waterdelta_batch_variables.py to enter paths to data files.")

    group.add_argument("-applysubwateruse", "--applysubwateruse", action = "store_true", help = "Apply updated water use data from '_non_intersecting_basin_centroids.txt' to a WATER.txt file for a WATER simulation.  Use wateruse_batch_variables.py to enter paths to data files.")

    group.add_argument("-applysubdeltas", "--applysubdeltas", action = "store_true", help = "Apply updated water deltas data from '_non_intersecting_basin_tiles.txt' to a WaterSimulation.xml file for a WATER simulation.  Use wateruse_deltas_variables.py to enter paths to data files.")

    group.add_argument("-oasis", "--oasis", nargs = "+", help = "List WATER text data file(s) that have Discharge + Water Use")
    group.add_argument("-ecoflowstationid", "--ecoflowstationid", nargs = "+", help = "List WATER text data file(s) that have Discharge + Water Use")
    group.add_argument("-ecoflowdrainageareaxml", "--ecoflowdrainageareaxml", nargs = "+", help = "List WATER xml data file(s)")
    group.add_argument("-ecoflowdrainageareashp", "--ecoflowdrainageareashp", nargs = "+", help = "List shapefiles(s)")

    parser.add_argument("-v", "--verbose", action = "store_true",  help = "Print general information about data file(s)")
    parser.add_argument("-labelfield", "--labelfield", nargs = 1,  help = "Write field name in shapefile to use in labeling drainageare.csv")    
    parser.add_argument("-areafield", "--areafield", nargs = 1,  help = "Write area field name in shapefile to use in drainageare.csv") 

    args = parser.parse_args()  

    # get files from command line arguments and process
    try:       

        if args.watertxtfiles:
            
            water_files_processing.process_water_files(file_list = args.watertxtfiles, settings = user_settings.settings, print_data = args.verbose)            
            
            sys.exit()
        
        elif args.watertxtfiledialog:
            
            root = Tkinter.Tk() 
            files = tkFileDialog.askopenfilenames(title = "Select WATER Text File(s)", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()      
            
            water_files_processing.process_water_files(file_list = root.tk.splitlist(files), settings = user_settings.settings, print_data = args.verbose)    
            
            sys.exit()

        elif args.watertxtcompare:
            
            water_files_processing.process_cmp(file_list = args.watertxtcompare, settings = user_settings.settings, print_data = args.verbose)               
            
            sys.exit()

        elif args.watertxtcomparefiledialog:
            
            root = Tkinter.Tk() 
            file1 = tkFileDialog.askopenfilename(title = "Select First WATER Text File To Use In Comparision", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()          

            root = Tkinter.Tk() 
            file2 = tkFileDialog.askopenfilename(title = "Select Second WATER Text File To Use In Comparision", filetypes = [("Text file","*.txt"), ("All files", ".*")])
            root.destroy()
            
            water_files_processing.process_cmp(file_list = [file1, file2], settings = user_settings.settings, print_data = args.verbose)   
            
            sys.exit()
            
        # ---------------------------------------------------------------------
        elif args.waterxmlfiles:
            
            water_files_processing.process_water_files(file_list = args.waterxmlfiles, settings = user_settings.settings, print_data = args.verbose)        
                     
            sys.exit()
        
        elif args.waterxmlfiledialog:
            root = Tkinter.Tk() 
            files = tkFileDialog.askopenfilenames(title = "Select WATER XML File(s)", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy() 

            water_files_processing.process_water_files(file_list = root.tk.splitlist(files), settings = user_settings.settings, print_data = args.verbose)              

            sys.exit()

        elif args.waterxmlcompare:

            water_files_processing.process_cmp(file_list = args.waterxmlcompare, settings = user_settings.settings, print_data = args.verbose)   
            
            sys.exit()

        elif args.waterxmlcomparefiledialog:
            root = Tkinter.Tk() 
            file1 = tkFileDialog.askopenfilename(title = "Select First WATER XML File To Use In Comparision", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy()          

            root = Tkinter.Tk() 
            file2 = tkFileDialog.askopenfilename(title = "Select Second WATER XML File To Use In Comparision", filetypes = [("XML file","*.xml"), ("All files", ".*")])
            root.destroy()
            
            water_files_processing.process_cmp(file_list = [file1, file2], settings = user_settings.settings, print_data = args.verbose)   
            
            sys.exit()

        # --------------------------------------------------------------------

        elif args.applywateruse:          

            print("\nProcessing wateruse ... please wait\n")                       

            wateruse_processing.apply_wateruse(settings = user_settings.settings)

            sys.exit()

        elif args.applysubwateruse:

            print("\nProcessing sub wateruse ... please wait\n")  

            wateruse_processing.apply_subwateruse(settings = user_settings.settings)

            sys.exit()

        # elif args.applydeltas:

        #     print("\nProcessing gcm deltas ... please wait\n")                                   
        #     apply_deltas_to_xml_files(files_dict = files_dict, arguments = args)
        #     sys.exit() 

        # elif args.applysubdeltas:

            
        #     apply_subwaterdeltas_to_xml_files(files_dict = files_dict, arguments = args)

        #     sys.exit()

        # ---------------------------------------------------------------------

        elif args.oasis:
           
            specific_output_file_processing.write_oasis_file(file_list = args.oasis, dir_name = user_settings.settings["oasis_directory_name"], file_name = user_settings.settings["oasis_file_name"])            
            
            sys.exit()

        elif args.ecoflowstationid:
           
            specific_output_file_processing.write_ecoflow_file_stationid(file_list = args.ecoflowstationid, dir_name = user_settings.settings["ecoflow_directory_name"], file_name = user_settings.settings["ecoflow_file_name"])        
            
            sys.exit()

        elif args.ecoflowdrainageareaxml:
           
            specific_output_file_processing.write_ecoflow_file_drainageareaxml(file_list = args.ecoflowdrainageareaxml, dir_name = user_settings.settings["ecoflow_directory_name"], file_name = user_settings.settings["ecoflow_drainage_area_file_name"])           
            
            sys.exit()

        elif args.ecoflowdrainageareashp:

            specific_output_file_processing.write_ecoflow_file_drainageareashp(file_list = args.ecoflowdrainageareashp, 
                                                                               dir_name = user_settings.settings["ecoflow_directory_name"], 
                                                                               file_name = user_settings.settings["ecoflow_drainage_area_file_name"], 
                                                                               label_field = user_settings.settings["basin_shapefile_id_field"], 
                                                                               query_field = user_settings.settings["basin_shapefile_area_field"],
            )

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

