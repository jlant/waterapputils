import nose.tools
from nose import with_setup

import sys
import numpy as np
import datetime

# my module
from waterapputils import helpers

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup fixture for testing """

    print >> sys.stderr, "SETUP: helpers tests"

    fixture["dates"] = np.array([datetime.datetime(2014, 01, 01, 0, 0) + datetime.timedelta(i) for i in range(11)])
    fixture["values"] = np.array([i for i in range(11)])
    
    fixture["shorter_dates"] = np.array([datetime.datetime(2014, 01, 03, 0, 0) + datetime.timedelta(i) for i in range(11)])
    fixture["longer_dates"] = np.array([datetime.datetime(2013, 12, 01, 0, 0) + datetime.timedelta(i) for i in range(180)])

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: helpers tests" 

def test_isfloat():
    
    nose.tools.assert_equals(True, helpers.isfloat(6.25))
    nose.tools.assert_equals(True, helpers.isfloat("6.25"))
    nose.tools.assert_equals(False, helpers.isfloat("2.5_"))
    nose.tools.assert_equals(False, helpers.isfloat("hello"))
   
def test_rmspecialchars():
    
    nose.tools.assert_equals("6.5", helpers.rmspecialchars("*6.5_"))
    nose.tools.assert_equals("4.25", helpers.rmspecialchars("*$^**(@4.25_+;"))    
    nose.tools.assert_equals("-4.1", helpers.rmspecialchars("-4.1")) 

def test_subset_data_dates_within_range():
    
    start = datetime.datetime(2014, 01, 04)
    end = datetime.datetime(2014, 01, 10)    
    
    expected_dates = np.array([datetime.datetime(2014, 1, 4, 0, 0), datetime.datetime(2014, 1, 5, 0, 0),
                               datetime.datetime(2014, 1, 6, 0, 0), datetime.datetime(2014, 1, 7, 0, 0),
                               datetime.datetime(2014, 1, 8, 0, 0), datetime.datetime(2014, 1, 9, 0, 0),
                               datetime.datetime(2014, 1, 10, 0, 0)])

    expected_values = np.array([3, 4, 5, 6, 7, 8, 9])
    
    actual_dates, actual_values = helpers.subset_data(dates = fixture["dates"], 
                                                             values = fixture["values"], 
                                                             start_date = start, 
                                                             end_date = end)

    nose.tools.assert_equals(actual_dates.all(), expected_dates.all())
    nose.tools.assert_equals(actual_values.all(), expected_values.all())

def test_subset_data_dates_outside_range():
    
    start = datetime.datetime(2013, 12, 01)
    end = datetime.datetime(2014, 01, 20)  
    
    expected_dates = np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0),
                               datetime.datetime(2014, 1, 3, 0, 0), datetime.datetime(2014, 1, 4, 0, 0),
                               datetime.datetime(2014, 1, 5, 0, 0), datetime.datetime(2014, 1, 6, 0, 0),
                               datetime.datetime(2014, 1, 7, 0, 0), datetime.datetime(2014, 1, 8, 0, 0),
                               datetime.datetime(2014, 1, 9, 0, 0), datetime.datetime(2014, 1, 10, 0, 0),
                               datetime.datetime(2014, 1, 11, 0, 0)])

    expected_values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    actual_dates, actual_values = helpers.subset_data(dates = fixture["dates"], 
                                                             values = fixture["values"], 
                                                             start_date = start, 
                                                             end_date = end)

    nose.tools.assert_equals(actual_dates.all(), expected_dates.all())
    nose.tools.assert_equals(actual_values.all(), expected_values.all())

def test_find_start_end_dates_shorter_range():

    expected_start_date = datetime.datetime(2014, 01, 03, 0, 0)
    expected_end_date = datetime.datetime(2014, 01, 11, 0, 0)

    actual_start_date, actual_end_date = helpers.find_start_end_dates(fixture["dates"], fixture["shorter_dates"]) 

    nose.tools.assert_equals(actual_start_date, expected_start_date)
    nose.tools.assert_equals(actual_end_date, expected_end_date)

def test_find_start_end_dates_longer_range():

    expected_start_date = datetime.datetime(2014, 01, 01, 0, 0)
    expected_end_date = datetime.datetime(2014, 01, 11, 0, 0)

    actual_start_date, actual_end_date = helpers.find_start_end_dates(fixture["dates"], fixture["longer_dates"]) 

    nose.tools.assert_equals(actual_start_date, expected_start_date)
    nose.tools.assert_equals(actual_end_date, expected_end_date)
