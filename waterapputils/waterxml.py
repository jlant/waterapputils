# -*- coding: utf-8 -*-
"""
Purpose: learn how to parse xml files

Source: http://docs.python.org/3/library/xml.etree.elementtree.html
"""

try:    
    import xml.etree.cElementTree as ET
except ImportError:    
    import xml.etree.ElementTree as ET


def fill_info(data_dict = None, element_str = None):
    """
    Fills a dictionary with information of interest contained in a 
    particular xml element.
    
    *Parameters:*
        data_dict : dictionary containing keys that match particular children in an element
        element_str : string of a particular element of interest
    
    *Return:*
        data_dict : dictionary containing data found in the element of interest  
    """
    for elem in tree.iter(tag = element_str):
        for child in elem:
            for key in data_dict:
                if child.tag == key:
                    data_dict[key] = child.text

    return data_dict

def get_data(element_str = None, sim_id_num = None):
    """
    Get all data parameters for an xml element for a particular simulation 
    id number, and return a list of dictionaries each containing the data 
    parameters found for the xml element.
    Done this way due to the struture of the WATERSimulation.xml file; repeated
    xml elements for different simulation id numbers.
    
    *Parameters:*
        element_str : string of a particular element of interest
        sim_id_num : integer of the simulation id of interest
    
    *Return:*
        data : list of dictionaries each containing data found in the element of interest  
    """        
    data = []
    for elem in tree.iter(tag = element_str):
        simid = int(elem.find('SimulID').text)
        if simid == sim_id_num:
            data_dict = {}            
            for child in elem:
                data_dict[child.tag] = child.text
        
            data.append(data_dict)    
            
    return data


def set_data(element_str = None, element_tag_str = None, sim_id_num = None, multiplicative_factor = None):
    """
    Set new data for a particular element tag in a particular xml element for
    a particular simulation id number using a multiplicative factor.  
    Multiplicative factor is applied to the particular element tag.
    
    *Parameters:*
        element_str : string of a particular element of interest
        element_tag_str : string of a particular element tag of interest
        sim_id_num : integer of the simulation id of interest
        mulitplicative_factor : float factor
    
    *Return:*
        No return
    """        
    for elem in tree.iter(tag = element_str):
        simid = int(elem.find('SimulID').text)
        if simid == sim_id_num:
            for child in elem:
                if child.tag == element_tag_str:
                     new_num = float(child.text) * multiplicative_factor
                     child.text = str(new_num)

tree = ET.parse('WATERSimulation.xml')
root = tree.getroot()
    
# define dictionaries for elements interest
project = {
    'ProjID': None,
    'UserName': None,
    'DateCreated': None,
    'ProjName': None
}

study = {
    'StudyID': None,
    'StudyLocDecDeg': None,
    'StudyDescription': None
}

# get information for elements of interest
project = fill_info(data_dict = project, element_str = 'Project')
study = fill_info(data_dict = study, element_str = 'Study')

# get simulation features, twi, discharge, precip, and temp for simulation number 1
sim_features1 = get_data(element_str = 'SimulationFeatures', sim_id_num = 1)
twi1 = get_data(element_str = 'SimulationTopographicWetnessIndex', sim_id_num = 1)
discharge1 = get_data(element_str = 'StudyUnitDischargeSeries', sim_id_num = 1)
precip1 = get_data(element_str = 'ClimaticPrecipitationSeries', sim_id_num = 1)
temp1 = get_data(element_str = 'ClimaticTemperatureSeries', sim_id_num = 1)


# modify the xml file
#temp1_updated = set_data(element_str = 'ClimaticTemperatureSeries', element_tag_str = 'SeriesValue', 
#                         sim_id_num = 1, multiplicative_factor = 2)
precip1_updated = set_data(element_str = 'ClimaticPrecipitationSeries', element_tag_str = 'SeriesValue', 
                         sim_id_num = 1, multiplicative_factor = 5) 
# write out new xml file
tree.write('WATERSimulation_updated.xml') 
 
for feature in sim_features1:
    print feature['AttName']
