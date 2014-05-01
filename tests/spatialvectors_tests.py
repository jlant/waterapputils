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
    fixture["basin_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))
    fixture["canes_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/CanES_proj_wgs.shp"))
    fixture["gfdl_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/GFDL_proj_wgs.shp"))
    fixture["giss_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/GISS_proj_wgs.shp"))
    fixture["ncar_file"] = os.path.abspath(os.path.join(os.getcwd(), "./data/deltas-gcm/gcm_proj_wgs/NCAR_proj_wgs.shp"))

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: spatialvectors tests" 


def test_get_intersected_field_values():

    expected = {"canes_tiles": ['31', '32', '21', '11'],
                "gfdl_tiles": ['41', '42', '31', '32', '21'],
                "giss_tiles": ['41', '42', '31', '21'],
                "ncar_tiles": ['82', '83', '84', '72', '73', '74', '62', '63', '64', '52', '53', '42', '43', '32', '22']}

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["basin_file"])   
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file"])
   
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()

    nose.tools.assert_equals(expected["canes_tiles"], actual["canes_tiles"])
    nose.tools.assert_equals(expected["gfdl_tiles"], actual["gfdl_tiles"])    
    nose.tools.assert_equals(expected["giss_tiles"], actual["giss_tiles"])   
    nose.tools.assert_equals(expected["ncar_tiles"], actual["ncar_tiles"])