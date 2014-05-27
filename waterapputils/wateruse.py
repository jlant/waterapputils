# -*- coding: utf-8 -*-
"""
:Module: wateruse.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading, writing, processing, and logging errors in water use text data files.
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

# my modules
import helpers

def read_file(filepath):
    """    
    Open WATER text file, create a file object for read_file_in(filestream) to process.
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
    with open(filepath, "r") as f:
        data = read_file_in(f)
        
    return data

def read_file_in(filestream):
    """    
    Read and process a WATER *.txt file. Finds any parameter and its respective data.
    
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
    expected = {
    
        "huc12": list of string ids,
    
        "newhydroid": list of string ids,
                
        "AqGwWL": list of float water use values,
        
        "CoGwWL": list of float water use values,

        ...
    }
    """
    
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file 
    patterns = {
        "months": "(#)\s([JFMASOND].+)\t(.+)",
        "column_names": "(huc12)\t(.+)",
        "data_row": "([0-9]{11})\t(.+)"
    }        

   # initialize a dictionary to hold all the data of interest
    initial_data = {"months": None, "column_names": None, "parameters": []}      
    
    # process file
    for line in data_file: 
        # find match
        match_months = re.search(pattern = patterns["months"], string = line)
        match_column_names = re.search(pattern = patterns["column_names"], string = line)
        match_data_row = re.search(pattern = patterns["data_row"], string = line)

        # if match is found add it to data dictionary
        if match_months:
            initial_data["months"] = match_months.group(2).strip()
            
        if match_column_names:
            initial_data["column_names"] = match_column_names.group(0).split("\t") 
            
            for name in initial_data["column_names"]:
                initial_data["parameters"].append({"name": name, "index": initial_data["column_names"].index(name), "data": []})
                
        if match_data_row:
            for parameter in initial_data["parameters"]:
                value = match_data_row.group(0).split("\t")[parameter["index"]] 
                parameter["data"].append(value)

    # format data into a dictionary; dynamically create keys with column names
    data = {"months": initial_data["months"]}
    string_columns = ["huc12", "newhydroid"]

    for parameter in initial_data["parameters"]:
        if parameter["name"] in string_columns:
            pass    # leave values as strings
        else:
            for i in range(len(parameter["data"])):     # ensure that value is a float
                value = helpers.convert_to_float(value = parameter["data"][i], helper_str = "parameter {}".format(parameter["name"]))                
                                       
                parameter["data"][i] = float(value)
        
        # populate data dictionary with clean data sets
        data[parameter["name"]] = parameter["data"]
            
    # return data
    return data
    
def _create_test_data():
    """ Create test data for tests """

    fixture = {} 
    
    fixture["data_file"] = \
        """
        # JFM_WU																								
        # released 2014, March 7																								
        huc12	newhydroid	AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL
        20401010101	256	2	5	2	5	-2
        20401010101	241	4	3	4	3	-4
        20401010101	222	6	4	6	4	-6
        20401010101	220	3	8	3	8	-8
        20401010101	12	1	3	1	3	-1
        20401010101	11	2	6	2	6	-1
        20401010102	8	2	1	2	1	-1
        """
    
    return fixture

def _print_test_info(actual, expected):
    """   
    For testing purposes, assert that all expected values and actual values match. 
    Prints assertion error when there is no match.  Prints values to user to scan
    if interested. Helps a lot for debugging. This function mirrors what is done
    in nosetests.
    
    Parameters
    ----------
    expected : dictionary  
        Dictionary holding expected data values
    actual : dictionary
        Dictionary holding expected data values
    """
    for key in actual.keys():
        np.testing.assert_equal(actual[key], expected[key], err_msg = "For key * {} *, actual value(s) * {} * do not equal expected value(s) * {} *".format(key, actual[key], expected[key]))        

        print("*{}*".format(key))                     
        print("    actual:   {}".format(actual[key]))  
        print("    expected: {}\n".format(expected[key]))

def test_read_file_in():
    """ Test read_file_in() """
    
    print("--- Testing read_file_in() ---")

    # expected values
    expected = {"months": "JFM_WU",
                "huc12": ["20401010101", "20401010101", "20401010101", "20401010101", "20401010101", "20401010101", "20401010102"],
                "newhydroid": ["256", "241", "222", "220", "12", "11", "8"],
                "AqGwWL": [2.0, 4.0, 6.0, 3.0, 1.0, 2.0, 2.0],
                "CoGwWL": [5.0, 3.0, 4.0, 8.0, 3.0, 6.0, 1.0],
                "DoGwWL": [2.0, 4.0, 6.0, 3.0, 1.0, 2.0, 2.0],
                "InGwWL": [5.0, 3.0, 4.0, 8.0, 3.0, 6.0, 1.0],
                "IrGwWL": [-2.0, -4.0, -6.0, -8.0, -1.0, -1.0, -1.0]
    }
    
    # create test data
    fixture = _create_test_data()
    fileobj = StringIO(fixture["data_file"])
    
    # read file object
    actual = read_file_in(fileobj)
    
    # print results
    _print_test_info(actual, expected)

def main():
    
    test_read_file_in()

if __name__ == "__main__":
    main()