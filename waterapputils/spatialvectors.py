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

def get_intersected_field_values(intersector, intersectee, intersectee_field):
    """   
    Get the field values associated with a shapefile that are intersected by 
    another shapefile.
    
    Parameters
    ----------
    intersector : osgeo.ogr.DataSource object
        A shapefile object.
    intersectee : osgeo.ogr.DataSource object
        A shapefile object.
    intersectee_field: string
        String name of a field in intersectee.

    Returns
    -------
    field_values : list
        List of values for a particular field that were intersected by another shapefile.b

    Notes
    -----
    For example, used to find Global Climate Model (gcm) tile values intersected by a
    particular basin. If basin shapefile intersects gcm shapefile, returns
    the GCM tile values that are intersected.
    """
#    intersectee_data = get_shapefile_data(shapefile = intersectee)
#    
#    assert intersectee_field in intersectee_data["fields"], "Field {} not in shapefile {}".format(intersectee_field, intersectee_data["name"])
    
    intersectee_layer = intersectee.GetLayer()
    intersector_layer = intersector.GetLayer()
    intersector_feature = intersector_layer.GetFeature(0)
    intersector_geometry = intersector_feature.GetGeometryRef()
    
    field_values = []    
    num_features = intersectee_layer.GetFeatureCount()
    for feature_num in range(num_features):
        intersectee_feature = intersectee_layer.GetFeature(feature_num)
        intersectee_geometry = intersectee_feature.GetGeometryRef()
        
        if intersector_geometry.Intersect(intersectee_geometry):    
            field_values.append(intersectee_feature.GetField(intersectee_field))

    return field_values


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
        
def test_get_intersected_field_values():
    """ Test functionality of get_intersected_field_values """

    print("--- Testing get_intersected_field_values() ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = ['31', '32', '21', '11']    
    expected["gfdl_tiles"] = ['41', '42', '31', '32', '21']
    expected["giss_tiles"] = ['41', '42', '31', '21']
    expected["ncar_tiles"] = ['82', '83', '84', '72', '73', '74', '62', '63', '64', '52', '53', '42', '43', '32', '22'] 

    # paths to files
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_proj_wgs/testbasin_proj_wgs.shp"))
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
    
#    for key in actual.keys():
#        assert expected[key] ==  actual[key], "For key {}, expected tiles {} do not equal actual tiles {}".format(key, expected[key], actual[key])
#        print("    expected: {}".format(expected[key]))
#        print("    actual:   {}\n".format(actual[key])) 

#    import pdb
#    pdb.set_trace()
        
    _print_test_info(expected, actual)
    
def main():
    """ Test functionality geospatialvectors.py """

    print("")
    print("RUNNING TESTS ...")
    print("")
    
    test_get_intersected_field_values()
    
if __name__ == "__main__":
    main()    
    
    
    
    
    
    
    
    
    