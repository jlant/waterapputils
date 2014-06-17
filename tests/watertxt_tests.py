import nose.tools
from nose import with_setup 

import sys, os
import numpy as np
import datetime
from StringIO import StringIO

# my module
from waterapputils import watertxt

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: watertxt tests"
   
    # set up fixtures 
    fixture["date_str"] = "4/9/2014"
    
    fixture["data_file_clean"] = \
        """
         ------------------------------------------------------------------------------
         ----- WATER ------------------------------------------------------------------
         ------------------------------------------------------------------------------
        User:	jlant
        Date:	4/9/2014 15:50:47 PM
        StationID:	012345
        Date	Discharge (cfs)	Subsurface Flow (mm/day)	Impervious Flow (mm/day)	Infiltration Excess (mm/day)	Initial Abstracted Flow (mm/day)	Overland Flow (mm/day)	PET (mm/day)	AET(mm/day)	Average Soil Root zone (mm)	Average Soil Unsaturated Zone (mm)	Snow Pack (mm)	Precipitation (mm/day)	Storage Deficit (mm/day)	Return Flow (mm/day)
        4/1/2014	2.0	50.0	2	0	0.1	3.0	5	5	40.0	4.0	150	0.5	300.0	-5.0
        4/2/2014	6.0	55.0	8	1.5	0.2	9.0	3	12	50.0	3.0	125	0.4	310.0	-4.5
        4/3/2014	10.0	45.0	2	1.5	0.3	3.0	13	13	60.0	2.0	25	0.3	350.0	-4.0
        """   

    fixture["data_file_bad_single_parameter"] = \
        """
         ------------------------------------------------------------------------------
         ----- WATER ------------------------------------------------------------------
         ------------------------------------------------------------------------------
        User:	jlant
        Date:	4/10/2014 00:00:00 PM
        StationID:	000000
        Date	Discharge (cfs)	Subsurface Flow (mm/day)
        4/1/2014	5.0	50.0	
        4/2/2014	10.0	55.0	
        4/3/2014		60.0	
        4/4/2014		65.0	
        4/5/2014	5.5	45.0	
        """   

    # create a sample data set    
    dates = np.array([datetime.datetime(2014, 04, 01, 0, 0), 
                      datetime.datetime(2014, 04, 02, 0, 0), 
                      datetime.datetime(2014, 04, 03, 0, 0),
    ])
    
    discharge_data = np.array([2, 6, 10])
    subsurface_data = np.array([50, 55, 45])
    impervious_data = np.array([2, 8, 2])
    infiltration_data = np.array([0, 1.5, 1.5])
    initialabstracted_data = np.array([0.1, 0.2, 0.3])
    overlandflow_data = np.array([3, 9, 3])
    pet_data = np.array([5, 3, 13])
    aet_data = np.array([5, 12, 13])
    avgsoilrootzone_data = np.array([40, 50, 60])
    avgsoilunsaturatedzone_data = np.array([4, 3, 2])
    snowpack_data = np.array([150, 125, 25])
    precipitation_data = np.array([0.5, 0.4, 0.3])
    storagedeficit_data = np.array([300, 310, 350])
    returnflow_data = np.array([-5.0, -4.5, -4.0])
    
    fixture["sample_data_dict"] = {
        "user": "jlant",
        "date_created": "4/9/2014 15:50:47 PM",
        "stationid": "012345",
        "column_names": ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'],
        "dates": dates,
        "parameters": [
            {"name": "Discharge (cfs)",
            "index": 0,
            "data": discharge_data,
            "mean": np.mean(discharge_data),
            "max": np.max(discharge_data),
            "min": np.min(discharge_data)
            },
            {"name": "Subsurface Flow (mm/day)",
            "index": 1,
            "data": subsurface_data,
            "mean": np.mean(subsurface_data),
            "max": np.max(subsurface_data),
            "min": np.min(subsurface_data)
            },
            {"name": "Impervious Flow (mm/day)",
            "index": 2,
            "data": impervious_data,
            "mean": np.mean(impervious_data),
            "max": np.max(impervious_data),
            "min": np.min(impervious_data)
            },
            {"name": "Infiltration Excess (mm/day)",
            "index": 3,
            "data": infiltration_data,
            "mean": np.mean(infiltration_data),
            "max": np.max(infiltration_data),
            "min": np.min(infiltration_data)
            },
            {"name": "Initial Abstracted Flow (mm/day)",
            "index": 4,
            "data": initialabstracted_data,
            "mean": np.mean(initialabstracted_data),
            "max": np.max(initialabstracted_data),
            "min": np.min(initialabstracted_data)
            },            
            {"name": "Overland Flow (mm/day)",
            "index": 5,
            "data": overlandflow_data,
            "mean": np.mean(overlandflow_data),
            "max": np.max(overlandflow_data),
            "min": np.min(overlandflow_data)
            },
            {"name": "PET (mm/day)",
            "index": 6,
            "data": pet_data,
            "mean": np.mean(pet_data),
            "max": np.max(pet_data),
            "min": np.min(pet_data)
            },
            {"name": "AET(mm/day)",
            "index": 7,
            "data": aet_data,
            "mean": np.mean(aet_data),
            "max": np.max(aet_data),
            "min": np.min(aet_data)
            },
            {"name": "Average Soil Root zone (mm)",
            "index": 8,
            "data": avgsoilrootzone_data,
            "mean": np.mean(avgsoilrootzone_data),
            "max": np.max(avgsoilrootzone_data),
            "min": np.min(avgsoilrootzone_data)
            },
            {"name": "Average Soil Unsaturated Zone (mm)",
            "index": 9,
            "data": avgsoilunsaturatedzone_data,
            "mean": np.mean(avgsoilunsaturatedzone_data),
            "max": np.max(avgsoilunsaturatedzone_data),
            "min": np.min(avgsoilunsaturatedzone_data)
            },
            {"name": "Snow Pack (mm)",
            "index": 10,
            "data": snowpack_data,
            "mean": np.mean(snowpack_data),
            "max": np.max(snowpack_data),
            "min": np.min(snowpack_data)
            },
            {"name": "Precipitation (mm/day)",
            "index": 11,
            "data": precipitation_data,
            "mean": np.mean(precipitation_data),
            "max": np.max(precipitation_data),
            "min": np.min(precipitation_data)
            },
            {"name": "Storage Deficit (mm/day)",
            "index": 12,
            "data": storagedeficit_data,
            "mean": np.mean(storagedeficit_data),
            "max": np.max(storagedeficit_data),
            "min": np.min(storagedeficit_data)
            },
            {"name": "Return Flow (mm/day)",
            "index": 13,
            "data": returnflow_data,
            "mean": np.mean(returnflow_data),
            "max": np.max(returnflow_data),
            "min": np.min(returnflow_data)
            },
        ],  
    }


    dates_all_months = np.array([datetime.datetime(2014, 1, 1, 0, 0), 
                      datetime.datetime(2014, 2, 1, 0, 0), 
                      datetime.datetime(2014, 3, 1, 0, 0),
                      datetime.datetime(2014, 4, 1, 0, 0), 
                      datetime.datetime(2014, 5, 1, 0, 0), 
                      datetime.datetime(2014, 6, 1, 0, 0),
                      datetime.datetime(2014, 7, 1, 0, 0), 
                      datetime.datetime(2014, 8, 1, 0, 0), 
                      datetime.datetime(2014, 9, 1, 0, 0),
                      datetime.datetime(2014, 10, 1, 0, 0), 
                      datetime.datetime(2014, 11, 1, 0, 0), 
                      datetime.datetime(2014, 12, 1, 0, 0)]
    )
    
    discharge_data_all_months = np.array([3, 6, 10, 12, 15, 16, 18, 15, 11, 7, 5, 2])
    subsurface_data_all_months = np.array([50, 55, 45, 40, 35, 30, 25, 20, 15, 20, 25, 30])
       
    fixture["sample_data_dict_all_months"] = {
        "user": "jlant",
        "date_created": "4/9/2014 15:50:47 PM",
        "stationid": "012345",
        "column_names": ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'],
        "dates": dates_all_months,
        "parameters": [
            {"name": "Discharge (cfs)",
            "index": 0,
            "data": discharge_data_all_months,
            "mean": np.mean(discharge_data_all_months),
            "max": np.max(discharge_data_all_months),
            "min": np.min(discharge_data_all_months)
            },
            {"name": "Subsurface Flow (mm/day)",
            "index": 1,
            "data": subsurface_data_all_months,
            "mean": np.mean(subsurface_data_all_months),
            "max": np.max(subsurface_data_all_months),
            "min": np.min(subsurface_data_all_months)
            }
        ],  
    }

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: watertxt tests"      

