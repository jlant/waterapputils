import os, sys
import numpy as np
import osgeo.ogr
from StringIO import StringIO

# my module
from waterapputils import spatialvectors

# define the global fixture to hold the data that goes into the functions you test
fixture = {}

def setup():
    """ Setup and initialize fixture for testing """

    print >> sys.stderr, "SETUP: spatialvectors tests"
   
    # set up fixtures    
    fixture["test_poly_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/test_poly_nad83.shp"))
    fixture["test_poly_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/test_poly_wgs84.shp"))     

    fixture["water_basin_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/water_basin_nad83.shp"))
    fixture["water_basin_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/water_basin_wgs84.shp"))

    fixture["water_basin_pourpoint_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/water_basin_pourpoint_nad83.shp"))
    fixture["water_basin_pourpoint_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/water_basin_pourpoint_wgs84.shp"))

    fixture["water_basins_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/water_basins_nad83.shp"))
    fixture["water_basins_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/water_basins_wgs84.shp"))

    fixture["canes_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/CanES_nad83.shp"))
    fixture["gfdl_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GFDL_nad83.shp"))
    fixture["giss_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GISS_nad83.shp"))
    fixture["ncar_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/NCAR_nad83.shp"))
    
    fixture["canes_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/CanES_wgs84.shp"))
    fixture["gfdl_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GFDL_wgs84.shp"))
    fixture["giss_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GISS_wgs84.shp"))
    fixture["ncar_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/NCAR_wgs84.shp"))

    fixture["wateruse_centroids_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/wateruse-centroids/wateruse_centroids_nad83.shp"))  
    fixture["wateruse_centroids_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/wateruse-centroids/wateruse_centroids_wgs84.shp"))

    fixture["wateruse_centroids_sample_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp"))  
    fixture["wateruse_centroids_sample_wgs84"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_wgs84.shp"))  

    fixture["csv_non_intersecting_data_file"] = \
    """
    basin, centroids
    0123456, 45, 50, 55, 60 
    7890123, 65, 70, 75, 80 
    """

def teardown():
    """ Print to standard error when all tests are finished """
    
    print >> sys.stderr, "TEARDOWN: spatialvectors tests" 


def test_create_shapefile_dict():
    """ Test create_shapefile_dict() """

    # expected values to test with actual values
    expected = {"shapefile_datatype": None, "type": None, "path": None, "name": None, "num_features": None, "fields": [], "spatialref": None, "extents": ()}
    
    # actual values
    actual = spatialvectors.create_shapefile_dict()
  
    np.testing.assert_equal(expected, actual)

def test_fill_shapefile_dict1():

    # expected values to test with actual values
    expected = {"extents": (1551876.4646765331, 1813149.8783592982, 1873153.3560966868, 2513535.4955471633), 
                "name": "test_poly_nad83.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["test_poly_nad83"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict2():

    # expected values to test with actual values
    expected = {"extents": (-76.86408896229705, -73.50137064718774, 38.33140005688863, 43.98678328958175), 
                "name": "test_poly_wgs84.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["test_poly_wgs84"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 

    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict3():

    # expected values to test with actual values
    expected = {"extents": (1634846.262699829, 1674156.2626998313, 2118676.340300313, 2162946.3403003197), 
                "name": "water_basin_nad83.shp", 
                "fields": ['OBJECTID', 'Id', 'Shape_Leng', 'Shape_Area'], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basin_nad83"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 

    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict4():

    # expected values to test with actual values
    expected = {"extents": (-76.3557164298209, -75.83406785380727, 40.52224451815593, 40.89012237818175), 
                "name": "water_basin_wgs84.shp", 
                "fields": ['OBJECTID', 'Id', 'Shape_Leng', 'Shape_Area'], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basin_wgs84"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 

    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict5():

    # expected values to test with actual values
    expected = {"extents": (1667931.2626998292, 1667931.2626998292, 2121671.340300318, 2121671.340300318), 
                "name": "water_basin_pourpoint_nad83.shp", 
                "fields": ['OBJECTID', 'POINTID', 'GRID_CODE'], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POINT", 
                "spatialref": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basin_pourpoint_nad83"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 

    np.testing.assert_equal(actual, expected)


def test_fill_shapefile_dict6():

    # expected values to test with actual values
    expected = {"extents": (-77.34375265636656, -71.71875035838741, 36.27781521345216, 44.64950905729846), 
                "name": "CanES_wgs84.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "SHAPE_Area", "TileDRB", "Tile"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\gcm-tiles", 
                "num_features": 6, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    canes_shapefile = osgeo.ogr.Open(fixture["canes_wgs84"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = canes_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 
  
    np.testing.assert_equal(actual, expected)


def test_fill_shapefile_dict7():

    # expected values to test with actual values
    expected = {"extents": (-74.88702164959378, -74.44895756386826, 41.86688996255413, 42.31789523609384), 
                "name": "wateruse_centroids_sample_wgs84.shp", 
                "fields": ["newhydroid", "HUC_12"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "\\data\\spatial-datafiles\\wateruse-centroids", 
                "num_features": 8, 
                "type": "POINT", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    wateruse_centroids_sample_shapefile = osgeo.ogr.Open(fixture["wateruse_centroids_sample_wgs84"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = wateruse_centroids_sample_shapefile)

    actual["path"] = actual["path"].split("waterapputils")[1]       # remove dependency of full root path 
  
    np.testing.assert_equal(actual, expected)
    


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
        
    # Open the shapefiles
    basin_shapefile_wgs84 = osgeo.ogr.Open(fixture["test_poly_wgs84"]) 
    basin_shapefile_nad83 = osgeo.ogr.Open(fixture["test_poly_nad83"]) 
    canes_shapefile_wgs84 = osgeo.ogr.Open(fixture["canes_wgs84"])
    
    # actual values
    actual = {}
    actual["test_poly_wgs84"] = spatialvectors.get_shapefile_coords(shapefile = basin_shapefile_wgs84)
    actual["test_poly_nad83"] = spatialvectors.get_shapefile_coords(shapefile = basin_shapefile_nad83)
    actual["canes_wgs84"] = spatialvectors.get_shapefile_coords(shapefile = canes_shapefile_wgs84)

    np.testing.assert_equal(actual["test_poly_wgs84"], expected["test_poly_wgs84"])      
    np.testing.assert_equal(actual["test_poly_nad83"], expected["test_poly_nad83"]) 
    np.testing.assert_equal(actual["canes_wgs84"], expected["canes_wgs84"])   


def test_get_intersected_field_values1():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["test_poly_wgs84"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_wgs84"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_wgs84"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_wgs84"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_wgs84"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile", intersector_field = "")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile", intersector_field = "")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile", intersector_field = "")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile", intersector_field = "")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["canes_tiles"], expected["canes_tiles"])
    np.testing.assert_equal(actual["gfdl_tiles"], expected["gfdl_tiles"])    
    np.testing.assert_equal(actual["giss_tiles"], expected["giss_tiles"])   
    np.testing.assert_equal(actual["ncar_tiles"], expected["ncar_tiles"])


def test_get_intersected_field_values2():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["test_poly_nad83"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_nad83"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_nad83"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_nad83"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_nad83"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile", intersector_field = "")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile", intersector_field = "")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile", intersector_field = "")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile", intersector_field = "")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["canes_tiles"], expected["canes_tiles"])
    np.testing.assert_equal(actual["gfdl_tiles"], expected["gfdl_tiles"])    
    np.testing.assert_equal(actual["giss_tiles"], expected["giss_tiles"])   
    np.testing.assert_equal(actual["ncar_tiles"], expected["ncar_tiles"])

    
def test_get_intersected_field_values3():

    # expected values to test with actual values
    expected = {}
    expected["newhydroid"] = {"01413500": ["149", "61", "22"], "01420500": ["440", "390", "257"], "01414500": None, "01435000": ["262", "220"]}   

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basins_nad83"])    
    point_shapefile = osgeo.ogr.Open(fixture["wateruse_centroids_sample_nad83"])

    # actual values    
    actual = {}
    actual["newhydroid"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = point_shapefile, intersectee_field = "newhydroid", intersector_field = "STAID")

    for shapefile in [basin_shapefile, point_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["newhydroid"], expected["newhydroid"])

def test_get_intersected_field_values4():

    # expected values to test with actual values
    expected = {}
    expected["newhydroid"] = {"01413500": ["149", "61", "22"], "01420500": ["440", "390", "257"], "01414500": None, "01435000": ["262", "220"]}   

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basins_wgs84"])    
    point_shapefile = osgeo.ogr.Open(fixture["wateruse_centroids_sample_wgs84"])

    # actual values    
    actual = {}
    actual["newhydroid"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = point_shapefile, intersectee_field = "newhydroid", intersector_field = "STAID")

    for shapefile in [basin_shapefile, point_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["newhydroid"], expected["newhydroid"])    

def test_validate_field_values():

    # expected values to test with actual values
    expected = {} 
    expected["intersected"] = {"0": ["12", "11", "8"]}
    expected["non_intersected"] = {"1": None}

    # sample field values dictionary
    field_values_dict = {"0": ["12", "11", "8"], "1": None} 
    
    # actual values    
    actual = {}
    actual["intersected"], actual["non_intersected"] = spatialvectors.validate_field_values(field_values_dict)

    np.testing.assert_equal(actual["intersected"], expected["intersected"])    
    np.testing.assert_equal(actual["non_intersected"], expected["non_intersected"]) 

def test_read_field_values_file_in():

    # expected values to test with actual values
    expected = {} 
    expected["data"] = {"0123456": ["45", "50", "55", "60"], "7890123": ["65", "70", "75", "80"]}

    # convert string to a file object
    file_obj = StringIO(fixture["csv_non_intersecting_data_file"])
    
    # actual values    
    actual = {}
    actual["data"] = spatialvectors.read_field_values_file_in(file_obj)

    np.testing.assert_equal(actual["data"], expected["data"]) 


def test_get_field_values():

    # expected values to test with actual values
    expected = {}
    expected = {'01413500': '163.229819866', '01420500': '242.401970189', '01414500': '25.109982983', '01435000': '66.6622693618'}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basins_wgs84"])  

    actual = spatialvectors.get_field_values(shapefile = basin_shapefile, id_field = "STAID", query_field = "da_sqmi")

    basin_shapefile.Destroy()  

    # print test results        
    np.testing.assert_equal(actual, expected)  
    
def test_get_shapefile_areas():
    expected = {}
    expected = {'01413500': 422764983.7640325, '01420500': 627820731.9907457, '01414500': 65034817.5157996, '01435000': 172655175.67497352}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["water_basins_nad83"])    

    actual = spatialvectors.get_shapefile_areas(shapefile = basin_shapefile, id_field = "STAID")

    basin_shapefile.Destroy()  

    # print test results        
    np.testing.assert_equal(actual, expected)  