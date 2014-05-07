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
    fixture["testbasin_single_fid"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))
    fixture["testbasin_multi_fid"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin_proj_wgs/testbasin_multi_proj_wgs.shp"))
    fixture["testbasin_orig_proj"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin/testbasin.shp"))
    fixture["waterbasin_single_fid"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin_proj_wgs/waterbasin_proj_wgs.shp"))
    fixture["waterbasin_multi_fid"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin_proj_wgs/waterbasin_multi_proj_wgs.shp"))
    fixture["canes_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))
    fixture["gfdl_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/GFDL_proj_wgs.shp"))
    fixture["giss_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/GISS_proj_wgs.shp"))
    fixture["ncar_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/NCAR_proj_wgs.shp"))
    fixture["canes_file_orig_proj"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/CanES/shapefile/CanES.shp"))
    fixture["gfdl_file_orig_proj"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/GFDL/shapefile/GFDL.shp"))
    fixture["giss_file_orig_proj"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/GISS/shapefile/GISS.shp"))
    fixture["ncar_file_orig_proj"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/NCAR/shapefile/NCAR.shp"))



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

    # expected values to test with actual values
    expected = {"extents": (-76.86408896229581, -73.5013706471868, 38.33140005688545, 43.986783289578774), 
                "name": "testbasin_proj_wgs.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict2():

    # expected values to test with actual values
    expected = {"extents": (-76.3557164298209, -75.83406785380727, 40.52224451815593, 40.89012237818175), 
                "name": "waterbasin_proj_wgs.shp", 
                "fields": ["OBJECTID", "Id", "Shape_Leng", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["waterbasin_single_fid"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict3():

    # expected values to test with actual values
    expected = {"extents": (-75.46839351213258, -74.35718960764397, 39.85602095657912, 42.36690057316007), 
                "name": "waterbasin_multi_proj_wgs.shp", 
                "fields": ["STAID", "da_sqmi", "ForestSum", "AgSum", "DevSum", "FORdivAG"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                "num_features": 12, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
    
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["waterbasin_multi_fid"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict4():

    # expected values to test with actual values
    expected = {"extents": (1551876.4646765331, 1813149.8783592982, 1873153.3560966868, 2513535.4955471633), 
                "name": "testbasin.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_orig_proj"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_get_intersected_field_values1():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(expected["canes_tiles"], actual["canes_tiles"])
    np.testing.assert_equal(expected["gfdl_tiles"], actual["gfdl_tiles"])    
    np.testing.assert_equal(expected["giss_tiles"], actual["giss_tiles"])   
    np.testing.assert_equal(expected["ncar_tiles"], actual["ncar_tiles"])

def test_get_intersected_field_values2(): 

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"], "1": ["21", "22"], "2": ["12"]}   
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"], "1": [ "22"], "2": ["22"]} 
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"], "1": [ "22"], "2": ["22"]} 
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"], "1": ["43", "44", "33", "34"], "2": ["24"]}  

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_multi_fid"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(expected["canes_tiles"], actual["canes_tiles"])
    np.testing.assert_equal(expected["gfdl_tiles"], actual["gfdl_tiles"])    
    np.testing.assert_equal(expected["giss_tiles"], actual["giss_tiles"])   
    np.testing.assert_equal(expected["ncar_tiles"], actual["ncar_tiles"])


def test_get_intersected_field_values3():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_orig_proj"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_orig_proj"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file_orig_proj"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file_orig_proj"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file_orig_proj"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(expected["canes_tiles"], actual["canes_tiles"])
    np.testing.assert_equal(expected["gfdl_tiles"], actual["gfdl_tiles"])    
    np.testing.assert_equal(expected["giss_tiles"], actual["giss_tiles"])   
    np.testing.assert_equal(expected["ncar_tiles"], actual["ncar_tiles"])
    
    
    
    
    