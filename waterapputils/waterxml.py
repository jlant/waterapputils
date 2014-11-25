# -\*- coding: utf-8 -*-
"""
:Module: waterxml.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading, processing, and writing WATER XML data files.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

try:    
    import xml.etree.cElementTree as ET
except ImportError:    
    import xml.etree.ElementTree as ET

import numpy as np
import datetime
import logging
from StringIO import StringIO
import os

def read_file(filepath):
    """    
    Open WATER xml file using parser from ElementTree library
    
    Parameters
    ----------
    filepath : string
        A string path to file.
        
    Returns
    -------
    tree : ElementTree object  
        Object that contains xml data in a tree. 
        
    """    
    tree = ET.parse(filepath)
        
    return tree

def create_project_dict():
    """
    Create dictionary containing keys that correspond to project elements in the 
    WATER \*.xml file.
    
    Returns
    -------
    project : dictionary 
        Dictionary containing information found in the project element
    
    Notes
    -----
    project = {"ProjID": None, "UserName": None, "DateCreated": None, "ProjName": None}    
    """
    
    project = {"ProjID": None, "UserName": None, "DateCreated": None, "ProjName": None}

    return project 

def create_study_dict():
    """
    Create dictionary containing keys that correspond to study elements in the 
    WATER \*.xml file.
    
    Returns
    -------
    study : dictionary 
        Dictionary containing information found in the study element
    
    Notes
    -----
    study = {"StudyID": None, "StudyLocDecDeg": None, "StudyDescription": None}
    
    """
    study = {"StudyID": None, "StudyLocDecDeg": None, "StudyDescription": None}

    return study 

def create_simulation_dict():
    """
    Create dictionary containing keys that correspond to simulation elements in the 
    WATER \*.xml file. Contains simulation feature information, topographic wetness data, 
    discharge values, precipitation values, and temperature values.
    
    Returns
    -------
    study : dictionary 
        Dictionary containing information found in the study element
    
    Notes
    -----
    simulation = {"SimulID": [], "StudyID": [], "RegionType": [], "SimulationFeatures": [],
             "SimulationTopographicWetnessIndex": [], "StudyUnitDischargeSeries": [],
             "ClimaticPrecipitationSeries": [], "ClimaticTemperatureSeries": []}
    
    """
    simulation = {"SimulID": [], "StudyID": [], "RegionType": [], "SimulationFeatures": [],
             "SimulationTopographicWetnessIndex": [], "StudyUnitDischargeSeries": [],
             "ClimaticPrecipitationSeries": [], "ClimaticTemperatureSeries": []}

    return simulation

def fill_dict(waterxml_tree, data_dict, element, keys):
    """
    Fills a dictionary with information of interest contained in a 
    particular xml element and set of keys.
    
    Parameters
    ----------
    waterxml_tree : ElementTree object 
        Tree object of WATER \*.xml file 
    data_dict : dictionary 
        Dictionary containing keys that match particular children in a particular element
    element : string 
        String of a particular element of interest
    keys: list 
        List of keys to get information from
    
    Returns
    -------
    data_dict : dictionary 
        Dictionary containing keys that match particular children in a particular element 
    """
    for elem in waterxml_tree.iter(tag = element):
        for child in elem:
            for key in data_dict:
                if child.tag == key and key in keys:
                    if type(data_dict[key]) is list:
                        data_dict[key].append(child.text)
                    else:
                        data_dict[key] = child.text

    return data_dict

def get_simulation_data(waterxml_tree, element, sim_id_num):
    """
    Get the data associated with the feature, topographic wetness, and climatic timeseries data.
    
    Parameters
    ----------
    waterxml_tree : ElementTree object 
        Tree object of WATER \*.xml file 
    element : string 
        String of a particular element of interest
    sim_id_num : int
        Integer of the simulation id of interest
    
    Returns
    -------
    data : list
        List of dictionaries each containing data found in the element of interest
    """

    data = []
    for elem in waterxml_tree.iter(tag = element):
        simid = int(elem.find("SimulID").text)
        if simid == int(sim_id_num):
            data_dict = {}            
            for child in elem:
                data_dict[child.tag] = child.text
        
            data.append(data_dict)    
            
    return data    
    
def fill_simulation_dict(waterxml_tree, simulation_dict):
    """
    Fills the simulation dictionary with feature, topographic wetness, and climatic timeseries data.
    
    Parameters
    ----------
    waterxml_tree : ElementTree object 
        Tree object of WATER \*.xml file 
    data_dict : dictionary 
        Dictionary containing keys that match particular children in a particular element
    element : string 
        String of a particular element of interest
    keys: list 
        List of keys to get information from
    
    Returns
    -------
    simulation_dict : dictionary 
        Dictionary containing keys that match particular children in the simulation element
    """
    # fill general information about simulation
    simulation_dict = fill_dict(waterxml_tree = waterxml_tree, data_dict = simulation_dict, element = "StudySimulation", keys = ["SimulID", "StudyID", "RegionType"])    
    
    # fill feature, topographic wetness, and climatic timeseries data
    specific_keys = ["SimulationFeatures", "SimulationTopographicWetnessIndex", "StudyUnitDischargeSeries", "ClimaticPrecipitationSeries", "ClimaticTemperatureSeries"]
    for key in specific_keys:
        for i in range(len(simulation_dict["SimulID"])):                
            data = get_simulation_data(waterxml_tree = waterxml_tree, element = key, sim_id_num = simulation_dict["SimulID"][i])
            simulation_dict[key].append(data)
    
    return simulation_dict
    
def get_xml_data(waterxml_tree):
    """
    Get information of interest contained in the 'Project', 'Study', and 
    'StudySimulation' xml elements. Return three dictionaries containing 
    information of interest:
    
    Parameters
    ----------
    waterxml_tree : ElementTree object 
        Tree object of WATER \*.xml file 
    
    Returns
    -------
    project : dictionary 
        Dictionary containing information found in the 'Project' element
    study : dictionary 
        Dictionary containing information found in the 'Study' element
    simulation : dictionary 
        Dictionary containing information found in the 'StudySimulation' element
        
    See Also
    --------
    create_project_dict(), create_study_dict(), create_simulation_dict()       
    """    
    
    project = create_project_dict()
    study = create_study_dict()
    simulation = create_simulation_dict()
    
    # get information for elements of interest and fill respective dictionaries
    project = fill_dict(waterxml_tree = waterxml_tree, data_dict = project, element = "Project", keys = project.keys())
    study = fill_dict(waterxml_tree = waterxml_tree, data_dict = study, element = "Study", keys = study.keys())
    
    # get the rest of the study_simulation data; features, topographic wetness data, and climate data
    simulation = fill_simulation_dict(waterxml_tree = waterxml_tree, simulation_dict = simulation) 
                                                                                                                                                                                                                         
    return project, study, simulation


def get_series_date(date_time):
    """   
    Get dates, values, and units from timeseries parameters contained in the 
    simulation dictionary. i.e. 2014-01-01T00:00:00-05:00
    
    Parameters
    ----------
    date_time : string
        String date value
        
    Returns
    -------
    date : Datetime object     
    """
    date_str = date_time.split('T')[0]            
    year = date_str.split('-')[0]
    month = date_str.split('-')[1]
    day = date_str.split('-')[2]
    date = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
    
    return date

def get_topographic_wetness_index_data(simulation_dict):
    """   
    Get bin id, bin mean value, and bin fraction for topographic wetness index data contained in the 
    simulation dictionary. '
    
    Parameters
    ----------
    simulation_dict : dictionary 
        Dictionary containing keys that match particular children in the simulation element
        
    Returns
    -------
    bin_ids : numpy array
        Array of float values
    bin_value_means : numpy array
        Array of float values
    bin_value_fractions : numpy array
        Array of float values

    Notes
    -----
    Each topographic wetness index parameter has the following xml elements:
    'BinID'
    'SimulID'
    'BinValueMean'
    'BinValueFraction'        
    """
    bin_ids = []
    bin_value_means = []
    bin_value_fractions = []     
    for i in range(len(simulation_dict["SimulID"])):                            # loop for each simulation id
        bin_id = []
        bin_value_mean = []
        bin_value_fraction = []                            
        parameter = simulation_dict["SimulationTopographicWetnessIndex"][i]     # get the topographic wetness index for a particular simulation id
        for j in range(len(parameter)):                                         # loop for each parameter dictionary for a particular simulation id          
            idnum = parameter[j]["BinID"]
            mean = parameter[j]["BinValueMean"]
            fraction = parameter[j]["BinValueFraction"]
            
            bin_id.append(idnum)
            bin_value_mean.append(mean)            
            bin_value_fraction.append(fraction)

        bin_id = np.array(bin_id, dtype = float)    
        bin_value_mean = np.array(bin_value_mean, dtype = float)
        bin_value_fraction = np.array(bin_value_fraction, dtype = float)

        bin_ids.append(bin_id)
        bin_value_means.append(bin_value_mean)            
        bin_value_fractions.append(bin_value_fraction)
    
    return bin_ids, bin_value_means, bin_value_fractions


    
def get_timeseries_data(simulation_dict, timeseries_key):
    """   
    Get dates, values, and units for a timeseries for all 'SimulID' contained in the 
    simulation dictionary. Return lists of dates, values, and units which correspond to
    the number of simulations
    
    Parameters
    ----------
    simulation_dict : dictionary 
        Dictionary containing keys that match particular children in the simulation element
    timeseries_key : string
        String parameter name of a timeseries parameter
        
    Returns
    -------
    dates : list
        list of numpy arrays of datetime objects
    values : list
        list of numpy arrays of float values
    units : list
        list of strings

    Notes
    -----
    Valid key values for the timeseries parameter include "StudyUnitDischargeSeries", 
    "ClimaticPrecipitationSeries", or "ClimaticTemperatureSeries"

    Each timeseries parameter has the following xml elements:
    'SeriesID'
    'SimulID'
    'SeriesDate'
    'SeriesValue'
    'SeriesUnitCode'
    'SeriesUnit' 

    The original structure of the WATER \*.xml unfortunately has lots of repeated data across SimulID's
    The original \*.xml structure repeats each timeseries 3 times since there are always 3 SimulID's.
    This is why the \*.xml has such a large size.
    
    For example, for StudyUnitDischargeSeries if there were 2 dates and 2 corresponding values, there would be 3 repeated arrays of data each corresponding to a particular SimulID
    
    "SimulID" = ['1', '2', '3']    
    dates = [array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0), array([datetime.datetime(2014, 1, 1, 0, 0), datetime.datetime(2014, 1, 2, 0, 0) ]       
    values = [array([ 100.,  110.]), array([ 100.,  110.]), array([ 100.,  110.])]
    units = ['mm per day', 'mm per day', 'mm per day']
    """
    
    assert timeseries_key in ["StudyUnitDischargeSeries", "ClimaticPrecipitationSeries", "ClimaticTemperatureSeries"], "Key {} not a valid timeseries parameter name".format(timeseries_key)

    dates = []
    values = []
    units = []     
    for i in range(len(simulation_dict["SimulID"])):        # loop for each simulation id
        date = []
        value = []
        unit = []
        parameter = simulation_dict[timeseries_key][i]      # get the timeseries parameter for a particular simulation id
        for j in range(len(parameter)):                     # loop for each parameter dictionary for a particular simulation id
            d = get_series_date(date_time = parameter[j]["SeriesDate"])                       
            v = parameter[j]['SeriesValue']
            u = parameter[j]['SeriesUnit']
            
            date.append(d)
            value.append(v)            
            unit.append(u)
            
        date = np.array(date)    
        value = np.array(value, dtype = float)
        unit = unit[0]
          
        dates.append(date)
        values.append(value)
        units.append(unit)
    
    return dates, values, units

def apply_factors(waterxml_tree, element, factors):
    """
    Apply monthly factors to a specific element (parameter). The factors are applied 
    to the particular element tag.  If the element is 'ClimaticTemperatureSeries'
    the factor is additive, otherwise the factor is multiplicative.
     
    Parameters
    ----------
    waterxml_tree : ElementTree object 
        Tree object of WATER \*.xml file 
    element : string
        String name of parameter
    factors : dictionary
        Dictionary holding monthly multiplicative factors
    
    Notes
    -----    
    factors = {

        'January': 2.0,
        
        'February': 0.98,
        
        'March': 0.97,
        
        'April': 1.04,
        
        'May': 1.10,
        
        'June': 0.99,
        
        'July': 0.97,
        
        'August': 1.25,
        
        'September': 1.21,
        
        'October': 1.11,
        
        'November': 1.10,
        
        'December': 2.0

    }  
    """
    for elem in waterxml_tree.iter(tag = element):
        # get element date and match the appropriate factor fraom factors   
        date = get_series_date(date_time = elem.find('SeriesDate').text)

        # match the month from the date value to the factors dictionary key
        month = date.strftime("%B")     # get month 
        factor = factors[month]         # get the factor that corresponds to a specific month 
        
        # get element value
        elem_value = elem.find('SeriesValue')
        
        # calculate new value based on monthly factor
        if element == 'ClimaticTemperatureSeries':
            new_value = float(elem_value.text) + factor
        else:
            new_value = float(elem_value.text) * factor
        
        # set new value
        elem_value.text = "{}".format(new_value)

def write_file(waterxml_tree, save_path, filename = "WATERSimulation.xml"):
    """   
    Write xml data contained in water xml tree to an output file in the 
    same format as the original WATER output xml file.
    
    Parameters
    ----------
    waterxml_tree : ElementTree object 
        Tree object of WATER \*.xml file 
    save_path : string 
        String path to save file.
    filename : string
        String name of output file. Default name is WATER.txt.
    """    
    filepath = os.path.join(save_path, filename) 
    
    waterxml_tree.write(filepath) 


def get_study_unit_total_area(simulation_dict):
    """   
    Get study unit total area for simulation feature data contained in the 
    simulation dictionary. '
    
    Parameters
    ----------
    simulation_dict : dictionary 
        Dictionary containing keys that match particular children in the simulation element
        
    Returns
    -------
    area_means : numpy array
        Array of float values

    Notes
    -----
    Each Simulation Feature parameter has the following xml elements:
    'SimulID'
    'AttID'
    'AttstdDev'
    'AttCode'
    'AttName'
    'AttUnits'
    'AttUnitsCode'
    'AttDescription'
    'AttMaxVal'
    'AttMeanVal'
    'AttMinVal'
    """
    area_means = []
    for i in range(len(simulation_dict["SimulID"])):                            
        area_mean = []
        parameter = simulation_dict["SimulationFeatures"][i]                    
        for j in range(len(parameter)):
            name = parameter[j]["AttName"]                                                  
            if name == "Study Unit Total Area":
                mean = parameter[j]["AttMeanVal"]  

                area_mean.append(mean)

        area_mean = np.array(area_mean, dtype = float)

        area_means.append(area_mean)            

    return area_means


def _create_test_data():
    """ Create test data to use with tests """
    
    fixture = {}
    
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
    
    xml_tree = read_file(fileobj)  

    return xml_tree    

def _print_test_info(actual, expected):
    """   
    For testing purposes, assert that all expected values and actual values match. 
    Prints assertion error when there is no match.  Prints values to user to scan
    if interested. Helps a lot for debugging. This function mirrors what is done
    in nosetests.
    
    Parameters
    ----------
    expected : dictionary  
        Dictionary holding expected data values
    actual : dictionary
        Dictionary holding expected data values
    """
    for key in actual.keys():
        np.testing.assert_equal(actual[key], expected[key], err_msg = "For key * {} *, actual value(s) * {} * do not equal expected value(s) * {} *".format(key, actual[key], expected[key]))        

        print("*{}*".format(key))                     
        print("    actual:   {}".format(actual[key]))  
        print("    expected: {}\n".format(expected[key]))

def test_create_project_dict():
    """ Test functionality of create_project_dict """

    print("--- Testing create_project_dict() ---") 

    # expected values to test with actual values
    expected = {"ProjID": None, "UserName": None, "DateCreated": None, "ProjName": None}
    
    # actual values
    actual = create_project_dict()
  
    # print results
    _print_test_info(actual, expected) 

def test_create_study_dict():
    """ Test functionality of create_study_dict """

    print("--- Testing create_study_dict() ---") 

    # expected values to test with actual values
    expected = {"StudyID": None, "StudyLocDecDeg": None, "StudyDescription": None}
    
    # actual values
    actual = create_study_dict()
  
    # print results
    _print_test_info(actual, expected) 


def test_create_simulation_dict():
    """ Test functionality of create_simulation_dict """

    print("--- Testing create_simulation_dict() ---") 

    # expected values to test with actual values
    expected = {"SimulID": [], "StudyID": [], "RegionType": [], "SimulationFeatures": [],
             "SimulationTopographicWetnessIndex": [], "StudyUnitDischargeSeries": [],
             "ClimaticPrecipitationSeries": [], "ClimaticTemperatureSeries": []}
    
    # actual values
    actual = create_simulation_dict()
  
    # print results
    _print_test_info(actual, expected) 


def test_fill_dict():
    """ Test functionality of fill_dict """

    print("--- Testing fill_dict() ---")    

    expected_project = {"ProjID": "1", "UserName": "jlant", "DateCreated": "2014-04-22T10:00:00.0000-00:00", "ProjName": "my-project"}
    expected_study = {"StudyID": "1", "StudyLocDecDeg": "40.5, -75.9", "StudyDescription": "Test simulation"}
    
    xml_tree = _create_test_data()
    
    project = create_project_dict() 
    study = create_study_dict()
    
    actual_project = fill_dict(waterxml_tree = xml_tree, data_dict = project, element = "Project", keys = project.keys())
    actual_study = fill_dict(waterxml_tree = xml_tree, data_dict = study, element = "Study", keys = study.keys())

    # print results
    _print_test_info(actual_project, expected_project) 
    _print_test_info(actual_study, expected_study) 
      
def test_fill_simulation_dict():
    """ Test functionality of fill_dict """

    print("--- Testing fill_dict() ---")     

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
    

    xml_tree = _create_test_data()
    
    simulation = create_simulation_dict()

    # actual values
    actual = fill_simulation_dict(waterxml_tree = xml_tree, simulation_dict = simulation)
    
    # print results
    _print_test_info(actual, expected)


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
  


    xml_tree = _create_test_data()
    
    actual_project, actual_study, actual_simulation = get_xml_data(waterxml_tree = xml_tree)

    # print results
    _print_test_info(actual_project, expected_project)
    _print_test_info(actual_study, expected_study)
    _print_test_info(actual_simulation, expected_simulation)


def test_get_topographic_wetness_index_data():
    """ Test get_topographic_wetness_index_data """

    print("--- get_topographic_wetness_index_data() ---")     

    expected = {"bin_ids": [np.array([1., 2.])],
                "bin_value_means": [np.array([3.1, 4.2])],
                "bin_value_fractions": [np.array([0.002, 0.005])]}    

    xml_tree = _create_test_data()
    
    simulation = create_simulation_dict()

    simulation = fill_simulation_dict(waterxml_tree = xml_tree, simulation_dict = simulation)

    actual = {}
    actual["bin_ids"], actual["bin_value_means"], actual["bin_value_fractions"] = get_topographic_wetness_index_data(simulation_dict = simulation)

     # print results
    _print_test_info(actual, expected)
    

def test_get_timeseries_data():
    """ Test get_timeseries_data """

    print("--- Testing get_timeseries_data() ---")     

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
    
    xml_tree = _create_test_data()
    
    simulation = create_simulation_dict()

    simulation = fill_simulation_dict(waterxml_tree = xml_tree, simulation_dict = simulation)

    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")

     # print results
    _print_test_info(actual, expected)
               
def test_apply_factors():
    """ Test apply_factors functionality """

    print("--- Testing apply_factors() ---") 

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


    factors = {
        "January": 2.0,
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
    
    month = "January"

    print("*Factor used*\n    expected : actual")
    print("    2.0 : {}".format(factors[month]))
    print("")
    
    xml_tree = _create_test_data()
    
    simulation = create_simulation_dict()

    simulation = fill_simulation_dict(waterxml_tree = xml_tree, simulation_dict = simulation)

    q_dates, q_values, q_units = get_timeseries_data(simulation_dict = simulation, timeseries_key = "StudyUnitDischargeSeries")
    p_dates, p_values, p_units = get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticPrecipitationSeries")
    t_dates, t_values, t_units = get_timeseries_data(simulation_dict = simulation, timeseries_key = "ClimaticTemperatureSeries")
    
    apply_factors(waterxml_tree = xml_tree, element = "StudyUnitDischargeSeries", factors = factors)
    apply_factors(waterxml_tree = xml_tree, element = "ClimaticPrecipitationSeries", factors = factors)
    apply_factors(waterxml_tree = xml_tree, element = "ClimaticTemperatureSeries", factors = factors)

    simulation_updated = create_simulation_dict()

    simulation_updated = fill_simulation_dict(waterxml_tree = xml_tree, simulation_dict = simulation_updated)

    actual = {}
    actual["q_dates"], actual["q_values"], actual["q_units"] = get_timeseries_data(simulation_dict = simulation_updated, timeseries_key = "StudyUnitDischargeSeries")
    actual["p_dates"], actual["p_values"], actual["p_units"] = get_timeseries_data(simulation_dict = simulation_updated, timeseries_key = "ClimaticPrecipitationSeries")
    actual["t_dates"], actual["t_values"], actual["t_units"] = get_timeseries_data(simulation_dict = simulation_updated, timeseries_key = "ClimaticTemperatureSeries")

     # print results
    _print_test_info(actual, expected)

def test_write_file():
    """ Test write_file functionality """

    print("--- Testing write_file ---") 

    factors = {
        "January": 2.0,
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
    
    xml_tree = _create_test_data()
    write_file(waterxml_tree = xml_tree , save_path = os.getcwd())

    apply_factors(waterxml_tree = xml_tree, element = "StudyUnitDischargeSeries", factors = factors)
    apply_factors(waterxml_tree = xml_tree, element = "ClimaticPrecipitationSeries", factors = factors)
    apply_factors(waterxml_tree = xml_tree, element = "ClimaticTemperatureSeries", factors = factors)

    write_file(waterxml_tree = xml_tree , save_path = os.getcwd(), filename = "WATERSimulation_updated.xml")

    print("Created 2 files {} and {} in current working directory. Please check for proper writing".format("WATERSimulation.xml", "WATERSimulation_sampledeltas.xml")) 
    print("")  


def test_get_study_unit_total_area():
    """ Test get_topographic_wetness_index_data """

    print("--- get_topographic_wetness_index_data() ---")     

    expected = {"area_means": [np.array([100.])],
    }  

    xml_tree = _create_test_data()
    
    simulation = create_simulation_dict()

    simulation = fill_simulation_dict(waterxml_tree = xml_tree, simulation_dict = simulation)

    actual = {}
    actual["area_means"] = get_study_unit_total_area(simulation_dict = simulation)

     # print results
    _print_test_info(actual, expected)

def main():
    """ Test functionality waterxml.py """

    print("")
    print("RUNNING TESTS ...")
    print("")
    
    # test_create_project_dict()
     
    # test_create_study_dict()

    # test_create_simulation_dict()
    
    # test_fill_dict()

    # test_fill_simulation_dict()

    # test_get_xml_data()

    # test_get_topographic_wetness_index_data()
    
    # test_get_timeseries_data()

    # test_apply_factors()

    # test_write_file()

    test_get_study_unit_total_area()
    
if __name__ == "__main__":
    main()