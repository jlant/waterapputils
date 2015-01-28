# -*- coding: utf-8 -*-
"""
:Module: waterapputils.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Main controller that handles user input options for processing WATER application simulations and output files
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
from modules import water_files_processing
from modules import wateruse_processing
from modules import gcm_delta_processing
from modules import specific_output_file_processing
from modules import map_processing
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

    group.add_argument("-applywateruse", "--applywateruse", action = "store_true", help = "Apply water use data to a WATER.txt file(s) for a WATER simulation.  Use user_settings.py to enter paths to data files.")
    group.add_argument("-applysubwateruse", "--applysubwateruse", action = "store_true", help = "Apply substitute water use data. Uses sub_wateruse_info_file_name variable in user_settings.py")

    group.add_argument("-applygcmdeltas", "--applygcmdeltas", action = "store_true", help = "Apply global climate deltas to a WATERSimulation.xml file for a WATER simulations.  Use user_settings.py to enter paths to data files.")
    group.add_argument("-applysubgcmdeltas", "--applysubgcmdeltas", action = "store_true", help = "Apply updated water deltas data. Uses sub_gcm_delta_info_file_name variable in user_settings.py ")

    group.add_argument("-oasis", "--oasis", nargs = "+", help = "List WATER text data file(s) that have Discharge + Water Use")
    group.add_argument("-ecoflowstationid", "--ecoflowstationid", nargs = "+", help = "List WATER text data file(s) that have Discharge + Water Use")
    group.add_argument("-ecoflowdaxml", "--ecoflowdaxml", nargs = "+", help = "List WATER xml data file(s)")
    group.add_argument("-ecoflowdashp", "--ecoflowdashp", nargs = "+", help = "List shapefile(s)")

    group.add_argument("-map", "--map", nargs = "+", help = "List shapefile(s) to plot on a map")
    group.add_argument("-mapsim", "--mapsim", action = "store_true",  help = "Create map of a WATER simulation. Specify settings in user_settings.py")

    parser.add_argument("-v", "--verbose", action = "store_true",  help = "Print general information about data file(s)")
    parser.add_argument("-outfilename", "--outfilename", nargs = 1,  help = "Write file name to write drainage area csv file.")  
    parser.add_argument("-labelfield", "--labelfield", nargs = 1,  help = "Write field name in shapefile to use in labeling drainagearea.csv")    
    parser.add_argument("-areafield", "--areafield", nargs = 1,  help = "Write area field name in shapefile to use in drainagearea.csv")
    parser.add_argument("-samplesingle", "--samplesingle", action = "store_true",  help = "Flag to use sample single batch settings user_settings.py") 
    parser.add_argument("-samplebatch", "--samplebatch", action = "store_true",  help = "Flag to use sample batch batch settings user_settings.py") 
    parser.add_argument("-simdir", "--simdir", nargs = 1,  help = "Flag to use a user supplied path to simulation directory instead of using simulation directory set in user_settings.py") 

    args = parser.parse_args()  

    # get files from command line arguments and process
    try:       

        # text file processing
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
        
        # xml file processing  
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

        # applying water use
        elif args.applywateruse:          

            print("\nProcessing wateruse ... please wait\n")

            if args.samplesingle:
                settings = user_settings.sample_single_settings
            elif args.samplebatch:
                settings = user_settings.sample_batch_settings
            elif args.simdir:
                settings = user_settings.settings
                settings["simulation_directory"] = args.simdir[0]
            else:
                settings = user_settings.settings                       

            wateruse_processing.apply_wateruse(settings = settings)

            sys.exit()

        elif args.applysubwateruse:

            print("\nProcessing sub wateruse ... please wait\n")  

            if args.samplesingle:
                settings = user_settings.sample_single_settings
            elif args.samplebatch:
                settings = user_settings.sample_batch_settings
            elif args.simdir:
                settings = user_settings.settings
                settings["simulation_directory"] = args.simdir[0]
            else:
                settings = user_settings.settings 

            wateruse_processing.apply_subwateruse(settings = settings)

            sys.exit()

        # writing specific outputs; oasis and ecoflow files
        elif args.oasis:

            if args.outfilename:
                oasis_file_name = args.outfilename[0]
            else:
                oasis_file_name = user_settings.settings["oasis_file_name"]
           
            specific_output_file_processing.write_oasis_file(file_list = args.oasis, dir_name = user_settings.settings["oasis_directory_name"], file_name = oasis_file_name)            
            
            sys.exit()

        elif args.ecoflowstationid:

            if args.outfilename:
                ecoflow_file_name = args.outfilename[0]
            else:
                ecoflow_file_name = user_settings.settings["ecoflow_file_name"]
           
            specific_output_file_processing.write_ecoflow_file_stationid(file_list = args.ecoflowstationid, dir_name = user_settings.settings["ecoflow_directory_name"], file_name = ecoflow_file_name)        
            
            sys.exit()

        elif args.ecoflowdaxml:

            if args.outfilename:
                da_file_name = args.outfilename[0]
            else:
                da_file_name = user_settings.settings["ecoflow_drainage_area_file_name"]

            specific_output_file_processing.write_ecoflow_file_drainageareaxml(file_list = args.ecoflowdaxml, dir_name = user_settings.settings["ecoflow_directory_name"], file_name = da_file_name)           
            
            sys.exit()

        elif args.ecoflowdashp:

            if args.outfilename:
                da_file_name = args.outfilename[0]
            else:
                da_file_name = user_settings.settings["ecoflow_drainage_area_file_name"]

            if args.labelfield:
                label_field = args.labelfield[0]
            else:
                label_field = ""           

            if args.areafield:
                area_field = args.areafield[0]
            else:
                area_field = ""  

            specific_output_file_processing.write_ecoflow_file_drainageareashp(file_list = args.ecoflowdashp, dir_name = user_settings.settings["ecoflow_directory_name"], 
                                                                               file_name = da_file_name, label_field = label_field, query_field = area_field,
            )

            sys.exit()

        # applying gcm deltas
        elif args.applygcmdeltas:

            print("\nProcessing gcm deltas ... please wait\n")  

            if args.samplesingle:
                settings = user_settings.sample_single_settings
            elif args.samplebatch:
                settings = user_settings.sample_batch_settings
            elif args.simdir:
                settings = user_settings.settings
                settings["simulation_directory"] = args.simdir[0]
            else:
                settings = user_settings.settings                       
           
            gcm_delta_processing.apply_gcm_deltas(settings = settings)

            sys.exit()


        elif args.applysubgcmdeltas:

            print("\nProcessing sub gcm deltas ... please wait\n")  

            if args.samplesingle:
                settings = user_settings.sample_single_settings
            elif args.samplebatch:
                settings = user_settings.sample_batch_settings
            elif args.simdir:
                settings = user_settings.settings
                settings["simulation_directory"] = args.simdir[0]
            else:
                settings = user_settings.settings 

            gcm_delta_processing.apply_sub_gcm_deltas(settings = settings)

            sys.exit()

        elif args.map:

            print("\nCreating map ... please wait\n")

            map_processing.create_map(files_list = args.map, settings = user_settings.settings, title = "A map!", is_visible = True)

            sys.exit()

        elif args.mapsim:

            print("\nCreating map ... please wait\n")

            if args.samplesingle:
                settings = user_settings.sample_single_settings
            elif args.samplebatch:
                settings = user_settings.sample_batch_settings
            else:
                settings = user_settings.settings 

            map_processing.create_simulation_map(settings = settings)

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

