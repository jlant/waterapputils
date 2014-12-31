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

def get_map_extents(shapefiles, shp_name = None):
    """   
    Get max and min extent coordinates from a list of shapefiles to use as the 
    extents on the map. Use the map extents to calculate the map center and the 
    standard parallels.
    
    Parameters
    ----------
    shapefiles : list 
        List of shapefile_data dictionaries 
    shp_name : string
        String name of shapefile to use for getting map extents 

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

    if shp_name:
        for shapefile_data in shapefiles:            
            if shp_name in shapefile_data["name"].split("_")[0]:
                lons.append(shapefile_data["extents"][0:2])
                lats.append(shapefile_data["extents"][2:])
        
    else:
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

def plot_shapefiles_map(shapefiles, display_fields = [], colors = [], title = None, is_visible = False, save_path = None, save_name = "map.png", shp_name = None, buff = 1.0):
    """   
    Generate a map showing all the shapefiles in the shapefile_list.  
    Shapefiles should be in a Geographic Coordinate System (longitude and 
    latitude coordinates) such as World WGS84; Matplotlib"s basemap library 
    does the proper transformation to a projected coordinate system.  The projected
    coordinate system used is Albers Equal Area.
    
    Parameters
    ----------
    shapefiles : list 
        List of dictionaries containing shapefile information
    title : string 
        String title for plot
    display_fields : list 
        List of strings that correspond to a shapefile field where the corresponding value(s) will be displayed.
    colors : list
        List of strings that correspond to colors to be displayed
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    shp_name : string
        String name of shapefile to use for getting map extents 
    buff : float
        Float value in coordinate degrees to buffer the map with
    """  

    extent_coords, center_coords, standard_parallels = get_map_extents(shapefiles, shp_name = shp_name)    

    # create the figure
    plt.figure(figsize = (10,10))    
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
    bmap.drawparallels(np.arange(-80., 81., 1.), labels = [1, 0, 0, 0], linewidth = 0.5)
    bmap.drawmeridians(np.arange(-180., 181., 1.), labels = [0, 0, 0, 1], linewidth = 0.5)
     
    # plot each shapefile on the basemap    
    legend_handles = []
    legend_labels = []
    colors_index = 0
    colors_list = ["b", "g", "y", "r", "c", "y", "m", "orange", "aqua", "darksalmon", "gold", "k"]
    for shapefile_data in shapefiles:
        
        # set up colors to use
        if colors:
            color = colors[colors_index]        
        elif colors_index > len(colors_list) - 1:
            color = np.random.rand(3,)
        else:
            color = colors_list[colors_index]         
        
        full_path = os.path.join(shapefile_data["path"], shapefile_data["name"].split(".")[0])
        
        shp_tuple = bmap.readshapefile(full_path, "shp", drawbounds = False)                            # use basemap shapefile reader for ease of plotting
        for shape_dict, shape in zip(bmap.shp_info, bmap.shp):                                          # zip the shapefile information and its shape as defined by basemap

            if shapefile_data["type"] == "POLYGON":
                p1 = mpl.patches.Polygon(shape, facecolor = color, edgecolor = "k",
                                         linewidth = 1, alpha = 0.7, label = shapefile_data["name"])            
                plt.gca().add_patch(p1)
                xx, yy = zip(*shape)
                txt_x = str(np.mean(xx))
                txt_y = str(np.mean(yy))
                
            elif shapefile_data["type"] == "POINT":
                x, y = shape

                if "usgsgages" in shapefile_data["name"].split("_")[0]:
                    p1 = bmap.plot(x, y, color = color, marker = "^", markersize = 10, label = shapefile_data["name"])
                elif "wateruse" in shapefile_data["name"].split("_")[0]:
                    p1 = bmap.plot(x, y, color = color, marker = "o", markersize = 5, label = shapefile_data["name"])
                else:
                    print("what!!")
                    p1 = bmap.plot(x, y, color = color, marker = "o", markersize = 10, label = shapefile_data["name"])

                txt_x = str(x)
                txt_y = str(y)
                
            else:
                xx, yy = zip(*shape)
                p1 = bmap.plot(xx, yy, linewidth = 1, color = color, label = shapefile_data["name"])
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
        legend_labels.append(shapefile_data["name"].split("_")[0])

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
         
        filepath = os.path.join(save_path, save_name)
        plt.savefig(filepath, dpi = 100)                        
      
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()

def _create_shapefile_test_data():
    """ Create test data for tests """
    import spatialvectors
    import osgeo.ogr
    
    fixture = {}

    # open the shapefiles
    test_poly_wgs84_shapefile = osgeo.ogr.Open(os.path.abspath(os.path.join(os.getcwd(), "../data/spatial-datafiles/basins/test_poly_wgs84.shp"))) 
    water_basin_wgs84_shapefile = osgeo.ogr.Open(os.path.abspath(os.path.join(os.getcwd(), "../data/spatial-datafiles/basins/water_basin_wgs84.shp")))      
    water_basins_wgs84_shapefile = osgeo.ogr.Open(os.path.abspath(os.path.join(os.getcwd(), "../data/spatial-datafiles/basins/water_basins_wgs84.shp")))  
    water_basin_pourpoint_wgs84_shapefile = osgeo.ogr.Open(os.path.abspath(os.path.join(os.getcwd(), "../data/spatial-datafiles/basins/water_basin_pourpoint_wgs84.shp")))      
    canes_wgs84_shapefile = osgeo.ogr.Open(os.path.abspath(os.path.join(os.getcwd(), "../data/spatial-datafiles/gcm-tiles/CanES_wgs84.shp"))) 
    wateruse_centroids_sample_wgs84_shapefile = osgeo.ogr.Open(os.path.abspath(os.path.join(os.getcwd(), "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_wgs84.shp"))) 

    fixture["test_poly_wgs84"] = spatialvectors.fill_shapefile_dict(shapefile = test_poly_wgs84_shapefile)
    fixture["water_basin_wgs84"] = spatialvectors.fill_shapefile_dict(shapefile = water_basin_wgs84_shapefile)
    fixture["water_basins_wgs84"] = spatialvectors.fill_shapefile_dict(shapefile = water_basins_wgs84_shapefile)
    fixture["water_basin_pourpoint_wgs84"] = spatialvectors.fill_shapefile_dict(shapefile = water_basin_pourpoint_wgs84_shapefile)
    fixture["canes_wgs84"] = spatialvectors.fill_shapefile_dict(shapefile = canes_wgs84_shapefile)  
    fixture["wateruse_centroids_sample_wgs84"] = spatialvectors.fill_shapefile_dict(shapefile = wateruse_centroids_sample_wgs84_shapefile)  

    return fixture

def test_print_shapefile_data():
    """ Test print_shapefile_data """
    
    print("--- Testing print_shapefile_data ---")
    
    fixture = _create_shapefile_test_data()
    print_shapefile_data(shapefile_dict = fixture["test_poly_wgs84"])
    
    print("")

def test_plot_shapefiles_map(map_type = "test_poly"):
    """ Test plot_shapefile_data """
    
    print("--- Testing plot_shapefile_data() ---")
    
    fixture = _create_shapefile_test_data()

    if map_type == "test_poly":
        plot_shapefiles_map(shapefiles = [fixture["test_poly_wgs84"]], display_fields = ["Id"], title = "Testing plotting of map")   

    if map_type == "water_basin":
        plot_shapefiles_map(shapefiles = [fixture["water_basin_wgs84"], fixture["water_basin_pourpoint_wgs84"]], display_fields = ["Id", "POINTID"], colors = ["g", "r"], title = "Water basin with pour point")       
        
    if map_type == "climate_change":
        plot_shapefiles_map(shapefiles = [fixture["canes_wgs84"], fixture["water_basins_wgs84"]], display_fields = ["Tile", "STAID"], title = "Climate Change: CanES GCM with sample basins")   

    if map_type == "water_use":
        plot_shapefiles_map(shapefiles = [fixture["water_basins_wgs84"], fixture["wateruse_centroids_sample_wgs84"]], display_fields = ["Tile", "STAID"], colors = ["g", "b"], title = "Water Use: Sample water use point with sample basins")   


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
        map_types = ["test_poly", "water_basin", "climate_change", "water_use"]
        map_type = raw_input("Please type one of the following map types to plot:\n{}\n".format(map_types))
        if map_type in map_types:
            test_plot_shapefiles_map(map_type)
        else:
            print("invalid map type selected: {}".format(map_type))

if __name__ == "__main__":
    main()  