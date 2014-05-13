# -*- coding: utf-8 -*-
"""
:Module: deltas.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading, processing, and logging errors in delta text files.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import re
import numpy as np
import logging
from StringIO import StringIO
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
    
    filestream = open(filename, "r")
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
        
        "Model": string of model name,
        
        "Scenario": string of scenario name,
        
        "Target": string of scenario name,
        
        "Variable": string of variable name,
        
        "Tile": list of tile numbers,
        
        "January": array of delta values for each tile
        
        . . .
        
        "December": array of delta values for each tile
            
    }         
    """ 
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file
    patterns = {
        "column_names": "(Model.+)",
        "data_row": "([a-zA-z0-9-]+)\t(\w+)\t(\d+)\t(.+)"
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
                value = helpers.convert_to_float(value = parameter["data"][i], helper_str = "parameter {}".format(parameter["name"]))                
                                       
                parameter["data"][i] = float(value)
        
        # populate data dictionary with clean data sets
        data[parameter["name"]] = parameter["data"]
            
    # return data
    return data
       
def get_monthly_values(delta_data, tile_list):
    """   
    Get monthly values based on tile(s) of interest.
    
    Parameters
    ----------
    delta_data : list 
        List of dictionaries holding data from many delta data files
    tile_list : list
        List of string tile values
        
    Returns
    -------
    values: list
        List containing lists of monthly values; shape is n x 12 where n is number of tiles in tile_list   
    
    Notes
    -----
    values = [[  1.3   2.7   3.3   4.7   5.3   6.7   7.3   8.7   9.3  10.7  11.3  12.7]
              [  1.2   2.8   3.2   4.8   5.2   6.8   7.2   8.8   9.2  10.8  11.2  12.8]]
    """
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]       
    values = []
    for tile in tile_list:
        if tile in delta_data["Tile"]:
            monthly_values = []
            tile_index = delta_data["Tile"].index(tile)
            for month in month_list:
                value = delta_data[month][tile_index]
                monthly_values.append(value)
                
            values.append(monthly_values)

        else: 
            logging.warn("{} tile is not in the tile list contained in delta_data.".format(tile)) 

    return values
    
def format_to_monthly_dict(values):
    """
    Format array of values into a dictionary with monthly keys.
    
    Parameters
    ----------
    values: list
        List containing lists of monthly values; shape is n x 12 
        
    Returns
    -------
    values_dict : dictionary
        Dictionary containing monthly keys with corresponding values.
    
    Notes
    -----
    {"January": [2.0, 1.0],
     "February": [0.98, 0.99],
     "March": [0.97, 1.10],
     "April": [1.04, 1.02],
     "May": [1.10, 0.99],
     "June": [0.99, 0.98],
     "July": [0.87, 0.75],
     "August": [0.75, 0.95],
     "September": [0.95, 0.9],
     "October": [0.98, 0.8],
     "November": [1.10, 1.05],
     "December": [2.0, 1.10]
    }
    """
    assert np.shape(values)[1] == 12

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    values_dict = helpers.create_monthly_dict()

    month_enum_list = list(enumerate(months))
    for values_list in values:
        for index, month in month_enum_list:
            values_dict[month].append(values_list[index])
  
    return values_dict
    
def calculate_avg_delta_values(deltas_data, tile_list):
    """   
    Get monthly averaged delta data values for a specific list of tiles.
    
    Parameters
    ----------
    delta_data: list 
        List of dictionaries holding data from delta data files.
        
    Returns
    -------
    avg_delta_values: dictionary 
        Dictionary keys corresponding to delta variable type (i.e. precipitation (Ppt)) holding averaged data values for a specific list of tiles.
        
    Notes
    -----          
    avg_delta_values = {
        "Ppt": {
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
    }         
    """ 
    # check that each tile in tile list is contained in the deltas_data     
    for tile in tile_list:
        if tile not in deltas_data["Tile"]:
            raise ValueError, "{} tile is not in tile list contined in deltas_data".format(tile)

    avg_delta_values = {}
  
    # initialize avg_delta_values with keys corresponding to variable type  
    variable_type = deltas_data["Variable"]
    avg_delta_values[variable_type] = helpers.create_monthly_dict()
    
    # get delta values that correspond to a list of tiles
    values = get_monthly_values(deltas_data, tile_list = tile_list)    
    
    # format the values into a dictionary containing monthly keys
    values_dict = format_to_monthly_dict(values)
    
    # compute average of delta values for each month and put it in avg_delta_values
    for key, value in values_dict.iteritems():
        avg_value = np.average(value)
        avg_delta_values[variable_type][key] = avg_value
       
    return avg_delta_values   

def get_avg_deltas(delta_files, tiles):
    """    
    Get all average Global Climate Model (GCM) delta values for a list of specific 
    (GCM) tile values.

    Parameters
    ----------
    delta_files : list
        List of delta files to calculate average delta values for
    tiles : list
        List of Global Climate Model tile values.
    
    See Also
    --------
    calculate_avg_delta_values()
    """
    # calculate average values for a list of delta files
    avg_deltas = {}
    for delta_file in delta_files:
        
        # read the delta file
        deltas_data = read_file(delta_file) 
                
        # calculate average deltas for a list of tiles
        avg_delta_values = calculate_avg_delta_values(deltas_data = deltas_data, tile_list = tiles)
        
        # update avgerage delta values dictionary 
        avg_deltas.update(avg_delta_values)   
    
    return avg_deltas

    
