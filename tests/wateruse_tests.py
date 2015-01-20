from __future__ import print_function
import sys
import numpy as np
from StringIO import StringIO

# my module
from waterapputils.modules import wateruse

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print("SETUP: wateruse tests", file = sys.stdout) 
    
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

    fixture["factor_file"] = \
        """
        # water use factors																									
        AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL
        2	      2	      2	      2	      2
        """

    fixture["factor_file_variable"] = \
        """
        # water use factors																									
        AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL
        2	      3	      4	      5	      6
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

    fixture["wateruse_factors"] = {"column_names": ["AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL"],
                                   "AqGwWL": 2.0,
                                   "CoGwWL": 2.0,
                                   "DoGwWL": 2.0,
                                   "InGwWL": 2.0,
                                   "IrGwWL": 2.0
    }

    fixture["wateruse_factors_variable"] = {"column_names": ["AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL"],
                                           "AqGwWL": 2.0,
                                           "CoGwWL": 3.0,
                                           "DoGwWL": 4.0,
                                           "InGwWL": 5.0,
                                           "IrGwWL": 6.0
    }

def teardown():
    """ Print to standard error when all tests are finished """
    
    print("SETUP: wateruse tests", file = sys.stdout) 


def _perform_assertion(actual, expected, description = "", do_almost_equal = False):
    """   
    For testing purposes, assert that all expected values and actual values match. 
    Prints assertion error when there is no match.  Prints values to user to scan
    if verbose is True. Helps a lot for debugging and creates a log of tests. 
    
    Parameters
    ----------
    expected : dictionary  
        Dictionary holding expected data values
        
    actual : dictionary
        Dictionary holding expected data values
           
    Notes
    -----
    In order to capture stdout, need to run nosetests with -s or --nocapture flag    
    
    nosetests -s
    
    OR 
    
    nostests --nocapture
    """
    # print description to stderr 
    print("\n--- " + description + " ---\n", file = sys.stdout)  

    # for each in the actual result, assert equality to expected and print error message if actual does not equal expected. 
    for key in actual.keys():
        if do_almost_equal:
            np.testing.assert_almost_equal(actual[key], expected[key], err_msg = "For key * {} *, actual value(s) * {} * do not equal expected value(s) * {} *".format(key, actual[key], expected[key]))        
        else:
            np.testing.assert_equal(actual[key], expected[key], err_msg = "For key * {} *, actual value(s) * {} * do not equal expected value(s) * {} *".format(key, actual[key], expected[key]))        

        #print details to stderr; nosetests only displays stderr so displaying to stderr instead of stdout
        print("*{}*".format(key), file = sys.stdout) 
        print("    actual:   {}".format(actual[key]), file = sys.stdout) 
        print("    expected: {}\n".format(expected[key]), file = sys.stdout) 

def _get_all_total_wateruse_for_tests(wateruse_files, id_list, wateruse_factor_file = None, in_cfs = False):
    """ Test get_all_total_wateruse - strictly a test function here that mirrors get_all_total_wateruse in water.py but creates fileobj from StringIO instead of reading a file path """

    # calculate average values for a list of water use files
    all_total_wateruse_dict = {}
    for wateruse_file in wateruse_files:
        fileobj = StringIO(wateruse_file)
        wateruse_data = wateruse.read_file_in(fileobj) 

        # if water use factor file is supplied, then apply factors        
        if wateruse_factor_file:
            # read water use factor file
            fileobj_factors = StringIO(wateruse_factor_file)
            wateruse_factors = wateruse.read_factor_file_in(fileobj_factors)
                
            # calculate average wateruse for a list of ids
            total_wateruse_dict = wateruse.get_total_wateruse(wateruse_data = wateruse_data, id_list = id_list, wateruse_factors = wateruse_factors)

        else:
            # calculate average wateruse for a list of ids
            total_wateruse_dict = wateruse.get_total_wateruse(wateruse_data = wateruse_data, id_list = id_list)

        # convert values to cfs
        if in_cfs:
            for key, value in total_wateruse_dict.iteritems():
                value_cfs = wateruse.convert_wateruse_units(value)
                total_wateruse_dict[key] = value_cfs
        
        # update dictionary 
        all_total_wateruse_dict.update(total_wateruse_dict)   
    
    return all_total_wateruse_dict

def test_read_file_in():
    """ Test read_file_in() """

    # description of test    
    description = "Test read_file_in() - test reading of water use files; using simplified water use formatted file"

    # expected values to test with actual values
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
    _perform_assertion(actual, expected, description = description)  

def test_read_factor_file_in():
    """ Test read_factor_file_in() """
    
    # description of test    
    description = "Test read_file_in() - test reading of water use files; using simplified water use formatted file"

    # expected values
    expected = {"column_names": ["AqGwWL", "CoGwWL", "DoGwWL", "InGwWL", "IrGwWL"],
                "AqGwWL": 2.0,
                "CoGwWL": 2.0,
                "DoGwWL": 2.0,
                "InGwWL": 2.0,
                "IrGwWL": 2.0
    }
    
    # create test data
    fileobj = StringIO(fixture["factor_file"])
    
    # read file object
    actual = wateruse.read_factor_file_in(fileobj)
   
    # assert equality
    _perform_assertion(actual, expected, description = description)

def test_get_wateruse_values1():
    """ Test get_wateruse_values() """    

    # description of test        
    description = "Test get_wateruse_values() part 1 - test getting water use values for a particular list of id (hydroid) values WITHOUT water use factors"     
    
    # expected values to test with actual values
    expected = {}    
    expected["ids_256_241_222_220"] = [[2.0, 5.0, 2.0, 5.0, -2.0], [4.0, 3.0, 4.0, 3.0, -4.0], [6.0, 4.0, 6.0, 4.0, -6.0], [3.0, 8.0, 3.0, 8.0, -8.0]]
    expected["ids_12_11_8"] = [[1.0, 3.0, 1.0, 3.0, -1.0], [2.0, 6.0, 2.0, 6.0, -1.0], [2.0, 1.0, 2.0, 1.0, -1.0]]
    
    actual = {}
    actual["ids_256_241_222_220"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"])
    actual["ids_12_11_8"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"])

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_wateruse_values2():
    """ Test get_wateruse_values() """    

    # description of test        
    description = "Test get_wateruse_values() part 2 - test getting water use values for a particular list of id (hydroid) values WITH water use factors"     
    
    # expected values to test with actual values
    expected = {}    
    expected["ids_256_241_222_220"] = [[4.0, 10.0, 4.0, 10.0, -4.0], [8.0, 6.0, 8.0, 6.0, -8.0], [12.0, 8.0, 12.0, 8.0, -12.0], [6.0, 16.0, 6.0, 16.0, -16.0]]
    expected["ids_12_11_8"] = [[2.0, 6.0, 2.0, 6.0, -2.0], [4.0, 12.0, 4.0, 12.0, -2.0], [4.0, 2.0, 4.0, 2.0, -2.0]]
    
    actual = {}
    actual["ids_256_241_222_220"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"], wateruse_factors = fixture["wateruse_factors"])
    actual["ids_12_11_8"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"], wateruse_factors = fixture["wateruse_factors"])

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_wateruse_values3():
    """ Test get_wateruse_values() """    

    # description of test        
    description = "Test get_wateruse_values() part 3 - test getting water use values for a particular list of id (hydroid) values WITH water use factors that are VARIABLE"     
    
    # expected values to test with actual values
    expected = {}    
    expected["ids_256_241_222_220"] = [[4.0, 15.0, 8.0, 25.0, -12.0], [8.0, 9.0, 16.0, 15.0, -24.0], [12.0, 12.0, 24.0, 20.0, -36.0], [6.0, 24.0, 12.0, 40.0, -48.0]]
    expected["ids_12_11_8"] = [[2.0, 9.0, 4.0, 15.0, -6.0], [4.0, 18.0, 8.0, 30.0, -6.0], [4.0, 3.0, 8.0, 5.0, -6.0]]
    
    actual = {}
    actual["ids_256_241_222_220"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"], wateruse_factors = fixture["wateruse_factors_variable"])
    actual["ids_12_11_8"] = wateruse.get_wateruse_values(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"], wateruse_factors = fixture["wateruse_factors_variable"])

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_sum_values1():
    """ Test sum_values() part 1 - ids [256, 241, 222, 220] """

    # description of test        
    description = "Test sum_values() : part 1 - test calculating sums (row wise, column wise, and total) for a list of lists using ids = [256, 241, 222, 220]"     
    
    # expected values to test with actual values
    expected = {}    
    expected["row_wise"] = np.array([ 15.,  20.,  15.,  20., -20.])
    expected["column_wise"] = np.array([ 12.,  10.,  14.,  14.])
    expected["total"] = 50.0

    # actual values       
    actual = wateruse.sum_values(values = fixture["ids_256_241_222_220_values"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)   

def test_sum_values2():
    """ Test sum_values()  part 2 - ids [12, 11, 8] """

    # description of test        
    description = "Test sum_values() : part 2 - test calculating sums (row wise, column wise, and total) for a list of lists using ids = [12, 11, 8]"     
    
    # expected values to test with actual values
    expected = {}    
    expected["row_wise"] = np.array([ 5.,  10.,  5.,  10., -3.])
    expected["column_wise"] = np.array([ 7.,  15., 5.])
    expected["total"] = 27.0

    # actual values       
    actual = wateruse.sum_values(values = fixture["ids_12_11_8_values"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)   

def test_convert_wateruse_units():
    """ Test convert_wateruse_units() """
    
    description = "Test convert_wateruse_units() which converts from mega gallons per day to cubic feet per second"

    # expected values
    expected = {"1": 1.5472337962962963,
                "5": 7.736168981481482
    }
    
    # read file object
    actual = {"1" : wateruse.convert_wateruse_units(value = 1.),
              "5" : wateruse.convert_wateruse_units(value = 5.)
    }
    
    # assert equality
    _perform_assertion(actual, expected, description = description) 
    
def test_create_monthly_wateruse_dict1():
    """ Test create_monthly_wateruse_dict() part 1 - testing January, Februray, March """

    # description of test        
    description = "Test sum_values() : part 1 - test creating a dictionary with monthly keys (January, Februray, March) having values that correspond to the sum total water use"     

    # expected values to test with actual values
    expected = {"January": 5.0,
                "February": 5.0,
                "March": 5.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data"], wateruse_value = 5.0)  

    # assert equality
    _perform_assertion(actual, expected, description = description)   

def test_create_monthly_wateruse_dict2():
    """ Test create_monthly_wateruse_dict() part 2 - testing April, May, June """

    # description of test        
    description = "Test sum_values() : part 2 - test creating a dictionary with monthly keys (April, May, June) having values that correspond to the sum total water use"     

    # expected values to test with actual values
    expected = {"April": 2.0,
                "May": 2.0,
                "June": 2.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data_months_AMJ"], wateruse_value = 2.0)  
   
    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_create_monthly_wateruse_dict3():
    """ Test create_monthly_wateruse_dict() part 3 - testing July, August, September """

    # description of test        
    description = "Test sum_values() : part 3 - test creating a dictionary with monthly keys (July, August, September) having values that correspond to the sum total water use"     

    # expected values to test with actual values
    expected = {"July": 3.0,
                "August": 3.0,
                "September": 3.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data_months_JAS"], wateruse_value = 3.0)  

    # assert equality
    _perform_assertion(actual, expected, description = description)   

def test_create_monthly_wateruse_dict4():
    """ Test create_monthly_wateruse_dict() part 4 - testing October, November, December """

    # description of test        
    description = "Test sum_values() : part 4 - test creating a dictionary with monthly keys (October, November, December) having values that correspond to the sum total water use"     

    # expected values to test with actual values
    expected = {"October": 4.0,
                "November": 4.0,
                "December": 4.0,
    } 

    # actual values       
    actual = wateruse.create_monthly_wateruse_dict(wateruse_data = fixture["wateruse_data_months_OND"], wateruse_value = 4.0)  

    # assert equality
    _perform_assertion(actual, expected, description = description)  
    

def test_get_total_wateruse1():
    """ Test get_total_wateruse() part 1 - ids [256, 241, 222, 220] """    

    # description of test        
    description = "Test get_total_wateruse() : part 1 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220]"     

    # expected values to test with actual values
    expected = {"January": 50.0,
                "February": 50.0,
                "March": 50.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_total_wateruse2():
    """ Test get_total_wateruse() part 2 - ids [12, 11, 8] """  

    # description of test        
    description = "Test get_total_wateruse() : part 2 - test getting the total sum of water use for ids (hydroids) [12, 11, 8]"     

    # expected values to test with actual values
    expected = {"January": 27.0,
                "February": 27.0,
                "March": 27.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_total_wateruse3():
    """ Test get_total_wateruse() part 3 - ids [256, 241, 222, 220]  WITH water use factors"""    

    # description of test        
    description = "Test get_total_wateruse() : part 3 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] WITH water use factors"     

    # expected values to test with actual values
    expected = {"January": 100.0,
                "February": 100.0,
                "March": 100.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"], wateruse_factors = fixture["wateruse_factors"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_total_wateruse4():
    """ Test get_total_wateruse() part 4 - ids [256, 241, 222, 220]  WITH water use factors"""    

    # description of test        
    description = "Test get_total_wateruse() : part 4 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] WITH water use factors that are VARIABLE"     

    # expected values to test with actual values
    expected = {"January": 130.0,
                "February": 130.0,
                "March": 130.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["256", "241", "222", "220"], wateruse_factors = fixture["wateruse_factors_variable"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_total_wateruse5():
    """ Test get_total_wateruse() part 5 - ids [12, 11, 8] WITH water use factors"""    

    # description of test        
    description = "Test get_total_wateruse() : part 5 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] WITH water use factors that are VARIABLE"     

    # expected values to test with actual values
    expected = {"January": 92.0,
                "February": 92.0,
                "March": 92.0,
    }  

    # actual values       
    actual = wateruse.get_total_wateruse(wateruse_data = fixture["wateruse_data"], id_list = ["12", "11", "8"], wateruse_factors = fixture["wateruse_factors_variable"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  


def test_get_all_total_wateruse1():
    """ Test get_all_total_wateruse() part 1 - ids [256, 241, 222, 220] """

    # description of test        
    description = "Test get_all_total_wateruse() : part 1 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] for multiple water use files (the entire year)"     

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
    actual = _get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256", "241", "222", "220"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_all_total_wateruse2():
    """ Test get_all_total_wateruse() part 2 - ids [12, 11, 8] """

    # description of test        
    description = "Test get_all_total_wateruse() : part 2 - test getting the total sum of water use for ids (hydroids) [12, 11, 8] for multiple water use files (the entire year)"     

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
    actual = _get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["12", "11", "8"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)  

def test_get_all_total_wateruse3():
    """ Test get_all_total_wateruse() part 3 - ids [256] """

    # description of test        
    description = "Test get_all_total_wateruse() : part 3 - test getting the total sum of water use for ids (hydroids) [256] for multiple water use files (the entire year)"     

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
                "December": 12.0
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    # actual values       
    actual = _get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256"])  

    # assert equality
    _perform_assertion(actual, expected, description = description)     
    
def test_get_all_total_wateruse4():
    """ Test get_all_total_wateruse() part 4 - ids [256, 241, 222, 220] WITH water use factors """

    # description of test        
    description = "Test get_all_total_wateruse() : part 4 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] for multiple water use files (the entire year) WITH water use factors"     

    # expected values to test with actual values
    expected = {"January": 100.0,
                "February": 100.0,
                "March": 100.0,
                "April": 100.0,
                "May": 100.0,
                "June": 100.0,
                "July": 100.0,
                "August": 100.0,
                "September": 100.0,
                "October": 100.0,
                "November": 100.0,
                "December": 100.0
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    wateruse_factor_file = fixture["factor_file"]

    # actual values       
    actual = _get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256", "241", "222", "220"], wateruse_factor_file = wateruse_factor_file)  

    # assert equality
    _perform_assertion(actual, expected, description = description) 

def test_get_all_total_wateruse5():
    """ Test get_all_total_wateruse() part 5 - ids [256, 241, 222, 220] WITH water use factors """

    # description of test        
    description = "Test get_all_total_wateruse() : part 5 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] for multiple water use files (the entire year) WITH water use factors that are VARIABLE"     

    # expected values to test with actual values
    expected = {"January": 130.0,
                "February": 130.0,
                "March": 130.0,
                "April": 130.0,
                "May": 130.0,
                "June": 130.0,
                "July": 130.0,
                "August": 130.0,
                "September": 130.0,
                "October": 130.0,
                "November": 130.0,
                "December": 130.0
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    wateruse_factor_file = fixture["factor_file_variable"]

    # actual values       
    actual = _get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256", "241", "222", "220"], wateruse_factor_file = wateruse_factor_file)  

    # assert equality
    _perform_assertion(actual, expected, description = description)

def test_get_all_total_wateruse6():
    """ Test get_all_total_wateruse() part 6 - ids [256, 241, 222, 220] WITH water use factors """

    # description of test        
    description = "Test get_all_total_wateruse() : part 5 - test getting the total sum of water use for ids (hydroids) [256, 241, 222, 220] for multiple water use files (the entire year) WITH water use factors that are VARIABLE in CFS"     

    # expected values to test with actual values
    expected = {"January": 201.140393519,
                "February": 201.140393519,
                "March": 201.140393519,
                "April": 201.140393519,
                "May": 201.140393519,
                "June": 201.140393519,
                "July": 201.140393519,
                "August": 201.140393519,
                "September": 201.140393519,
                "October": 201.140393519,
                "November": 201.140393519,
                "December": 201.140393519
    } 

    # make a list of water use files   
    wateruse_files_list = [fixture["data_file_JFM"], fixture["data_file_AMJ"], fixture["data_file_JAS"], fixture["data_file_OND"]]

    wateruse_factor_file = fixture["factor_file_variable"]

    # actual values       
    actual = _get_all_total_wateruse_for_tests(wateruse_files = wateruse_files_list, id_list = ["256", "241", "222", "220"], wateruse_factor_file = wateruse_factor_file, in_cfs = True)  

    # assert equality
    _perform_assertion(actual, expected, description = description, do_almost_equal = True)