def test_get_date():
    
    expected = datetime.datetime(2014, 4, 9, 0, 0)
    
    actual = watertxt.get_date(date_str = fixture["date_str"])

    nose.tools.assert_equals(actual, expected)
    
def test_create_parameter():

    expected1 = {"name": None, "index": None, "data": [], "mean": None, "max": None, "min": None}
    
    actual1 = watertxt.create_parameter()

    nose.tools.assert_equals(actual1["name"], expected1["name"])
    nose.tools.assert_equals(actual1["index"], expected1["index"])
    nose.tools.assert_equals(actual1["data"], expected1["data"])
    nose.tools.assert_equals(actual1["mean"], expected1["mean"])
    nose.tools.assert_equals(actual1["max"], expected1["max"])
    nose.tools.assert_equals(actual1["min"], expected1["min"])

    expected2 = {"name": "discharge", "index": 0, "data": [1, 2, 3], "mean": 2, "max": 3, "min": 1}
    
    actual2 = watertxt.create_parameter(name = "discharge", index = 0, data = [1, 2, 3], mean = 2, max = 3, min = 1)    
    
    nose.tools.assert_equals(actual2["name"], expected2["name"])
    nose.tools.assert_equals(actual2["index"], expected2["index"])
    nose.tools.assert_equals(actual2["data"], expected2["data"])
    nose.tools.assert_equals(actual2["mean"], expected2["mean"])
    nose.tools.assert_equals(actual2["max"], expected2["max"])
    nose.tools.assert_equals(actual2["min"], expected2["min"])

