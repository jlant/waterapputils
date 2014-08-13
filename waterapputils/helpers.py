# -*- coding: utf-8 -*-
"""
:Module: helpers.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Collection of helper functions.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os
import numpy as np
import datetime
import re
import logging
import fnmatch


def now():
    """    
    Return current date and time in a format that can be used as a file name. 
    Format: year-month-day_hour.minute.second.microsecond; e.g. 2014-03-18_15.51.46.25
      
    Returns
    -------
    date_time : string
        String of current date and time in %Y-%m-%d_%H.%M.%S.%f format.       
        
    Notes
    -----
    The length of the microsecond string is trimed to 2 digits.
    """  
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")[:-4]
    
    return date_time

def find_file(name, path):
    """    
    Return the full path to a particular file the matches a file name provided.
    
    Parameters
    ----------    
    name : string
        String name of file
    path : string
        String path 
        
    Returns
    -------
    result : string 
        String of the full path for a file.
    """
    result = None       
    for root, directories, files in os.walk(path):
        if name in files:
            result = os.path.join(root, name)  

    # if file was not found, raise an error
    if not result:
        raise IOError("Did not find {} files in directory: {}".format(name, path))
        
    return result
       
def find_files(name, path):
    """    
    Return a list of full paths to a file matching a file name provided.  
    Search starts from path provided.
    
    Parameters
    ----------    
    name : string
        String name of file
    path : string
        String path 
       
    Returns
    -------
    results : list 
        List of strings of full paths for a file. 
    """    
    results = []   
    for root, dirs, files in os.walk(path):
        if name in files:
            results.append(os.path.join(root, name))

    # if no results (files) were found, raise an error
    if not results:
        raise IOError("Did not find {} files in directory: {}".format(name, path))
            
    return results

def find_files_with_pattern(pattern, path):
    """    
    Return a list of full paths to a file matching a pattern (e.g. *.txt).  
    Search starts from path provided.   
    
    Parameters
    ----------    
    pattern : string
        String pattern to match a file
    path : string
        String path to start search 
        
    Returns
    -------
    results : list 
        List of strings of full paths for a file. 
    """  
    results = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                results.append(os.path.join(root, name))

    # if no results (files) were found, raise an error
    if not results:
        raise IOError("Did not find {} files in directory: {}".format(name, path))

    return results

def get_file_paths(path, file_ext = None):
    """    
    Return a list of full file paths from a directory including its subdirectories.
    Filter files based on its file extension.    
    
    Parameters
    ----------    
    path : string
        String path 
    file_ext : string
        String file extention; e.g. ".txt" 
        
    Returns
    -------
    file_paths : list 
        List of strings of full file paths from a directory.
    """     
    file_paths = []  
    for root, directories, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if file_ext and filepath.endswith(file_ext):
                file_paths.append(filepath) 

    return file_paths

def get_file_info(path):
    """    
    Get file directory and name from a file path.
    
    Parameters
    ----------
    path : string
        String path
      
    Returns
    -------
    filedir : string
        String file directory path
    filename : string
        String file name    
    """ 
    filedir, filename = os.path.split(path)
    
    # filedir is an empty string then file is in current directory 
    if not filedir: 
        filedir = os.getcwd()

    return filedir, filename

def make_directory(path, directory_name):
    """    
    Make a directory if is does not exist.
    
    Parameters
    ----------
    path: string
        String path 
    directory_name : string
        String name
      
    Returns
    -------
    directory_path : string
        String path to made directory.  
    """    
    directory_path = os.path.join(path, directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)         
    
    return directory_path

def isfloat(value):
    """   
    Determine if string value can be converted to a float. Return True if
    value can be converted to a float and False otherwise.
    
    Parameters
    ----------
    value : string
        String value to try to convert to a float.
        
    Returns
    -------
    bool : bool
        
    Examples
    --------
    >>> import nwispy_helpers
    >>> nwispy_helpers.isfloat(value = "2.5")
    True
    >>> nwispy_helpers.isfloat(value = "hello world")
    False
    >>> nwispy_helpers.isfloat(value = "5.5_")
    False
    """
    
    try:
        float(value)
        return True
        
    except ValueError:
        return False

def rmspecialchars(value):
    """   
    Remove any special characters except period (.) and negative (-) from numeric values
    
    Parameters
    ----------
    value : string
        String value to remove any existing characters from
        
    Returns
    -------
    value : string
        String value to without any special characters
        
    Examples
    --------
    >>> import helpers
    >>> helpers.rmspecialchars(value = "*6.5_")
    6.5
    >>> helpers.rmspecialchars(value = "ICE")
    ICE
    >>> helpers.rmspecialchars(value = "-4.2")
    -4.2
    >>> helpers.rmspecialchars(value = "")
    
    >>> helpers.rmspecialchars(value = "%&!@#8.32&#*;")
    8.32
    """
    value = re.sub("[^A-Za-z0-9.-]+", "", value)
    
    return value

def convert_to_float(value, helper_str = None):
    """   
    Convert a value to a float. If value is not a valid float, log as an error
    with a helper_str (e.g. value"s coorsponding date) to help locate the 
    error and replace value with a nan.
    
    Parameters
    ----------
    value : string
        String value to convert.
    helper_str : string
        String message to be placed in error log if value can not be converted to a float. e.g. value"s corresponding date of occurance.
        
    Returns
    -------
    value : {float, nan}
        Float or numpy nan value 
    """
    # remove any special characters present in string value
    value = rmspecialchars(value)    
    
    if isfloat(value):
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

def create_monthly_dict():
    """
    Create a dictionary containing monthly keys and empty lists as initial values
    
    Returns
    -------
    values_dict : dictionary
        Dictionary containing monthly keys with corresponding values.
    
    Notes
    -----
    {"January": [],
     "February": [],
     "March": [],
     "April": [],
     "May": [],
     "June": [],
     "July": [],
     "August": [],
     "September": [],
     "October": [],
     "November": [],
     "December": []
    }
    """
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]       

    # initialize dictionary
    monthly_dict = {}
    for month in months:
        monthly_dict[month] = []

    return monthly_dict

def print_monthly_dict(monthly_dict):
    """    
    Print a dictionary in a nice format.
    
    Parameters
    ----------
    monthly_dict : dictionary
        Dictionary containing monthly keys.  
    """      
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]       
    for month in months:
        print("\t\t{0:<15}\t{1:<15}\n".format(month, monthly_dict[month]))

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
    >>> import watertxt
    >>> import numpy as np
    >>> watertxt.compute_simple_stats([1, 2, 3, 4])
    (2.5, 4, 1)
    
    >>> watertxt.compute_simple_stats([2, np.nan, 6, 1])
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

    
def subset_data(dates, values, start_date, end_date):
    """   
    Subset the dates and values arrays to match the range of the start_date
    and end_date. If start_date and end_date are not within the range of dates
    specified in dates, then the start_date and end_date are set to the
    first and last dates in the array dates.
            
    Parameters 
    ----------
    dates : array 
        Array of dates as datetime objects. 
    data : array
        Array of numbers.
    start_date : datetime object
        A date as a datetime object.
    end_date : datetime object
        A date as a datetime object.
        
    Returns
    -------
    (subset_dates, subset_values) : tuple 
        Tuple of arrays of dates and values that were subsetted.
    """ 
    if len(dates) != len(values):
        raise ValueError("Lengths of dates and values are not equal!")
        
    else:
        # if start_date or end_date are not within dates, set them to the 
        # first and last elements in dates
        if start_date < dates[0] or start_date > dates[-1]:
            start_date = dates[0]  
        
        if end_date > dates[-1] or end_date < dates[0]:
            end_date = dates[-1] 

        # find start and ending indices; have to convert idx from array to int to slice
        start_idx = int(np.where(dates == start_date)[0])
        end_idx = int(np.where(dates == end_date)[0])
        
        # subset variable and date range; 
        date_subset = dates[start_idx:end_idx + 1] 
        values_subset = values[start_idx:end_idx + 1] 
        
        return date_subset, values_subset

def find_start_end_dates(dates1, dates2):
    """  
    Find start and end dates between two different sized arrays of datetime
    objects.

    Parameters 
    ----------
    dates1 : list
        List of datetime objects.
        
    dates2 : list 
        List of datetime objects.
    
    Returns
    -------
    (start_date, end_date) : tuple 
        Tuple of datetime objects.
    """
    # make sure that dates overlap
    date1_set = set(dates1)    
    date2_set = set(dates2)
       
    if date1_set.intersection(date2_set):
        # pick later of two dates for start date; pick earlier of two dates for end date
        if dates2[0] > dates1[0]: 
            start_date = dates2[0]         
        else:
            start_date = dates1[0]
        
        if dates2[-1] > dates1[-1]: 
            end_date = dates1[-1]        
        else:
            end_date = dates2[-1]

        return start_date, end_date

    else:
       raise ValueError("No matching dates for find_start_end_dates()") 


def create_nan_array(shape, dtype = float):
    """  
    Find start and end dates between two different sized arrays of datetime
    objects.

    Parameters 
    ----------
    shape : tuple 
        Tuple containing shape of desired nan array.
        
    dtype : data type
        Data type desired for the array; e.g. float
    
    Returns
    -------
    nan_array : array
        Array containing only nan values
    """     
    nan_array = np.empty(shape, dtype)
    nan_array.fill(np.nan)
    
    return nan_array


def _print_test_info(expected, actual):
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
   
def main():
    """ Test functionality of helpers """
    
if __name__ == "__main__":
    main()        
    
    