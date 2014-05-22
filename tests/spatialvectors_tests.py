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
    fixture["testbasin_single_fid_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/testbasin_proj_wgs.shp"))
    fixture["testbasin_multi_fid_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/testbasin_multi_proj_wgs.shp"))
    fixture["testbasin_single_fid_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/testbasin.shp"))    

    fixture["waterbasin_single_fid_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/waterbasin_proj_wgs.shp"))
    fixture["waterbasin_multi_fid_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/waterbasin_multi_proj_wgs.shp"))

    fixture["canes_file_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/CanES_proj_wgs.shp"))
    fixture["gfdl_file_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GFDL_proj_wgs.shp"))
    fixture["giss_file_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GISS_proj_wgs.shp"))
    fixture["ncar_file_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/NCAR_proj_wgs.shp"))
    fixture["canes_file_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/CanES.shp"))
    fixture["gfdl_file_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GFDL.shp"))
    fixture["giss_file_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/GISS.shp"))
    fixture["ncar_file_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/gcm-tiles/NCAR.shp"))

    fixture["test_basinsmall_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/test_basinsmall_proj_wgs.shp"))    
    fixture["dem_basin_centroids_proj_wgs"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/dem_basin_centroids_proj_wgs.shp"))
    fixture["test_basinsmall_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/test_basinsmall.shp"))    
    fixture["dem_basin_centroids_proj_nad83"] = os.path.abspath(os.path.join(os.getcwd(), "./data/spatial-datafiles/basins/dem_basin_centroids.shp"))


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
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid_proj_wgs"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict2():

    # expected values to test with actual values
    expected = {"extents": (-76.3557164298209, -75.83406785380727, 40.52224451815593, 40.89012237818175), 
                "name": "waterbasin_proj_wgs.shp", 
                "fields": ["OBJECTID", "Id", "Shape_Leng", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["waterbasin_single_fid_proj_wgs"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)

    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict3():

    # expected values to test with actual values
    expected = {"extents": (-75.46839351213258, -74.35718960764397, 39.85602095657912, 42.36690057316007), 
                "name": "waterbasin_multi_proj_wgs.shp", 
                "fields": ["STAID", "da_sqmi", "ForestSum", "AgSum", "DevSum", "FORdivAG"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\basins", 
                "num_features": 12, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
    
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["waterbasin_multi_fid_proj_wgs"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict4():

    # expected values to test with actual values
    expected = {"extents": (1551876.4646765331, 1813149.8783592982, 1873153.3560966868, 2513535.4955471633), 
                "name": "testbasin.shp", 
                "fields": ["Id"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\basins", 
                "num_features": 1, 
                "type": "POLYGON", 
                "spatialref": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs "}
                
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid_proj_nad83"])  
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = basin_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict4():

    # expected values to test with actual values
    expected = {"extents": (-77.34375265636656, -71.71875035838741, 36.27781521345216, 44.64950905729846), 
                "name": "CanES_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "SHAPE_Area", "TileDRB", "Tile"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\gcm-tiles", 
                "num_features": 6, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_proj_wgs"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = canes_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict5():

    # expected values to test with actual values
    expected = {"extents": (-77.50000269499992, -72.50000069999992, 38.426973659000055, 44.49439100300006), 
                "name": "GFDL_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "Tile_DRB", "Tile", "Shape_Le_1", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\gcm-tiles", 
                "num_features": 6, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file_proj_wgs"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = gfdl_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict6():

    # expected values to test with actual values
    expected = {"extents": (-77.50000282499991, -72.50000059199992, 36.000007148000066, 46.00000926800006), 
                "name": "GISS_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "Tile_DRB", "Tile", "Shape_Le_1", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\gcm-tiles", 
                "num_features": 10, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file_proj_wgs"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = giss_shapefile)
  
    np.testing.assert_equal(actual, expected)
    
def test_fill_shapefile_dict7():

    # expected values to test with actual values
    expected = {"extents": (-78.125002881412, -73.12500082090243, 36.753934288860414, 44.293199945821605), 
                "name": "NCAR_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "SHAPE_Area", "Tile_DRB", "Tile"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\gcm-tiles", 
                "num_features": 32, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file_proj_wgs"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = ncar_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_fill_shapefile_dict8():

    # expected values to test with actual values
    expected = {"extents": (-76.36786373172723, -74.39059291460879, 38.71298637220271, 42.42374381313648), 
                "name": "dem_basin_centroids_proj_wgs.shp", 
                "fields": ["newhydroid", "HUC_12"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\spatial-datafiles\\basins", 
                "num_features": 3736, 
                "type": "POINT", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}
                
    # Open the shapefiles
    ncar_shapefile = osgeo.ogr.Open(fixture["dem_basin_centroids_proj_wgs"])
    
    # actual values
    actual = spatialvectors.fill_shapefile_dict(shapefile = ncar_shapefile)
  
    np.testing.assert_equal(actual, expected)

def test_get_shapefile_coords():

    # expected values to test with actual values
    expected = {}
    expected["testbasin"] = {"0": ([-76.5241897068253, -75.23041385228197, -73.58652704198151, -73.5013706471868, -75.02093324688161, -75.08254377360929, -76.46844548090678, -76.86408896229581, -76.76898146953256, -76.86020288529657, -76.5241897068253], 
                                    [43.72112550966717, 43.986783289578774, 43.58481904994738, 42.78125135043379, 42.064154034262806, 40.419906887537, 38.33140005688545, 40.22529559781875, 40.95275941413145, 41.661899956299614, 43.72112550966717])}

    expected["testbasin_nad83"] = {"0": ([1551876.4646765331, 1646948.1658269956, 1785445.705257233, 1813149.8783592982, 1710314.4423011306, 1745561.219742352, 1679365.164213511, 1603362.2856433871, 1594846.0132731413, 1571503.7313467045, 1551876.4646765331], 
                                          [2462788.591455278, 2513535.4955471633, 2499530.126391299, 2413895.970528247, 2307638.3618463, 2126904.9022905156, 1873153.3560966868, 2074193.2284434838, 2155620.5060083373, 2231871.9603013936, 2462788.591455278])}

    expected["canes"] = {"0": ([-77.34375265636656, -74.53125172872296, -74.53125153884916, -77.34375244277751, -77.34375265636656], [44.649508846266905, 44.64950895861966, 41.85894444448356, 41.85894433988654, 44.649508846266905]), 
                         "1": ([-74.53125172872296, -71.71875078911197, -71.71875062341081, -74.53125153884916, -74.53125172872296], [44.64950895861966, 44.64950905729846, 41.85894453702035, 41.85894444448356, 44.64950895861966]),                          
                         "2": ([-77.34375244277751, -74.53125153884916, -74.53125137708862, -77.34375226209623, -77.34375244277751], [41.85894433988654, 41.85894444448356, 39.068379891689446, 39.068379795204585, 41.85894433988654]), 
                         "3": ([-74.53125153884916, -71.71875062341081, -71.71875048096074, -74.53125137708862, -74.53125153884916], [41.85894444448356, 41.85894453702035, 39.0683799778016, 39.068379891689446, 41.85894444448356]), 
                         "4": ([-77.34375226209623, -74.53125137708862, -74.53125123940792, -77.34375210963982, -77.34375226209623], [39.068379795204585, 39.068379891689446, 36.277815301487045, 36.27781521345216, 39.068379795204585]),
                         "5": ([-74.53125137708862, -71.71875048096074, -71.71875035838741, -74.53125123940792, -74.53125137708862], [39.068379891689446, 39.0683799778016, 36.27781538090664, 36.277815301487045, 39.068379891689446])
    }
            
    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid_proj_wgs"]) 
    basin_shapefile_nad83 = osgeo.ogr.Open(fixture["testbasin_single_fid_proj_nad83"])
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_proj_wgs"])
    
    # actual values
    actual = {}
    actual["testbasin"] = spatialvectors.get_shapefile_coords(shapefile = basin_shapefile)
    actual["testbasin_nad83"] = spatialvectors.get_shapefile_coords(shapefile = basin_shapefile_nad83)
    actual["canes"] = spatialvectors.get_shapefile_coords(shapefile = canes_shapefile)

    np.testing.assert_equal(actual["testbasin"], expected["testbasin"])      
    np.testing.assert_equal(actual["testbasin_nad83"], expected["testbasin_nad83"]) 
    np.testing.assert_equal(actual["canes"], expected["canes"])   


def test_get_intersected_field_values1():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid_proj_wgs"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_proj_wgs"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file_proj_wgs"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file_proj_wgs"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file_proj_wgs"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["canes_tiles"], expected["canes_tiles"])
    np.testing.assert_equal(actual["gfdl_tiles"], expected["gfdl_tiles"])    
    np.testing.assert_equal(actual["giss_tiles"], expected["giss_tiles"])   
    np.testing.assert_equal(actual["ncar_tiles"], expected["ncar_tiles"])

def test_get_intersected_field_values2(): 

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"], "1": ["21", "22"], "2": ["12"]}   
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"], "1": [ "22"], "2": ["22"]} 
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"], "1": [ "22"], "2": ["22"]} 
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"], "1": ["43", "44", "33", "34"], "2": ["24"]}  

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_multi_fid_proj_wgs"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_proj_wgs"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file_proj_wgs"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file_proj_wgs"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file_proj_wgs"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["canes_tiles"], expected["canes_tiles"])
    np.testing.assert_equal(actual["gfdl_tiles"], expected["gfdl_tiles"])    
    np.testing.assert_equal(actual["giss_tiles"], expected["giss_tiles"])   
    np.testing.assert_equal(actual["ncar_tiles"], expected["ncar_tiles"])


def test_get_intersected_field_values3():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"0": ["31", "32", "21", "11"]}
    expected["gfdl_tiles"] = {"0": ["41", "42", "31", "32", "21"]}
    expected["giss_tiles"] = {"0": ["41", "42", "31", "21"]}
    expected["ncar_tiles"] = {"0": ["82", "83", "84", "72", "73", "74", "62", "63", "64", "52", "53", "42", "43", "32", "22"]}

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["testbasin_single_fid_proj_nad83"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_proj_nad83"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file_proj_nad83"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file_proj_nad83"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file_proj_nad83"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["canes_tiles"], expected["canes_tiles"])
    np.testing.assert_equal(actual["gfdl_tiles"], expected["gfdl_tiles"])    
    np.testing.assert_equal(actual["giss_tiles"], expected["giss_tiles"])   
    np.testing.assert_equal(actual["ncar_tiles"], expected["ncar_tiles"])


def test_get_intersected_field_values4():

    # expected values to test with actual values
    expected = {}
    expected["canes_tiles"] = {"01466500": ["22"], "01440000": ["21"], "01415000": ["31"], "01439500": ["21"], "01440400": ["21"], "01442500": ["21"], "01413500": ["31", "32"], "01420500": ["31", "32", "21"], "01435000": ["31", "32"], "01422500": ["31"], "01414500": ["31"], "01422389": ["31"]}   
    expected["gfdl_tiles"] = {"01466500": ["22"], "01440000": ["32"], "01415000": ["32"], "01439500": ["31"], "01440400": ["31"], "01442500": ["31"], "01413500": ["32"], "01420500": ["32"], "01435000": ["32"], "01422500": ["32"], "01414500": ["32"], "01422389": ["32"]} 
    expected["giss_tiles"] = {"01466500": ["22"], "01440000": ["32"], "01415000": ["42"], "01439500": ["31"], "01440400": ["31"], "01442500": ["31"], "01413500": ["42"], "01420500": ["42", "32"], "01435000": ["42", "32"], "01422500": ["42"], "01414500": ["42"], "01422389": ["42"]}
    expected["ncar_tiles"] = {"01466500": ["43"], "01440000": ["53"], "01415000": ["63"], "01439500": ["53"], "01440400": ["53"], "01442500": ["53"], "01413500": ["63"], "01420500": ["63"], "01435000": ["63", "64"], "01422500": ["63"], "01414500": ["63"], "01422389": ["63"]}

    # Open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["waterbasin_multi_fid_proj_wgs"])    
    canes_shapefile = osgeo.ogr.Open(fixture["canes_file_proj_wgs"])
    gfdl_shapefile = osgeo.ogr.Open(fixture["gfdl_file_proj_wgs"])
    giss_shapefile = osgeo.ogr.Open(fixture["giss_file_proj_wgs"])
    ncar_shapefile = osgeo.ogr.Open(fixture["ncar_file_proj_wgs"])

    # actual values    
    actual = {}
    actual["canes_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = canes_shapefile, intersectee_field = "Tile", intersector_field = "STAID")    
    actual["gfdl_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = gfdl_shapefile, intersectee_field = "Tile", intersector_field = "STAID")
    actual["giss_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = giss_shapefile, intersectee_field = "Tile", intersector_field = "STAID")
    actual["ncar_tiles"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = ncar_shapefile, intersectee_field = "Tile", intersector_field = "STAID")

    for shapefile in [basin_shapefile, canes_shapefile, gfdl_shapefile, giss_shapefile, ncar_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["canes_tiles"], expected["canes_tiles"])
    np.testing.assert_equal(actual["gfdl_tiles"], expected["gfdl_tiles"])    
    np.testing.assert_equal(actual["giss_tiles"], expected["giss_tiles"])   
    np.testing.assert_equal(actual["ncar_tiles"], expected["ncar_tiles"]) 
    
def test_get_intersected_field_values5():

    # expected values to test with actual values
    expected = {}
    expected["newhydroid"] = {"0": ["12", "11", "8"], "1": ["256", "241", "220", "222"]}  

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["test_basinsmall_proj_wgs"])    
    point_shapefile = osgeo.ogr.Open(fixture["dem_basin_centroids_proj_wgs"])

    # actual values    
    actual = {}
    actual["newhydroid"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = point_shapefile, intersectee_field = "newhydroid")

    for shapefile in [basin_shapefile, point_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["newhydroid"], expected["newhydroid"])

    
def test_get_intersected_field_values6():

    # expected values to test with actual values
    expected = {}
    expected["newhydroid"] = {"0": ["12", "11", "8"], "1": ["256", "241", "220", "222"]}  

    # open the shapefiles
    basin_shapefile = osgeo.ogr.Open(fixture["test_basinsmall_proj_nad83"])    
    point_shapefile = osgeo.ogr.Open(fixture["dem_basin_centroids_proj_nad83"])

    # actual values    
    actual = {}
    actual["newhydroid"] = spatialvectors.get_intersected_field_values(intersector = basin_shapefile, intersectee = point_shapefile, intersectee_field = "newhydroid")

    for shapefile in [basin_shapefile, point_shapefile]:
        shapefile.Destroy()  

    np.testing.assert_equal(actual["newhydroid"], expected["newhydroid"])
    