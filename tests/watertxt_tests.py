import nose.tools
from nose import with_setup 

import sys
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
    pet_data = np.array([5, 13, 3])
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



def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: watertxt tests"      

def test_get_date():
    
    expected = datetime.datetime(2014, 4, 9, 0, 0)
    
    actual = watertxt.get_date(date_str = fixture["date_str"])

    nose.tools.assert_equals(actual, expected)
    
def test_create_parameter():

    expected1 = {"name": None, "index": None, "data": [], "mean": None, "max": None, "min": None}
    
    parameter1 = watertxt.create_parameter()

    nose.tools.assert_equals(expected1["name"], parameter1["name"])
    nose.tools.assert_equals(expected1["index"], parameter1["index"])
    nose.tools.assert_equals(expected1["data"], parameter1["data"])
    nose.tools.assert_equals(expected1["mean"], parameter1["mean"])
    nose.tools.assert_equals(expected1["max"], parameter1["max"])
    nose.tools.assert_equals(expected1["min"], parameter1["min"])

    expected2 = {"name": "discharge", "index": 0, "data": [1, 2, 3], "mean": 2, "max": 3, "min": 1}
    
    parameter2 = watertxt.create_parameter(name = "discharge", index = 0, data = [1, 2, 3], mean = 2, max = 3, min = 1)    
    
    nose.tools.assert_equals(expected2["name"], parameter2["name"])
    nose.tools.assert_equals(expected2["index"], parameter2["index"])
    nose.tools.assert_equals(expected2["data"], parameter2["data"])
    nose.tools.assert_equals(expected2["mean"], parameter2["mean"])
    nose.tools.assert_equals(expected2["max"], parameter2["max"])
    nose.tools.assert_equals(expected2["min"], parameter2["min"])

@with_setup(setup, teardown)
def test_add_parameter():

    wateruse_data = np.array([3.0, 2.5, -5.5])
    expected = {"name": "Water Use (cfs)", "index": 14, "data": wateruse_data, 
                "mean": np.mean(wateruse_data), "max": np.max(wateruse_data), "min": np.min(wateruse_data)}    
    
    data = watertxt.add_parameter(watertxt_data = fixture["sample_data_dict"], name = "Water Use (cfs)", param_data = np.array([3.0, 2.5, -5.5])) 

    nose.tools.assert_equals(expected["name"], data["parameters"][-1]["name"])
    nose.tools.assert_equals(expected["index"], data["parameters"][-1]["index"])
    nose.tools.assert_almost_equals(expected["data"].all(), data["parameters"][-1]["data"].all())
    nose.tools.assert_equals(expected["mean"], data["parameters"][-1]["mean"])
    nose.tools.assert_equals(expected["max"], data["parameters"][-1]["max"])
    nose.tools.assert_equals(expected["min"], data["parameters"][-1]["min"])    

@with_setup(setup, teardown)
def test_get_parameter():

    subsurface_data = np.array([50., 55., 45.])
    expected = {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data, 
                "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)}
    
    parameter = watertxt.get_parameter(watertxt_data = fixture["sample_data_dict"], name = "Subsurface Flow")
    
    nose.tools.assert_equals(expected["name"], parameter["name"])
    nose.tools.assert_equals(expected["index"], parameter["index"])
    nose.tools.assert_almost_equals(expected["data"].all(), parameter["data"].all())
    nose.tools.assert_equals(expected["mean"], parameter["mean"])
    nose.tools.assert_equals(expected["max"], parameter["max"])
    nose.tools.assert_equals(expected["min"], parameter["min"]) 
    
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
        np.array([-5, -4.5, -4]),    
    ]
  
    values_all = watertxt.get_all_values(watertxt_data = fixture["sample_data_dict"])
    
    nose.tools.assert_almost_equals(expected[0].all(), values_all[0].all())
    nose.tools.assert_almost_equals(expected[1].all(), values_all[1].all())
    nose.tools.assert_almost_equals(expected[2].all(), values_all[2].all())
    nose.tools.assert_almost_equals(expected[3].all(), values_all[3].all())
    nose.tools.assert_almost_equals(expected[4].all(), values_all[4].all())
    nose.tools.assert_almost_equals(expected[5].all(), values_all[5].all())    
    nose.tools.assert_almost_equals(expected[6].all(), values_all[6].all())    
    nose.tools.assert_almost_equals(expected[7].all(), values_all[7].all())
    nose.tools.assert_almost_equals(expected[8].all(), values_all[8].all())
    nose.tools.assert_almost_equals(expected[9].all(), values_all[9].all())
    nose.tools.assert_almost_equals(expected[10].all(), values_all[10].all())
    nose.tools.assert_almost_equals(expected[11].all(), values_all[11].all())    
    nose.tools.assert_almost_equals(expected[12].all(), values_all[12].all())
    nose.tools.assert_almost_equals(expected[13].all(), values_all[13].all())

