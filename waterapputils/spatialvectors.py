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

def get_intersected_field_values_multi(intersector, intersectee, intersectee_field):
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

def test_fill_shapefile_dict():
    """ Test fill_shapefile_dict() """

    print("--- fill_shapefile_dict() ---") 

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

#    import pdb
#    pdb.set_trace()
  
    # print results
    _print_test_info(actual, expected) 
        
def test_get_intersected_field_values():
    """ Test functionality of get_intersected_field_values """

    print("--- Testing get_intersected_field_values() ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = ["31", "32", "21", "11"]    
    expected["gfdl_tiles"] = ["41", "42", "31", "32", "21"]
    expected["giss_tiles"] = ["41", "42", "31", "21"]
    expected["ncar_tiles"] = ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"] 

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

def test_get_intersected_field_values_multi():
    """ Test functionality of get_intersected_field_values """

    print("--- Testing get_intersected_field_values() ---")  

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = ["31", "32", "21", "22"]    
    expected["gfdl_tiles"] = ["31", "32", "22"]
    expected["giss_tiles"] = ["42", "31", "32", "22"]
    expected["ncar_tiles"] = ["63", "53", "43"] 

    # paths to files
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../data/deltas-gcm/testbasin_multi_basins_proj_wgs/F12gt75run_wgs.shp"))
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

    test_fill_shapefile_dict()
    
#    test_get_intersected_field_values()

#    test_get_intersected_field_values_multi()
    
if __name__ == "__main__":
    main()    
    
    
    
    
    
    
    
    
    