def _create_test_data():
    """ Create a delta data dictionary for tests """

    data = {"Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", "Tile": ["11", "12", "21", "22", "31", "32"],
            "January": [1.3, 1.2, 1.3, 1.4, 1.5, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
            "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
            "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
            "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]           
    }

    return data

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
    """ Test read_file_in() functionality"""

    print("--- Testing read_file_in() ---")

    expected = {"Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", "Tile": ['11', '12', '21', '22', '31', '32'],
                "January": [1.3, 1.2, 1.3, 1.4, 1.5, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
               "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
               "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
               "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]
    }          


    fixture = {}
    
    fixture["data_file"] = \
        """
        Model	Scenario	Target	Variable	Tile	January	February	March	April	May	June	July	August	September	October	November	December
        CanESM2	rcp45	2030	PET	11	1.3	2.7	3.3	4.7	5.3	6.7	7.3	8.7	9.3	10.7	11.3	12.7
        CanESM2	rcp45	2030	PET	12	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        CanESM2	rcp45	2030	PET	21	1.3	2.9	3.3	4.9	5.3	6.9	7.3	8.9	9.3	10.9	11.3	12.9
        CanESM2	rcp45	2030	PET	22	1.4	2.3	3.4	4.3	5.4	6.3	7.4	8.3	9.4	10.3	11.4	12.3
        CanESM2	rcp45	2030	PET	31	1.5	2.2	3.5	4.2	5.5	6.2	7.5	8.2	9.5	10.2	11.5	12.2
        CanESM2	rcp45	2030	PET	32	1.6	2.3	3.6	4.3	5.6	6.3	7.6	8.3	9.6	10.3	11.6	12.3
        """
        
    fileobj = StringIO(fixture["data_file"])

    actual = read_file_in(fileobj)    

    # print results
    _print_test_info(actual, expected)
    
    
def test_get_monthly_values():
    """ Test get_monthly_values() """

    print("--- Testing get_monthly_values() ---")
    
    # expected values to test with actual values
    expected = {}    
    expected["tiles_11_12"] = [[1.3, 2.7, 3.3, 4.7, 5.3, 6.7, 7.3, 8.7, 9.3, 10.7, 11.3, 12.7], [1.2, 2.8, 3.2, 4.8, 5.2, 6.8, 7.2, 8.8, 9.2, 10.8, 11.2, 12.8]]
    expected["tiles_12_22_32"] = [[1.2, 2.8, 3.2, 4.8, 5.2, 6.8, 7.2, 8.8, 9.2, 10.8, 11.2, 12.8], [1.4, 2.3, 3.4, 4.3, 5.4, 6.3, 7.4, 8.3, 9.4, 10.3, 11.4, 12.3], [1.6, 2.3, 3.6, 4.3, 5.6, 6.3, 7.6, 8.3, 9.6, 10.3, 11.6, 12.3]]

    data = _create_test_data()
    
    actual = {}
    actual["tiles_11_12"] = get_monthly_values(delta_data = data, tile_list = ["11", "12"])
    actual["tiles_12_22_32"] = get_monthly_values(delta_data = data, tile_list = ["12", "22", "32"])

    # print results
    _print_test_info(actual, expected)
    
def test_format_to_monthly_dict():
    """ Test format_to_monthly_dict() """

    print("--- Testing format_to_monthly_dict() ---")

    expected1 = {'January': [1.1], 'February': [2.2], 'March': [3.3], 'April': [4.4], 'May': [5.5], 'June': [6.6], 'July': [7.7], 'August': [8.8], 'September': [9.9], 'October': [10.0], 'November': [11.1], 'December': [12.2]}
    expected2 = {'January': [1.1, 1.9], 'February': [2.2, 2.8], 'March': [3.3, 3.7], 'April': [4.4, 4.6], 'May': [5.5, 5.5], 'June': [6.6, 6.4], 'July': [7.7, 7.3], 'August': [8.8, 8.2], 'September': [9.9, 9.1], 'October': [10.0, 10.0], 'November': [11.1, 11.9], 'December': [12.2, 12.8]}    

    values1 = [[1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11.1, 12.2]]
    values2 = [[1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11.1, 12.2], [1.9, 2.8, 3.7, 4.6, 5.5, 6.4, 7.3, 8.2, 9.1, 10.0, 11.9, 12.8]] 
    
    actual1 = format_to_monthly_dict(values1)
    actual2 = format_to_monthly_dict(values2)
    
    # print results
    _print_test_info(actual1, expected1)
    _print_test_info(actual2, expected2)

def test_calculate_avg_delta_values():
    """ Test get_delta_values() """
    
    print("--- Testing get_delta_values() ---")

    expected = {}
    expected["PET"] = {'January': 1.25, 'February': 2.75, 'March': 3.25, 'April': 4.75, 'May': 5.25, 'June': 6.75, 'July': 7.25, 'August': 8.75, 'September': 9.25, 'October': 10.75, 'November': 11.25, 'December': 12.75}    
    
    data = _create_test_data()
    actual = calculate_avg_delta_values(deltas_data = data, tile_list = ["11", "12"])

    # print results
    _print_test_info(actual, expected)       
    
    
def main():
    """ Test functionality of reading files """

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_read_file_in()

    test_get_monthly_values()
    
    test_format_to_monthly_dict()

    test_calculate_avg_delta_values()

    
if __name__ == "__main__":
    main()