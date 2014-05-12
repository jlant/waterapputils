# -*- coding: utf-8 -*-
"""
:Module: spatialvectors.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/  

:Synopsis: Handles viewing shapefiles with a base map.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# my modules
import spatialvectors

def print_shapefile_data(shapefile_dict):
    """   
    Print information contained in the shapefile dictionary. 
    
    Parameters
    ----------
    shapefile_dict : dictionary 
        Dictionary containing information found in a shapefile   
    """   
    print("")
    print("--- SHAPEFILE INFORMATION ---")
    print("")    
    print("Name:\n    {}\n".format(shapefile_dict["name"]))
    print("Path:\n    {}\n".format(shapefile_dict["path"]))
    print("Type:\n    {}\n".format(shapefile_dict["type"]))
    print("Spatial reference:\n    {}\n".format(shapefile_dict["spatialref"]))
    print("Extents:\n    {}\n".format(shapefile_dict["extents"]))    
    print("Fields:\n    {}\n".format(shapefile_dict["fields"]))
    print("Number of features:\n    {}\n".format(shapefile_dict["num_features"]))

def get_map_extents(shapefiles):
    """   
    Get max and min extent coordinates from a list of shapefiles to use as the 
    extents on the map. Use the map extents to calculate the map center and the 
    standard parallels.
    
    Parameters
    ----------
    shapefiles : list 
        List of shapefile_data dictionaries 
                              
    Returns
    -------
    extent_coords : dictionary 
        Dictionary containing "lon_min", "lon_max", "lat_max", "lat_min" keys with respective calculated values
    center_coords : dictionary 
        Dictionary containing "lon", "lat" keys with respective calculated values
    standard_parallels : dictionary 
        Dictionary containing "first", "second" keys with respective calculated values (first = min(lat), second = max(lat))   
    """
    extent_coords = {}    
    center_coords = {}
    standard_parallels = {}
    
    lons = []
    lats = []
    for shapefile_data in shapefiles:
        lons.append(shapefile_data["extents"][0:2])
        lats.append(shapefile_data["extents"][2:])
    
    extent_coords["lon_min"] = np.min(lons)
    extent_coords["lon_max"] = np.max(lons)
    extent_coords["lat_min"] = np.min(lats)
    extent_coords["lat_max"] = np.max(lats)
     
    center_coords["lon"] = np.mean([extent_coords["lon_min"], extent_coords["lon_max"]])
    center_coords["lat"] = np.mean([extent_coords["lat_min"], extent_coords["lat_max"]])
    
    standard_parallels["first"] = extent_coords["lat_min"]
    standard_parallels["second"] = extent_coords["lat_max"]
        
    return extent_coords, center_coords, standard_parallels

def plot_shapefiles_map(shapefiles, display_fields = [], title = None, is_visible = True, save_path = None):
    """   
    Generate a map showing all the shapefiles in the shapefile_list.  
    Shapefiles should be in a Geographic Coordinate System (longitude and 
    latitude coordinates) such as World WGS84; Matplotlib"s basemap library 
    does the proper transformation to a projected coordinate system.  The projected
    coordinate system used is Lambert Conformal Conic.
    
    Parameters
    ----------
    shapefiles : list 
        List of dictionaries containing shapefile information
    title : string 
        String title for plot
    display_fields : list 
        List of strings that correspond to a shapefile field where the corresponding value(s) will be displayed.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    """   
    # get the map extents to map center the map appropriately around shapefile data; buffer the extents a bit as well
    extent_coords, center_coords, standard_parallels = get_map_extents(shapefiles)    
    buff = 10   

    # create the figure
    plt.figure(figsize = (12,10))    
    plt.title(title)
    
    # create the basemap object with Albers Equal Area Conic Projection
    bmap = Basemap(projection = "aea", 
                   llcrnrlon = extent_coords["lon_min"] - buff, llcrnrlat = extent_coords["lat_min"] - buff, 
                   urcrnrlon = extent_coords["lon_max"] + buff, urcrnrlat = extent_coords["lat_max"] + buff, 
                   lat_1 = standard_parallels["first"], lat_2 = standard_parallels["second"],
                   lon_0 = center_coords["lon"], lat_0 = center_coords["lat"],
                   resolution = "h", area_thresh = 10000)    
    
    # have basemap object plot background stuff
    bmap.drawcoastlines()
    bmap.drawcountries()
    bmap.drawrivers(linewidth = 1, color = "blue")
    bmap.drawstates()
    bmap.drawmapboundary(fill_color = "aqua")
    bmap.fillcontinents(color = "coral", lake_color = "aqua")
    bmap.drawparallels(np.arange(-80., 81., 10.), labels = [1, 0, 0, 0])
    bmap.drawmeridians(np.arange(-180., 181., 10.), labels = [0, 0, 0, 1])
     
    # plot each shapefile on the basemap    
    legend_handles = []
    legend_labels = []
    colors_index = 0
    for shapefile_data in shapefiles:
        
        # set up colors to use
        colors_list = ["b", "g", "y", "r", "c", "y", "m", "orange", "aqua", "darksalmon", "gold", "k"]
        if colors_index > len(colors_list) - 1:
            color = np.random.rand(3,)
        else:
            color = colors_list[colors_index]         
        
        full_path = "/".join([shapefile_data["path"], shapefile_data["name"].split(".")[0]])
        shp_tuple = bmap.readshapefile(full_path, "shp", drawbounds = False)          # use basemap shapefile reader for ease of plotting
        for shape_dict, shape in zip(bmap.shp_info, bmap.shp):                                        # zip the shapefile information and its shape as defined by basemap

            if shapefile_data["type"] == "POLYGON":
                p1 = mpl.patches.Polygon(shape, facecolor = color, edgecolor = color,
                                         linewidth = 2, alpha = 0.7, label = shapefile_data["name"])            
                plt.gca().add_patch(p1)
                xx, yy = zip(*shape)
                txt_x = str(np.mean(xx))
                txt_y = str(np.mean(yy))
                
            elif shapefile_data["type"] == "POINT":
                x, y = shape
                p1 = bmap.plot(x, y, color = color, marker = "o", markersize = 12, label = shapefile_data["name"])
                txt_x = str(x)
                txt_y = str(y)
                
            else:
                xx, yy = zip(*shape)
                p1 = bmap.plot(xx, yy, linewidth = 2, color = color, label = shapefile_data["name"])
                txt_x = str(np.mean(xx))
                txt_y = str(np.mean(yy))
            
            
            if isinstance(p1, list):
                p1 = p1[0]

            # control text display of shapefile fields
            for display_field in display_fields:
                if display_field in shape_dict.keys():
                    plt.text(txt_x, txt_y, shape_dict[display_field], color = "k", fontsize = 12, fontweight = "bold")

        colors_index += 1    
        legend_handles.append(p1)    
        legend_labels.append(shapefile_data["name"])

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    
    # edit the contents of handles and labels to only show 1 legend per shape
    handles = legend_handles
    labels = legend_labels
    legend = ax.legend(handles, labels, fancybox = True, numpoints = 1)
    legend.get_frame().set_alpha(0.5)
    legend.draggable(state = True)

    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)

        filename = "-".join("Shapefile","Map")  + ".png"           
        filepath = os.path.join(save_path, filename)
        plt.savefig(filepath, dpi = 100)                        
      
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()

def _create_shapefile_test_data():
    """ Create test data for tests """
    
    fixture = {}
   
    fixture["testbasin"] = {"extents": (-76.86408896229581, -73.5013706471868, 38.33140005688545, 43.986783289578774), 
                            "name": "testbasin_proj_wgs.shp", 
                            "fields": ["Id"], 
                            "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                            "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                            "num_features": 1, 
                            "type": "POLYGON", 
                            "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    fixture["waterbasin"] = {"extents": (-76.3557164298209, -75.83406785380727, 40.52224451815593, 40.89012237818175), 
                            "name": "waterbasin_proj_wgs.shp", 
                            "fields": ["OBJECTID", "Id", "Shape_Leng", "Shape_Area"], 
                            "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                            "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                            "num_features": 1, 
                            "type": "POLYGON", 
                            "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    fixture["waterbasin_multi"] = {"extents": (-75.46839351213258, -74.35718960764397, 39.85602095657912, 42.36690057316007), 
                                    "name": "waterbasin_multi_proj_wgs.shp", 
                                    "fields": ["STAID", "da_sqmi", "ForestSum", "AgSum", "DevSum", "FORdivAG"], 
                                    "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                                    "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\testbasin_proj_wgs", 
                                    "num_features": 12, 
                                    "type": "POLYGON", 
                                    "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    fixture["canes"] = {"extents": (-77.34375265636656, -71.71875035838741, 36.27781521345216, 44.64950905729846), 
                        "name": "CanES_proj_wgs.shp", 
                        "fields": ["OBJECTID", "SHAPE_Leng", "SHAPE_Area", "TileDRB", "Tile"], 
                        "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                        "path": "C:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\gcm_proj_wgs", 
                        "num_features": 6, 
                        "type": "POLYGON", 
                        "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    fixture["gfdl"] = {"extents": (-77.50000269499992, -72.50000069999992, 38.426973659000055, 44.49439100300006), 
                "name": "GFDL_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "Tile_DRB", "Tile", "Shape_Le_1", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\gcm_proj_wgs", 
                "num_features": 6, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    fixture["giss"] = {"extents": (-77.50000282499991, -72.50000059199992, 36.000007148000066, 46.00000926800006), 
                "name": "GISS_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "Tile_DRB", "Tile", "Shape_Le_1", "Shape_Area"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\gcm_proj_wgs", 
                "num_features": 10, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}

    fixture["ncar"] = {"extents": (-78.125002881412, -73.12500082090243, 36.753934288860414, 44.293199945821605), 
                "name": "NCAR_proj_wgs.shp", 
                "fields": ["OBJECTID", "SHAPE_Leng", "SHAPE_Area", "Tile_DRB", "Tile"], 
                "shapefile_datatype": "<class 'osgeo.ogr.DataSource'>", 
                "path": "c:\\Users\\jlant\\jeremiah\\projects\\python-projects\\waterapputils\\data\\deltas-gcm\\gcm_proj_wgs", 
                "num_features": 32, 
                "type": "POLYGON", 
                "spatialref": "+proj=longlat +datum=WGS84 +no_defs "}


    return fixture

def test_print_shapefile_data():
    """ Test print_shapefile_data """
    
    print("--- Testing print_shapefile_data ---")
    
    fixture = _create_shapefile_test_data()
    print_shapefile_data(shapefile_dict = fixture["testbasin"])
    
    print("")

def test_plot_shapefiles_map():
    """ Test plot_shapefile_data """
    
    print("--- Testing plot_shapefile_data ---")
    
    fixture = _create_shapefile_test_data()
    
    plot_shapefiles_map(shapefiles = [fixture["testbasin"], fixture["waterbasin"]], display_fields = ["Id", "Id"], title = "Testing plotting of map")    

    plot_shapefiles_map(shapefiles = [fixture["testbasin"], fixture["waterbasin_multi"]], display_fields = ["STAID"], title = "Sample test basins")

    plot_shapefiles_map(shapefiles = [fixture["canes"], fixture["waterbasin_multi"]], display_fields = ["Tile", "STAID"], title = "Canes GCM with sample basins")

    plot_shapefiles_map(shapefiles = [fixture["canes"], fixture["gfdl"], fixture["giss"], fixture["ncar"], fixture["waterbasin_multi"]], display_fields = ["Tile"], title = "Many GCM's with sample basins")
    
    
    print("")

def main():
    """ Test functionality of waterapputils_viewer() """

    print("")
    print("RUNNING TESTS ...")
    print("")

    ans_print_shapefile_data = raw_input("Do you want to test print_shapefile_data()? y/n ")
    if ans_print_shapefile_data == "y":
        test_print_shapefile_data()

    ans_plot_shapefile_data = raw_input("Do you want to test plot_shapefiles_map()? y/n ")
    if ans_plot_shapefile_data == "y":
        test_plot_shapefiles_map()

if __name__ == "__main__":
    main()  