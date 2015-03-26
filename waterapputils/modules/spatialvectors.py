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

import os
import osgeo.ogr
import osgeo.osr
from StringIO import StringIO
import re
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


def get_intersected_field_values(intersector, intersectee, intersectee_field, intersector_field):
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

    if intersector_field:
        assert intersector_field in intersector_data["fields"], \
               "Field does not exist in shapefile.\nField: {}\nShapefile: {}\n  fields: {}".format(intersector_field, intersector_data["name"], intersector_data["fields"])
    else:
        intersector_field = "FID"

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
                field_value = str(intersectee_feature.GetField(intersectee_field))
                field_values.append(field_value)

        if intersector_field == "FID":
            intersector_field_value = str(intersector_feature.GetFID())
        else:
            intersector_field_value = str(intersector_feature.GetField(intersector_field))

        # check that intersections were found; if not, then assign None for field values
        if field_values:       
            field_values_dict[intersector_field_value] = field_values
        else:
            field_values_dict[intersector_field_value] = None

    return field_values_dict

def validate_field_values(field_values_dict):
    """   
    Validate field values from field values dictionary supplied by returning a
    dictionary containing field values without None and a dictionary containing field 
    values that have None.
    
    Parameters
    ----------
    field_values_dict : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.

    Returns
    -------
    field_values_dict_without_none : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.
        
    field_values_dict_with_none : dictionary
        Dictionary containing lists of values for a particular field that were not intersected by another shapefile.
    """
    field_values_dict_with_none = {}
    field_values_dict_without_none = {}
    for key, value in field_values_dict.iteritems():
        if value is None:
            field_values_dict_with_none[key] = value
        else:
            field_values_dict_without_none[key] = value
            
    return field_values_dict_without_none, field_values_dict_with_none

def read_field_values_file(filepath):
    """
    Read a file containing rows of basin ids that are not intersected by any water use basin centroids

    Parameters
    ----------    
    filepath : string
        String path to file

    """    
    with open(filepath, "r") as f:
        field_values_dict = read_field_values_file_in(f)
            
    return field_values_dict

def read_field_values_file_in(filestream):
    """
    Read a file containing rows of basin ids that are not intersected by any water use basin centroids

    Parameters
    ----------    
    filepath : string
        String path to file

    """    
    header = "basinid"

    datafile = filestream.readlines() 

    field_values_dict = {}
    for line in datafile:
        line = line.strip()                        
        if line and header.strip() not in line:
            line = line.strip()
            line_list = line.split(",")
            items = [item.strip() for item in line_list[1:]]
            field_values_dict[line_list[0]] = items

    return field_values_dict
        

def write_field_values_file(filepath, filename, field_values_dict, special_id = "000", field_id = "newhydroid"):
    """
    Write a file containing rows of basin ids that are not intersected by any water use basin centroids

    Parameters
    ----------
    filepath : string
        String path to directory where file will be saved
    filename : string
        String name of file to be saved
    field_values_dict : dictionary
        Dictionary containing lists of values for a particular field that were intersected by another shapefile.
    """
    fullpath = os.path.join(filepath, filename)
    with open(fullpath, "w") as f:
        line_str = "basinid,{}\n".format(field_id)
        f.write(line_str)        
        for key in field_values_dict.keys():
            f.write("{},{}\n".format(key, special_id))

def get_field_values(shapefile, id_field, query_field):
    """
    Get specific field values for a shapefile.

    Parameters
    ----------
    shapefile : osgeo.ogr.DataSource object
        A shapefile object.
    id_field: string
        String name of a field in shapefile whose values will be used as keys in the field values dictionary.
    query_field: string
        String name of a field in shapefile 

    Returns
    -------
    field_values_dict : Dictionary
        Dictionary containing values for a particular field in a shapefile
    """

    # make sure that the supplied fields are contained in the shapefile datasets
    shapefile_data = fill_shapefile_dict(shapefile = shapefile)

    if id_field:
        assert id_field in shapefile_data["fields"], \
        "ID Field does not exist in shapefile.\nField: {}\nShapefile: {}\n  fields: {}".format(id_field, shapefile_data["name"], shapefile_data["fields"])
    else:
        id_field = "FID"

    assert query_field in shapefile_data["fields"], \
        "Field does not exist in shapefile.\nField: {}\nShapefile: {}\n  fields: {}".format(query_field, shapefile_data["name"], shapefile_data["fields"])

    shapefile_layer = shapefile.GetLayer()

    field_values_dict = {}
    for i in range(shapefile_layer.GetFeatureCount()):
        shapefile_feature = shapefile_layer.GetFeature(i)

        if id_field == "FID":
            id_field_value = str(shapefile_feature.GetFID())
        else:
            id_field_value = str(shapefile_feature.GetField(id_field))

        query_field_value = str(shapefile_feature.GetField(query_field))

        if id_field_value and query_field_value:       
            field_values_dict[id_field_value] = query_field_value
        else:
            print("Problem with id field value {} and query field value {} ".format(id_field_value, query_field_value))

    return field_values_dict

