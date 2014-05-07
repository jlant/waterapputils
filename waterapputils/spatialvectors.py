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

def create_field_dict(key_list):
    """
    Create dictionary containing user defined keys.

    Parameters
    ----------
    keys_list : list
        List of strings that will be the keys in the dictionary.
    
    Returns
    -------
    field_dict : dictionary 
        Dictionary containing information found in a shapefile    
    """
    field_dict = {}
    for key in key_list:
        field_dict[key] = None

    return field_dict 


#def get_intersected_field_values(intersector, intersectee, intersectee_field):
#    """   
#    Get the field values associated with a shapefile that are intersected by 
#    another shapefile.
#    
#    Parameters
#    ----------
#    intersector : osgeo.ogr.DataSource object
#        A shapefile object.
#    intersectee : osgeo.ogr.DataSource object
#        A shapefile object.
#    intersectee_field: string
#        String name of a field in intersectee.
#
#    Returns
#    -------
#    field_values : list
#        List of values for a particular field that were intersected by another shapefile.b
#
#    Notes
#    -----
#    For example, used to find Global Climate Model (gcm) tile values intersected by a
#    particular basin. If basin shapefile intersects gcm shapefile, returns
#    the GCM tile values that are intersected.
#    """
#    intersectee_data = fill_shapefile_dict(shapefile = intersectee)
#    
#    assert intersectee_field in intersectee_data["fields"], "Field {} not in shapefile {}".format(intersectee_field, intersectee_data["name"])
#    
#    intersectee_layer = intersectee.GetLayer()
#    intersector_layer = intersector.GetLayer()
#    intersector_feature = intersector_layer.GetFeature(0)
#    intersector_geometry = intersector_feature.GetGeometryRef()
#    
#    field_values = []    
#    num_features = intersectee_layer.GetFeatureCount()
#    for feature_num in range(num_features):
#        intersectee_feature = intersectee_layer.GetFeature(feature_num)
#        intersectee_geometry = intersectee_feature.GetGeometryRef()
#        
#        if intersector_geometry.Intersect(intersectee_geometry):    
#            field_values.append(intersectee_feature.GetField(intersectee_field))
#
#    return field_values

def get_intersected_field_values(intersector, intersectee, intersectee_field, intersector_field = "FID"):
    """   
    Get the intersectee field values of interest associated with a shapefile 
    that is intersected by another shapefile.  The dictionary returned has key(s) 
    that correspond to the intersector field value of interest (FID by default) and 
    values corresponding to intersectee field values that are intersected.  
    
    Parameters
    ----------
    intersector : osgeo.ogr.DataSource object
        A shapefile object.
    intersectee : osgeo.ogr.DataSource object
        A shapefile object.
    intersector_field: string
        String name of a field in intersector whose values will be used as keys in the field values dictionary.
    intersectee_field: string
        String name of a field in intersectee whose values will be retrieved if itersection occurs.

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
    """
    # make sure that the supplied fields are contained in the shapefile datasets
    intersector_data = fill_shapefile_dict(shapefile = intersector)
    intersectee_data = fill_shapefile_dict(shapefile = intersectee)    

    assert intersectee_field in intersectee_data["fields"], "Field {} not in shapefile {}".format(intersectee_field, intersectee_data["name"])

    if intersector_field != "FID":
        assert intersector_field in intersector_data["fields"], "Field {} not in shapefile {}".format(intersector_field, intersector_data["name"])

    # get the shapefile layer    
    intersectee_layer = intersectee.GetLayer()
    intersector_layer = intersector.GetLayer()
    
    # loop through each intersector feature and find its respective intersections with each of the intersectee features
    field_values_dict = {}
    for num in range(intersector_layer.GetFeatureCount()):
        intersector_feature = intersector_layer.GetFeature(num)
        intersector_geometry = intersector_feature.GetGeometryRef()
            
        field_values = []    
        intersectee_num_features = intersectee_layer.GetFeatureCount()
        for feature_num in range(intersectee_num_features):
            intersectee_feature = intersectee_layer.GetFeature(feature_num)
            intersectee_geometry = intersectee_feature.GetGeometryRef()
            
            if intersector_geometry.Intersect(intersectee_geometry):    
                field_values.append(intersectee_feature.GetField(intersectee_field))

        if intersector_field == "FID":
            intersector_field_value = str(intersector_feature.GetFID())
        else:
            intersector_field_value = str(intersector_feature.GetField(intersector_field))
        
        field_values_dict[intersector_field_value] = field_values

    return field_values_dict

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

    print("--- create_shapefile_dict() ---") 

    # expected values to test with actual values
    expected = {"shapefile_datatype": None, "type": None, "path": None, "name": None, "num_features": None, "fields": [], "spatialref": None, "extents": ()}
    
    # actual values
    actual = create_shapefile_dict()
  
    # print results
    _print_test_info(actual, expected) 

def test_create_field_dict():
    """ Test create_field_dict() """

    print("--- create_field_dict() ---") 

    # expected values to test with actual values
    expected = {"key1": None, "key2": None, "key3": None}
    
    # actual values
    actual = create_field_dict(key_list = ["key1", "key2", "key3"])
  
    # print results
    _print_test_info(actual, expected) 

def test_fill_shapefile_dict1():
    """ Test fill_shapefile_dict() """

    print("--- fill_shapefile_dict() part 1 - sample shapefile ---") 

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

    print("--- fill_shapefile_dict() part 2 - sample WATER basin ---") 

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
        
def test_get_intersected_field_values1():
    """ Test functionality of get_intersected_field_values """

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
    """ Test functionality of get_intersected_field_values """

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
    
def main():
    """ Test functionality geospatialvectors.py """

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_create_shapefile_dict()

    test_create_field_dict()

    test_fill_shapefile_dict1()

    test_fill_shapefile_dict2()
    
    test_fill_shapefile_dict3()
    
    test_get_intersected_field_values1()

    test_get_intersected_field_values2()
    
if __name__ == "__main__":
    main()    
    
    
    
    
    
    
    
    
    