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

def read_file(filepath, factor_file = None):
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
        if factor_file:
            data = read_factor_file_in(f)
        else:
            data = read_file_in(f)            
        
    return data

def read_file_in(filestream):
    """    
    Read and process a water use *.txt file. Finds any parameter and its respective data.
    
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
        "months": "(#)\s([JFMASOND].+)",
        "units": "(#)\s(Units:)(.+)",
        "column_names": "(huc12)\t(.+)",
        "data_row": "(^[0-9]{,11})\t(.+)"
    }  

   # initialize a temporary dictionary to hold data of interest
    initial_data = {"months": None, "units": None, "column_names": None, "parameters": []}      
    
    # process file
    for line in data_file: 
        line = line.strip()
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

def read_factor_file_in(filestream):
    """    
    Read and process a water use factor *.txt file. Finds any parameter and its respective data.
    
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
                
        "AqGwWL": float water use factor value,
        
        "CoGwWL": float water use factor value,

        ...
    }
    """
    
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file 
    patterns = {
        "column_names": "(^[aA-zZ].+)",
        "data_row": "(^[0-9].+)"
    }  

   # initialize a temporary dictionary to hold data of interest
    initial_data = {"column_names": None, "parameters": []}      
    
    # process file
    for line in data_file: 
        line = line.strip()
        # find match
        match_column_names = re.search(pattern = patterns["column_names"], string = line)
        match_data_row = re.search(pattern = patterns["data_row"], string = line)

        # if match is found add it to data dictionary            
        if match_column_names:
            initial_data["column_names"] = match_column_names.group(0).split("\t") 
            
            for name in initial_data["column_names"]:
                initial_data["parameters"].append({"name": name, "index": initial_data["column_names"].index(name), "data": None})

        if match_data_row:
            for parameter in initial_data["parameters"]:
                value = match_data_row.group(0).split("\t")[parameter["index"]] 
                parameter["data"] = value

    # format data into a dictionary; dynamically create keys with column names
    data = {"column_names": initial_data["column_names"]}

    for parameter in initial_data["parameters"]:
        # ensure that value is a float
        value = helpers.convert_to_float(value = parameter["data"], helper_str = "parameter {}".format(parameter["name"]))                
                                   
        parameter["data"] = float(value)
        
        # populate data dictionary with clean data sets
        data[parameter["name"]] = parameter["data"]
            
    # return data
    return data

def get_wateruse_values(wateruse_data, id_list, wateruse_factors = None):
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
    values : list
        List containing lists of water use values for each id in id_list; shape is m x n where m is the number of water use values and n is number of ids in id_list   
    
    Notes
    -----
    values = [[  1.3   2.7   3.3   4.7   5.3   6.7   7.3   8.7   9.3  10.7  11.3  12.7]
              [  1.2   2.8   3.2   4.8   5.2   6.8   7.2   8.8   9.2  10.8  11.2  12.8]]
    """
    # get all water use types from column names
    wateruse_types = []
    for name in wateruse_data["column_names"]:
        if name not in ["huc12", "newhydroid"]:
            wateruse_types.append(name)

    # make sure that wateruse_factors have same keys as wateruse types from wateruse_data
    assert wateruse_factors["column_names"] == wateruse_types, "Water use column names {} do not equal water use types {}".format(wateruse_factors.keys(), wateruse_types)
    
    # put all values into a list of lists; apply water use factors if they exist    
    values = []
    for id_num in id_list:
        if id_num in wateruse_data["newhydroid"]:
            wateruse_type_values = []
            id_index = wateruse_data["newhydroid"].index(id_num)
            for wateruse_type in wateruse_types:
                if wateruse_factors:
                    value = wateruse_data[wateruse_type][id_index] * wateruse_factors[wateruse_type]
                else:
                    value = wateruse_data[wateruse_type][id_index]
                        
                wateruse_type_values.append(value)
                
            values.append(wateruse_type_values)

        else: 
            logging.warn("Id number {} is not in wateruse_data.".format(id_num)) 

    return values