def get_shapefile_areas(shapefile, id_field = ""):
    """   
    Get the areas of each feature in a shapefile. 
    Loops through each feature contained in a shapefile (e.g. each FID) and gets the area. 
    Returns a dictionary containing keys that correspond to each feature, namely,
    the features FID number with corresponding area values.
    
    Parameters
    ----------
    shapefile : osgeo.ogr.DataSource 
        A shapefile object.        
    id_field : string
        A string id id_field to use as keys in return dictionary

    Returns
    -------
    areas : dictionary
        Dictionary containing feature id and areas

    Notes
    ----- 
    Area units are in the linear units of the projected coordinate system
    """   
    
    # get shapefile data
    shapefile_data = fill_shapefile_dict(shapefile)

    # make sure the id field is in the list of fields, if not, then set to "FID"
    if id_field:
        assert id_field in shapefile_data["fields"], \
               "Field does not exist in shapefile.\nField: {}\nShapefile: {}\n  fields: {}".format(intersector_field, intersector_data["name"], intersector_data["fields"])
    else:
        id_field = "FID"

    shapefile_layer = shapefile.GetLayer()
    
    areas = {}
    for feature_num in range(shapefile_layer.GetFeatureCount()):
        shapefile_feature = shapefile_layer.GetFeature(feature_num)
        shapefile_geometry = shapefile_feature.GetGeometryRef()            
        area = shapefile_geometry.GetArea()           

        # assign the features FID as the key in coords with corresponding lon and lat values
        if id_field == "FID":
            id_field_value = str(shapefile_feature.GetFID())
        else:
            id_field_value = str(shapefile_feature.GetField(id_field))

        areas[id_field_value] = area
    
    return areas

def get_areas_dict(shapefile, id_field, query_field):
    """
    Wrapper for get_shapefile_areas().  If there is no query_field (e.g. area_field),
    then calculate the area.  All WATER application shapefiles are in the Albers NAD83 projection,
    so areas are in units of meters squared by default.  Convert from units of meters squared
    to units of miles squared. 

    Parameters
    ----------
    shapefile : osgeo.ogr.DataSource 
        A shapefile object.        
    id_field : string
        A string id id_field to use as keys in return dictionary
    query_field : string
        A string field that exists in shapefile

    Returns
    -------
    areas : dictionary
        Dictionary containing feature id and areas

    Notes
    ----- 
    Area units are in the linear units of the projected coordinate system. 
    All WATER application shapefiles are in the Albers NAD83 projection. 
    """
    # get the areas for each region
    if query_field:
        areas = get_field_values(shapefile = shapefile, id_field = id_field, query_field = query_field)   
    else:
        if id_field:
            areas = get_shapefile_areas(shapefile, id_field = id_field)

            # convert from m**2 to mi**2; water application uses NAD83 projection with units of meters
            areas = helpers.convert_area_values(areas, in_units = "m2", out_units = "mi2")
        else:
            areas = get_shapefile_areas(shapefile)

            # convert from m**2 to mi**2; water application uses NAD83 projection with units of meters
            areas = helpers.convert_area_values(areas, in_units = "m2", out_units = "mi2")  

    return areas