@with_setup(setup, teardown)
def test_set_parameter_values():
    """ Test set_parameter functionality """
    
    print("--- Testing set_parameter ---") 
    
    subsurface_data = np.array([100, 110, 120])
    watertxt_data = watertxt.set_parameter_values(watertxt_data = fixture["sample_data_dict"], name = "Subsurface Flow", values = subsurface_data)

    expected = {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data, 
                "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)}


    updated_subsurface_data = watertxt.get_parameter(watertxt_data, name = "Subsurface Flow")

    nose.tools.assert_equals(expected["name"], updated_subsurface_data["name"])
    nose.tools.assert_equals(expected["index"], updated_subsurface_data["index"])
    nose.tools.assert_almost_equals(expected["data"].all(), updated_subsurface_data["data"].all())
    nose.tools.assert_equals(expected["mean"], updated_subsurface_data["mean"])
    nose.tools.assert_equals(expected["max"], updated_subsurface_data["max"])
    nose.tools.assert_equals(expected["min"], updated_subsurface_data["min"]) 


@with_setup(setup, teardown) 
def test_data_file_clean():

    expected = fixture["sample_data_dict"]    
    
    fileobj = StringIO(fixture["data_file_clean"])
    actual = watertxt.read_file_in(filestream = fileobj)
	
    nose.tools.assert_equals(actual["user"], expected["user"])
    nose.tools.assert_equals(actual["date_created"], expected["date_created"])
    nose.tools.assert_equals(actual["stationid"], expected["stationid"])
    nose.tools.assert_equals(actual["column_names"], expected["column_names"])

    nose.tools.assert_equals(actual["dates"].all(), expected["dates"].all())
    
    nose.tools.assert_equals(actual["parameters"][0]["name"], expected["parameters"][0]["name"])
    nose.tools.assert_equals(actual["parameters"][0]["index"], expected["parameters"][0]["index"])

    nose.tools.assert_equals(actual["parameters"][1]["name"], expected["parameters"][1]["name"])
    nose.tools.assert_equals(actual["parameters"][1]["index"], expected["parameters"][1]["index"])

    nose.tools.assert_equals(actual["parameters"][2]["name"], expected["parameters"][2]["name"])
    nose.tools.assert_equals(actual["parameters"][2]["index"], expected["parameters"][2]["index"])
    
    nose.tools.assert_equals(actual["parameters"][3]["name"], expected["parameters"][3]["name"])
    nose.tools.assert_equals(actual["parameters"][3]["index"], expected["parameters"][3]["index"])

    nose.tools.assert_equals(actual["parameters"][4]["name"], expected["parameters"][4]["name"])
    nose.tools.assert_equals(actual["parameters"][4]["index"], expected["parameters"][4]["index"])

    nose.tools.assert_equals(actual["parameters"][5]["name"], expected["parameters"][5]["name"])
    nose.tools.assert_equals(actual["parameters"][5]["index"], expected["parameters"][5]["index"])

    nose.tools.assert_equals(actual["parameters"][6]["name"], expected["parameters"][6]["name"])
    nose.tools.assert_equals(actual["parameters"][6]["index"], expected["parameters"][6]["index"])

    nose.tools.assert_equals(actual["parameters"][7]["name"], expected["parameters"][7]["name"])
    nose.tools.assert_equals(actual["parameters"][7]["index"], expected["parameters"][7]["index"])

    nose.tools.assert_equals(actual["parameters"][8]["name"], expected["parameters"][8]["name"])
    nose.tools.assert_equals(actual["parameters"][8]["index"], expected["parameters"][8]["index"])

    nose.tools.assert_equals(actual["parameters"][9]["name"], expected["parameters"][9]["name"])
    nose.tools.assert_equals(actual["parameters"][9]["index"], expected["parameters"][9]["index"])

    nose.tools.assert_equals(actual["parameters"][10]["name"], expected["parameters"][10]["name"])
    nose.tools.assert_equals(actual["parameters"][10]["index"], expected["parameters"][10]["index"])

    nose.tools.assert_equals(actual["parameters"][11]["name"], expected["parameters"][11]["name"])
    nose.tools.assert_equals(actual["parameters"][11]["index"], expected["parameters"][11]["index"])

    nose.tools.assert_equals(actual["parameters"][12]["name"], expected["parameters"][12]["name"])
    nose.tools.assert_equals(actual["parameters"][12]["index"], expected["parameters"][12]["index"])

    nose.tools.assert_equals(actual["parameters"][13]["name"], expected["parameters"][13]["name"])
    nose.tools.assert_equals(actual["parameters"][13]["index"], expected["parameters"][13]["index"])
    
    nose.tools.assert_almost_equals(actual["parameters"][0]["data"].all(), expected["parameters"][0]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][1]["data"].all(), expected["parameters"][1]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][2]["data"].all(), expected["parameters"][2]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][3]["data"].all(), expected["parameters"][3]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][4]["data"].all(), expected["parameters"][4]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][5]["data"].all(), expected["parameters"][5]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][6]["data"].all(), expected["parameters"][6]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][7]["data"].all(), expected["parameters"][7]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][8]["data"].all(), expected["parameters"][8]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][9]["data"].all(), expected["parameters"][9]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][10]["data"].all(), expected["parameters"][10]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][11]["data"].all(), expected["parameters"][11]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][12]["data"].all(), expected["parameters"][12]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][13]["data"].all(), expected["parameters"][13]["data"].all())
     
    
    nose.tools.assert_almost_equals(actual["parameters"][0]["mean"], expected["parameters"][0]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["max"], expected["parameters"][0]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["min"], expected["parameters"][0]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][1]["mean"], expected["parameters"][1]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][1]["max"], expected["parameters"][1]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][1]["min"], expected["parameters"][1]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][2]["mean"], expected["parameters"][2]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][2]["max"], expected["parameters"][2]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][2]["min"], expected["parameters"][2]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][3]["mean"], expected["parameters"][3]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][3]["max"], expected["parameters"][3]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][3]["min"], expected["parameters"][3]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][4]["mean"], expected["parameters"][4]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][4]["max"], expected["parameters"][4]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][4]["min"], expected["parameters"][4]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][5]["mean"], expected["parameters"][5]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][5]["max"], expected["parameters"][5]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][5]["min"], expected["parameters"][5]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][6]["mean"], expected["parameters"][6]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][6]["max"], expected["parameters"][6]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][6]["min"], expected["parameters"][6]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][7]["mean"], expected["parameters"][7]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][7]["max"], expected["parameters"][7]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][7]["min"], expected["parameters"][7]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][8]["mean"], expected["parameters"][8]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][8]["max"], expected["parameters"][8]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][8]["min"], expected["parameters"][8]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][9]["mean"], expected["parameters"][9]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][9]["max"], expected["parameters"][9]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][9]["min"], expected["parameters"][9]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][10]["mean"], expected["parameters"][10]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][10]["max"], expected["parameters"][10]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][10]["min"], expected["parameters"][10]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][11]["mean"], expected["parameters"][11]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][11]["max"], expected["parameters"][11]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][11]["min"], expected["parameters"][11]["min"])
         
    nose.tools.assert_almost_equals(actual["parameters"][12]["mean"], expected["parameters"][12]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][12]["max"], expected["parameters"][12]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][12]["min"], expected["parameters"][12]["min"])

    nose.tools.assert_almost_equals(actual["parameters"][13]["mean"], expected["parameters"][13]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][13]["max"], expected["parameters"][13]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][13]["min"], expected["parameters"][13]["min"])
    
    
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

    nose.tools.assert_equals(actual["dates"].all(), expected["dates"].all())
    
    nose.tools.assert_equals(actual["parameters"][0]["name"], expected["parameters"][0]["name"])
    nose.tools.assert_equals(actual["parameters"][0]["index"], expected["parameters"][0]["index"])

    nose.tools.assert_equals(actual["parameters"][1]["name"], expected["parameters"][1]["name"])
    nose.tools.assert_equals(actual["parameters"][1]["index"], expected["parameters"][1]["index"])
    
    nose.tools.assert_almost_equals(actual["parameters"][0]["data"].all(), expected["parameters"][0]["data"].all())
    nose.tools.assert_almost_equals(actual["parameters"][1]["data"].all(), expected["parameters"][1]["data"].all())
       
    nose.tools.assert_almost_equals(actual["parameters"][0]["mean"], expected["parameters"][0]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["max"], expected["parameters"][0]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][0]["min"], expected["parameters"][0]["min"])
       
    nose.tools.assert_almost_equals(actual["parameters"][1]["mean"], expected["parameters"][1]["mean"])
    nose.tools.assert_almost_equals(actual["parameters"][1]["max"], expected["parameters"][1]["max"])
    nose.tools.assert_almost_equals(actual["parameters"][1]["min"], expected["parameters"][1]["min"])


@with_setup(setup, teardown) 
def test_apply_factors():
    
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
    

      