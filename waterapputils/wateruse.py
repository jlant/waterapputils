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
    
b        "huc12": list of string ids,
    
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
        "months": "(#)\s([JFMASOND].+)",
        "units": "(#)\s(Units:)(.+)",
        "column_names": "(huc12)\t(.+)",
        "data_row": "([0-9]{11})\t(.+)"
    }        

   # initialize a temporary dictionary to hold data of interest
    initial_data = {"months": None, "units": None, "column_names": None, "parameters": []}      
    
    # process file
    for line in data_file: 
        # find match
        match_months = re.search(pattern = patterns["months"], string = line)
        match_units = re.search(pattern = patterns["units"], string = line)
        match_column_names = re.search(pattern = patterns["column_names"], string = line)
        match_data_row = re.search(pattern = patterns["data_row"], string = line)

        # if match is found add it to data dictionary
        if match_months:
            initial_data["months"] = match_months.group(2).strip()

        if match_units:
            initial_data["units"] = match_units.group(3).strip()
            
        if match_column_names:
            initial_data["column_names"] = match_column_names.group(0).split("\t") 
            
            for name in initial_data["column_names"]:
                initial_data["parameters"].append({"name": name, "index": initial_data["column_names"].index(name), "data": []})
                
        if match_data_row:
            for parameter in initial_data["parameters"]:
                value = match_data_row.group(0).split("\t")[parameter["index"]] 
                parameter["data"].append(value)

    # format data into a dictionary; dynamically create keys with column names
    data = {"months": initial_data["months"], "units": initial_data["units"], "column_names": initial_data["column_names"]}
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

def get_wateruse_values(wateruse_data, id_list):
    """   
    Get water use values based on id(s) of interest.
    
    Parameters
    ----------
    wateruse_data : list 
        List of dictionaries holding data from many water use data files
    id_list : list
        List of string id values
        
    Returns
    -------
    values: list
        List containing lists of water use values for each id in id_list; shape is m x n where m is the number of water use values and n is number of ids in id_list   
    
    Notes
    -----
    values = [[  1.3   2.7   3.3   4.7   5.3   6.7   7.3   8.7   9.3  10.7  11.3  12.7]
              [  1.2   2.8   3.2   4.8   5.2   6.8   7.2   8.8   9.2  10.8  11.2  12.8]]
    """
    # get water use types of interest; 
#    wateruse_types = ["AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL", "LvGwWL", "MiGwWL", "ReGwWL", "TeGwWL", "WsGwWL", "AqSwWL", "CoSwWL", "InSwWL", "IrSwWL", "MiSwWL", "TeSwWL", "WsSwWL", "InGwRT", "InSwRT", "STswRT", "WSgwRT", "WSunkTR", "WStrans"]   
    wateruse_types = []
    for name in wateruse_data["column_names"]:
        if name not in ["huc12", "newhydroid"]:
            wateruse_types.append(name)
    
    # put all values into a list of lists    
    values = []
    for id_num in id_list:
        if id_num in wateruse_data["newhydroid"]:
            wateruse_type_values = []
            id_index = wateruse_data["newhydroid"].index(id_num)
            for wateruse_type in wateruse_types:
                value = wateruse_data[wateruse_type][id_index]
                wateruse_type_values.append(value)
                
            values.append(wateruse_type_values)

        else: 
            logging.warn("Id number {} is not in wateruse_data.".format(id_num)) 

    return values

def sum_values(values):
    """   
    Get water use values based on id(s) of interest.
    
    Parameters
    ----------
    values: list
        List containing lists of values
        
    Returns
    -------
    sums: dictionary
        Dictionary containing row-wise, column-wise, and total sums
    """
    assert np.rank(values) == 2, "Rank (dimensions) of values {} is not equal to 2".format(values)
    
    sums = {"row_wise": np.sum(values, axis = 0),
            "column_wise": np.sum(values, axis = 1),
            "total": np.sum(values)}

    return sums
    
    
def calculate_sum_wateruse_values(wateruse_data, id_list):
    """   
    Get summed wateruse data values for a specific list of ids.
    
    Parameters
    ----------
    wateruse_data : list 
        List of dictionaries holding data from wateruse data files.
        
    Returns
    -------
    sum_wateruse_values : dictionary 
        Dictionary keys corresponding to delta variable type (i.e. precipitation (Ppt)) holding averaged data values for a specific list of tiles.
        
    Notes
    -----          
    sum_wateruse_values = {
        "January": 2.0,
        "February": 0.98,
        "March": 0.97,
        "April": 1.04,
        "May": 1.10,
        "June": 0.99,
        "July": 0.87,
        "August": 0.75,
        "September": 0.95,
        "October": 0.98,
        "November": 1.10,
        "December": 2.0
    }         
    """ 
    # check that each id in id list is contained in the wateruse_data     
    for id_num in id_list:
        if id_num not in wateruse_data["newhydroid"]:
            raise ValueError, "newhydroid {} is not contined in wateruse_data".format(id_num)
  
    # initialize avg_delta_values with keys corresponding to variable type  
    sum_wateruse_values = helpers.create_monthly_dict()
    
    # get wateruse values that correspond to a list of ids
    values = get_wateruse_values(wateruse_data, id_list = id_list)    
    
    
    # compute sum of wateruse values for each month and put it in sum_wateruse_values

       
    return sum_wateruse_values   

