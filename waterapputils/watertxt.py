# -*- coding: utf-8 -*-
"""
:Module: watertxt.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading, writing, processing, and logging errors in WATER output text data files.
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
    data = {
        "user": None,
        
        "date_created": None,
        
        "stationid": None,
        
        "column_names": None,
        
        "dates": [],
        
        "parameters": [], 
          
    }      
            
    ** Note: The "parameters" key contains a list of dictionaries containing
    the parameters found in the data file; i.e.
    
    See Also
    --------
    create_parameter : Create new dictionary to hold parameter data
    """
    
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file 
    patterns = {
        "user": "(User:)\t(.+)",
        "date_created": "(Date:)\t(.+)",
        "stationid": "(StationID:)\t(.+)",
        "column_names": "(Date)\t(.+)",
        "data_row": "([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\t(.+)"
    }        

   # initialize a dictionary to hold all the data of interest
    data = {
        "user": None,
        "date_created": None,
        "stationid": None,
        "column_names": None,
        "dates": [],
        "parameters": []
    }      
    
    # process file
    for line in data_file: 
        # find match
        match_user = re.search(pattern = patterns["user"], string = line)
        match_date_created = re.search(pattern = patterns["date_created"], string = line)
        match_stationid = re.search(pattern = patterns["stationid"], string = line)       
        match_column_names = re.search(pattern = patterns["column_names"], string = line)
        match_data_row = re.search(pattern = patterns["data_row"], string = line)
     
        # if match is found, add it to data dictionary
        if match_user:
            data["user"] = match_user.group(2) 
            
        if match_date_created:
            data["date_created"] = match_date_created.group(2)
            
        if match_stationid:
            data["stationid"] = match_stationid.group(2)
            
        if match_column_names:
            data["column_names"] = match_column_names.group(2).split("\t")
            # create a dictionary for each column_name (excluding "Date")
            for name in data["column_names"]:
                parameter = create_parameter(name = name, index = data["column_names"].index(name), data = [], mean = None, max = None, min = None)
                
                data["parameters"].append(parameter)

        if match_data_row:
            # add date to data dictionary
            date = get_date(date_str = match_data_row.group(1))
            data["dates"].append(date)            
            
            for parameter in data["parameters"]:
                value = match_data_row.group(2).split("\t")[parameter["index"]]
                
                value = helpers.convert_to_float(value = value, helper_str = "parameter {} on {}".format(parameter["name"], date.strftime("%Y-%m-%d_%H.%M")))                
                                       
                parameter["data"].append(float(value)) 
            
    # convert the date list to a numpy array
    data["dates"] = np.array(data["dates"]) 
    
    # convert each parameter data list in data["parameter"] convert to a numpy array and
    # compute mean, max, and min 
    for parameter in data["parameters"]:
        parameter["data"] = np.array(parameter["data"])
        
        param_mean, param_max, param_min = helpers.compute_simple_stats(data = parameter["data"])
        
        parameter["mean"] = param_mean
        parameter["max"] = param_max
        parameter["min"] = param_min
        
    # return data
    return data

def create_parameter(name = None, index = None, data = [], mean = None, max = None, min = None):
    """   
    Create a new dictionary that contains keys and associated data for watertxt_data 
           
    Returns
    -------
    parameter : dictionary
        Parameter that can be added to watertxt_data dictionary 
    
    Examples
    --------
    parameters = {
        "name": string of parameter name,
        
        "index": integer of column index data is located,
        
        "data": numpy array of data values,
        
        "mean": mean of data values,
        
        "max": max of data values,
        
        "min": min of data values
    } 
    """  
    parameter = {"name": name, "index": index, "data": data, 
                  "mean": mean, "max": max, "min": min
    }    
    
    return parameter

def get_date(date_str):
    """   
    Parse date strings and return a datetime object.
    
    Parameters
    ----------
    date_str : str
        String in a daily forma. i.e. 4/9/2014

    Returns
    -------
    date : datetime object           
    """
    # get date from the data row
    day = date_str.split("/")[1]
    month = date_str.split("/")[0]
    year = date_str.split("/")[2]
                
    date = datetime.datetime(int(year), int(month), int(day))
    
    return date
                
