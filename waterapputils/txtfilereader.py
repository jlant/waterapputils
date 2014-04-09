# -*- coding: utf-8 -*-
"""
:Module: txtfilereader.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading, processing, and logging errors in WATER output text data files
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
        'user': None,
        
        'date_created': None,
        
        'stationid': None,
        
        'column_names': None,
        
        'dates': [],
        
        'parameters': [], 
          
    }      
            
    ** Note: The 'parameters' key contains a list of dictionaries containing
    the parameters found in the data file; i.e.
    
    parameters[0] = {
        'name': string of parameter name,
        
        'index': integer of column index data is located,
        
        'data': numpy array of data values,
        
        'mean': mean of data values,
        
        'max': max of data values,
        
        'min': min of data values
    }        
    """
    
    # read all the lines in the filestream
    data_file = filestream.readlines()
    
    # regular expression patterns in data file 
    patterns = {
        'user': '(User:)\t(.+)',
        'date_created': '(Date:)\t(.+)',
        'stationid': '(StationID:)\t(.+)',
        'column_names': '(Date)\t(.+)',
        'data_row': '([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\t(.+)'
    }        

   # initialize a dictionary to hold all the data of interest
    data = {
        'user': None,
        'date_created': None,
        'stationid': None,
        'column_names': None,
        'dates': [],
        'parameters': []
    }      
    
    # process file
    for line in data_file: 
        # find match
        match_user = re.search(pattern = patterns['user'], string = line)
        match_date_created = re.search(pattern = patterns['date_created'], string = line)
        match_stationid = re.search(pattern = patterns['stationid'], string = line)       
        match_column_names = re.search(pattern = patterns['column_names'], string = line)
        match_data_row = re.search(pattern = patterns['data_row'], string = line)
     
        # if match is found add it to data dictionary
        if match_user:
            data['user'] = match_user.group(2) 
        if match_date_created:
            data['date_created'] = match_date_created.group(2)
        if match_stationid:
            data['stationid'] = match_stationid.group(2)
        if match_column_names:
            # group(2) does not include dates which are added during data row match
            data['column_names'] = match_column_names.group(2).split('\t')
            # create a dictionary for each column_name (excluding 'Date')
            for name in data['column_names']:
                data['parameters'].append({
                    'name': name,
                    'index': data['column_names'].index(name) ,
                    'data': [],
                    'mean': None,
                    'max': None,
                    'min': None
                })

        if match_data_row:
            # add date to data dictionary
            date = get_date(date_str = match_data_row.group(1))
            data['dates'].append(date)            
            
            for parameter in data['parameters']:
                value = match_data_row.group(2).split('\t')[parameter['index']]
                
                value = convert_to_float(value = value, helper_str = "parameter {} on {}".format(parameter["name"], date.strftime("%Y-%m-%d_%H.%M")))                
                                       
                parameter['data'].append(float(value)) 
                
            
    # convert the date list to a numpy array
    data['dates'] = np.array(data['dates']) 
    
    # convert each parameter data list in data['parameter'] convert to a numpy array and
    # compute mean, max, and min 
    for parameter in data['parameters']:
        parameter["data"] = np.array(parameter["data"])
        
        param_mean, param_max, param_min = compute_simple_stats(data = parameter["data"])
        
        parameter["mean"] = param_mean
        parameter["max"] = param_max
        parameter["min"] = param_min
        
    # return data
    return data

def compute_simple_stats(data):
    """   
    Compute simple statistics (mean, max, min) on a data array. Can handle nan values.
    If the entire data array consists of only nan values, then log the error and raise a ValueError.
    
    Parameters
    ----------
    data : array
        An array of numbers to compute simple statistics on. 
        
    Returns
    -------
    (mean, max, min) : tuple 
        Returns a tuple of mean, max, and min stats.        

    Raises
    ------
    ValueError
        If data array only contains nan values.

    Examples
    --------
    >>> import txtfilereader
    >>> import numpy as np
    >>> txtfilereader.compute_simple_stats([1, 2, 3, 4])
    (2.5, 4, 1)
    
    >>> txtfilereader.compute_simple_stats([2, np.nan, 6, 1])
    (3.0, 6.0, 1.0)
    """    
    # check if all values are nan
    if not np.isnan(data).all():
        param_mean = np.nanmean(data)
        param_max = np.nanmax(data)
        param_min = np.nanmin(data)
        
        return param_mean, param_max, param_min
    else:
        error_str = "*Bad data* All values are NaN. Please check data"
        logging.warn(error_str)
        
        raise ValueError