def get_sum_wateruse(wateruse_files, ids):
    """    
    Get all summed water use values for a list of specific id values.

    Parameters
    ----------
    wateruse_files : list
        List of water use files to calculate the sum of all water use values 
    ids : list
        List of ids values.
    
    See Also
    --------
    calculate_sum_wateruse_values()
    """
    # calculate average values for a list of water use files
    sum_wateruse = {}
    for wateruse_file in wateruse_files:
        
        # read the delta file
        wateruse_data = read_file(wateruse_file) 
                
        # calculate average wateruse for a list of ids
        sum_wateruse_values = calculate_sum_wateruse_values(wateruse_data = wateruse_data, id_list = ids)
        
        # update avgerage delta values dictionary 
        sum_wateruse.update(sum_wateruse_values)   
    
    return sum_wateruse






    
def _create_test_data():
    """ Create test data for tests """

    fixture = {} 
    
    fixture["data_file"] = \
        """
        # JFM_WU	
        # Units: Mgal/day																							
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

    fixture["wateruse_data"] = {"months": "JFM_WU", 
                                "units": "Mgal/day",
                                "column_names": ["huc12", "newhydroid", "AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL"],
                                "huc12": ["20401010101", "20401010101", "20401010101", "20401010101", "20401010101", "20401010101", "20401010102"],
                                "newhydroid": ["256", "241", "222", "220", "12", "11", "8"],
                                "AqGwWL": [2.0, 4.0, 6.0, 3.0, 1.0, 2.0, 2.0],
                                "CoGwWL": [5.0, 3.0, 4.0, 8.0, 3.0, 6.0, 1.0],
                                "DoGwWL": [2.0, 4.0, 6.0, 3.0, 1.0, 2.0, 2.0],
                                "InGwWL": [5.0, 3.0, 4.0, 8.0, 3.0, 6.0, 1.0],
                                "IrGwWL": [-2.0, -4.0, -6.0, -8.0, -1.0, -1.0, -1.0]
    }


    fixture["values_data"] = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    
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
                "units": "Mgal/day",
                "column_names": ["huc12", "newhydroid", "AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL"],
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

def test_get_wateruse_values():
    """ Test get_wateruse_values() """

    print("--- Testing get_wateruse_values() for different id lists ---")
    
    # expected values to test with actual values
    expected = {}    
    expected["ids_256_241_222_220"] = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    expected["ids_12_11_8"] = [[1.0, 3.0, 1.0, 3.0, -1.0], [2.0, 6.0, 2.0, 6.0, -1.0], [2.0, 1.0, 2.0, 1.0, -1.0]]

    fixture = _create_test_data()
    
    actual = {}
    actual["ids_256_241_222_220"] = get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"])
    actual["ids_12_11_8"] = get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"])

    # print results
    _print_test_info(actual, expected)

def test_sum_wateruse_values():
    """ Test sum_wateruse_values() """

    print("--- Testing sum_wateruse_values() ---")
    
    # expected values to test with actual values
    expected = {}    
    expected["row_wise"] = np.array([ 15.,  20.,  15.,  20., -20.])
    expected["column_wise"] = np.array([ 12.,  10.,  14.,  14.])
    expected["total"] = 50.0

    # create test data
    fixture = _create_test_data()

    # actual values       
    actual = sum_wateruse_values(values = fixture["values_data"])  

    # print results
    _print_test_info(actual, expected)    


def test_format_to_monthly_dict():
    """ Test format_to_monthly_dict() """

    print("--- Testing format_to_monthly_dict() ---")

    expected1 = {'January': [1.1], 'February': [2.2], 'March': [3.3], 'April': [4.4], 'May': [5.5], 'June': [6.6], 'July': [7.7], 'August': [8.8], 'September': [9.9], 'October': [10.0], 'November': [11.1], 'December': [12.2]}
    expected2 = {'January': [1.1, 1.9], 'February': [2.2, 2.8], 'March': [3.3, 3.7], 'April': [4.4, 4.6], 'May': [5.5, 5.5], 'June': [6.6, 6.4], 'July': [7.7, 7.3], 'August': [8.8, 8.2], 'September': [9.9, 9.1], 'October': [10.0, 10.0], 'November': [11.1, 11.9], 'December': [12.2, 12.8]}    

    values1 = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    values2 = [[1.0, 3.0, 1.0, 3.0, -1.0], [2.0, 6.0, 2.0, 6.0, -1.0], [2.0, 1.0, 2.0, 1.0, -1.0]]
    
    actual1 = format_to_monthly_dict(values1)
    actual2 = format_to_monthly_dict(values2)
    
    # print results
    _print_test_info(actual1, expected1)
    _print_test_info(actual2, expected2)

def main():

    print("")
    print("RUNNING TESTS ...")
    print("")
    
    test_read_file_in()

    test_get_wateruse_values()

    test_sum_wateruse_values()

if __name__ == "__main__":
    main()