def write_file(watertxt_data, save_path, filename = "WATER.txt"):
    """   
    Write data contained in water data dictionary to an output file in the 
    same format as the original WATER output text file.
    
    Parameters
    ----------
    watertxt_data : dictionary 
        Dictionary holding data found in WATER output text file.
    save_path : string 
        String path to save file.
    filename : string
        String name of output file. Default name is WATER.txt.
    """ 
    
    header = "\
 ------------------------------------------------------------------------------\n\
 ----- WATER ------------------------------------------------------------------\n\
 ------------------------------------------------------------------------------\n"
   
    filepath = os.path.join(save_path, filename)    

    with open(filepath, "w") as output_file:
        output_file.write(header)
        output_file.writelines("\n".join(["User:\t{}".format(watertxt_data["user"]),
                                          "Date:\t{}".format(watertxt_data["date_created"]),
                                          "StationID:\t{}".format(watertxt_data["stationid"]),
                                          "Date\t{}\n".format("\t".join(watertxt_data["column_names"]))
        ]))
        
        # make a single list of all the data values from the watertxt_data["parameters"] list            
        values_all = get_all_values(watertxt_data)

        nrows = len(values_all[0])
        ncols = len(values_all)        
        dates = watertxt_data["dates"]
        for i in range(nrows):
            date_str = dates[i].strftime("%m/%d/%Y")
            output_file.write(date_str + "\t")
            row = []
            for j in range(ncols):
                row.append(str(values_all[j][i]))

            output_file.write("\t".join(row) + "\n")
       
def add_parameter(watertxt_data, name, param_data):
    """
    Add a parameter to the list of existing parameters in watertxt_data and the
    list of column names. The new parameter will is appended to the end of the 
    existing parameter list.
    
    Parameters
    ----------
    watertxt_data : dictionary 
        Dictionary holding data found in WATER output text file.
    name : string
        String name of parameter
    param_data : numpy array
        Array of parameter data values
        
    Returns
    -------
    watertxt_data : dictionary 
        Updated dictionary with the new parameter added.
    """
    # add name to column names 
    watertxt_data["column_names"].append(name)
    
    # compute simple stats
    param_mean, param_max, param_min = helpers.compute_simple_stats(data = param_data)

    # find last index
    indices = []
    for parameter in watertxt_data["parameters"]:
        indices.append(parameter["index"])

    # add to parameter list    
    watertxt_data["parameters"].append({"name": name, "index": max(indices) + 1, "data": param_data,
                                       "mean": param_mean, "max": param_max, "min": param_min}
    )    
    
    return watertxt_data    

def get_parameter(watertxt_data, name):
    """   
    Get dates, values, and units from a particular parameter contained in the 
    water_data dictionary. 
    
    Parameters
    ----------
    watertxt_data : dictionary 
        Dictionary holding data found in WATER output text file.
    name : string
        String name of parameter

    Returns
    -------
    values : numpy array of floats        
    """           
    for parameter in watertxt_data['parameters']:
        if parameter['name'].split('(')[0].strip() == name.split('(')[0].strip():              
            return parameter

def get_all_values(watertxt_data):
    """
    Get all numeric data values from watertxt_data dictionary in same order as 
    the column_names list in watertxt_data. Just ensuring proper ordering here as
    values should already be in same order as the column_names because the 
    watertxt_data["parameters"] is a list that was assembled in column_name order.
    
    Parameters
    ----------
    watertxt_data : dictionary 
        Dictionary holding data found in WATER output text file.
    
    Returns
    -------
    values_all : list
        List of data arrays.
    """
    values_all = []
    for column_name in watertxt_data["column_names"]:
        parameter = get_parameter(watertxt_data, name = column_name)
        values_all.append(parameter["data"])

    return values_all

