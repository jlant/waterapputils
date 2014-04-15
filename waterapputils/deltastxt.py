# -*- coding: utf-8 -*-
"""
:Module: deltastxt.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading, processing, and logging errors in delta text files.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import re
import numpy as np
import datetime
import logging
from StringIO import StringIO
import os
import pdb
# my modules
import helpers

def read_file(filename):
    """    
    Open delta *.txt file, create a file object for read_file_in(filestream) to process.
    This function is responsible to opening the file, removing the file opening  
    responsibility from read_file_in(filestream) so that read_file_in(filestream)  
    can be unit tested.
    
    Parameters
    ----------
    filestream : file object
        A file object that contains an open data file.
        
    Returns
    -------
    data : dictionary 
        Returns a dictionary containing data found in data file. 

    See Also
    --------
    read_file_in : Read data file object 
    """
    
    filestream = open(filename, 'r')
    data = read_file_in(filestream)
    filestream.close()
    
    return data

def read_file_in(filestream):
    """    
    Read and process a delta *.txt file. Returns a dictionary with keys named
    as the column header names found in the file.        
        
    Parameters
    ----------
    filestream : file object
        A python file object that contains an open data file.
        
    Returns
    -------
    data : dictionary 
        Returns a dictionary containing data found in data file. 

    Notes
    -----          
    data = {
        
        'Model': string of model name,
        
        'Scenario': string of scenario name,
        
        'Target': string of scenario name,
        
        'Variable': string of variable name,
        
        'Tile': list of tile numbers,
        
        'January': array of delta values for each tile
        
        . . .
        
        'December': array of delta values for each tile
            
    }         
    """ 
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file
    patterns = {
        "column_names": "(Model.+)",
        "data_row": "(\w+)\t(\w+)\t(\d+)\t(.+)"
    }        

   # initialize a dictionary to hold all the data of interest
    initial_data = {
        "column_names": None,
        "parameters": []
    }      
    
    # process file
    for line in data_file:     
        match_column_names = re.search(pattern = patterns["column_names"], string = line)
        match_data_row = re.search(pattern = patterns["data_row"], string = line)
     
        # if match is found add it to data dictionary
        if match_column_names:
            initial_data["column_names"] = match_column_names.group(0).split("\t") 
            
            for name in initial_data["column_names"]:
                initial_data["parameters"].append({"name": name, "index": initial_data["column_names"].index(name), "data": []})
                
        if match_data_row:
            for parameter in initial_data["parameters"]:
                value = match_data_row.group(0).split("\t")[parameter["index"]] 
                parameter["data"].append(value)
                
                
    # format data into a dictionary; remove duplicate text values from certain column_names, and dynamically create keys with column names
    data = {}
    duplicate_value_columns = ["Model", "Scenario", "Target", "Variable"]
    
    for parameter in initial_data["parameters"]:
        if parameter["name"] in duplicate_value_columns:
            parameter["data"] = parameter["data"][0]                        # duplicate values, so just get first value
        elif parameter["name"] == "Tile":
            pass                                                            # leave Tile values as strings
        else:
            for i in range(len(parameter["data"])):                         # ensure that value is a float
                value = convert_to_float(value = parameter["data"][i], helper_str = "parameter {}".format(parameter["name"]))                
                                       
                parameter["data"][i] = float(value)
        
        # populate data dictionary with clean data sets
        data[parameter["name"]] = parameter["data"]
            
    # return data
    return data
       
def convert_to_float(value, helper_str = None):
    """   
    Convert a value to a float. If value is not a valid float, log as an error
    with a helper_str (i.e. value"s coorsponding date) to help locate the 
    error and replace value with a nan.
    
    Parameters
    ----------
    value : str
        String value to convert.
    helper_str : str
        String message to be placed in error log if value can not be converted to a float. i.e. value"s corresponding date of occurance.
        
    Returns
    -------
    value : {float, nan}
        Float or numpy nan value 
    """
    # remove any special characters present in string value
    value = helpers.rmspecialchars(value)    
    
    if helpers.isfloat(value):
        value = float(value)
    else:        
        if value == "":
            error_str = "*Missing value* {}. *Solution* - Replacing with NaN value".format(helper_str)
            logging.warn(error_str)
            value = np.nan

        else:
            error_str = "*Bad value* {}. *Solution* - Replacing with NaN value".format(helper_str)
            logging.warn(error_str)
            value = np.nan
            
    return value

def test_read_file_in():
    """ Test read_file_in() functionality"""

    print("--- Testing read_file_in() ---")

    fixture = {}
    
    fixture["data file"] = \
        """
        Model	Scenario	Target	Variable	Tile	January	February	March	April	May	June	July	August	September	October	November	December
        CanESM2	rcp45	2030	PET	11	1.1	2.7	3.1	4.7	5.1	6.7	7.1	8.7	9.1	10.7	11.1	12.7
        CanESM2	rcp45	2030	PET	12	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        CanESM2	rcp45	2030	PET	21	1.3	2.9	3.3	4.9	5.3	6.9	7.3	8.9	9.3	10.9	11.3	12.9
        CanESM2	rcp45	2030	PET	22	1.4	2.1	3.4	4.1	5.4	6.1	7.4	8.1	9.4	10.1	11.4	12.1
        CanESM2	rcp45	2030	PET	31	1.5	2.2	3.5	4.2	5.5	6.2	7.5	8.2	9.5	10.2	11.5	12.2
        CanESM2	rcp45	2030	PET	32	1.6	2.3	3.6	4.3	5.6	6.3	7.6	8.3	9.6	10.3	11.6	12.3
        """
        
    fileobj = StringIO(fixture["data file"])
    
    data = read_file_in(fileobj)

    print("*Number of keys in data*\n    actual")
    print("    17 : {}\n".format(len(data.keys())))

    print("*Keys in data*\n    actual")
    print("    {}\n".format(data.keys()))

    print("*Model*\n    expected : actual")
    print("    CanESM2 : {}\n".format(data["Model"]))

    print("*Scenario*\n    expected : actual")
    print("    rcp45 : {}\n".format(data["Scenario"]))

    print("*Target*\n    expected : actual")
    print("    2030 : {}\n".format(data["Target"]))

    print("*Tile*\n    expected : actual")
    print("    ['11', '12', '21', '22', '31', '32'] : {}\n".format(data["Tile"]))

    print("*January*\n    expected : actual")
    print("    [1.1, 1.2, 1.3, 1.4, 1.5, 1.6] : {}\n".format(data["January"]))

    print("*February*\n    expected : actual")
    print("    [2.7, 2.8, 2.9, 2.1, 2.2, 2.3] : {}\n".format(data["February"]))

    print("*March*\n    expected : actual")
    print("    [3.1, 3.2, 3.3, 3.4, 3.5, 3.6] : {}\n".format(data["March"]))

    print("*April*\n    expected : actual")
    print("    [4.7, 4.8, 4.9, 4.1, 4.2, 4.3] : {}\n".format(data["April"]))

    print("*May*\n    expected : actual")
    print("    [5.1, 5.2, 5.3, 5.4, 5.5, 5.6] : {}\n".format(data["May"]))   

    print("*June*\n    expected : actual")
    print("    [6.7, 6.8, 6.9, 6.1, 6.2, 6.3] : {}\n".format(data["June"]))   

    print("*July*\n    expected : actual")
    print("    [7.1, 7.2, 7.3, 7.4, 7.5, 7.6] : {}\n".format(data["July"]))   

    print("*August*\n    expected : actual")
    print("    [8.7, 8.8, 8.9, 8.1, 8.2, 8.3] : {}\n".format(data["August"]))   

    print("*September*\n    expected : actual")
    print("    [9.1, 9.2, 9.3, 9.4, 9.5, 9.6] : {}\n".format(data["September"]))   

    print("*October*\n    expected : actual")
    print("    [10.7, 10.8, 10.9, 10.1, 10.2, 10.3] : {}\n".format(data["October"]))   

    print("*November*\n    expected : actual")
    print("    [11.1, 11.2, 11.3, 11.4, 11.5, 11.6] : {}\n".format(data["November"]))   

    print("*December*\n    expected : actual")
    print("    [12.7, 12.8, 12.9, 12.1, 12.2, 12.3] : {}\n".format(data["December"]))   

    print("")

def main():
    """ Test functionality of reading files """

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_read_file_in()

    
if __name__ == "__main__":
    main()