def reproject_shapefile_to_wgs84(shapefile, out_shapefile_suffix = "_reproj_wgs84.shp"):
    """
    Reproject shapefile to WGS 84.  All WATER application shapefiles are in the Albers NAD83 projection.
    Create a new shapefile with the new projection.

    Parameters
    ----------
    shapefile : osgeo.ogr.DataSource 
        A shapefile object.    
    out_shapefile_suffix : string
        String name to join to end of shapefile

    Returns
    -------
    out_shapefile : string
        String path to reprojected shapefile

    Notes
    -----
    Good reference: http://spatialreference.org/
    """
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')

    # get some standard information about the shapefile
    shp_file_dict = fill_shapefile_dict(shapefile)

    # get spatial reference from layer
    in_layer = shapefile.GetLayer()
    in_spatial_ref = in_layer.GetSpatialRef()

    # make sure projection is NAD_1983_Albers
    projection_str = in_spatial_ref.GetAttrValue("PROJCS")

    assert projection_str == "NAD_1983_Albers", "Projection Error!\n\nShapefile must be NAD_1983_Albers like all other WATER shapefiles to project.\n\nShapefile projection:\n    {}\ndoes not equal\n    NAD_1983_Albers.".format(projection_str)

    # create output spatial reference - WGS 84
    out_spatial_ref = osgeo.osr.SpatialReference()
    out_spatial_ref.ImportFromEPSG(4326)                # EPSG 4326 = WGS 84

    # create the CoordinateTransformation
    coord_trans = osgeo.osr.CoordinateTransformation(in_spatial_ref, out_spatial_ref)

    # create the output layer
    out_shapefile_name = shp_file_dict["name"].split(".shp")[0] + out_shapefile_suffix
    out_shapefile = os.path.join(shp_file_dict["path"], out_shapefile_name)

    if os.path.exists(out_shapefile):
        driver.DeleteDataSource(out_shapefile)

    if shp_file_dict["type"] == "POLYGON":
        geom_type = osgeo.ogr.wkbMultiPolygon
    elif shp_file_dict["type"] == "POINT":
        geom_type = osgeo.ogr.wkbPoint
    else:
        geom_type = osgeo.ogr.wkbMultiLineString

    out_dataset = driver.CreateDataSource(out_shapefile)
    out_layer = out_dataset.CreateLayer(out_shapefile_name.split(".shp")[0], geom_type = geom_type)

    # add fields from input shp to output shp
    in_layer_def = in_layer.GetLayerDefn()
    for i in range(0, in_layer_def.GetFieldCount()):
        field_def = in_layer_def.GetFieldDefn(i)
        out_layer.CreateField(field_def)

    # get the output layer's feature definition
    out_layer_def = out_layer.GetLayerDefn()

    # add geometry to output shp
    in_feature = in_layer.GetNextFeature()
    while in_feature:
        geom = in_feature.GetGeometryRef()          # input shp geometry
        geom.Transform(coord_trans)                 # reproject geometry

        out_feature = osgeo.ogr.Feature(out_layer_def)    # create a new feature
        out_feature.SetGeometry(geom)               # set the geometry and attribute
        for i in range(0, out_layer_def.GetFieldCount()):
            out_feature.SetField(out_layer_def.GetFieldDefn(i).GetNameRef(), in_feature.GetField(i))

        out_layer.CreateFeature(out_feature)        # add the feature to the shapefile

        # destroy features and get the next input feature
        out_feature.Destroy()
        in_feature.Destroy()
        in_feature = in_layer.GetNextFeature()

    # close the shapefiles
    shapefile.Destroy()
    out_dataset.Destroy()

    # create the ESRI.prj file
    prj_filename = out_shapefile.split(".shp")[0] + ".prj"
    out_spatial_ref.MorphToESRI()
    prj_file = open(prj_filename, 'w')
    prj_file.write(out_spatial_ref.ExportToWkt())
    prj_file.close()


    return out_shapefile


def reproject(shapefiles):
    """
    Reproject a list of shapefiles to Geographic (WGS84) coordinates. 
    If any shapefile in the list is already in Geographic coordinates,
    then its path is added to the list returned.

    Parameters
    ----------
    shapefiles : list
        List of filled shapefile dictionaries

    Returns
    -------
    shp_reproj_list : list
        List of paths to reprojected shapefiles

    See Also
    --------
    fill_shapefile_dict()

    """
    shp_reproj_list = []
    for shapefile in shapefiles:
        shp = osgeo.ogr.Open(shapefile) 

        layer = shp.GetLayer()
        spatial_ref = layer.GetSpatialRef()
        if spatial_ref.IsProjected():   
            shp_path = reproject_shapefile_to_wgs84(shapefile = shp)
        
        else:
            shp_path = shapefile

        shp_reproj_list.append(shp_path)

    return shp_reproj_list

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


