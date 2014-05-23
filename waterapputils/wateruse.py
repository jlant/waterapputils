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

    
def _create_test_data():
    """ Create test data for tests """

    fixture = {} 
    
    fixture["data_file"] = \
        """
        # JFM_WU																								
        # released 2014, March 7																								
        huc12	newhydroid	AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL	LvGwWL	MiGwWL	ReGwWL	TeGwWL	WsGwWL	AqSwWL	CoSwWL	InSwWL	IrSwWL	MiSwWL	TeSwWL	WsSwWL	InGwRT	InSwRT	STswRT	WSgwRT	WSunkTR	WStrans
        20401010101	256	2	0	0	0	0	0	0		0	0	0	0	0	0	0	0	-0.00225682	0	0	0	0		0
        20401010101	241	4	0	0	0	0	0	0		0	0	0	0	0	0	0	0	-0.016137437	0	0	0	0		0
        20401010101	220	6	0	0	0	0	0	0		0	-5.32E-05	0	0	0	0	0	0	-0.021012399	0	0	0	0		0
        20401010101	8	0	0	0	0	0	0	0		0	0	0	0	0	0	0	0	-0.027395508	0	0	0	0		0
        20401010101	12	0	0	0	0	0	0	0		0	-2.65E-06	0	0	0	0	0	0	-0.052423916	0	0	0	0		0
        20401010101	222	3	0	0	0	0	0	0		0	0	0	0	0	0	0	0	-0.058066851	0	0	0	0		0
        20401010102	11	0	0	0	0	0	0	0		0	0	0	0	0	0	0	0	-0.000150877	0	0	0	0		0
        """
