import nose.tools
from nose import with_setup 

import sys
import numpy as np
import datetime
from StringIO import StringIO

# my module
from waterapputils import deltas

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: deltatxt tests"
   
    # set up fixtures 
    fixture["data_file1"] = \
        """
        Model	Scenario	Target	Variable	Tile	January	February	March	April	May	June	July	August	September	October	November	December
        CanESM2	rcp45	2030	PET	11	1.3	2.7	3.3	4.7	5.3	6.7	7.3	8.7	9.3	10.7	11.3	12.7
        CanESM2	rcp45	2030	PET	12	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        CanESM2	rcp45	2030	PET	21	1.3	2.9	3.3	4.9	5.3	6.9	7.3	8.9	9.3	10.9	11.3	12.9
        CanESM2	rcp45	2030	PET	22	1.4	2.3	3.4	4.3	5.4	6.3	7.4	8.3	9.4	10.3	11.4	12.3
        CanESM2	rcp45	2030	PET	31	1.5	2.2	3.5	4.2	5.5	6.2	7.5	8.2	9.5	10.2	11.5	12.2
        CanESM2	rcp45	2030	PET	32	1.6	2.3	3.6	4.3	5.6	6.3	7.6	8.3	9.6	10.3	11.6	12.3
        """ 

    fixture["data_file2"] = \
        """
        Model	Scenario	Target	Variable	Tile	January	February	March	April	May	June	July	August	September	October	November	December
        GFDL-ESM2G	rcp45	2060	Tmax	11	1.6	2.3	3.6	4.3	5.6	6.3	7.6	8.3	9.6	10.3	11.6	12.3
        GFDL-ESM2G	rcp45	2060	Tmax	12	1.3	2.9	3.3	4.9	5.3	6.9	7.3	8.9	9.3	10.9	11.3	12.9
        GFDL-ESM2G	rcp45	2060	Tmax	21	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        GFDL-ESM2G	rcp45	2060	Tmax	22	1.3	2.7	3.3	4.7	5.3	6.7	7.3	8.7	9.3	10.7	11.3	12.7
        GFDL-ESM2G	rcp45	2060	Tmax	31	1.5	2.2	3.5	4.2	5.5	6.2	7.5	8.2	9.5	10.2	11.5	12.2
        GFDL-ESM2G	rcp45	2060	Tmax	32	1.4	2.3	3.4	4.3	5.4	6.3	7.4	8.3	9.4	10.3	11.4	12.3
        GFDL-ESM2G	rcp45	2060	Tmax	41	1.3	2.7	3.3	4.7	5.3	6.7	7.3	8.7	9.3	10.7	11.3	12.7
        GFDL-ESM2G	rcp45	2060	Tmax	42	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        """ 

    fixture["data_file_bad"] = \
        """
        Model	Scenario	Target	Variable	Tile	January	February	March	April	May	June	July	August	September	October	November	December
        CanESM2	rcp45	2030	PET	11	1.3	2.7	3.3	4.7	5.3	6.7	7.3	8.7	9.3	10.7	11.3	12.7
        CanESM2	rcp45	2030	PET	12	1.2	2.8	3.2	4.8	5.2	6.8	7.2	8.8	9.2	10.8	11.2	12.8
        CanESM2	rcp45	2030	PET	21		2.9	3.3	4.9	5.3	6.9	7.3	8.9	9.3	10.9	11.3	12.9
        CanESM2	rcp45	2030	PET	22	1.4	2.3	3.4	4.3	5.4	6.3	7.4	8.3	9.4	10.3	11.4	12.3
        CanESM2	rcp45	2030	PET	31		2.2	3.5	4.2	5.5	6.2	7.5	8.2	9.5	10.2	11.5	12.2
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

    fixture["sample_data_bad"] = {
       "Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", 
       "Tile": ["11", "12", "21", "22", "31", "32"],
       "January": [1.3, 1.2, 1.3, 1.4, 1.5, np.nan], "February": [2.7, 2.8, 2.9, 2.3, 2.2, np.nan], "March": [3.3, 3.2, 3.3, 3.4, 3.5, np.nan],
       "April": [4.7, 4.8, 4.9, 4.3, 4.2, np.nan], "May": [5.3, 5.2, 5.3, 5.4, 5.5, np.nan], "June": [6.7, 6.8, 6.9, 6.3, 6.2, np.nan],
       "July": [7.3, 7.2, 7.3, 7.4, 7.5, np.nan], "August": [8.7, 8.8, 8.9, 8.3, 8.2, np.nan], "September": [9.3, 9.2, 9.3, 9.4, 9.5, np.nan],
       "October": [10.7, 10.8, 10.9, 10.3, 10.2, np.nan], "November": [11.3, 11.2, 11.3, 11.4, 11.5, np.nan], "December": [12.7, 12.8, 12.9, 12.3, 12.2, np.nan]           
    }  

    fixture["sample_monthly_values1"] = [[1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11.1, 12.2]]

    fixture["sample_monthly_values2"] = [[1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11.1, 12.2], [1.9, 2.8, 3.7, 4.6, 5.5, 6.4, 7.3, 8.2, 9.1, 10.0, 11.9, 12.8]]

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: deltatxt tests"      

def test_read_file_in_data_file1():
 
    expected = {"Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", "Tile": ['11', '12', '21', '22', '31', '32'],
                "January": [1.3, 1.2, 1.3, 1.4, 1.5, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
       "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
       "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
       "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]
    }          
     
    fileobj = StringIO(fixture["data_file1"])
    
    actual = deltas.read_file_in(fileobj)

    nose.tools.assert_equals(expected.keys(), actual.keys())
    nose.tools.assert_equals(expected["Model"], actual["Model"])
    nose.tools.assert_equals(expected["Scenario"], actual["Scenario"])
    nose.tools.assert_equals(expected["Target"], actual["Target"])
    nose.tools.assert_equals(expected["Tile"], actual["Tile"])
       
    nose.tools.assert_equals(expected["January"], actual["January"])
    nose.tools.assert_equals(expected["February"], actual["February"])
    nose.tools.assert_equals(expected["April"], actual["April"])
    nose.tools.assert_equals(expected["May"], actual["May"])
    nose.tools.assert_equals(expected["June"], actual["June"])
    nose.tools.assert_equals(expected["July"], actual["July"])
    nose.tools.assert_equals(expected["August"], actual["August"])
    nose.tools.assert_equals(expected["September"], actual["September"])
    nose.tools.assert_equals(expected["October"], actual["October"])
    nose.tools.assert_equals(expected["November"], actual["November"])
    nose.tools.assert_equals(expected["December"], actual["December"])

def test_read_file_in_data_file2():
     
    expected = {
        "Model": "GFDL-ESM2G", "Scenario": "rcp45", "Target": "2060", "Variable": "Tmax", "Tile": ['11', '12', '21', '22', '31', '32', '41', '42'],
        "January": [1.6, 1.3, 1.2, 1.3, 1.5, 1.4, 1.3, 1.2], "February": [2.3, 2.9, 2.8, 2.7, 2.2, 2.3, 2.7, 2.8], "March": [3.6, 3.3, 3.2, 3.3, 3.5, 3.4, 3.3, 3.2],
        "April": [4.3, 4.9, 4.8, 4.7, 4.2, 4.3, 4.7, 4.8], "May": [5.6, 5.3, 5.2, 5.3, 5.5, 5.4, 5.3, 5.2], "June": [6.3, 6.9, 6.8, 6.7, 6.2, 6.3, 6.7, 6.8],
        "July": [7.6, 7.3, 7.2, 7.3, 7.5, 7.4, 7.3, 7.2], "August": [8.3, 8.9, 8.8, 8.7, 8.2, 8.3, 8.7, 8.8], "September": [9.6, 9.3, 9.2, 9.3, 9.5, 9.4, 9.3, 9.2],
        "October": [10.3, 10.9, 10.8, 10.7, 10.2, 10.3, 10.7, 10.8], "November": [11.6, 11.3, 11.2, 11.3, 11.5, 11.4, 11.3, 11.2], "December": [12.3, 12.9, 12.8, 12.7, 12.2, 12.3, 12.7, 12.8]
    }    
     
    fileobj = StringIO(fixture["data_file2"])
    
    actual = deltas.read_file_in(fileobj)

    nose.tools.assert_equals(expected.keys(), actual.keys())
    nose.tools.assert_equals(expected["Model"], actual["Model"])
    nose.tools.assert_equals(expected["Scenario"], actual["Scenario"])
    nose.tools.assert_equals(expected["Target"], actual["Target"])
    nose.tools.assert_equals(expected["Tile"], actual["Tile"])
       
    nose.tools.assert_equals(expected["January"], actual["January"])
    nose.tools.assert_equals(expected["February"], actual["February"])
    nose.tools.assert_equals(expected["April"], actual["April"])
    nose.tools.assert_equals(expected["May"], actual["May"])
    nose.tools.assert_equals(expected["June"], actual["June"])
    nose.tools.assert_equals(expected["July"], actual["July"])
    nose.tools.assert_equals(expected["August"], actual["August"])
    nose.tools.assert_equals(expected["September"], actual["September"])
    nose.tools.assert_equals(expected["October"], actual["October"])
    nose.tools.assert_equals(expected["November"], actual["November"])
    nose.tools.assert_equals(expected["December"], actual["December"])

def test_read_file_in_data_file_bad():
 
    expected = {"Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", "Tile": ['11', '12', '21', '22', '31', '32'],
                "January": [1.3, 1.2, np.nan, 1.4, np.nan, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
       "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
       "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
       "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]
    }          
     
    fileobj = StringIO(fixture["data_file_bad"])
    
    actual = deltas.read_file_in(fileobj)

    nose.tools.assert_equals(expected.keys(), actual.keys())
    nose.tools.assert_equals(expected["Model"], actual["Model"])
    nose.tools.assert_equals(expected["Scenario"], actual["Scenario"])
    nose.tools.assert_equals(expected["Target"], actual["Target"])
    nose.tools.assert_equals(expected["Tile"], actual["Tile"])
       
    nose.tools.assert_equals(np.array(expected["January"]).all(), np.array(actual["January"]).all())
    nose.tools.assert_equals(expected["February"], actual["February"])
    nose.tools.assert_equals(expected["April"], actual["April"])
    nose.tools.assert_equals(expected["May"], actual["May"])
    nose.tools.assert_equals(expected["June"], actual["June"])
    nose.tools.assert_equals(expected["July"], actual["July"])
    nose.tools.assert_equals(expected["August"], actual["August"])
    nose.tools.assert_equals(expected["September"], actual["September"])
    nose.tools.assert_equals(expected["October"], actual["October"])
    nose.tools.assert_equals(expected["November"], actual["November"])
    nose.tools.assert_equals(expected["December"], actual["December"])
    
def test_get_monthly_values():

    expected1 = [[1.3, 2.7, 3.3, 4.7, 5.3, 6.7, 7.3, 8.7, 9.3, 10.7, 11.3, 12.7], [1.2, 2.8, 3.2, 4.8, 5.2, 6.8, 7.2, 8.8, 9.2, 10.8, 11.2, 12.8]]

    actual1 = deltas.get_monthly_values(delta_data = fixture["sample_data"], tile_list = ["11", "12"])

    nose.tools.assert_equals(expected1[0], actual1[0])
    nose.tools.assert_equals(expected1[1], actual1[1])
    
    expected2 = [[1.2, 2.8, 3.2, 4.8, 5.2, 6.8, 7.2, 8.8, 9.2, 10.8, 11.2, 12.8], [1.4, 2.3, 3.4, 4.3, 5.4, 6.3, 7.4, 8.3, 9.4, 10.3, 11.4, 12.3], [1.6, 2.3, 3.6, 4.3, 5.6, 6.3, 7.6, 8.3, 9.6, 10.3, 11.6, 12.3]]

    actual2 = deltas.get_monthly_values(delta_data = fixture["sample_data"], tile_list = ["12", "22", "32"])

    nose.tools.assert_equals(expected2[0], actual2[0])
    nose.tools.assert_equals(expected2[1], actual2[1])
    nose.tools.assert_equals(expected2[2], actual2[2])

def test_format_to_monthly_dict():
    """ Test format_to_monthly_dict functionality """

    expected1 = {'January': [1.1], 'February': [2.2], 'March': [3.3], 'April': [4.4], 'May': [5.5], 'June': [6.6], 'July': [7.7], 'August': [8.8], 'September': [9.9], 'October': [10.0], 'November': [11.1], 'December': [12.2]}
    expected2 = {'January': [1.1, 1.9], 'February': [2.2, 2.8], 'March': [3.3, 3.7], 'April': [4.4, 4.6], 'May': [5.5, 5.5], 'June': [6.6, 6.4], 'July': [7.7, 7.3], 'August': [8.8, 8.2], 'September': [9.9, 9.1], 'October': [10.0, 10.0], 'November': [11.1, 11.9], 'December': [12.2, 12.8]}    

    actual1 = deltas.format_to_monthly_dict(values = fixture["sample_monthly_values1"])
    actual2 = deltas.format_to_monthly_dict(values = fixture["sample_monthly_values2"])

    nose.tools.assert_equals(expected1["January"], actual1["January"])
    nose.tools.assert_equals(expected1["February"], actual1["February"])
    nose.tools.assert_equals(expected1["April"], actual1["April"])
    nose.tools.assert_equals(expected1["May"], actual1["May"])
    nose.tools.assert_equals(expected1["June"], actual1["June"])
    nose.tools.assert_equals(expected1["July"], actual1["July"])
    nose.tools.assert_equals(expected1["August"], actual1["August"])
    nose.tools.assert_equals(expected1["September"], actual1["September"])
    nose.tools.assert_equals(expected1["October"], actual1["October"])
    nose.tools.assert_equals(expected1["November"], actual1["November"])
    nose.tools.assert_equals(expected1["December"], actual1["December"])
    
    nose.tools.assert_equals(expected2["January"], actual2["January"])
    nose.tools.assert_equals(expected2["February"], actual2["February"])
    nose.tools.assert_equals(expected2["April"], actual2["April"])
    nose.tools.assert_equals(expected2["May"], actual2["May"])
    nose.tools.assert_equals(expected2["June"], actual2["June"])
    nose.tools.assert_equals(expected2["July"], actual2["July"])
    nose.tools.assert_equals(expected2["August"], actual2["August"])
    nose.tools.assert_equals(expected2["September"], actual2["September"])
    nose.tools.assert_equals(expected2["October"], actual2["October"])
    nose.tools.assert_equals(expected2["November"], actual2["November"])
    nose.tools.assert_equals(expected2["December"], actual2["December"])

def test_calculate_avg_delta_values1():
    
    expected = {'PET' : {'January': 1.25, 'February': 2.75, 'March': 3.25, 'April': 4.75, 'May': 5.25, 'June': 6.75, 'July': 7.25, 'August': 8.75, 'September': 9.25, 'October': 10.75, 'November': 11.25, 'December': 12.75}}    
    
    actual = deltas.calculate_avg_delta_values(deltas_data = fixture["sample_data"], tile_list = ["11", "12"])
    
    nose.tools.assert_equals(expected["PET"]["January"], actual["PET"]["January"])
    nose.tools.assert_equals(expected["PET"]["February"], actual["PET"]["February"])
    nose.tools.assert_equals(expected["PET"]["April"], actual["PET"]["April"])
    nose.tools.assert_equals(expected["PET"]["May"], actual["PET"]["May"])
    nose.tools.assert_equals(expected["PET"]["June"], actual["PET"]["June"])
    nose.tools.assert_equals(expected["PET"]["July"], actual["PET"]["July"])
    nose.tools.assert_equals(expected["PET"]["August"], actual["PET"]["August"])
    nose.tools.assert_equals(expected["PET"]["September"], actual["PET"]["September"])
    nose.tools.assert_equals(expected["PET"]["October"], actual["PET"]["October"])
    nose.tools.assert_equals(expected["PET"]["November"], actual["PET"]["November"])
    nose.tools.assert_equals(expected["PET"]["December"], actual["PET"]["December"])    

def test_calculate_avg_delta_values2():
    
    expected = {'PET' : {'January': 1.3666666666666667, 'February': 2.6, 'March': 3.3666666666666667, 'April': 4.6, 'May': 5.3666666666666667, 'June': 6.6, 'July': 7.3666666666666667, 'August': 8.6, 'September': 9.3666666666666667, 'October': 10.6, 'November': 11.3666666666666667, 'December': 12.6}}    
    
    actual = deltas.calculate_avg_delta_values(deltas_data = fixture["sample_data"], tile_list = ["11", "12", "32"])
    
    nose.tools.assert_almost_equals(expected["PET"]["January"], actual["PET"]["January"])
    nose.tools.assert_almost_equals(expected["PET"]["February"], actual["PET"]["February"])
    nose.tools.assert_almost_equals(expected["PET"]["April"], actual["PET"]["April"])
    nose.tools.assert_almost_equals(expected["PET"]["May"], actual["PET"]["May"])
    nose.tools.assert_almost_equals(expected["PET"]["June"], actual["PET"]["June"])
    nose.tools.assert_almost_equals(expected["PET"]["July"], actual["PET"]["July"])
    nose.tools.assert_almost_equals(expected["PET"]["August"], actual["PET"]["August"])
    nose.tools.assert_almost_equals(expected["PET"]["September"], actual["PET"]["September"])
    nose.tools.assert_almost_equals(expected["PET"]["October"], actual["PET"]["October"])
    nose.tools.assert_almost_equals(expected["PET"]["November"], actual["PET"]["November"])
    nose.tools.assert_almost_equals(expected["PET"]["December"], actual["PET"]["December"]) 
    
def test_calculate_avg_delta_values3():
    
    expected = {'PET' : {'January': 1.25, 'February': 2.75, 'March': 3.25, 'April': 4.75, 'May': 5.25, 'June': 6.75, 'July': 7.25, 'August': 8.75, 'September': 9.25, 'October': 10.75, 'November': 11.25, 'December': 12.75}}    
    
    actual = deltas.calculate_avg_delta_values(deltas_data = fixture["sample_data_bad"], tile_list = ["11", "12"])
    
    nose.tools.assert_equals(np.array(expected["PET"]["January"]).all(), np.array(actual["PET"]["January"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["February"]).all(), np.array(actual["PET"]["February"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["April"]).all(), np.array(actual["PET"]["April"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["May"]).all(), np.array(actual["PET"]["May"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["June"]).all(), np.array(actual["PET"]["June"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["July"]).all(), np.array(actual["PET"]["July"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["August"]).all(), np.array(actual["PET"]["August"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["September"]).all(), np.array(actual["PET"]["September"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["October"]).all(), np.array(actual["PET"]["October"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["November"]).all(), np.array(actual["PET"]["November"]).all())
    nose.tools.assert_equals(np.array(expected["PET"]["December"]).all(), np.array(actual["PET"]["December"]).all())   
    
    
    
    
    
    
    
    
    