def test_fill_shapefile_dict():

    # expected values to test with actual values
    expected = {"extents": (-76.86408896229705, -73.50137064718774, 38.33140005688863, 43.98678328958175), 
                "name": "test_poly_wgs84.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
    
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/test_poly_wgs84.shp"))
            
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)  
    
    # actual values
    actual = fill_shapefile_dict(shapefile = basin_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 

    # print test results        
    _print_test_info(expected, actual)
    
def test_get_shapefile_coords():

    # expected values to test with actual values
    expected = {}
    expected["test_poly_wgs84"] = {"0": ([-76.52418970682646, -75.23041385228304, -73.58652704198245, -73.50137064718774, -75.02093324688268, -75.08254377361038, -76.468445480908, -76.86408896229705, -76.76898146953378, -76.8602028852978, -76.52418970682646], 
                                        [43.72112550967012, 43.98678328958175, 43.58481904995042, 42.78125135043684, 42.06415403426586, 40.41990688754016, 38.33140005688863, 40.225295597821855, 40.95275941413454, 41.66189995630268, 43.72112550967012])}

    expected["test_poly_nad83"] = {"0": ([1551876.4646765331, 1646948.1658269956, 1785445.705257233, 1813149.8783592982, 1710314.4423011306, 1745561.219742352, 1679365.164213511, 1603362.2856433871, 1594846.0132731413, 1571503.7313467045, 1551876.4646765331], 
                                        [2462788.591455278, 2513535.4955471633, 2499530.126391299, 2413895.970528247, 2307638.3618463, 2126904.9022905156, 1873153.3560966868, 2074193.2284434838, 2155620.5060083373, 2231871.9603013936, 2462788.591455278])}

    expected["canes_wgs84"] ={  '0': ([-77.34375265636656, -74.53125172872296, -74.53125153884916, -77.34375244277751, -77.34375265636656], [44.649508846266905, 44.64950895861966, 41.85894444448356, 41.85894433988654, 44.649508846266905]), 
                                '1': ([-74.53125172872296, -71.71875078911197, -71.71875062341081, -74.53125153884916, -74.53125172872296], [44.64950895861966, 44.64950905729846, 41.85894453702035, 41.85894444448356, 44.64950895861966]),
                                '2': ([-77.34375244277751, -74.53125153884916, -74.53125137708862, -77.34375226209623, -77.34375244277751], [41.85894433988654, 41.85894444448356, 39.068379891689446, 39.068379795204585, 41.85894433988654]), 
                                '3': ([-74.53125153884916, -71.71875062341081, -71.71875048096074, -74.53125137708862, -74.53125153884916], [41.85894444448356, 41.85894453702035, 39.0683799778016, 39.068379891689446, 41.85894444448356]), 
                                '4': ([-77.34375226209623, -74.53125137708862, -74.53125123940792, -77.34375210963982, -77.34375226209623], [39.068379795204585, 39.068379891689446, 36.277815301487045, 36.27781521345216, 39.068379795204585]),
                                '5': ([-74.53125137708862, -71.71875048096074, -71.71875035838741, -74.53125123940792, -74.53125137708862], [39.068379891689446, 39.0683799778016, 36.27781538090664, 36.277815301487045, 39.068379891689446])}

    basin_file_wgs84 = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/test_poly_wgs84.shp"))
    basin_file_nad83 = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/test_poly_nad83.shp"))
    canes_file_wgs84 = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/gcm-tiles/canes_wgs84.shp"))
        
    # Open the shapefiles
    basin_shapefile_wgs84 = osgeo.ogr.Open(basin_file_wgs84) 
    basin_shapefile_nad83 = osgeo.ogr.Open(basin_file_nad83) 
    canes_shapefile_wgs84 = osgeo.ogr.Open(canes_file_wgs84)
    
    # actual values
    actual = {}
    actual["test_poly_wgs84"] = get_shapefile_coords(shapefile = basin_shapefile_wgs84)
    actual["test_poly_nad83"] = get_shapefile_coords(shapefile = basin_shapefile_nad83)
    actual["canes_wgs84"] = get_shapefile_coords(shapefile = canes_shapefile_wgs84)

    # print test results        
    _print_test_info(expected, actual)


def test_get_shapefile_areas():
    """ Test get_shapefile_areas() """

    print("--- Testing get_shapefile_areas() - projected coordinate system is Albers_Equal_Area_Conic_USGS_CONUS_NAD83 with units of meters ")  

    expected = {}
    expected = {'01413500': 422764983.7640325, '01420500': 627820731.9907457, '01414500': 65034817.5157996, '01435000': 172655175.67497352}

    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/water_basins_nad83.shp"))

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    

    actual = get_shapefile_areas(shapefile = basin_shapefile, field = "STAID")

    basin_shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)
    

