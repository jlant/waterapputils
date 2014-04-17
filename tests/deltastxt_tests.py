import nose.tools
from nose import with_setup 

import sys
import numpy as np
import datetime
from StringIO import StringIO

# my module
from waterapputils import deltastxt

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: deltatxt tests"
   
    # set up fixtures 
    fixture["data file"] = \
        """
        Model	Scenario	Target	Variable	Tile	January	February	March	April	May	June	July	August	September	October	November	December
        CanESM2	rcp45	2030	PET	11	1.3	2.7	3.3	4.7	5.3	6.7	7.3	8.7	9.3	10.7	11.3	12.7
        CanESM2	rcp45	2030	PET	12	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        CanESM2	rcp45	2030	PET	21	1.3	2.9	3.3	4.9	5.3	6.9	7.3	8.9	9.3	10.9	11.3	12.9
        CanESM2	rcp45	2030	PET	22	1.4	2.3	3.4	4.3	5.4	6.3	7.4	8.3	9.4	10.3	11.4	12.3
        CanESM2	rcp45	2030	PET	31	1.5	2.2	3.5	4.2	5.5	6.2	7.5	8.2	9.5	10.2	11.5	12.2
        CanESM2	rcp45	2030	PET	32	1.6	2.3	3.6	4.3	5.6	6.3	7.6	8.3	9.6	10.3	11.6	12.3
        """ 
      
    fixture["sample_data"] = {
       "Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", 
       "Tile": ["11", "12", "21", "22", "31", "32"],
       "January": [1.3, 1.2, 1.3, 1.4, 1.5, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
       "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
       "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
       "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]           
    }    


def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: deltatxt tests"      


    