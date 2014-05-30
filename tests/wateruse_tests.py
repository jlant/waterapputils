import nose.tools
from nose import with_setup 

import sys
import numpy as np
import datetime
from StringIO import StringIO

# my module
from waterapputils import wateruse

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

# define global to print out tests when actual matches expected
VERBOSE = True

def _perform_assertion(actual, expected, verbose):
    """   
    For testing purposes, assert that all expected values and actual values match. 
    Prints assertion error when there is no match.  Prints values to user to scan
    if verbose is True. Helps a lot for debugging. 
    
    Parameters
    ----------
    expected : dictionary  
        Dictionary holding expected data values
        
    actual : dictionary
        Dictionary holding expected data values
        
    verbose : boolean
        Boolean to print out details when actual matches expected
    """
    for key in actual.keys():
        np.testing.assert_equal(actual[key], expected[key], err_msg = "For key * {} *, actual value(s) * {} * do not equal expected value(s) * {} *".format(key, actual[key], expected[key]))        

        if verbose:
            print >> sys.stderr, "\n*{}*".format(key)
            print >> sys.stderr, "    actual:   {}".format(actual[key])
            print >> sys.stderr, "    expected: {}\n".format(expected[key])

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: wateruse tests"
   
    # set up fixtures 
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
    fixture["data_file_AMJ"] = \
        """
        # AMJ_WU	
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

    fixture["data_file_JAS"] = \
        """
        # JAS_WU	
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

    fixture["data_file_OND"] = \
        """
        # OND_WU	
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

    fixture["ids_256_241_222_220_values"] = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    fixture["ids_12_11_8_values"] = [[1.0, 3.0, 1.0, 3.0, -1.0], [2.0, 6.0, 2.0, 6.0, -1.0], [2.0, 1.0, 2.0, 1.0, -1.0]]

    fixture["wateruse_data_months_AMJ"] = {"months": "AMJ_WU"}
    fixture["wateruse_data_months_JAS"] = {"months": "JAS_WU"}
    fixture["wateruse_data_months_OND"] = {"months": "OND_WU"}

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: wateruse tests" 


def test_read_file_in():

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
    fileobj = StringIO(fixture["data_file_JFM"])
    
    # read file object
    actual = wateruse.read_file_in(fileobj)
    
    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_get_wateruse_values():
    
    # expected values to test with actual values
    expected = {}    
    expected["ids_256_241_222_220"] = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    expected["ids_12_11_8"] = [[1.0, 3.0, 1.0, 3.0, -1.0], [2.0, 6.0, 2.0, 6.0, -1.0], [2.0, 1.0, 2.0, 1.0, -1.0]]
    
    actual = {}
    actual["ids_256_241_222_220"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"])
    actual["ids_12_11_8"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"])

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_sum_values1():
    """ Test sum_values() part 1 - ids [256, 241, 222, 220] """
    
    # expected values to test with actual values
    expected = {}    
    expected["row_wise"] = np.array([ 15.,  20.,  15.,  20., -20.])
    expected["column_wise"] = np.array([ 12.,  10.,  14.,  14.])
    expected["total"] = 50.0

    # actual values       
    actual = wateruse.sum_values(values = fixture["ids_256_241_222_220_values"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)   

def test_sum_values2():
    """ Test sum_values()  part 2 - ids [12, 11, 8] """
    
    # expected values to test with actual values
    expected = {}    
    expected["row_wise"] = np.array([ 5.,  10.,  5.,  10., -3.])
    expected["column_wise"] = np.array([ 7.,  15., 5.])
    expected["total"] = 27.0

    # actual values       
    actual = wateruse.sum_values(values = fixture["ids_12_11_8_values"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)   
    
def test_create_monthly_wateruse_dict1():
    """ Test create_monthly_wateruse_dict() part 1 - testing January, Februray, March """

    # expected values to test with actual values
    expected = {"January": 5.0,
                "February": 5.0,
                "March": 5.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data"], wateruse_value = 5.0)  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)   

def test_create_monthly_wateruse_dict2():
    """ Test create_monthly_wateruse_dict() part 2 - testing April, May, June """

    # expected values to test with actual values
    expected = {"April": 2.0,
                "May": 2.0,
                "June": 2.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data_months_AMJ"], wateruse_value = 2.0)  
   
    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_create_monthly_wateruse_dict3():
    """ Test create_monthly_wateruse_dict() part 3 - testing July, August, September """

    # expected values to test with actual values
    expected = {"July": 3.0,
                "August": 3.0,
                "September": 3.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data_months_JAS"], wateruse_value = 3.0)  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)   

def test_create_monthly_wateruse_dict4():
    """ Test create_monthly_wateruse_dict() part 4 - testing October, November, December """

    # expected values to test with actual values
    expected = {"October": 4.0,
                "November": 4.0,
                "December": 4.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data_months_OND"], wateruse_value = 4.0)  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  
    

def test_get_total_wateruse1():
    """ Test get_total_wateruse() part 1 - ids [256, 241, 222, 220] """    

    # expected values to test with actual values
    expected = {"January": 50.0,
                "February": 50.0,
                "March": 50.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_get_total_wateruse2():
    """ Test get_total_wateruse() part 2 - ids [12, 11, 8] """  

    # expected values to test with actual values
    expected = {"January": 27.0,
                "February": 27.0,
                "March": 27.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_get_all_total_wateruse1():
    """ Test get_all_total_wateruse() part 1 - ids [256, 241, 222, 220] """

    # expected values to test with actual values
    expected = {"January": 50.0,
                "February": 50.0,
                "March": 50.0,
                "April": 50.0,
                "May": 50.0,
                "June": 50.0,
                "July": 50.0,
                "August": 50.0,
                "September": 50.0,
                "October": 50.0,
                "November": 50.0,
                "December": 50.0
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    # actual values       
    actual = wateruse.get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256", "241", "222", "220"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_get_all_total_wateruse2():
    """ Test get_all_total_wateruse() part 2 - ids [12, 11, 8] """

    # expected values to test with actual values
    expected = {"January": 27.0,
                "February": 27.0,
                "March": 27.0,
                "April": 27.0,
                "May": 27.0,
                "June": 27.0,
                "July": 27.0,
                "August": 27.0,
                "September": 27.0,
                "October": 27.0,
                "November": 27.0,
                "December": 27.0
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    # actual values       
    actual = wateruse.get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["12", "11", "8"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)  

def test_get_all_total_wateruse3():
    """ Test get_all_total_wateruse() part 3 - ids [256] """

    # expected values to test with actual values
    expected = {"January": 12.0,
                "February": 12.0,
                "March": 12.0,
                "April": 12.0,
                "May": 12.0,
                "June": 12.0,
                "July": 12.0,
                "August": 12.0,
                "September": 12.0,
                "October": 12.0,
                "November": 12.0,
                "December": 2.0
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    # actual values       
    actual = wateruse.get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256"])  

    # assert equality
    _perform_assertion(actual, expected, verbose = VERBOSE)     