def set_parameter_values(watertxt_data, name, values):
    """   
    Set new values for a particular parameter contained in the watertxt_data
    dictionary. 
    
    Parameters
    ----------
    watertxt_data : dictionary 
        Dictionary holding data found in WATER output text file.
    name : string
        String name of parameter
    values : numpy array
        Array of data values
    
    Returns
    -------
    watertxt_data : dictionary 
        Dictionary holding updated data values 
    """      
    for parameter in watertxt_data['parameters']:
        if parameter["name"].split('(')[0].strip() == name.split("(")[0].strip():
            
            param_mean, param_max, param_min = helpers.compute_simple_stats(data = values)
            parameter["data"] = values
            parameter["mean"] = param_mean
            parameter["max"] = param_max
            parameter["min"] = param_min

    return watertxt_data
 
def apply_factors(watertxt_data, name, factors):
    """
    Apply monthly multiplicative factors to a specific parameter.
    
    Parameters
    ----------
    watertxt_data : dictionary 
        Dictionary holding data found in WATER output text file.
    name : string
        String name of parameter
    factors : dictionary
        Dictionary holding monthly multiplicative factors
       
    Returns
    -------
    watertxt_data : dictionary 
        Dictionary holding updated data with factors applied.
    
    Notes
    -----    
    factors = {
        'January': 2.0,
        'February': 0.98,
        'March': 0.97,
        'April': 1.04,
        'May': 1.10,
        'June': 0.99,
        'July': 0.97,
        'August': 1.25,
        'September': 1.21,
        'October': 1.11,
        'November': 1.10,
        'December': 2.0
    }  
    """  
    parameter = get_parameter(watertxt_data, name) 
    
    assert len(parameter["data"]) == len(watertxt_data["dates"]), "Length of {} parameter values does not match length of date values".format(name)
    
    new_values = []
    for i in range(len(watertxt_data["dates"])):
        date = watertxt_data["dates"][i]
        
        # match the month from the date value to the factors dictionary key
        month = date.strftime("%B")     # get month 
        factor = factors[month]         # get the factor that corresponds to a specific month 
        
        # apply factor
        new_value = parameter["data"][i] * factor
        new_values.append(new_value)
            
    new_values = np.array(new_values)

    # set new values in water_data    
    watertxt_data = set_parameter_values(watertxt_data, name, values = new_values)

    return watertxt_data      