@with_setup(setup, teardown)
def test_add_parameter():

    wateruse_data = np.array([3.0, 2.5, -5.5])
    expected = {"name": "Water Use (cfs)", "index": 14, "data": wateruse_data, 
                "mean": np.mean(wateruse_data), "max": np.max(wateruse_data), "min": np.min(wateruse_data)}    
    
    data = watertxt.add_parameter(watertxt_data = fixture["sample_data_dict"], name = "Water Use (cfs)", param_data = np.array([3.0, 2.5, -5.5])) 

    actual = data["parameters"][-1]
    nose.tools.assert_equals(actual["name"], expected["name"])
    nose.tools.assert_equals(actual["index"], expected["index"])

    nose.tools.assert_equals(actual["mean"], expected["mean"])
    nose.tools.assert_equals(actual["max"], expected["max"])
    nose.tools.assert_equals(actual["min"], expected["min"])    

    np.testing.assert_equal(actual["data"], expected["data"])

@with_setup(setup, teardown)
def test_get_parameter():

    subsurface_data = np.array([50., 55., 45.])
    expected = {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data, 
                "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)}
    
    actual = watertxt.get_parameter(watertxt_data = fixture["sample_data_dict"], name = "Subsurface Flow")
    
    nose.tools.assert_equals(actual["name"], expected["name"])
    nose.tools.assert_equals(actual["index"], expected["index"])

    nose.tools.assert_equals(actual["mean"], expected["mean"])
    nose.tools.assert_equals(actual["max"], expected["max"])
    nose.tools.assert_equals(actual["min"], expected["min"]) 

    np.testing.assert_equal(actual["data"], expected["data"])
    
@with_setup(setup, teardown)  
def test_get_all_values():
    
    expected = [
        np.array([2, 6, 10]),
        np.array([50, 55, 45]),
        np.array([2, 8, 2]),
        np.array([0, 1.5, 1.5]),
        np.array([0.1, 0.2, 0.3]),
        np.array([3, 9, 3]),
        np.array([5, 3, 13]),
        np.array([5, 12, 13]),
        np.array([40, 50, 60]),
        np.array([4, 3, 2]),
        np.array([150, 125, 25]),
        np.array([0.5, 0.4, 0.3]),
        np.array([300, 310, 350]),
        np.array([-5, -4.5, -4.]),    
    ]
  
    actual = watertxt.get_all_values(watertxt_data = fixture["sample_data_dict"])

    for i in range(len(actual)):
        np.testing.assert_equal(actual[i], expected[i])

@with_setup(setup, teardown)
def test_set_parameter_values():
    
    subsurface_data = np.array([100, 110, 120])
    watertxt_data = watertxt.set_parameter_values(watertxt_data = fixture["sample_data_dict"], name = "Subsurface Flow", values = subsurface_data)

    expected = {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data, 
                "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)}


    actual = watertxt.get_parameter(watertxt_data, name = "Subsurface Flow")

    nose.tools.assert_equals(actual["name"], expected["name"])
    nose.tools.assert_equals(actual["index"], expected["index"])

    nose.tools.assert_equals(actual["mean"], expected["mean"])
    nose.tools.assert_equals(actual["max"], expected["max"])
    nose.tools.assert_equals(actual["min"], expected["min"]) 

    np.testing.assert_equal(actual["data"], expected["data"])


@with_setup(setup, teardown) 
def test_data_file_clean():

    expected = fixture["sample_data_dict"]    
    
    fileobj = StringIO(fixture["data_file_clean"])
    actual = watertxt.read_file_in(filestream = fileobj)
	
    nose.tools.assert_equals(actual["user"], expected["user"])
    nose.tools.assert_equals(actual["date_created"], expected["date_created"])
    nose.tools.assert_equals(actual["stationid"], expected["stationid"])
    nose.tools.assert_equals(actual["column_names"], expected["column_names"])

    np.testing.assert_equal(actual["dates"], expected["dates"])
    
    for i in range(len(actual["parameters"])):
        np.testing.assert_equal(actual["parameters"][i]["name"], expected["parameters"][i]["name"])        
        np.testing.assert_equal(actual["parameters"][i]["index"], expected["parameters"][i]["index"])
         
        np.testing.assert_equal(expected["parameters"][i], actual["parameters"][i], err_msg = "Error in: {}".format(actual["parameters"][i]["name"]))
        
        np.testing.assert_equal(actual["parameters"][i]["mean"], expected["parameters"][i]["mean"])
        np.testing.assert_equal(actual["parameters"][i]["max"], expected["parameters"][i]["max"])
        np.testing.assert_equal(actual["parameters"][i]["min"], expected["parameters"][i]["min"])    
    
def test_data_file_bad_single_parameter():

    dates = np.array([datetime.datetime(2014, 04, 01, 0, 0), 
                      datetime.datetime(2014, 04, 02, 0, 0), 
                      datetime.datetime(2014, 04, 03, 0, 0),
                      datetime.datetime(2014, 04, 04, 0, 0), 
                      datetime.datetime(2014, 04, 05, 0, 0),
    ])
   
    discharge_data = np.array([5.0, 10.0, np.nan, np.nan, 5.5])  
    subsurface_data = np.array([50, 55, 60, 65, 45])

 
    expected = {
        "user": "jlant",
        "date_created": "4/10/2014 00:00:00 PM",
        "stationid": "000000",
        "column_names": ['Discharge (cfs)', 'Subsurface Flow (mm/day)'],
        "dates": dates,
        "parameters": [
            {"name": "Discharge (cfs)",
            "index": 0,
            "data": discharge_data,
            "mean": np.nanmean(discharge_data),
            "max": np.nanmax(discharge_data),
            "min": np.nanmin(discharge_data)
            },
            {"name": "Subsurface Flow (mm/day)",
            "index": 1,
            "data": subsurface_data,
            "mean": np.nanmean(subsurface_data),
            "max": np.nanmax(subsurface_data),
            "min": np.nanmin(subsurface_data)
            },
        ]
    }
	
    fileobj = StringIO(fixture["data_file_bad_single_parameter"])
    actual = watertxt.read_file_in(filestream = fileobj)

    nose.tools.assert_equals(actual["user"], expected["user"])
    nose.tools.assert_equals(actual["date_created"], expected["date_created"])
    nose.tools.assert_equals(actual["stationid"], expected["stationid"])
    nose.tools.assert_equals(actual["column_names"], expected["column_names"])

    np.testing.assert_equal(actual["dates"], expected["dates"])

    for i in range(len(actual["parameters"])):
        np.testing.assert_equal(actual["parameters"][i]["name"], expected["parameters"][i]["name"])        
        np.testing.assert_equal(actual["parameters"][i]["index"], expected["parameters"][i]["index"])
         
        np.testing.assert_equal(expected["parameters"][i], actual["parameters"][i], err_msg = "Error in: {}".format(actual["parameters"][i]["name"]))
        
        np.testing.assert_equal(actual["parameters"][i]["mean"], expected["parameters"][i]["mean"])
        np.testing.assert_equal(actual["parameters"][i]["max"], expected["parameters"][i]["max"])
        np.testing.assert_equal(actual["parameters"][i]["min"], expected["parameters"][i]["min"])  

@with_setup(setup, teardown) 
def test_apply_factors_single_parameter1():
    
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

    dates = np.array([datetime.datetime(2014, 04, 01, 0, 0), 
                      datetime.datetime(2014, 04, 02, 0, 0), 
                      datetime.datetime(2014, 04, 03, 0, 0)
    ])
   
    updated_discharge_data = np.array([6, 18, 30])  
 
    expected = {
        "user": "jlant",
        "date_created": "4/9/2014 15:50:47 PM",
        "stationid": "012345",
        "column_names": ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'],
        "dates": dates,
        "parameters": [
            {"name": "Discharge (cfs)",
            "index": 0,
            "data": updated_discharge_data,
            "mean": np.mean(updated_discharge_data),
            "max": np.max(updated_discharge_data),
            "min": np.min(updated_discharge_data)
            }]
    }

    actual = watertxt.apply_factors(watertxt_data = fixture["sample_data_dict"], name = "Discharge", factors = factors)    
    
    nose.tools.assert_equals(expected["parameters"][0]["name"], actual["parameters"][0]["name"])
    nose.tools.assert_equals(expected["parameters"][0]["index"], actual["parameters"][0]["index"])
    
    nose.tools.assert_almost_equals(actual["parameters"][0]["data"].all(), expected["parameters"][0]["data"].all())
       
    nose.tools.assert_almost_equals(actual["parameters"][0]["mean"], expected["parameters"][0]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["max"], expected["parameters"][0]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["min"], expected["parameters"][0]["min"])

@with_setup(setup, teardown)
def test_apply_factors_single_parameter2():
    
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

    dates = np.array([datetime.datetime(2014, 04, 01, 0, 0), 
                      datetime.datetime(2014, 04, 02, 0, 0), 
                      datetime.datetime(2014, 04, 03, 0, 0)
    ])
   
    updated_discharge_data = np.array([5, 9, 13])  
 
    expected = {
        "user": "jlant",
        "date_created": "4/9/2014 15:50:47 PM",
        "stationid": "012345",
        "column_names": ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'],
        "dates": dates,
        "parameters": [
            {"name": "Discharge (cfs)",
            "index": 0,
            "data": updated_discharge_data,
            "mean": np.mean(updated_discharge_data),
            "max": np.max(updated_discharge_data),
            "min": np.min(updated_discharge_data)
            }]
    }

    actual = watertxt.apply_factors(watertxt_data = fixture["sample_data_dict"], name = "Discharge", factors = factors, is_additive = True)    
    
    nose.tools.assert_equals(expected["parameters"][0]["name"], actual["parameters"][0]["name"])
    nose.tools.assert_equals(expected["parameters"][0]["index"], actual["parameters"][0]["index"])
    
    nose.tools.assert_almost_equals(actual["parameters"][0]["data"].all(), expected["parameters"][0]["data"].all())
       
    nose.tools.assert_almost_equals(actual["parameters"][0]["mean"], expected["parameters"][0]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["max"], expected["parameters"][0]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["min"], expected["parameters"][0]["min"])

@with_setup(setup, teardown)
def test_apply_factors_multi_parameters():
    
    factors = {
        "January": 1.5,
        "February": 2.0,
        "March": 2.5,
        "April": 3.0,
        "May": 3.5,
        "June": 4.0,
        "July": 4.5,
        "August": 5.5,
        "September": 6.0,
        "October": 6.5,
        "November": 7.0,
        "December": 7.5
    }     

    dates = np.array([datetime.datetime(2014, 1, 1, 0, 0), 
                      datetime.datetime(2014, 2, 1, 0, 0), 
                      datetime.datetime(2014, 3, 1, 0, 0),
                      datetime.datetime(2014, 4, 1, 0, 0), 
                      datetime.datetime(2014, 5, 1, 0, 0), 
                      datetime.datetime(2014, 6, 1, 0, 0),
                      datetime.datetime(2014, 7, 1, 0, 0), 
                      datetime.datetime(2014, 8, 1, 0, 0), 
                      datetime.datetime(2014, 9, 1, 0, 0),
                      datetime.datetime(2014, 10, 1, 0, 0), 
                      datetime.datetime(2014, 11, 1, 0, 0), 
                      datetime.datetime(2014, 12, 1, 0, 0)]
    )

    discharge_data_all_months = np.array([4.5, 12, 25, 36, 52.5, 64, 81, 82.5, 66, 45.5, 35, 15])
    subsurface_data_all_months = np.array([75, 110, 112.5, 120, 122.5, 120, 112.5, 110, 90, 130, 175, 225])
      
    expected = {
        "user": "jlant",
        "date_created": "4/9/2014 15:50:47 PM",
        "stationid": "012345",
        "column_names": ['Discharge (cfs)', 'Subsurface Flow (mm/day)', 'Impervious Flow (mm/day)', 'Infiltration Excess (mm/day)', 'Initial Abstracted Flow (mm/day)', 'Overland Flow (mm/day)', 'PET (mm/day)', 'AET(mm/day)', 'Average Soil Root zone (mm)', 'Average Soil Unsaturated Zone (mm)', 'Snow Pack (mm)', 'Precipitation (mm/day)', 'Storage Deficit (mm/day)', 'Return Flow (mm/day)'],
        "dates": dates,
        "parameters": [
            {"name": "Discharge (cfs)",
            "index": 0,
            "data": discharge_data_all_months,
            "mean": np.mean(discharge_data_all_months),
            "max": np.max(discharge_data_all_months),
            "min": np.min(discharge_data_all_months)
            },
            {"name": "Subsurface Flow (mm/day)",
            "index": 1,
            "data": subsurface_data_all_months,
            "mean": np.mean(subsurface_data_all_months),
            "max": np.max(subsurface_data_all_months),
            "min": np.min(subsurface_data_all_months)
            }
        ],  
    }  

    actual_q = watertxt.apply_factors(watertxt_data = fixture["sample_data_dict_all_months"], name = "Discharge", factors = factors)    
    actual_s = watertxt.apply_factors(watertxt_data = fixture["sample_data_dict_all_months"], name = "Subsurface Flow", factors = factors)
    
    nose.tools.assert_equals(actual_q["parameters"][0]["name"], expected["parameters"][0]["name"])
    nose.tools.assert_equals(actual_q["parameters"][0]["index"], expected["parameters"][0]["index"])    
    nose.tools.assert_equals(actual_s["parameters"][1]["name"], expected["parameters"][1]["name"])
    nose.tools.assert_equals(actual_s["parameters"][1]["index"], expected["parameters"][1]["index"])
    
    nose.tools.assert_almost_equals(actual_q["parameters"][0]["data"].all(), expected["parameters"][0]["data"].all())
    nose.tools.assert_almost_equals(actual_s["parameters"][1]["data"].all(), expected["parameters"][1]["data"].all())
       
    nose.tools.assert_almost_equals(actual_q["parameters"][0]["mean"], expected["parameters"][0]["mean"])
    nose.tools.assert_almost_equals(actual_q["parameters"][0]["max"], expected["parameters"][0]["max"])
    nose.tools.assert_almost_equals(actual_q["parameters"][0]["min"], expected["parameters"][0]["min"])               
    nose.tools.assert_almost_equals(actual_s["parameters"][1]["mean"], expected["parameters"][1]["mean"])
    nose.tools.assert_almost_equals(actual_s["parameters"][1]["max"], expected["parameters"][1]["max"])
    nose.tools.assert_almost_equals(actual_s["parameters"][1]["min"], expected["parameters"][1]["min"])

@with_setup(setup, teardown)
def test_apply_wateruse():
    """ Test apply_wateruse() functionality """

    # create water use totals
    wateruse_totals = {
        'January': 2.0,
        'February': 2.0,
        'March': 2.0,
        'April': 3.0,
        'May': 3.0,
        'June': 3.0,
        'July': 4.0,
        'August': 4.0,
        'September': 4.0,
        'October': -5.0,
        'November': -5.0,
        'December': -5.0
    }  

    wateruse_totals_data = np.array([2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, -5.0, -5.0, -5.0])

    discharge_and_wateruse_data = np.array([5.0, 8.0, 12.0, 15.0, 18.0, 19.0, 22.0, 19.0, 15.0, 2.0, 0.0, -3.0])

    # expected values to test with actual values
    expected_wateruse_totals = {"name": "Water Use (cfs)", "index": 2, "data": wateruse_totals_data, "mean": np.mean(wateruse_totals_data), "max": np.max(wateruse_totals_data), "min": np.min(wateruse_totals_data)}    
    expected_discharge_and_wateruse = {"name": "Discharge + Water Use (cfs)", "index": 3, "data": discharge_and_wateruse_data, "mean": np.mean(discharge_and_wateruse_data), "max": np.max(discharge_and_wateruse_data), "min": np.min(discharge_and_wateruse_data)}

    # apply water use
    data = watertxt.apply_wateruse(watertxt_data = fixture["sample_data_dict_all_months"], wateruse_totals = wateruse_totals) 
    
    # actual values
    actual_wateruse_totals = watertxt.get_parameter(watertxt_data = data, name = "Water Use")
    actual_discharge_and_wateruse = watertxt.get_parameter(watertxt_data = data, name = "Discharge + Water Use") 

    # make assertions for wateruse_totals
    nose.tools.assert_almost_equals(actual_wateruse_totals["name"], expected_wateruse_totals["name"])
    nose.tools.assert_almost_equals(actual_wateruse_totals["index"], expected_wateruse_totals["index"])
    
    nose.tools.assert_almost_equals(actual_wateruse_totals["mean"], expected_wateruse_totals["mean"])          
    nose.tools.assert_almost_equals(actual_wateruse_totals["max"], expected_wateruse_totals["max"])
    nose.tools.assert_almost_equals(actual_wateruse_totals["min"], expected_wateruse_totals["min"])

    nose.tools.assert_almost_equals(actual_wateruse_totals["data"].all(), expected_wateruse_totals["data"].all())
    
    # make assertions for discharge and wateruse_totals
    nose.tools.assert_almost_equals(actual_discharge_and_wateruse["name"], expected_discharge_and_wateruse["name"])
    nose.tools.assert_almost_equals(actual_discharge_and_wateruse["index"], expected_discharge_and_wateruse["index"])
    
    nose.tools.assert_almost_equals(actual_discharge_and_wateruse["mean"], expected_discharge_and_wateruse["mean"])          
    nose.tools.assert_almost_equals(actual_discharge_and_wateruse["max"], expected_discharge_and_wateruse["max"])
    nose.tools.assert_almost_equals(actual_discharge_and_wateruse["min"], expected_discharge_and_wateruse["min"])

    nose.tools.assert_almost_equals(actual_discharge_and_wateruse["data"].all(), expected_discharge_and_wateruse["data"].all())

def test_write_file():
    """ Test write_file functionality """

    # create water use totals
    wateruse_totals = {
        'January': 2.0,
        'February': 2.0,
        'March': 2.0,
        'April': 3.0,
        'May': 3.0,
        'June': 0.0,
        'July': 4.0,
        'August': 4.0,
        'September': 4.0,
        'October': 5.0,
        'November': 5.0,
        'December': 5.0
    }  


    # write water formatted file   
    data = fixture["sample_data_dict"]
    watertxt.write_file(watertxt_data = data, save_path = os.path.join(os.getcwd(), "tests"))

    # write water formatted file with new values set in discharge
    data = fixture["sample_data_dict"]
    new_discharge_data = np.array([230, 240, 280])
    data = watertxt.set_parameter_values(watertxt_data = data, name = "Discharge", values = new_discharge_data)
    watertxt.write_file(watertxt_data = data , save_path = os.path.join(os.getcwd(), "tests"), filename = "WATER_new_discharge_data.txt")
    
    # apply water use
    data = fixture["sample_data_dict"]
    data = watertxt.apply_wateruse(watertxt_data = data, wateruse_totals = wateruse_totals)     
    watertxt.write_file(watertxt_data = data , save_path = os.path.join(os.getcwd(), "tests"), filename = "WATER_wateruse.txt") 

@with_setup(setup, teardown)        
def test_write_oasis_file1():
    """ Test write_oasis_file functionality part 1 - Discharge only; NO water use applied """
      
    # create test data
    data = fixture["sample_data_dict"]
    
    # write file
    watertxt.write_oasis_file(watertxt_data = data, save_path = os.path.join(os.getcwd(), "tests"), filename = "oasis-file1.txt")  

@with_setup(setup, teardown) 
def test_write_timeseries_file1():
    """ Test write_oasis_file functionality part 1 - Discharge only; NO water use applied """
      
    # create test data
    data = fixture["sample_data_dict"]
    
    # write file
    watertxt.write_timeseries_file(watertxt_data = data, name = "Discharge + Water Use", save_path = os.path.join(os.getcwd(), "tests"), filename = "oasis-file2.txt")  

@with_setup(setup, teardown) 
def test_write_oasis_file2():
    """ Test write_oasis_file functionality part 2 - Discharge + Water Use; water use is applied """

    # create water use totals
    wateruse_totals = {
        'January': 2.0,
        'February': 2.0,
        'March': 2.0,
        'April': 3.0,
        'May': 3.0,
        'June': 0.0,
        'July': 4.0,
        'August': 4.0,
        'September': 4.0,
        'October': 5.0,
        'November': 5.0,
        'December': 5.0
    }  

    print("--- Testing write_oasis_file part 2 - Discharge + Water Use; water use is applied ---") 
       
    # create test data
    data = fixture["sample_data_dict"]
    
    # apply water use
    data = watertxt.apply_wateruse(watertxt_data = data, wateruse_totals = wateruse_totals)     
    
    # write file
    watertxt.write_oasis_file(watertxt_data = data, save_path = os.path.join(os.getcwd(), "tests"), filename = "oasis-file_discharge_and_wateruse.txt") 
    
     