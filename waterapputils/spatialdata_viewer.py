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

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_map_extents(shapefile_list):
    """   
    Get max and min extent coordinates from a list of shapefiles to use as the 
    extents on the map. Use the map extents to calculate the map center and the 
    standard parallels.
    
    Parameters
    ----------
    shapefile_list : list 
        List of shapefile_data dictionaries 
                              
    Returns
    -------
    extent_coords : dictionary 
        Dictionary containing 'lon_min', 'lon_max', 'lat_max', 'lat_min' keys with respective calculated values
    center_coords : dictionary 
        Dictionary containing 'lon', 'lat' keys with respective calculated values
    standard_parallels : dictionary 
        Dictionary containing 'first', 'second' keys with respective calculated values (first = min(lat), second = max(lat))   
    """

    extent_coords = {}    
    center_coords = {}
    standard_parallels = {}
    
    lons = []
    lats = []
    for shapefile_data in shapefile_list:
        lons.append(shapefile_data['extents'][0:2])
        lats.append(shapefile_data['extents'][2:])
    
    extent_coords['lon_min'] = np.min(lons)
    extent_coords['lon_max'] = np.max(lons)
    extent_coords['lat_min'] = np.min(lats)
    extent_coords['lat_max'] = np.max(lats)
     
    center_coords['lon'] = np.mean([extent_coords['lon_min'], extent_coords['lon_max']])
    center_coords['lat'] = np.mean([extent_coords['lat_min'], extent_coords['lat_max']])
    
    standard_parallels['first'] = extent_coords['lat_min']
    standard_parallels['second'] = extent_coords['lat_max']
        
    return extent_coords, center_coords, standard_parallels

def plot_map(shapefile_list, title_str):
    """   
    Generate a map showing all the shapefiles in the shapefile_list.  
    Shapefiles should be in a Geographic Coordinate System (longitude and 
    latitude coordinates) such as World WGS84; Matplotlib's basemap library 
    does the proper transformation to a projected coordinate system.  The projected
    coordinate system used is Lambert Conformal Conic.
    
    *Parameters*:
        shapefile_list : list of dictionaries containing osgeo.ogr.DataSource shapefile and shapefile information
        title_str : string title for plot

            Example shapefile_list:
                    shapefile_list = [shapefile_data1, shapefile_data2]

    *Return*:
        No return
        
    """
    
    extent_coords, center_coords, standard_parallels = get_map_extents(shapefile_list)    
    
    plt.figure(figsize = (12,10))
    
    buff = 10
    m = Basemap(projection = 'aea', 
                llcrnrlon = extent_coords['lon_min'] - buff, llcrnrlat = extent_coords['lat_min'] - buff, 
                urcrnrlon = extent_coords['lon_max'] + buff, urcrnrlat = extent_coords['lat_max'] + buff, 
                lat_1 = standard_parallels['first'], lat_2 = standard_parallels['second'],
                lon_0 = center_coords['lon'], lat_0 = center_coords['lat'],
                resolution = 'h', area_thresh = 10000)    

    m.drawcoastlines()
    m.drawcountries()
    m.drawrivers(linewidth = 1, color = 'blue')
    m.drawstates()
    m.drawmapboundary(fill_color = 'aqua')
    m.fillcontinents(color = 'coral', lake_color = 'aqua')
    m.drawparallels(np.arange(-80., 81., 10.), labels = [1, 0, 0, 0])
    m.drawmeridians(np.arange(-180., 181., 10.), labels = [0, 0, 0, 1])
    
    legend_handles = []
    legend_labels = []
    for shapefile_data in shapefile_list:
        shp_tuple = m.readshapefile(shapefile_data['path'], 'shp', drawbounds = False)
        for shape_dict, shape in zip(m.shp_info, m.shp):

            if shapefile_data['type'] == 'POLYGON':
                p1 = mpl.patches.Polygon(shape, facecolor = shapefile_data['display_color'], edgecolor = shapefile_data['display_color'],
                                         linewidth = 2, alpha = 0.5, label = shapefile_data['name'])            
                plt.gca().add_patch(p1)
                xx, yy = zip(*shape)
                txt_x = str(np.mean(xx))
                txt_y = str(np.mean(yy))
                
            elif shapefile_data['type'] == 'POINT':
                x, y = shape
                p1 = m.plot(x, y, color = shapefile_data['display_color'], marker = shapefile_data['display_marker'], markersize = 12, label = shapefile_data['name'])
                txt_x = str(x)
                txt_y = str(y)
                
            else:
                xx, yy = zip(*shape)
                p1 = m.plot(xx, yy, linewidth = 2, color = shapefile_data['display_color'], label = shapefile_data['name'])
                txt_x = str(np.mean(xx))
                txt_y = str(np.mean(yy))
                
            if isinstance(p1, list):
                p1 = p1[0]
    
            field_label = shapefile_data['display_field']
            if field_label in shape_dict.keys():
                plt.text(txt_x, txt_y, shape_dict[field_label], color = 'k', fontsize = 12, fontweight = 'bold')
    
        legend_handles.append(p1)    
        legend_labels.append(shapefile_data['name'])

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    # edit the contents of handles and labels to only show 1 legend per shape
    handles = legend_handles
    labels = legend_labels
    legend = ax.legend(handles, labels, fancybox = True, numpoints = 1)
    legend.get_frame().set_alpha(0.5)
    legend.draggable(state = True)

    plt.title(title_str)

    plt.show()