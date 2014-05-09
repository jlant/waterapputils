# -*- coding: utf-8 -*-
"""
:Module: spatialvectors.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles reading and processing shapefiles.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os, sys
import osgeo.ogr
import pdb
import numpy as np

# my modules
import helpers

def create_shapefile_dict():
    """
    Create dictionary containing keys that correspond to general information contained
    in a shapefile.
    
    Returns
    -------
    shapefile_dict : dictionary 
        Dictionary containing information found in a shapefile
    
    Notes
    -----           
    shapefile_dict = {"shapefile_datatype": None, "type": None, "path": None, "name": None, "num_features": None, "fields": [], "spatialref": None, "extents": ()}                 
    """
    
    shapefile_dict = {"shapefile_datatype": None, "type": None, "path": None, "name": None, "num_features": None, "fields": [], "spatialref": None, "extents": ()}

    return shapefile_dict 

def get_shapefile_coords(shapefile):
    """   
    Get the coordinates (longitudes and latitudes) of each feature in a shapefile. 
    Loops through each feature contained in a shapefile (e.g. each FID) and gets the features
    coordinates. Returns a dictionary containing keys that correspond to each feature, namely,
    the features FID number with corresponding longitude and latitude values.
    
    Parameters
    ----------
    shapefile : osgeo.ogr.DataSource 
        A shapefile object.        

    Returns
    -------
    coordinates : dictionary
        Dictionary containing
    """   
    shapefile_layer = shapefile.GetLayer()
    
    coords = {}
    for feature_num in range(shapefile_layer.GetFeatureCount()):
        shapefile_feature = shapefile_layer.GetFeature(feature_num)
        shapefile_geometry = shapefile_feature.GetGeometryRef()            
        points = shapefile_geometry.GetGeometryRef(0)           

        lons = []
        lats = []
        for i in xrange(points.GetPointCount()):
            lons.append(points.GetX(i))
            lats.append(points.GetY(i))
        
        # assign the features FID as the key in coords with corresponding lon and lat values
        fid = str(shapefile_feature.GetFID())
        coords[fid] = (lons, lats)
    
    return coords


def fill_shapefile_dict(shapefile):
    """   
    Get general shapefile information data source.
    
    Parameters
    ----------
    shapefile : osgeo.ogr.DataSource 
        A shapefile object.

    Returns
    -------
    shapefile_dict : dictionary 
        Dictionary containing general information about a shapefile

    Notes
    -----            
    shapefile_data = {"shapefile_datatype": osgeo.ogr.DataSource,
                      "type": string of geometry type (POLYGON, POINT, etc.),
                      "path": string path including name of shapefile,
                      "name": string name of shapefile
                      "fields": list containing fields contained in shapefile,
                      "spatialref": string of shapefile's spatial reference,
                      "extents": tuple of shapefile extents}
    
    """
    # create dictionary to hold shapefile data of interest
    shapefile_dict = create_shapefile_dict()    
    
    shapefile_layer = shapefile.GetLayer()
    shapefile_feature = shapefile_layer.GetFeature(0)
    shapefile_geometry = shapefile_feature.geometry()
    
    shapefile_fields = []
    shapefile_layerdef = shapefile_layer.GetLayerDefn()
    for i in range(shapefile_layerdef.GetFieldCount()):
        shapefile_fields.append(shapefile_layerdef.GetFieldDefn(i).GetName())        

    shapefile_dir, shapefile_filename = helpers.get_file_info(path = shapefile.GetName())
        
    shapefile_dict["shapefile_datatype"] = "{}".format(type(shapefile))
    shapefile_dict["type"] = shapefile_geometry.GetGeometryName()
    shapefile_dict["path"] = shapefile_dir
    shapefile_dict["name"] = shapefile_filename
    shapefile_dict["num_features"] = shapefile_layer.GetFeatureCount()
    shapefile_dict["fields"] = shapefile_fields
    shapefile_dict["spatialref"] = shapefile_layer.GetSpatialRef().ExportToProj4()
    shapefile_dict["extents"] = shapefile_layer.GetExtent()
                  
    return shapefile_dict


def get_intersected_field_values(intersector, intersectee, intersectee_field, intersector_field = "FID"):
    """   
    Get the intersectee field values of interest associated with a shapefile 
    that is intersected by another shapefile.  A dictionary is returned with key(s) 
    that correspond to the intersector field value of interest (FID by default) and 
    values corresponding to intersectee field values that are intersected. This function 
    returns all the intersected features, and distinguishes between multiple features (FID's)
    in the intersector.   
    
    Parameters
    ----------
    intersector : osgeo.ogr.DataSource object
        A shapefile object.
    intersectee : osgeo.ogr.DataSource object
        A shapefile object.
    intersectee_field: string
        String name of a field in intersectee whose values will be retrieved if itersection occurs.
    intersector_field: string
        String name of a field in intersector whose values will be used as keys in the field values dictionary.

    Returns
    -------
    field_values_dict : Dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.

    Notes
    -----
    For example, this function is used to find Global Climate Model (gcm) tile values intersected by a
    particular basin. If basin shapefile intersects a particular GCM shapefile, the GCM tile values
    that are intersected by the basin shapefile are returned.  So, the intersector would be the basin and 
    the intersectee would be the GCM shapefile.
    
    For example,
    field_values_dict = {"0": ["31", "32", "21", "11"], "1": ["21", "22"], "2": ["12"]}
    
    Where the keys are each FID number of the intersector with corrsponding values that are the field values
    from the intersectee that are intersected.
    """
    # make sure that the supplied fields are contained in the shapefile datasets
    intersector_data = fill_shapefile_dict(shapefile = intersector)
    intersectee_data = fill_shapefile_dict(shapefile = intersectee)    

    assert intersector_data["spatialref"] == intersectee_data["spatialref"], \
           "Spatial references are not equal\nShapefile: {}\n  Spatial reference: {}\nShapefile: {}\n  Spatial reference: {}".format(intersector_data["name"], intersector_data["spatialref"], intersectee_data["name"], intersectee_data["spatialref"])

    assert intersectee_field in intersectee_data["fields"], \
           "Field does not exist in shapefile.\nField: {}\nShapefile: {}\n  fields: {}".format(intersectee_field, intersectee_data["name"], intersectee_data["fields"])

    if intersector_field != "FID":
        assert intersector_field in intersector_data["fields"], \
               "Field does not exist in shapefile.\nField: {}\nShapefile: {}\n  fields: {}".format(intersector_field, intersector_data["name"], intersector_data["fields"])

    # get the shapefile layer    
    intersectee_layer = intersectee.GetLayer()
    intersector_layer = intersector.GetLayer()
    
    # loop through each intersector feature and find its respective intersections with each of the intersectee features
    field_values_dict = {}
    for i in range(intersector_layer.GetFeatureCount()):                      # loop through intersector
        intersector_feature = intersector_layer.GetFeature(i)
        intersector_geometry = intersector_feature.GetGeometryRef()
            
        field_values = []    
        for j in range(intersectee_layer.GetFeatureCount()):                  # loop through intersectee
            intersectee_feature = intersectee_layer.GetFeature(j)
            intersectee_geometry = intersectee_feature.GetGeometryRef()
            
            if intersector_geometry.Intersect(intersectee_geometry):    
                field_values.append(intersectee_feature.GetField(intersectee_field))

        if intersector_field == "FID":
            intersector_field_value = str(intersector_feature.GetFID())
        else:
            intersector_field_value = str(intersector_feature.GetField(intersector_field))
        
        field_values_dict[intersector_field_value] = field_values

    return field_values_dict


def _print_test_info(expected, actual):
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

def test_create_shapefile_dict():
    """ Test create_shapefile_dict() """

    print("--- Testing create_shapefile_dict() ---") 

    # expected values to test with actual values
    expected = {"shapefile_datatype": None, "type": None, "path": None, "name": None, "num_features": None, "fields": [], "spatialref": None, "extents": ()}
    
    # actual values
    actual = create_shapefile_dict()
  
    # print results
    _print_test_info(actual, expected) 

def test_get_shapefile_coords():
    """ Test get_shapefile_coords() """
    
    print("--- Testing get_shapefile_coords() ---") 

    # expected values to test with actual values
    expected = {}
    expected["testbasin_wgs84"] = {"0": ([-76.5241897068253, -75.23041385228197, -73.58652704198151, -73.5013706471868, -75.02093324688161, -75.08254377360929, -76.46844548090678, -76.86408896229581, -76.76898146953256, -76.86020288529657, -76.5241897068253], 
                                    [43.72112550966717, 43.986783289578774, 43.58481904994738, 42.78125135043379, 42.064154034262806, 40.419906887537, 38.33140005688545, 40.22529559781875, 40.95275941413145, 41.661899956299614, 43.72112550966717])}

    expected["testbasin_nad83"] = {"0": ([1551876.4646765331, 1646948.1658269956, 1785445.705257233, 1813149.8783592982, 1710314.4423011306, 1745561.219742352, 1679365.164213511, 1603362.2856433871, 1594846.0132731413, 1571503.7313467045, 1551876.4646765331], 
                                          [2462788.591455278, 2513535.4955471633, 2499530.126391299, 2413895.970528247, 2307638.3618463, 2126904.9022905156, 1873153.3560966868, 2074193.2284434838, 2155620.5060083373, 2231871.9603013936, 2462788.591455278])}

    expected["canes_wgs84"] = {"0": ([-77.34375265636656, -74.53125172872296, -74.53125153884916, -77.34375244277751, -77.34375265636656], [44.649508846266905, 44.64950895861966, 41.85894444448356, 41.85894433988654, 44.649508846266905]), 
                         "1": ([-74.53125172872296, -71.71875078911197, -71.71875062341081, -74.53125153884916, -74.53125172872296], [44.64950895861966, 44.64950905729846, 41.85894453702035, 41.85894444448356, 44.64950895861966]),                          
                         "2": ([-77.34375244277751, -74.53125153884916, -74.53125137708862, -77.34375226209623, -77.34375244277751], [41.85894433988654, 41.85894444448356, 39.068379891689446, 39.068379795204585, 41.85894433988654]), 
                         "3": ([-74.53125153884916, -71.71875062341081, -71.71875048096074, -74.53125137708862, -74.53125153884916], [41.85894444448356, 41.85894453702035, 39.0683799778016, 39.068379891689446, 41.85894444448356]), 
                         "4": ([-77.34375226209623, -74.53125137708862, -74.53125123940792, -77.34375210963982, -77.34375226209623], [39.068379795204585, 39.068379891689446, 36.277815301487045, 36.27781521345216, 39.068379795204585]),
                         "5": ([-74.53125137708862, -71.71875048096074, -71.71875035838741, -74.53125123940792, -74.53125137708862], [39.068379891689446, 39.0683799778016, 36.27781538090664, 36.277815301487045, 39.068379891689446])
    }
            
                
    basin_file_wgs84 = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))
    basin_file_nad83 = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin/testbasin.shp"))
    canes_file_wgs84 = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))

    # Open the shapefiles
    basin_shapefile_wgs84 = osgeo.ogr.Open(basin_file_wgs84) 
    basin_shapefile_nad83 = osgeo.ogr.Open(basin_file_nad83) 
    canes_shapefile_wgs84 = osgeo.ogr.Open(canes_file_wgs84)
    
    # actual values
    actual = {}
    actual["testbasin_wgs84"] = get_shapefile_coords(shapefile = basin_shapefile_wgs84)
    actual["testbasin_nad83"] = get_shapefile_coords(shapefile = basin_shapefile_nad83)
    actual["canes_wgs84"] = get_shapefile_coords(shapefile = canes_shapefile_wgs84)

    # print results
    _print_test_info(actual, expected)   

def test_fill_shapefile_dict1():
    """ Test fill_shapefile_dict() """

    print("--- Testing fill_shapefile_dict() part 1 - sample shapefile ---") 

    # expected values to test with actual values
    expected = {"extents": (-76.86408896229581, -73.5013706471868, 38.33140005688545, 43.986783289578774), 
                "name": "testbasin_proj_wgs.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)  
    
    # actual values
    actual = fill_shapefile_dict(shapefile = basin_shapefile)
  
    # print results
    _print_test_info(actual, expected) 

def test_fill_shapefile_dict2():
    """ Test fill_shapefile_dict() """

    print("--- Testing fill_shapefile_dict() part 2 - sample WATER basin ---") 

    # expected values to test with actual values
    expected = {"extents": (-76.3557164298209, -75.83406785380727, 40.52224451815593, 40.89012237818175), 
                "name": "waterbasin_proj_wgs.shp", 
                "fields": ["OBJECTID", "Id", "Shape_Leng", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/waterbasin_proj_wgs.shp"))

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)  
   
    # actual values
    actual = fill_shapefile_dict(shapefile = basin_shapefile)
  
    # print results
    _print_test_info(actual, expected) 

def test_fill_shapefile_dict3():
    """ Test fill_shapefile_dict() """

    print("--- fill_shapefile_dict() part 3 - sample WATER basins as single shapefile ---") 

    # expected values to test with actual values
    expected = {"extents": (-75.46839351213258, -74.35718960764397, 39.85602095657912, 42.36690057316007), 
                "name": "waterbasin_multi_proj_wgs.shp", 
                "fields": ["STAID", "da_sqmi", "ForestSum", "AgSum", "DevSum", "FORdivAG"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                "num_features": 12, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/waterbasin_multi_proj_wgs.shp"))
    
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)  
    
    # actual values
    actual = fill_shapefile_dict(shapefile = basin_shapefile)
  
    # print results
    _print_test_info(actual, expected) 

def test_fill_shapefile_dict4():
    """ Test fill_shapefile_dict() """

    print("--- fill_shapefile_dict() part 4 - sample test basin as single shapefile ---") 

    # expected values to test with actual values
    expected = {"extents": (1551876.4646765331, 1813149.8783592982, 1873153.3560966868, 2513535.4955471633), 
                "name": "testbasin.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs "}
                
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin/testbasin.shp"))   
    
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)  
    
    # actual values
    actual = fill_shapefile_dict(shapefile = basin_shapefile)
  
    # print results
    _print_test_info(actual, expected) 
       
def test_get_intersected_field_values1():
    """ Test get_intersected_field_values() """

    print("--- Testing get_intersected_field_values() part 1 - sample shapefile with single feature ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # paths to files
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))
    canes_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))
    gfdl_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/GFDL_proj_wgs.shp"))
    giss_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/GISS_proj_wgs.shp"))
    ncar_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/NCAR_proj_wgs.shp"))

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    
    canes_shapefile = osgeo.ogr.Open(canes_file)
    gfdl_shapefile = osgeo.ogr.Open(gfdl_file)
    giss_shapefile = osgeo.ogr.Open(giss_file)
    ncar_shapefile = osgeo.ogr.Open(ncar_file)

    # actual values    
    actual = {}
    actual["canes_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)

def test_get_intersected_field_values2():
    """ Test get_intersected_field_values() """

    print("--- Testing get_intersected_field_values() part 2 - sample shapefile with multiple features ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"], "1": ["21", "22"], "2": ["12"]}   
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"], "1": [ "22"], "2": ["22"]} 
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"], "1": [ "22"], "2": ["22"]} 
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"], "1": ["43", "44", "33", "34"], "2": ["24"]}  

    # paths to files
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/testbasin_multi_proj_wgs.shp"))
    canes_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))
    gfdl_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/GFDL_proj_wgs.shp"))
    giss_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/GISS_proj_wgs.shp"))
    ncar_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/NCAR_proj_wgs.shp"))

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    
    canes_shapefile = osgeo.ogr.Open(canes_file)
    gfdl_shapefile = osgeo.ogr.Open(gfdl_file)
    giss_shapefile = osgeo.ogr.Open(giss_file)
    ncar_shapefile = osgeo.ogr.Open(ncar_file)

    # actual values    
    actual = {}
    actual["canes_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)

def test_get_intersected_field_values3():
    """ Test get_intersected_field_values() """

    print("--- Testing get_intersected_field_values() part 3 - sample shapefile with single feature in original projection ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # paths to files
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin/testbasin.shp"))
    canes_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/CanES/shapefile/CanES.shp"))
    gfdl_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/GFDL/shapefile/GFDL.shp"))
    giss_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/GISS/shapefile/GISS.shp"))
    ncar_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/NCAR/shapefile/NCAR.shp"))

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    
    canes_shapefile = osgeo.ogr.Open(canes_file)
    gfdl_shapefile = osgeo.ogr.Open(gfdl_file)
    giss_shapefile = osgeo.ogr.Open(giss_file)
    ncar_shapefile = osgeo.ogr.Open(ncar_file)

    # actual values    
    actual = {}
    actual["canes_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)
 
def test_get_intersected_field_values4():
    """ Test get_intersected_field_values() """

    print("--- Testing get_intersected_field_values() part 4 - sample shapefile with multiple features without default key identifier ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"01466500": ["22"], "01440000": ["21"], "01415000": ["31"], "01439500": ["21"], "01440400": ["21"], "01442500": ["21"], "01413500": ["31", "32"], "01420500": ["31", "32", "21"], "01435000": ["31", "32"], "01422500": ["31"], "01414500": ["31"], "01422389": ["31"]}   
    expected["gfdl_tiles"] = {"01466500": ["22"], "01440000": ["32"], "01415000": ["32"], "01439500": ["31"], "01440400": ["31"], "01442500": ["31"], "01413500": ["32"], "01420500": ["32"], "01435000": ["32"], "01422500": ["32"], "01414500": ["32"], "01422389": ["32"]} 
    expected["giss_tiles"] = {"01466500": ["22"], "01440000": ["32"], "01415000": ["42"], "01439500": ["31"], "01440400": ["31"], "01442500": ["31"], "01413500": ["42"], "01420500": ["42", "32"], "01435000": ["42", "32"], "01422500": ["42"], "01414500": ["42"], "01422389": ["42"]}
    expected["ncar_tiles"] = {"01466500": ["43"], "01440000": ["53"], "01415000": ["63"], "01439500": ["53"], "01440400": ["53"], "01442500": ["53"], "01413500": ["63"], "01420500": ["63"], "01435000": ["63", "64"], "01422500": ["63"], "01414500": ["63"], "01422389": ["63"]}

    # paths to files
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/waterbasin_multi_proj_wgs.shp"))
    canes_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))
    gfdl_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/GFDL_proj_wgs.shp"))
    giss_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/GISS_proj_wgs.shp"))
    ncar_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/gcm_proj_wgs/NCAR_proj_wgs.shp"))

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    
    canes_shapefile = osgeo.ogr.Open(canes_file)
    gfdl_shapefile = osgeo.ogr.Open(gfdl_file)
    giss_shapefile = osgeo.ogr.Open(giss_file)
    ncar_shapefile = osgeo.ogr.Open(ncar_file)

    # actual values    
    actual = {}
    actual["canes_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile", intersector_field = "STAID")    
    actual["gfdl_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile", intersector_field = "STAID")
    actual["giss_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile", intersector_field = "STAID")
    actual["ncar_tiles"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile", intersector_field = "STAID")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)  
   
def main():
    """ Test functionality geospatialvectors.py """

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_create_shapefile_dict()

    test_fill_shapefile_dict1()

    test_fill_shapefile_dict2()
    
    test_fill_shapefile_dict3()

    test_fill_shapefile_dict4()

    test_get_shapefile_coords()
    
    test_get_intersected_field_values1()

    test_get_intersected_field_values2()

    test_get_intersected_field_values3()

    test_get_intersected_field_values4()
    
if __name__ == "__main__":
    main()    
    
    
    
    
    
    
    
    
    