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
        "months": "(#)\s([JFMASOND].+)",
        "column_names": "(huc12)\t(.+)",
        "data_row": "([0-9]{11})\t(.+)"
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

def main():
    
    pass

if __name__ == "__main__":
    main()