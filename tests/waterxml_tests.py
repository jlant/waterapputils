import nose.tools
from nose import with_setup 

import sys
import numpy as np
import datetime
from StringIO import StringIO

# my module
from waterapputils import waterxml

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: waterxml tests"
   
    # set up fixtures 
 
    fixture["data_file"] = \
        """
        <Project>
            <ProjID>1</ProjID>
            <UserName>jlant</UserName>
            <DateCreated>2014-04-22T10:00:00.0000-00:00</DateCreated>
            <ProjName>my-project</ProjName>
            <Study>
                <StudyID>1</StudyID>
                <ProjID>1</ProjID>
                <StudyLocDecDeg>40.5, -75.9</StudyLocDecDeg>
                <StudyXLocation>1600000.0</StudyXLocation>
                <StudyYLocation>2100000.0</StudyYLocation>
                <StudyDescription>Test simulation</StudyDescription>
                <IsPointApproved>true</IsPointApproved>
                <IsDelineated>true</IsDelineated>
                <IsStudyApproved>true</IsStudyApproved>
                <StudySimulation>
                    <SimulID>1</SimulID>
                    <StudyID>1</StudyID>
                    <RegionType>4</RegionType>
                    <isInitialized>true</isInitialized>
                    <isLoaded>true</isLoaded>
                    <isCompleted>false</isCompleted>
                    <SimulationFeatures>
                        <AttID>1</AttID>
                        <SimulID>1</SimulID>
                        <AttName>Study Unit Total Area</AttName>
                        <AttCode>1</AttCode>
                        <AttMeanVal>100.0</AttMeanVal>
                        <AttMinVal>90.0</AttMinVal>
                        <AttMaxVal>110.0</AttMaxVal>
                        <AttstdDev>0</AttstdDev>
                        <AttDescription> Study unit total area</AttDescription>
                        <AttUnitsCode>303</AttUnitsCode>
                        <AttUnits>(sq Km)</AttUnits>
                    </SimulationFeatures>
                    <SimulationFeatures>
                        <AttID>2</AttID>
                        <SimulID>1</SimulID>
                        <AttName>Total Estimated Stream Area</AttName>
                        <AttCode>37</AttCode>
                        <AttMeanVal>5</AttMeanVal>
                        <AttMinVal>4</AttMinVal>
                        <AttMaxVal>6</AttMaxVal>
                        <AttstdDev>0</AttstdDev>
                        <AttDescription>Estimated area of stream coverage</AttDescription>
                        <AttUnitsCode>303</AttUnitsCode>
                        <AttUnits>(sq Km)</AttUnits>
                    </SimulationFeatures>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>1</BinID>
                        <SimulID>1</SimulID>
                        <BinValueMean>3.1</BinValueMean>
                        <BinValueFraction>0.002</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>2</BinID>
                        <SimulID>1</SimulID>
                        <BinValueMean>4.2</BinValueMean>
                        <BinValueFraction>0.005</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>100.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>110.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>3.0</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>4.5</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>11.1</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>12.2</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                </StudySimulation>             
            </Study>
        </Project>
        """

    fileobj = StringIO(fixture["data_file"])

    fixture["xml_tree"] = waterxml.read_file(fileobj)     
    
    fixture["factors"] = {"January": 2.0,
                          "February": 2.25,
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

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: waterxml tests"      

   
def test_create_project_dict():

    expected = {"ProjID": None, "UserName": None, "DateCreated": None, "ProjName": None}
    
    actual = waterxml.create_project_dict()

    nose.tools.assert_equals(expected["ProjID"], actual["ProjID"])
    nose.tools.assert_equals(expected["UserName"], actual["UserName"])
    nose.tools.assert_equals(expected["DateCreated"], actual["DateCreated"])
    nose.tools.assert_equals(expected["ProjName"], actual["ProjName"])
  
def test_create_study_dict():

    expected = {"StudyID": None, "StudyDescription": None, "StudyLocDecDeg": None}
    
    actual = waterxml.create_study_dict()

    nose.tools.assert_equals(expected["StudyID"], actual["StudyID"])
    nose.tools.assert_equals(expected["StudyDescription"], actual["StudyDescription"])
    nose.tools.assert_equals(expected["StudyLocDecDeg"], actual["StudyLocDecDeg"])
    
def test_create_simulation_dict():

    expected = {"SimulID": [], "StudyID": [], "RegionType": [], "SimulationFeatures": [], "SimulationTopographicWetnessIndex": [], 
                "StudyUnitDischargeSeries": [], "ClimaticPrecipitationSeries": [], "ClimaticTemperatureSeries": []}
    
    actual = waterxml.create_simulation_dict()

    nose.tools.assert_equals(expected["SimulID"], actual["SimulID"])
    nose.tools.assert_equals(expected["StudyID"], actual["StudyID"])
    nose.tools.assert_equals(expected["SimulationFeatures"], actual["SimulationFeatures"])
    nose.tools.assert_equals(expected["SimulationTopographicWetnessIndex"], actual["SimulationTopographicWetnessIndex"])        
    nose.tools.assert_equals(expected["StudyUnitDischargeSeries"], actual["StudyUnitDischargeSeries"])    
    nose.tools.assert_equals(expected["ClimaticPrecipitationSeries"], actual["ClimaticPrecipitationSeries"])    
    nose.tools.assert_equals(expected["ClimaticTemperatureSeries"], actual["ClimaticTemperatureSeries"])  

def test_fill_dict():
    
    expected_project = {"ProjID": "1", "UserName": "jlant", "DateCreated": "2014-04-22T10:00:00.0000-00:00", "ProjName": "my-project"}
    expected_study = {"StudyID": "1", "StudyDescription": "Test simulation", "StudyLocDecDeg": "40.5, -75.9"}
       
    project = waterxml.create_project_dict() 
    study = waterxml.create_study_dict()
    
    actual_project = waterxml.fill_dict(waterxml_tree = fixture["xml_tree"], data_dict = project, element = "Project", keys = project.keys())
    actual_study = waterxml.fill_dict(waterxml_tree = fixture["xml_tree"], data_dict = study, element = "Study", keys = study.keys())

    nose.tools.assert_equals(expected_project["ProjID"], actual_project["ProjID"])
    nose.tools.assert_equals(expected_project["UserName"], actual_project["UserName"])
    nose.tools.assert_equals(expected_project["DateCreated"], actual_project["DateCreated"])
    nose.tools.assert_equals(expected_project["ProjName"], actual_project["ProjName"])
    
    nose.tools.assert_equals(expected_study["StudyID"], actual_study["StudyID"])
    nose.tools.assert_equals(expected_study["StudyDescription"], actual_study["StudyDescription"])
    nose.tools.assert_equals(expected_study["StudyLocDecDeg"], actual_study["StudyLocDecDeg"])
    
def test_fill_simulation_dict():

    expected = {"SimulID": ["1"], "StudyID": ["1"], "RegionType": ["4"], 
                "SimulationFeatures": [[{"SimulID": "1", "AttCode": "1", "AttMinVal": "90.0", "AttName": "Study Unit Total Area", "AttUnits": "(sq Km)", "AttDescription": " Study unit total area", "AttUnitsCode": "303", "AttMaxVal": "110.0", "AttID": "1", "AttstdDev": "0", "AttMeanVal": "100.0"}, 
                                       {"SimulID": "1", "AttCode": "37", "AttMinVal": "4", "AttName": "Total Estimated Stream Area", "AttUnits": "(sq Km)", "AttDescription": "Estimated area of stream coverage", "AttUnitsCode": "303", "AttMaxVal": "6", "AttID": "2", "AttstdDev": "0", "AttMeanVal": "5"}]], 
                                        
                "SimulationTopographicWetnessIndex": [[{"BinID": "1", "SimulID": "1", "BinValueMean": "3.1", "BinValueFraction": "0.002"}, 
                                                       {"BinID": "2", "SimulID": "1", "BinValueMean": "4.2", "BinValueFraction": "0.005"}]],

                "StudyUnitDischargeSeries": [[{"SeriesID": "1", "SeriesDate": "2014-01-01T00:00:00-05:00", "SeriesUnitsCode": "54", "SimulID": "1", "SeriesValue": "100.0", "SeriesUnit": "mm per day"},
                                              {"SeriesID": "2", "SeriesDate": "2014-01-02T00:00:00-05:00", "SeriesUnitsCode": "54", "SimulID": "1", "SeriesValue": "110.0", "SeriesUnit": "mm per day"}]], 

                "ClimaticPrecipitationSeries": [[{"SeriesID": "1", "SeriesDate": "2014-01-01T00:00:00-05:00", "SeriesUnitsCode": "4", "SimulID": "1", "SeriesValue": "3.0", "SeriesUnit": "mm"},
                                                 {"SeriesID": "2", "SeriesDate": "2014-01-02T00:00:00-05:00", "SeriesUnitsCode": "4", "SimulID": "1", "SeriesValue": "4.5", "SeriesUnit": "mm"}]], 
                
                "ClimaticTemperatureSeries": [[{"SeriesID": "1", "SeriesDate": "2014-01-01T00:00:00-05:00", "SeriesUnitsCode": "31", "SimulID": "1", "SeriesValue": "11.1", "SeriesUnit": "Celsius"},
                                               {"SeriesID": "2", "SeriesDate": "2014-01-02T00:00:00-05:00", "SeriesUnitsCode": "31", "SimulID": "1", "SeriesValue": "12.2", "SeriesUnit": "Celsius"}]]
                }
    
    simulation = waterxml.create_simulation_dict()

    actual = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree"], simulation_dict = simulation)
 
    nose.tools.assert_equals(expected["SimulID"], actual["SimulID"])
    nose.tools.assert_equals(expected["StudyID"], actual["StudyID"])
    nose.tools.assert_equals(expected["RegionType"], actual["RegionType"])
    nose.tools.assert_equals(expected["SimulationFeatures"], actual["SimulationFeatures"])
    nose.tools.assert_equals(expected["SimulationTopographicWetnessIndex"], actual["SimulationTopographicWetnessIndex"])
    nose.tools.assert_equals(expected["StudyUnitDischargeSeries"], actual["StudyUnitDischargeSeries"])    
    nose.tools.assert_equals(expected["ClimaticPrecipitationSeries"], actual["ClimaticPrecipitationSeries"]) 
    nose.tools.assert_equals(expected["ClimaticTemperatureSeries"], actual["ClimaticTemperatureSeries"])     

def test_get_topographic_wetness_index_data():

    expected = {"bin_ids": np.array([1., 2.]),
                "bin_value_means": np.array([3.1, 4.2]),
                "bin_value_fractions": np.array([0.002, 0.005])}
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree"], simulation_dict = simulation)

    actual = {}
    actual["bin_ids"], actual["bin_value_means"], actual["bin_value_fractions"] = waterxml.get_topographic_wetness_index_data(simulation_dict = simulation)

    nose.tools.assert_equals(expected["bin_ids"].all(), actual["bin_ids"].all())
    nose.tools.assert_equals(expected["bin_value_means"].all(), actual["bin_value_means"].all())
    nose.tools.assert_equals(expected["bin_value_fractions"].all(), actual["bin_value_fractions"].all())
       
def test_get_timeseries_data():

    expected = {"q_dates": np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]),
                "p_dates": np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]),
                "t_dates": np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]),
                
                "q_values": np.array([100.0, 110.0]),
                "p_values": np.array([3, 4.5]),
                "t_values": np.array([11.1, 12.2]),           
            
                "q_units": "mm per day",
                "p_units": "mm",
                "t_units": "Celsius"
                }
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree"], simulation_dict = simulation)

    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")

    nose.tools.assert_equals(expected["q_dates"].all(), actual["q_dates"].all())
    nose.tools.assert_equals(expected["p_dates"].all(), actual["p_dates"].all())
    nose.tools.assert_equals(expected["t_dates"].all(), actual["t_dates"].all())

    nose.tools.assert_almost_equals(expected["q_values"].all(), actual["q_values"].all())
    nose.tools.assert_almost_equals(expected["p_values"].all(), actual["p_values"].all())
    nose.tools.assert_almost_equals(expected["t_values"].all(), actual["t_values"].all())

    nose.tools.assert_equals(expected["q_units"], actual["q_units"])
    nose.tools.assert_equals(expected["p_units"], actual["p_units"])
    nose.tools.assert_equals(expected["t_units"], actual["t_units"])