def _create_test_data(multiplicative_factor = 1, stationid = "012345", with_wateruse = False):
    """ Create test data for tests """

    dates = [datetime.datetime(2014, 04, 01, 0, 0), datetime.datetime(2014, 04, 02, 0, 0), datetime.datetime(2014, 04, 03, 0, 0)]
    
    discharge_data = np.array([2, 6, 10]) * multiplicative_factor
    subsurface_data = np.array([50, 55, 45]) * multiplicative_factor
    impervious_data = np.array([2, 8, 2]) * multiplicative_factor
    infiltration_data = np.array([0, 1.5, 1.5]) * multiplicative_factor
    initialabstracted_data = np.array([0.1, 0.2, 0.3]) * multiplicative_factor
    overlandflow_data = np.array([3, 9, 3]) * multiplicative_factor
    pet_data = np.array([5, 13, 3]) * multiplicative_factor
    aet_data = np.array([5, 12, 13]) * multiplicative_factor
    avgsoilrootzone_data = np.array([40, 50, 60]) * multiplicative_factor
    avgsoilunsaturatedzone_data = np.array([4, 3, 2]) * multiplicative_factor
    snowpack_data = np.array([150, 125, 25]) * multiplicative_factor
    precipitation_data = np.array([0.5, 0.4, 0.3]) * multiplicative_factor
    storagedeficit_data = np.array([300, 310, 350]) * multiplicative_factor
    returnflow_data = np.array([-5.0, -4.5, -4.0]) * multiplicative_factor
    
    parameters = [{"name": "Discharge (cfs)", "index": 0, "data": discharge_data,
                   "mean": np.mean(discharge_data), "max": np.max(discharge_data), "min": np.min(discharge_data)}, 
                  
                  {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data,
                   "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)},

                  {"name": "Impervious Flow (mm/day)", "index": 2, "data": impervious_data,
                   "mean": np.mean(impervious_data), "max": np.max(impervious_data), "min": np.min(impervious_data)},

                  {"name": "Infiltration Excess (mm/day)", "index": 3, "data": infiltration_data,
                   "mean": np.mean(infiltration_data), "max": np.max(infiltration_data), "min": np.min(infiltration_data)},

                  {"name": "Initial Abstracted Flow (mm/day)", "index": 4, "data": initialabstracted_data,
                   "mean": np.mean(initialabstracted_data), "max": np.max(initialabstracted_data), "min": np.min(initialabstracted_data)},

                  {"name": "Overland Flow (mm/day)", "index": 5, "data": overlandflow_data,
                   "mean": np.mean(overlandflow_data), "max": np.max(overlandflow_data), "min": np.min(overlandflow_data)},

                  {"name": "PET (mm/day)", "index": 6, "data": pet_data,
                   "mean": np.mean(pet_data), "max": np.max(pet_data), "min": np.min(pet_data)},

                  {"name": "AET (mm/day)", "index": 7, "data": aet_data,
                   "mean": np.mean(aet_data), "max": np.max(aet_data), "min": np.min(aet_data)},

                  {"name": "Average Soil Root zone (mm)", "index": 8, "data": avgsoilrootzone_data,
                   "mean": np.mean(avgsoilrootzone_data), "max": np.max(avgsoilrootzone_data), "min": np.min(avgsoilrootzone_data)},

                  {"name": "Average Soil Unsaturated Zone (mm)", "index": 9, "data": avgsoilunsaturatedzone_data,
                   "mean": np.mean(avgsoilunsaturatedzone_data), "max": np.max(avgsoilunsaturatedzone_data), "min": np.min(avgsoilunsaturatedzone_data)},

                  {"name": "Snow Pack (mm)", "index": 10, "data": snowpack_data,
                   "mean": np.mean(snowpack_data), "max": np.max(snowpack_data), "min": np.min(snowpack_data)},

                  {"name": "Precipitation (mm/day)", "index": 11, "data": precipitation_data,
                   "mean": np.mean(precipitation_data), "max": np.max(precipitation_data), "min": np.min(precipitation_data)},

                  {"name": "Storage Deficit (mm/day)", "index": 12, "data": storagedeficit_data,
                   "mean": np.mean(storagedeficit_data), "max": np.max(storagedeficit_data), "min": np.min(storagedeficit_data)},

                  {"name": "Return Flow (mm/day)", "index": 13, "data": returnflow_data,
                   "mean": np.mean(returnflow_data), "max": np.max(returnflow_data), "min": np.min(returnflow_data)},
    ] 

    column_names = ["Discharge (cfs)", "Subsurface Flow (mm/day)", "Impervious Flow (mm/day)", "Infiltration Excess (mm/day)", "Initial Abstracted Flow (mm/day)", "Overland Flow (mm/day)", "PET (mm/day)", "AET(mm/day)", "Average Soil Root zone (mm)", "Average Soil Unsaturated Zone (mm)", "Snow Pack (mm)", "Precipitation (mm/day)", "Storage Deficit (mm/day)", "Return Flow (mm/day)"]
    data = {"user": "jlant", "date_created": "4/9/2014 15:30:00 PM", "stationid": stationid, 
            "column_names": column_names,
            "parameters": parameters, "dates": dates}

    if with_wateruse:
        data = add_parameter(watertxt_data = data, name = "Water Use (cfs)", param_data = np.array([3.0, 2.5, -5.5]))
        discharge = get_parameter(watertxt_data = data, name = "Discharge")
        wateruse = get_parameter(watertxt_data = data, name = "Water Use")
        data = add_parameter(watertxt_data = data, name = "Discharge - Water Use (cfs)", param_data = discharge["data"] - wateruse["data"])

    return data

def test_create_parameter():
    """ Test the create_parameter funtionality"""

    print("--- Testing create_parameter ---")
    
    parameter = create_parameter()
    
    print("*Name*\n    expected : actual")
    print("    None : {}".format(parameter["name"]))
    print("*Index*\n    expected : actual")
    print("    None : {}".format(parameter["index"]))    
    print("*Data*\n    expected : actual")
    print("    [] : {}".format(parameter["data"]))
    print("*Mean, Max, Min*\n    expected : actual")
    print("    None, None, None : {}, {}, {}".format(parameter["mean"], parameter["max"], parameter["min"]))
    print("")
    
    parameter = create_parameter(name = "discharge", index = 0, data = [1, 2, 3], mean = 2, max = 3, min = 1)    
    
    print("*Name*\n    expected : actual")
    print("    discharge : {}".format(parameter["name"]))
    print("*Index*\n    expected : actual")
    print("    0 : {}".format(parameter["index"]))    
    print("*Data* expected : actual")
    print("    [1, 2, 3] : {}".format(parameter["data"]))
    print("*Mean, Max, Min*\n    expected : actual")
    print("    2, 3, 1 : {}, {}, {}".format(parameter["mean"], parameter["max"], parameter["min"]))
    print("")  

def test_get_date():
    """ Test the get_date functionality """
    
    print("--- Testing get_date() ---")
    
    date1 = get_date(date_str = "4/9/2014")
    print("*Date*\n    expected : actual")
    print("    2014-04-09 00:00:00 : {}".format(date1))
    
    print("") 


def test_get_all_values():
    """ Test get_dict_values functionality """

    print("--- Testing get_all_values ---") 
    
    data = _create_test_data()
    values_all = get_all_values(watertxt_data = data)
    
    print("*Data*\n    expected")
    print("    [  2.   6.  10.]")
    print("    [ 50.  55.  45.]")
    print("    [ 2.  8.  2.]")
    print("    [ 0.   1.5  1.5]")
    print("    [ 0.1  0.2  0.3]")
    print("    [ 3.  9.  3.]")
    print("    [  5.   3.  13.]")
    print("    [  5.  12.  13.]")
    print("    [ 40.  50.  60.]")
    print("    [ 4.  3.  2.]")
    print("    [ 150.  125.   25.]")
    print("    [ 0.5  0.4  0.3]")
    print("    [ 300.  310.  350.]")
    print("    [  -5.   -4.5   -4.0]")
    print("")    
    
    print("*Data*\n    actual")
    for data_array in values_all:
        print("    {}".format(data_array))
    
    print("")

def test_get_parameter():
    """ Test get_parameter functionality """

    print("--- Testing get_parameter ---") 
    
    data = _create_test_data()
    parameter = get_parameter(watertxt_data = data, name = "Subsurface Flow")
    
    print("*Added parameter name*\n    estimated : actual")    
    print("   Subsurface Flow (mm/day) : {}\n".format(parameter["name"]))

    print("*Added parameter index*\n    estimated : actual")    
    print("    1 : {}\n".format(parameter["index"]))

    print("*Added parameter data*\n    estimated : actual")    
    print("    [50.0 55. 45.] : {}\n".format(parameter["data"]))

    print("*Added parameter mean*\n    estimated : actual")    
    print("    50.0 : {}\n".format(parameter["mean"]))

    print("*Added parameter max*\n    estimated : actual")    
    print("    55.0 : {}\n".format(parameter["max"]))

    print("*Added parameter min*\n    estimated : actual")    
    print("    45.0 : {}\n".format(parameter["min"]))

def test_add_parameter():
    """ Test add_parameter functionality """

    print("--- Testing add_parameter ---") 
    
    data = _create_test_data()
    data = add_parameter(watertxt_data = data, name = "Water Use (cfs)", param_data = np.array([3.0, 2.5, -5.5])) 

    print("*Added parameter name*\n    estimated : actual")    
    print("    Water Use (cfs) : {}\n".format(data["parameters"][-1]["name"]))

    print("*Added parameter index*\n    estimated : actual")    
    print("    14 : {}\n".format(data["parameters"][-1]["index"]))

    print("*Added parameter data*\n    estimated : actual")    
    print("    [3.0 2.5 -5.5] : {}\n".format(data["parameters"][-1]["data"]))

    print("*Added parameter mean*\n    estimated : actual")    
    print("    0.0 : {}\n".format(data["parameters"][-1]["mean"]))

    print("*Added parameter max*\n    estimated : actual")    
    print("    3.0 : {}\n".format(data["parameters"][-1]["max"]))

    print("*Added parameter min*\n    estimated : actual")    
    print("    -5.5 : {}\n".format(data["parameters"][-1]["min"]))
    print("")


def test_set_parameter_values():
    """ Test set_parameter functionality """
    
    print("--- Testing set_parameter ---") 
    
    data = _create_test_data()
    
    new_values = np.array([100, 110, 120])
    watertxt_data = set_parameter_values(watertxt_data = data, name = "Discharge", values = new_values)

    updated_discharge = get_parameter(watertxt_data, name = "Discharge")

    print("*Updated parameter name*\n    estimated : actual")    
    print("    Discharge (cfs) : {}\n".format(updated_discharge["name"]))

    print("*Updated parameter index*\n    estimated : actual")    
    print("    0 : {}\n".format(updated_discharge["index"]))
   
    print("*Updated parameter data*\n    estimated : actual")    
    print("    [100 110 120] : {}\n".format(updated_discharge["data"]))

    print("*Updated parameter mean*\n    estimated : actual")    
    print("    110.0 : {}\n".format(updated_discharge["mean"]))

    print("*Updated parameter max*\n    estimated : actual")    
    print("    120.0 : {}\n".format(updated_discharge["max"]))

    print("*Updated parameter min*\n    estimated : actual")    
    print("    100.0 : {}\n".format(updated_discharge["min"]))
    print("")

def test_read_file_in():
    """ Test read_file_in() functionality"""

    print("--- Testing read_file_in() ---")

    fixture = {}
    
    fixture["data file"] = \
        """
         ------------------------------------------------------------------------------
         ----- WATER ------------------------------------------------------------------
         ------------------------------------------------------------------------------
        User:	jlant
        Date:	4/9/2014 15:50:47 PM
        StationID:	012345
        Date	Discharge (cfs)	Subsurface Flow (mm/day)	Impervious Flow (mm/day)	Infiltration Excess (mm/day)	Initial Abstracted Flow (mm/day)	Overland Flow (mm/day)	PET (mm/day)	AET(mm/day)	Average Soil Root zone (mm)	Average Soil Unsaturated Zone (mm)	Snow Pack (mm)	Precipitation (mm/day)	Storage Deficit (mm/day)	Return Flow (mm/day)
        4/1/2014	0.0	50.0	2	0	0.1	3.0	5	5	40.0	4.0	150	0.5	300.0	-5.0
        4/2/2014		55.0	8	1.5	0.2	9.0	3	12	50.0	3.0	125	0.4	310.0	-4.5
        4/3/2014	10.0	45.0	2	1.5	0.3	3.0	13	13	60.0	2.0	25	0.3	350.0	-4.0
        """
        
    fileobj = StringIO(fixture["data file"])
    
    data = read_file_in(fileobj)

    print("*User*\n    expected : actual")
    print("    jlant : {}".format(data["user"]))
    print("")

    print("*Date created*\n    expected : actual")
    print("    4/9/2014 15:50:47 PM : {}".format(data["date_created"]))
    print("")

    print("*StationID*\n    expected : actual")
    print("    012345 : {}".format(data["stationid"]))
    print("")

    print("*Column names*\n    expected : actual")
    print("    ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'] : \n    {}".format(data["column_names"]))
    print("")

    print("*Dates type*\n    expected : actual")
    print("    numpy.ndarray : {}".format(type(data["dates"]))) 
    print("")   
    
    print("*Dates*\n    expected : actual")
    print("    [datetime.datetime(2014, 4, 1, 0, 0) datetime.datetime(2014, 4, 2, 0, 0) datetime.datetime(2014, 4, 3, 0, 0)] : \n    {}".format(data["dates"]))
    print("")
    
    print("*Data type*\n    expected : actual")
    print("    numpy.ndarray : {}".format(type(data["parameters"][0]["data"])))    
    print("")

    print("*Parameters*\n    expected name, index, data, mean, max, min")
    print("    Discharge (cfs) 0 [  0.   nan  10.] 5.0 10.0 0.0")
    print("    Subsurface Flow (mm/day) 1 [ 50.  55.  45.] 50.0 55.0 45.0")
    print("    Impervious Flow (mm/day) 2 [ 2.  8.  2.] 4.0 8.0 2.0")
    print("    Infiltration Excess (mm/day) 3 [ 0.   1.5  1.5] 1.0 1.5 0.0")
    print("    Initial Abstracted Flow (mm/day) 4 [ 0.1  0.2  0.3] 0.2 0.3 0.1")
    print("    Overland Flow (mm/day) 5 [ 3.  9.  3.] 5.0 9.0 3.0")
    print("    PET (mm/day) 6 [  5.   3.  13.] 7.0 13.0 3.0")
    print("    AET(mm/day) 7 [  5.  12.  13.] 10.0 13.0 5.0")
    print("    Average Soil Root zone (mm) 8 [ 40.  50.  60.] 50.0 60.0 40.0")
    print("    Average Soil Unsaturated Zone (mm) 9 [ 4.  3.  2.] 3.0 4.0 2.0")
    print("    Snow Pack (mm) 10 [ 150.  125.   25.] 100.0 150.0 25.0")
    print("    Precipitation (mm/day) 11 [ 0.5  0.4  0.3] 0.4 0.5 0.3")
    print("    Storage Deficit (mm/day) 12 [ 300.  310.  350.] 320.0 350.0 300.0")
    print("    Return Flow (mm/day) 13 [  -5.   -4.5   -4.0] -4.5.0 -5.0 -4.0")
    print("")
    

    print("*Parameters*\n    actual name, index, data, mean, max, min")
    for parameter in data["parameters"]:
        print("    {} {} {} {} {} {}".format(parameter["name"], parameter["index"], parameter["data"], parameter["mean"], parameter["max"], parameter["min"]))    
    print("")


def test_apply_factors():
    """ Test apply_factors functionality """

    print("--- Testing apply_factors ---") 

    factors = {
        'January': 1.5,
        'February': 2.0,
        'March': 2.5,
        'April': 3.0,
        'May': 3.5,
        'June': 4.0,
        'July': 4.5,
        'August': 5.5,
        'September': 6.0,
        'October': 6.5,
        'November': 7.0,
        'December': 7.5
    }     
    
    param_name = "Discharge"
    month = "April"

    print("*Factor used*\n    expected : actual")
    print("    3.0 : {}".format(factors[month]))
    print("")
    
    data = _create_test_data()
    
    parameter = get_parameter(watertxt_data = data, name = param_name)
    
    print("*Parameter BEFORE applied factors*\n    actual name, index, data, mean, max, min")
    print("    {} {} {} {} {} {}".format(parameter["name"], parameter["index"], parameter["data"], parameter["mean"], parameter["max"], parameter["min"]))    
    print("")
    
    watertxt_data = apply_factors(watertxt_data = data, name = param_name, factors = factors)    

    parameter = get_parameter(watertxt_data = watertxt_data, name = param_name)

    print("*Parameter AFTER applied factors*\n    actual name, index, data, mean, max, min")
    print("    {} {} {} {} {} {}".format(parameter["name"], parameter["index"], parameter["data"], parameter["mean"], parameter["max"], parameter["min"]))    

    print("")    
    
def test_write_file():
    """ Test write_file functionality """

    print("--- Testing write_file ---") 
    
    data = _create_test_data()
    write_file(watertxt_data = data , save_path = os.getcwd())

    data = _create_test_data()
    new_discharge_data = np.array([230, 240, 280])
    data = set_parameter_values(watertxt_data = data, name = "Discharge", values = new_discharge_data)
    write_file(watertxt_data = data , save_path = os.getcwd(), filename = "WATER_new_discharge_data.txt")
    
    data = _create_test_data(with_wateruse = True)
    write_file(watertxt_data = data , save_path = os.getcwd(), filename = "WATER_wateruse.txt") 
    
    print("Created 3 files {}, {}, and {} in current working directory. Please check for proper writing".format("WATER.txt", "WATER_new_discharge_data.txt" , "WATER_wateruse.txt")) 
    print("")    
    
def main():
    """ Test functionality of watertxt """

    print("")
    print("RUNNING TESTS ...")
    print("")
    
    test_get_date()
    
    test_create_parameter()

    test_get_all_values()

    test_get_parameter()

    test_add_parameter()

    test_set_parameter_values() 

    test_read_file_in()

    test_write_file()

    test_apply_factors()
    
if __name__ == "__main__":
    main()