def sum_values(values):
    """   
    Sum values row-wise, column-wise, and absolute total. Return dictionary containing
    each sum.
    
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
    
def create_monthly_wateruse_dict(wateruse_data, wateruse_value):
    """   
    Create monthly wateruse dictionary according to the months in the wateruse_data
    
    Parameters
    ----------
    wateruse_data : dictionary
        Dictionary containing wateruse data from wateruse file
        
    Returns
    -------
    monthly_wateruse_dict : dictionary 
        Dictionary filled with data from wateruse_value for particular months specified by months in wateruse_data
        
    Notes
    -----          
    monthly_wateruse_dict = {
    
        "January": 5.0,

        "February": 5.0,

        "March": 5.0
    }        
    """
    wateruse_month_conversion = {"JFM": ["January", "February", "March"],
                                 "AMJ": ["April", "May", "June"],
                                 "JAS": ["July", "August", "September"],
                                 "OND": ["October", "November", "December"]
    }    

    # create an empty dictionary that will have monthly keys and values corresponding to the summed wateruse
    monthly_wateruse_dict = {}
    
    # loop through month conversion, if the key matches months in wateruse_data, then fill monthly_dict with values    
    for key, values in wateruse_month_conversion.iteritems():
        if key in wateruse_data["months"]:
            for month in values:
                monthly_wateruse_dict[month] = wateruse_value

    return monthly_wateruse_dict

def convert_wateruse_units(value):
    """   
    Convert values from a mega gallons to cubic feet per second
    
    Parameters
    ----------
    value : float
        Float value in mega gallons per day
        
    Returns
    -------
    converted_value: float
        Float value in cubic feet per second    
    """    
    # 1 Mgal / 1 day * 10**6 gal / 1 Mgal * 0.133681 ft**3 / 1 gal * 1 day / 24 hours * 1 hour / 3600 seconds
    conversion_factor = ((10**6. * 0.133681) / (24 * 3600)) 
    
    converted_value = value * conversion_factor

    return converted_value
    
def get_total_wateruse(wateruse_data, id_list, wateruse_factors = None):
    """   
    Return a dictionary with monthly keys containing the total wateruse for a specific list of ids
    
    Parameters
    ----------
    wateruse_data : dictionary 
        Dictionary containing wateruse data from wateruse file.
        
    Returns
    -------
    total_wateruse_dict : dictionary 
        Dictionary filled with data from wateruse_value for particular months specified by months in wateruse_data

    Notes
    -----          
    total_wateruse_dict = {
    
        "January": 5.0,

        "February": 5.0,

        "March": 5.0
    }   
    """ 
    # check that each id in id list is contained in the wateruse_data     
    for id_num in id_list:
        if id_num not in wateruse_data["newhydroid"]:
            raise ValueError, "newhydroid {} is not contined in wateruse_data".format(id_num)
  
    # get wateruse values that correspond to a list of ids
    values = get_wateruse_values(wateruse_data, id_list = id_list, wateruse_factor = wateruse_factors) 

    # calculate the sums of the wateruse values along different axes
    sums = sum_values(values)
    
    # fill sum_wateruse_dict with total water use
    total_wateruse_dict = create_monthly_wateruse_dict(wateruse_data, wateruse_value = sums["total"])

    return total_wateruse_dict   
    
def get_all_total_wateruse(wateruse_files, id_list, wateruse_factor_file = None, in_cfs = False):
    """    
    Get all total water use values for a list of specific id values. 
    The base unit in the water use data file is mega gallons per day (Mgal/day) .
    Can convert to cubic feet per second (cfs) using in_cubic_feet_per_sec flag.
    
    Parameters
    ----------
    wateruse_files : list
        List of water use files to calculate the sum of all water use values 
    ids : list
        List of ids values.
    in_cfs : boolean
        Boolean flag to convert units from Mgal to cfs 
    See Also
    --------
    get_total_wateruse()
    """
    # calculate average values for a list of water use files
    all_total_wateruse_dict = {}
    for wateruse_file in wateruse_files:

        # read the water use file
        wateruse_data = read_file(wateruse_file) 
        
        if wateruse_factor_file:
            # read water use factor file
            wateruse_factors = read_file(wateruse_factor_file, factor_file = True)
        
        # calculate average wateruse for a list of ids
        total_wateruse_dict = get_total_wateruse(wateruse_data = wateruse_data, id_list = id_list, wateruse_factors = wateruse_factors)

        # convert values to cfs
        if in_cfs:
            for key, value in total_wateruse_dict.iteritems():
                value_cfs = convert_wateruse_units(value)
                total_wateruse_dict[key] = value_cfs
        
        # update dictionary 
        all_total_wateruse_dict.update(total_wateruse_dict)   
    
    return all_total_wateruse_dict
  
def _create_test_data():
    """ Create test data for tests """

    fixture = {} 
    
    fixture["data_file_JFM"] = \
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

    fixture["factor_file"] = \
        """
        # water use factors																									
        AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL
        2	2	2	2	2
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

    fixture["ids_256_241_222_220_values"] = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    fixture["ids_12_11_8_values"] = [[1.0, 3.0, 1.0, 3.0, -1.0], [2.0, 6.0, 2.0, 6.0, -1.0], [2.0, 1.0, 2.0, 1.0, -1.0]]
    
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
    fileobj = StringIO(fixture["data_file_JFM"])
    
    # read file object
    actual = read_file_in(fileobj)
    
    # print results
    _print_test_info(actual, expected)

def test_read_factor_file_in():
    """ Test read_factor_file_in() """
    
    print("--- Testing read_factor_file_in() ---")

    # expected values
    expected = {"column_names": ["AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL"],
                "AqGwWL": 2.0,
                "CoGwWL": 2.0,
                "DoGwWL": 2.0,
                "InGwWL": 2.0,
                "IrGwWL": 2.0
    }
    
    # create test data
    fixture = _create_test_data()
    fileobj = StringIO(fixture["factor_file"])
    
    # read file object
    actual = read_factor_file_in(fileobj)
   
    # print results
    _print_test_info(actual, expected)

def main():

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_read_file_in()
    
    test_read_factor_file_in()
    
if __name__ == "__main__":
    main()