def test_apply_factors():
    
    expected = {"q_dates": np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]),
                "p_dates": np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]),
                "t_dates": np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]),
                
                "q_values": np.array([200.0, 220.0]),
                "p_values": np.array([6, 9.]),
                "t_values": np.array([13.1, 14.2]),           
            
                "q_units": "mm per day",
                "p_units": "mm",
                "t_units": "Celsius"
                }


    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree"], simulation_dict = simulation)

    q_dates, q_values, q_units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    p_dates, p_values, p_units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    t_dates, t_values, t_units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")
    
    waterxml.apply_factors(waterxml_tree = fixture["xml_tree"], element = "StudyUnitDischargeSeries", factors = fixture["factors"])
    waterxml.apply_factors(waterxml_tree = fixture["xml_tree"], element = "ClimaticPrecipitationSeries", factors = fixture["factors"])
    waterxml.apply_factors(waterxml_tree = fixture["xml_tree"], element = "ClimaticTemperatureSeries", factors = fixture["factors"])

    simulation_updated = waterxml.create_simulation_dict()

    simulation_updated = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree"], simulation_dict = simulation_updated)
    
    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")

    nose.tools.assert_equals(expected["q_dates"].all(), actual["q_dates"].all())
    nose.tools.assert_equals(expected["p_dates"].all(), actual["p_dates"].all())
    nose.tools.assert_equals(expected["t_dates"].all(), actual["t_dates"].all())

    nose.tools.assert_almost_equals(expected["q_values"].all(), actual["q_values"].all())
    nose.tools.assert_almost_equals(expected["p_values"].all(), actual["p_values"].all())
    nose.tools.assert_almost_equals(expected["t_values"].all(), actual["t_values"].all())

    nose.tools.assert_equals(expected["q_units"], actual["q_units"])
    nose.tools.assert_equals(expected["p_units"], actual["p_units"])
    nose.tools.assert_equals(expected["t_units"], actual["t_units"])
    
             