import nose.tools
from nose import with_setup 

import os, sys
import numpy as np
import osgeo.ogr

# my module
from waterapputils import spatialvectors

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: spatialvectors tests"
   
    # set up fixtures    
    fixture["basin_file_simple"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))
    fixture["basin_file_water_single"] = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/waterbasin_proj_wgs.shp"))
    fixture["basin_file_water_multi"] = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/waterbasin_proj_wgs.shp"))
    fixture["canes_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))
    fixture["gfdl_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/GFDL_proj_wgs.shp"))
    fixture["giss_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/GISS_proj_wgs.shp"))
    fixture["ncar_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/NCAR_proj_wgs.shp"))

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: spatialvectors tests" 


def test_create_shapefile_dict():
    """ Test create_shapefile_dict() """

    print("--- create_shapefile_dict() ---") 

    # expected values to test with actual values
    expected = {"shapefile_datatype": None, "type": None, "path": None, "name": None, "num_features": None, "fields": [], "spatialref": None, "extents": ()}
    
    # actual values
    actual = spatialvectors.create_shapefile_dict()
  
    np.testing.assert_equal(expected, actual)

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
#
#    import pdb
#    pdb.set_trace()
  
    # print results
    _print_test_info(actual, expected) 

def test_fill_shapefile_dict3():
    """ Test fill_shapefile_dict() """

    print("--- fill_shapefile_dict() part 3 - sample WATER basins as single shapefile ---") 

    # expected values to test with actual values
    expected = {"extents": (-75.46839351213258, -74.35718960764397, 39.85602095657912, 42.36690057316007), 
                "name": "F12gt75run_wgs.shp", 
                "fields": ["STAID", "da_sqmi", "ForestSum", "AgSum", "DevSum", "FORdivAG"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_multi_basins_proj_wgs", 
                "num_features": 12, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_multi_basins_proj_wgs/F12gt75run_wgs.shp"))
    
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)  
    
    # actual values
    actual = fill_shapefile_dict(shapefile = basin_shapefile)
  
    # print results
    _print_test_info(actual, expected) 

#def test_get_intersected_field_values():
#
#    expected = {"canes_tiles": ['31', '32', '21', '11'],
#                "gfdl_tiles": ['41', '42', '31', '32', '21'],
#                "giss_tiles": ['41', '42', '31', '21'],
#                "ncar_tiles": ['82', '83', '84', '72', '73', '74', '62', '63', '64', '52', '53', '42', '43', '32', '22']}
#
#    # Open the shapefiles
#    basin_shapefile = osgeo.ogr.Open(fixture["basin_file"])   
#    canes_shapefile = osgeo.ogr.Open(fixture["canes_file"])
#    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file"])
#    giss_shapefile = osgeo.ogr.Open(fixture["giss_file"])
#    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file"])
#   
#    actual = {}
#    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
#    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
#    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
#    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")
#
#    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
#        shapefile.Destroy()
#
#    nose.tools.assert_equals(expected["canes_tiles"], actual["canes_tiles"])
#    nose.tools.assert_equals(expected["gfdl_tiles"], actual["gfdl_tiles"])    
#    nose.tools.assert_equals(expected["giss_tiles"], actual["giss_tiles"])   
#    nose.tools.assert_equals(expected["ncar_tiles"], actual["ncar_tiles"])