def test_get_intersected_field_values():
    """ Test get_intersected_field_values() """

    print("--- Testing get_intersected_field_values() part 1 - sample shapefile with single feature ---")  

    expected = {}
    expected["newhydroid"] = {'01413500': ['149', '61', '22'], '01420500': ['440', '390', '257'], '01414500': None, '01435000': ['262', '220']}  

    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/water_basins_wgs84.shp"))
    point_file = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_wgs84.shp"))

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    
    point_shapefile = osgeo.ogr.Open(point_file)

    # actual values    
    actual = {}
    actual["newhydroid"] = get_intersected_field_values(intersector = basin_shapefile, intersectee = point_shapefile, intersectee_field = "newhydroid", intersector_field = "STAID")

    for shapefile in [basin_shapefile, point_shapefile]:
        shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)
    
    
def test_validate_field_values():
    """ Test validate_field_values() """

    print("--- Testing validate_field_values() - remove field value dictionary if value is None because that means missing intersections ---")  

    # expected values to test with actual values
    expected = {} 
    expected["intersected"] = {"0": ["12", "11", "8"]}
    expected["non_intersected"] = {"1": None}

    # sample field values dictionary
    field_values_dict = {"0": ["12", "11", "8"], "1": None} 
    
    # actual values    
    actual = {}
    actual["intersected"], actual["non_intersected"] = validate_field_values(field_values_dict)

    # print test results        
    _print_test_info(expected, actual)

def test_read_field_values_file_in():
    """ Test read_field_values_file() """

    print("--- Testing read_field_values_file() - read standard file - csv format ---")  

    fixture = {}
    fixture["data_file"] = \
    """
    basinid, centroids
    0123456, 45, 50, 55, 60 
    7890123, 65, 70, 75, 80 
    drb123,000

    """
    
    file_obj = StringIO(fixture["data_file"])

    # expected values to test with actual values
    expected = {} 
    expected["data"] = {"0123456": ["45", "50", "55", "60"], "7890123": ["65", "70", "75", "80"], "drb123": ["000"]}
    
    # actual values    
    actual = {}
    actual["data"] = read_field_values_file_in(file_obj)

    # print test results        
    _print_test_info(expected, actual)

def test_get_field_values():
    """ Test read_field_values_file() """

    print("--- Testing read_field_values_file() - read standard file - csv format ---")  

    expected = {}
    expected = {'01413500': '163.229819866', '01420500': '242.401970189', '01414500': '25.109982983', '01435000': '66.6622693618'}

    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/water_basins_wgs84.shp"))

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(basin_file)    

    actual = get_field_values(shapefile = basin_shapefile, id_field = "STAID", query_field = "da_sqmi")

    basin_shapefile.Destroy()  

    # print test results        
    _print_test_info(expected, actual)


def test_reproject_shapefile_to_wgs84():
    """ Test reproject_shapefile_to_wgs84() """

    print("--- Testing reproject_shapefile_to_wgs84() ---")  
    print("")
    expected = {}
    expected["full_path"] = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/water_basin_nad83_reproj_wgs84.shp"))

    # open the shapefile
    basin_file = os.path.abspath(os.path.join(os.getcwd(), "../../data/spatial-datafiles/basins/water_basin_nad83.shp"))
    basin_shapefile = osgeo.ogr.Open(basin_file)    

    actual = {}
    actual["full_path"] = reproject_shapefile_to_wgs84(shapefile = basin_shapefile)

    # print test results        
    _print_test_info(expected, actual)
    

def main():
    """ Test functionality geospatialvectors.py """

    print("")
    print("RUNNING TESTS ...")
    print("")

    # test_fill_shapefile_dict()

    # test_get_shapefile_coords()

    # test_get_shapefile_areas()

    # test_get_intersected_field_values()

    # test_validate_field_values()

    # test_read_field_values_file_in()
    
    # test_get_field_values()

    test_reproject_shapefile_to_wgs84()

if __name__ == "__main__":
    main()    
    
    
    
    
    
    
    
    
    