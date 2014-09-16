import nose.tools
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
 
    fixture["data_file1"] = \
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

    fixture["data_file2"] = \
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
                <StudySimulation>
                    <SimulID>2</SimulID>
                    <StudyID>1</StudyID>
                    <RegionType>4</RegionType>
                    <isInitialized>true</isInitialized>
                    <isLoaded>true</isLoaded>
                    <isCompleted>false</isCompleted>
                    <SimulationFeatures>
                        <AttID>1</AttID>
                        <SimulID>2</SimulID>
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
                        <SimulID>2</SimulID>
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
                        <SimulID>2</SimulID>
                        <BinValueMean>3.1</BinValueMean>
                        <BinValueFraction>0.002</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>2</BinID>
                        <SimulID>2</SimulID>
                        <BinValueMean>4.2</BinValueMean>
                        <BinValueFraction>0.005</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>2</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>100.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>2</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>110.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>2</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>3.0</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>2</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>4.5</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>2</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>11.1</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>2</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>12.2</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                </StudySimulation>             
            </Study>
        </Project>
        """


    fileobj1 = StringIO(fixture["data_file1"])
    fileobj2 = StringIO(fixture["data_file2"])

    fixture["xml_tree1"] = waterxml.read_file(fileobj1)  
    fixture["xml_tree2"] = waterxml.read_file(fileobj2)     
    
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

    nose.tools.assert_equals(actual["ProjID"], expected["ProjID"])
    nose.tools.assert_equals(actual["UserName"], expected["UserName"])
    nose.tools.assert_equals(actual["DateCreated"], expected["DateCreated"])
    nose.tools.assert_equals(actual["ProjName"], actual["ProjName"])
  
def test_create_study_dict():

    expected = {"StudyID": None, "StudyDescription": None, "StudyLocDecDeg": None}
    
    actual = waterxml.create_study_dict()

    nose.tools.assert_equals(actual["StudyID"], expected["StudyID"])
    nose.tools.assert_equals(actual["StudyDescription"], expected["StudyDescription"])
    nose.tools.assert_equals(actual["StudyLocDecDeg"], expected["StudyLocDecDeg"])
    
def test_create_simulation_dict():

    expected = {"SimulID": [], "StudyID": [], "RegionType": [], "SimulationFeatures": [], "SimulationTopographicWetnessIndex": [], 
                "StudyUnitDischargeSeries": [], "ClimaticPrecipitationSeries": [], "ClimaticTemperatureSeries": []}
    
    actual = waterxml.create_simulation_dict()

    nose.tools.assert_equals(actual["SimulID"], expected["SimulID"])
    nose.tools.assert_equals(actual["StudyID"], expected["StudyID"])
    nose.tools.assert_equals(actual["SimulationFeatures"], expected["SimulationFeatures"])
    nose.tools.assert_equals(actual["SimulationTopographicWetnessIndex"], expected["SimulationTopographicWetnessIndex"])        
    nose.tools.assert_equals(actual["StudyUnitDischargeSeries"], expected["StudyUnitDischargeSeries"])    
    nose.tools.assert_equals(actual["ClimaticPrecipitationSeries"], expected["ClimaticPrecipitationSeries"])    
    nose.tools.assert_equals(actual["ClimaticTemperatureSeries"], expected["ClimaticTemperatureSeries"])  

def test_fill_dict():
    
    expected_project = {"ProjID": "1", "UserName": "jlant", "DateCreated": "2014-04-22T10:00:00.0000-00:00", "ProjName": "my-project"}
    expected_study = {"StudyID": "1", "StudyDescription": "Test simulation", "StudyLocDecDeg": "40.5, -75.9"}
       
    project = waterxml.create_project_dict() 
    study = waterxml.create_study_dict()
    
    actual_project = waterxml.fill_dict(waterxml_tree = fixture["xml_tree1"], data_dict = project, element = "Project", keys = project.keys())
    actual_study = waterxml.fill_dict(waterxml_tree = fixture["xml_tree1"], data_dict = study, element = "Study", keys = study.keys())

    nose.tools.assert_equals(actual_project["ProjID"], expected_project["ProjID"])
    nose.tools.assert_equals(actual_project["UserName"], expected_project["UserName"])
    nose.tools.assert_equals(actual_project["DateCreated"], expected_project["DateCreated"])
    nose.tools.assert_equals(actual_project["ProjName"], expected_project["ProjName"])
    
    nose.tools.assert_equals(actual_study["StudyID"], expected_study["StudyID"])
    nose.tools.assert_equals(actual_study["StudyDescription"], expected_study["StudyDescription"])
    nose.tools.assert_equals(actual_study["StudyLocDecDeg"], expected_study["StudyLocDecDeg"])
    
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

    actual = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree1"], simulation_dict = simulation)
 
    nose.tools.assert_equals(actual["SimulID"], expected["SimulID"])
    nose.tools.assert_equals(actual["StudyID"], expected["StudyID"])
    nose.tools.assert_equals(actual["RegionType"], expected["RegionType"])
    nose.tools.assert_equals(actual["SimulationFeatures"], expected["SimulationFeatures"])
    nose.tools.assert_equals(actual["SimulationTopographicWetnessIndex"], expected["SimulationTopographicWetnessIndex"])
    nose.tools.assert_equals(actual["StudyUnitDischargeSeries"], expected["StudyUnitDischargeSeries"])    
    nose.tools.assert_equals(actual["ClimaticPrecipitationSeries"], expected["ClimaticPrecipitationSeries"]) 
    nose.tools.assert_equals(actual["ClimaticTemperatureSeries"], expected["ClimaticTemperatureSeries"])     

def test_get_xml_data():
    """ Test get_xml_data """

    print("--- Testing get_xml_data() ---")     

    expected_project = {"ProjID": "1", "UserName": "jlant", "DateCreated": "2014-04-22T10:00:00.0000-00:00", "ProjName": "my-project"}
    expected_study = {"StudyID": "1", "StudyLocDecDeg": "40.5, -75.9", "StudyDescription": "Test simulation"}

    expected_simulation = {"SimulID": ["1"], "StudyID": ["1"], "RegionType": ["4"], 
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
  
   
    actual_project, actual_study, actual_simulation = waterxml.get_xml_data(waterxml_tree = fixture["xml_tree1"])

    # print results
    np.testing.assert_equal(actual_project, expected_project)
    np.testing.assert_equal(actual_study, expected_study)
    np.testing.assert_equal(actual_simulation, expected_simulation)


def test_get_topographic_wetness_index_data_file1():

    expected = {"bin_ids": [np.array([1., 2.])],
                "bin_value_means": [np.array([3.1, 4.2])],
                "bin_value_fractions": [np.array([0.002, 0.005])]}
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree1"], simulation_dict = simulation)

    actual = {}
    actual["bin_ids"], actual["bin_value_means"], actual["bin_value_fractions"] = waterxml.get_topographic_wetness_index_data(simulation_dict = simulation)

    nose.tools.assert_equals(len(actual["bin_ids"]), len(expected["bin_ids"]))
    nose.tools.assert_equals(len(actual["bin_value_means"]), len(expected["bin_value_means"]))
    nose.tools.assert_equals(len(actual["bin_value_fractions"]), len(expected["bin_value_fractions"]))

    np.testing.assert_equal(actual["bin_ids"][0], expected["bin_ids"][0])
    np.testing.assert_equal(actual["bin_value_means"][0], expected["bin_value_means"][0])
    np.testing.assert_equal(actual["bin_value_fractions"][0], expected["bin_value_fractions"][0])


def test_get_topographic_wetness_index_data_file2():

    expected = {"bin_ids": [np.array([1., 2.]), np.array([1., 2.])],
                "bin_value_means": [np.array([3.1, 4.2]), np.array([3.1, 4.2])],
                "bin_value_fractions": [np.array([0.002, 0.005]), np.array([0.002, 0.005])]}
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree2"], simulation_dict = simulation)

    actual = {}
    actual["bin_ids"], actual["bin_value_means"], actual["bin_value_fractions"] = waterxml.get_topographic_wetness_index_data(simulation_dict = simulation)

    nose.tools.assert_equals(len(actual["bin_ids"]), len(expected["bin_ids"]))
    nose.tools.assert_equals(len(actual["bin_value_means"]), len(expected["bin_value_means"]))
    nose.tools.assert_equals(len(actual["bin_value_fractions"]), len(expected["bin_value_fractions"]))

    np.testing.assert_equal(actual["bin_ids"][0], expected["bin_ids"][0])
    np.testing.assert_equal(actual["bin_value_means"][0], expected["bin_value_means"][0])
    np.testing.assert_equal(actual["bin_value_fractions"][0], expected["bin_value_fractions"][0])

    np.testing.assert_equal(actual["bin_ids"][1], expected["bin_ids"][1])
    np.testing.assert_equal(actual["bin_value_means"][1], expected["bin_value_means"][1])
    np.testing.assert_equal(actual["bin_value_fractions"][1], expected["bin_value_fractions"][1])
       
def test_get_timeseries_data_file1():

    expected = {"q_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                "p_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                "t_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                
                "q_values": [np.array([100.0, 110.0])],
                "p_values": [np.array([3, 4.5])],
                "t_values": [np.array([11.1, 12.2])],           
            
                "q_units": ["mm per day"],
                "p_units": ["mm"],
                "t_units": ["Celsius"]
                }
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree1"], simulation_dict = simulation)

    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")

    nose.tools.assert_equals(len(actual["q_dates"]), len(expected["q_dates"]))
    nose.tools.assert_equals(len(actual["p_dates"]), len(expected["p_dates"]))
    nose.tools.assert_equals(len(actual["t_dates"]), len(expected["t_dates"]))

    np.testing.assert_equal(actual["q_dates"][0], expected["q_dates"][0])
    np.testing.assert_equal(actual["p_dates"][0], expected["p_dates"][0])
    np.testing.assert_equal(actual["t_dates"][0], expected["t_dates"][0])

    np.testing.assert_equal(actual["q_values"][0], expected["q_values"][0])
    np.testing.assert_equal(actual["p_values"][0], expected["p_values"][0])
    np.testing.assert_equal(actual["t_values"][0], expected["t_values"][0])

    np.testing.assert_equal(actual["q_units"][0], expected["q_units"][0])
    np.testing.assert_equal(actual["p_units"][0], expected["p_units"][0])
    np.testing.assert_equal(actual["t_units"][0], expected["t_units"][0])

def test_get_timeseries_data_file2():

    expected = {"q_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]), np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                "p_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]), np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                "t_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)]), np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                
                "q_values": [np.array([100.0, 110.0]), np.array([100.0, 110.0])],
                "p_values": [np.array([3, 4.5]), np.array([3, 4.5])],
                "t_values": [np.array([11.1, 12.2]), np.array([11.1, 12.2])],           
            
                "q_units": ["mm per day", "mm per day"],
                "p_units": ["mm", "mm"],
                "t_units": ["Celsius", "Celsius"]
                }
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree2"], simulation_dict = simulation)

    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")

    nose.tools.assert_equals(len(expected["q_dates"]), len(actual["q_dates"]))
    nose.tools.assert_equals(len(expected["p_dates"]), len(actual["p_dates"]))
    nose.tools.assert_equals(len(expected["t_dates"]), len(actual["t_dates"]))

    np.testing.assert_equal(actual["q_dates"][0], expected["q_dates"][0])
    np.testing.assert_equal(actual["p_dates"][0], expected["p_dates"][0])
    np.testing.assert_equal(actual["t_dates"][0], expected["t_dates"][0])

    np.testing.assert_equal(actual["q_values"][0], expected["q_values"][0])
    np.testing.assert_equal(actual["p_values"][0], expected["p_values"][0])
    np.testing.assert_equal(actual["t_values"][0], expected["t_values"][0])

    np.testing.assert_equal(actual["q_units"][0], expected["q_units"][0])
    np.testing.assert_equal(actual["p_units"][0], expected["p_units"][0])
    np.testing.assert_equal(actual["t_units"][0], expected["t_units"][0])

    np.testing.assert_equal(actual["q_dates"][1], expected["q_dates"][1])
    np.testing.assert_equal(actual["p_dates"][1], expected["p_dates"][1])
    np.testing.assert_equal(actual["t_dates"][1], expected["t_dates"][1])

    np.testing.assert_equal(actual["q_values"][1], expected["q_values"][1])
    np.testing.assert_equal(actual["p_values"][1], expected["p_values"][1])
    np.testing.assert_equal(actual["t_values"][1], expected["t_values"][1])

    np.testing.assert_equal(actual["q_units"][1], expected["q_units"][1])
    np.testing.assert_equal(actual["p_units"][1], expected["p_units"][1])
    np.testing.assert_equal(actual["t_units"][1], expected["t_units"][1])


def test_apply_factors():
    
    expected = {"q_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                "p_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                "t_dates": [np.array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0)])],
                
                "q_values": [np.array([200.0, 220.0])],
                "p_values": [np.array([6, 9.])],
                "t_values": [np.array([13.1, 14.2])],           
            
                "q_units": ["mm per day"],
                "p_units": ["mm"],
                "t_units": ["Celsius"]
                }
    
    simulation = waterxml.create_simulation_dict()

    simulation = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree1"], simulation_dict = simulation)

    q_dates, q_values, q_units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    p_dates, p_values, p_units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    t_dates, t_values, t_units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")
    
    waterxml.apply_factors(waterxml_tree = fixture["xml_tree1"], element = "StudyUnitDischargeSeries", factors = fixture["factors"])
    waterxml.apply_factors(waterxml_tree = fixture["xml_tree1"], element = "ClimaticPrecipitationSeries", factors = fixture["factors"])
    waterxml.apply_factors(waterxml_tree = fixture["xml_tree1"], element = "ClimaticTemperatureSeries", factors = fixture["factors"])

    simulation_updated = waterxml.create_simulation_dict()

    simulation_updated = waterxml.fill_simulation_dict(waterxml_tree = fixture["xml_tree1"], simulation_dict = simulation_updated)
    
    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = waterxml.get_timeseries_data(simulation_dict = simulation_updated, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = waterxml.get_timeseries_data(simulation_dict = simulation_updated, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = waterxml.get_timeseries_data(simulation_dict = simulation_updated, timeseries_key = "ClimaticTemperatureSeries")

    nose.tools.assert_equals(len(expected["q_dates"]), len(actual["q_dates"]))
    nose.tools.assert_equals(len(expected["p_dates"]), len(actual["p_dates"]))
    nose.tools.assert_equals(len(expected["t_dates"]), len(actual["t_dates"]))

    np.testing.assert_equal(actual["q_dates"][0], expected["q_dates"][0])
    np.testing.assert_equal(actual["p_dates"][0], expected["p_dates"][0])
    np.testing.assert_equal(actual["t_dates"][0], expected["t_dates"][0])

    np.testing.assert_equal(actual["q_values"][0], expected["q_values"][0])
    np.testing.assert_equal(actual["p_values"][0], expected["p_values"][0])
    np.testing.assert_equal(actual["t_values"][0], expected["t_values"][0])

    np.testing.assert_equal(actual["q_units"][0], expected["q_units"][0])
    np.testing.assert_equal(actual["p_units"][0], expected["p_units"][0])
    np.testing.assert_equal(actual["t_units"][0], expected["t_units"][0])
    
             