def convert_to_float(value, helper_str = None):
    """   
    Convert a value to a float. If value is not a valid float, log as an error
    with a helper_str (i.e. value's coorsponding date) to help locate the 
    error and replace value with a nan.
    
    Parameters
    ----------
    value : str
        String value to convert.
    helper_str : str
        String message to be placed in error log if value can not be converted to a float. i.e. value's corresponding date of occurance.
        
    Returns
    -------
    value : {float, nan}
        Float or numpy nan value 
    """
    if helpers.isfloat(value):
        value = float(value)
    else:
        if "_" in value:
            error_str = "*_ character* with float *Helper message* {}. *Solution* - Splitting on _ character".format(helper_str)
            logging.warn(error_str)
            value = value.strip("_")

        elif value == "":
            error_str = "*Missing value* {}. *Solution* - Replacing with NaN value".format(helper_str)
            logging.warn(error_str)
            value = np.nan

        else:
            error_str = "*Bad value* {}. *Solution* - Replacing with NaN value".format(helper_str)
            logging.warn(error_str)
            value = np.nan
            
    return value

def get_date(date_str):
    """   
    Parse date strings and return a datetime object.
    
    Parameter
    ---------
    daate_str : str
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


def test_get_date():
    """ Test the get_date functionality """
    
    print("--- Testing get_date() ---")
    
    date1 = get_date(date_str = "4/9/2014")
    print("*Date* expected : actual")
    print("    2014-04-09 00:00:00 : {}".format(date1))
    
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
        4/1/2014	0.0	50.0	2	0	0.1	3.0	5	5	40.0	4.0	150	0.5	300.0	5.0E-05
        4/2/2014	5.0	55.0	8	1.5	0.2	9.0	3	12	50.0	3.0	125	0.4	310.0	4.5E-05
        4/3/2014	10.0	45.0	2	1.5	0.3	3.0	13	13	60.0	2.0	25	0.3	350.0	4.0E-05
        """
        
    fileobj = StringIO(fixture["data file"])
    
    data = read_file_in(fileobj)

    print("*User* expected : actual")
    print("    jlant : {}".format(data["user"]))
    print("")

    print("*Date created* expected : actual")
    print("    4/9/2014 15:50:47 PM : {}".format(data["date_created"]))
    print("")

    print("*StationID* expected : actual")
    print("    012345 : {}".format(data["stationid"]))
    print("")

    print("*Column names* expected : actual")
    print("    ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil', 'Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'] : \n    {}".format(data["column_names"]))
    print("")

    print("*Dates* type expected : actual")
    print("    numpy.ndarray : {}".format(type(data["dates"]))) 
    print("")   
    
    print("*Dates* expected : actual")
    print("    [datetime.datetime(2014, 4, 1, 0, 0) datetime.datetime(2014, 4, 2, 0, 0) datetime.datetime(2014, 4, 3, 0, 0)] : \n    {}".format(data["dates"]))
    print("")
    
    print("Data type expected : actual")
    print("    numpy.ndarray : {}".format(type(data["parameters"][0]["data"])))    
    print("")

    print("*Parameters* expected name, index, data, mean, max, min")
    print("    Discharge (cfs) 0 [  0.   5.  10.] 5.0 10.0 0.0")
    print("    Subsurface Flow (mm/day) 1 [ 50.  55.  45.] 50.0 55.0 45.0")
    print("    Impervious Flow (mm/day) 2 [ 2.  8.  2.] 4.0 8.0 2.0")
    print("    Infiltration Excess (mm/day) 3 [ 0.   1.5  1.5] 1.0 1.5 0.0")
    print("    Initial Abstracted Flow (mm/day) 4 [ 0.1  0.2  0.3] 0.2 0.3 0.1")
    print("    Overland Flow (mm/day) 5 [ 3.  9.  3.] 5.0 9.0 3.0")
    print("    PET (mm/day) 6 [  5.   3.  13.] 7.0 13.0 3.0")
    print("    AET(mm/day) 7 [  5.  12.  13.] 10.0 13.0 5.0")
    print("    Average Soil Root zone (mm) 8 [ 40.  50.  60.] 50.0 60.0 40.0")
    print("    Average Soil Unsaturated Zone (mm) 9 [ 4.  3.  2.] 3.0 4.0 2.0")
    print("    Snow Pack (mm) 10 Snow Pack (mm) 10 [ 150.  125.   25.] 100.0 150.0 25.0")
    print("    Precipitation (mm/day) 11 [ 0.5  0.4  0.3] 0.4 0.5 0.3")
    print("    Storage Deficit (mm/day) 12 [ 300.  310.  350.] 320.0 350.0 300.0")
    print("    Return Flow (mm/day) 13 [  5.00000000e-05   4.50000000e-05   4.00000000e-05] 4.5e-05 5e-05 4e-05")
    print("")
    
    print("*Parameters* actual name, index, data, mean, max, min")
    for parameter in data["parameters"]:
        print("    {} {} {} {} {} {}".format(parameter["name"], parameter["index"], parameter["data"], parameter["mean"], parameter["max"], parameter["min"]))    
    print("")
    
def main():
    """ Test functionality of reading files """
    
    test_get_date()
    
    test_read_file_in()
    
if __name__ == "__main__":
    main()