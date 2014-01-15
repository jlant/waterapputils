# -*- coding: utf-8 -*-
"""
:Module: spatial.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Functions to do spatial analysis on GIS datasets. 

"""

import os
import Tkinter, tkFileDialog
import osgeo.ogr
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import shapely.wkt
import mpl_toolkits.basemap.pyproj as pyproj 

def get_intersectedtiles(gcm_shapefile, basin_shapefile):
    """   
    Get the tiles associated with the global climate model shapefile (gcm_shapefile)
    which are intersected by the basin shapefile.
    
    *Parameters*:
        gcm_shapefile : osgeo.ogr.DataSource 
        basin_shapefile : osgeo.ogr.DataSource 

    *Return*:
        tiles : list of string tile numbers
        
    """    
    gcm_layer = gcm_shapefile.GetLayer()

    basin_layer = basin_shapefile.GetLayer()
    basin_feature = basin_layer.GetFeature(0)
    basin_geometry = basin_feature.GetGeometryRef()
    
    tiles = []    
    num_features = gcm_layer.GetFeatureCount()
    for feature_num in range(num_features):
        gcm_feature = gcm_layer.GetFeature(feature_num)
        gcm_geometry = gcm_feature.GetGeometryRef()
        if basin_geometry.Intersect(gcm_geometry):    
            tiles.append(gcm_feature.GetField('Tile'))

        
    return tiles

def get_lonlat_old(shapefile):
    """   
    Get the longitudes and latitudes of a shapefile.  Shapefile should be in a
    Geographic Coordinate System (longitude and latitude coordinates) such as 
    World WGS84.
    
    *Parameters*:
        shapefile : osgeo.ogr.DataSource 

    *Return*:
        lon : array of longitudes
        lat : array of latitudes
        
    """   
    longitudes_all = []
    latitudes_all = []
    tiles_all = []
    num_layers = shapefile.GetLayerCount()
    for layer_num in range(num_layers) :
        shp_layer = shapefile.GetLayer(layer_num)
        spatial_ref = shp_layer.GetSpatialRef().ExportToProj4()
        num_features = shp_layer.GetFeatureCount()
        
        layer_def = shp_layer.GetLayerDefn()
        field_names = []
        for i in range(layer_def.GetFieldCount()):
            field_names.append(layer_def.GetFieldDefn(i).GetName())
        
        longitudes = []
        latitudes = []
        tiles = []
        for feature_num in range(num_features):
            shp_feature = shp_layer.GetFeature(feature_num)
            shp_geometry = shp_feature.GetGeometryRef()
            points = shp_geometry.GetGeometryRef(0)
            
            lon = []
            lat = []
            for i in xrange(points.GetPointCount()):
                lon.append(points.GetX(i))
                lat.append(points.GetY(i))
                
            longitudes.append(lon)
            latitudes.append(lat)
            
            if 'Tile' in field_names:
                tiles.append(str(shp_feature.GetField("Tile")))
            
    longitudes_all.append(longitudes)
    latitudes_all.append(latitudes)   

    longitudes_all = np.array(longitudes_all)        
    latitudes_all = np.array(latitudes_all)
        
    tiles_all.append(tiles)        
    
    return longitudes_all, latitudes_all, tiles_all

def get_lonlat(shapefile):
    """   
    Get the longitudes and latitudes of a shapefile.  Shapefile should be in a
    Geographic Coordinate System (longitude and latitude coordinates) such as 
    World WGS84.
    
    *Parameters*:
        shapefile : osgeo.ogr.DataSource 

    *Return*:
        longitudes_all : multi-dimensional array of all longitudes in shapefile
        latitudes_all : multi-dimensional array of all latitudes in shapefile
        
    """   
    longitudes_all = []
    latitudes_all = []
    num_layers = shapefile.GetLayerCount()
    for layer_num in range(num_layers) :
        shp_layer = shapefile.GetLayer(layer_num)
        spatial_ref = shp_layer.GetSpatialRef().ExportToProj4()
        num_features = shp_layer.GetFeatureCount()
        
        layer_def = shp_layer.GetLayerDefn()
        field_names = []
        for i in range(layer_def.GetFieldCount()):
            field_names.append(layer_def.GetFieldDefn(i).GetName())
        
        longitudes = []
        latitudes = []
        for feature_num in range(num_features):
            shp_feature = shp_layer.GetFeature(feature_num)
            shp_geometry = shp_feature.GetGeometryRef()
            points = shp_geometry.GetGeometryRef(0)
            
            lon = []
            lat = []
            for i in xrange(points.GetPointCount()):
                lon.append(points.GetX(i))
                lat.append(points.GetY(i))
                
            longitudes.append(lon)
            latitudes.append(lat)
            
    longitudes_all.append(longitudes)
    latitudes_all.append(latitudes)   

    longitudes_all = np.array(longitudes_all)        
    latitudes_all = np.array(latitudes_all)
    
    return longitudes_all, latitudes_all

def get_mapcoords(shapefile_list):
    """   
    Get max and min extent coordinates from a list of shapefiles to use as the 
    extents on the map. Use the map extents to calculate the map center and the 
    standard parallels.
    
    *Parameters*:
        shapefile_list : list of shapefile_data dictionaries 

    
        shapefile_data : dictionary containing general information about shapefile
            
            shapefile_data = {'shapefile': osgeo.ogr.DataSource,
                              'type': string of geometry type (POLYGON, POINT, etc.),
                              'path': string path including name of shapefile,
                              'name': string name of shapefile
                              'fields': list containing fields contained in shapefile,
                              'spatialref': string of shapefile's spatial reference,
                              'extents': tuple of shapefile extents}
                              
    *Return*:
        extent_coords : dictionary containing 'lon_min', 'lon_max', 'lat_max', 'lat_min' keys with respective calculated values
        center_coords : dictionary containing 'lon', 'lat' keys with respective calculated values
        standard_parallels : dictionary containing 'first', 'second' keys with respective calculated values (first = min(lat), second = max(lat))
    
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
    
def get_shapefiledata(shapefile):
    """   
    Get general shapefile information and shapefile data source into a dictionary.
    
    *Parameters*:
        shapefile : osgeo.ogr.DataSource 

    *Return*:
        shapefile_data : dictionary containing general information about shapefile
            
            shapefile_data = {'shapefile': osgeo.ogr.DataSource,
                              'type': string of geometry type (POLYGON, POINT, etc.),
                              'path': string path including name of shapefile,
                              'name': string name of shapefile
                              'fields': list containing fields contained in shapefile,
                              'spatialref': string of shapefile's spatial reference,
                              'extents': tuple of shapefile extents}
    
    """ 
    shapefile_name = shapefile.GetName().split('/')[-1]
    shapefile_path = shapefile.GetName().split('.')[0]
    shapefile_layer = shapefile.GetLayer()
    shapefile_spatialref = shapefile_layer.GetSpatialRef().ExportToProj4()
    shapefile_extents = shapefile_layer.GetExtent()
    shapefile_feature = shapefile_layer.GetFeature(0)
    shapefile_geometry = shapefile_feature.geometry()
    shapefile_type = shapefile_geometry.GetGeometryName()
    
    shapefile_fields = []
    shapefile_layerdef = shapefile_layer.GetLayerDefn()
    for i in range(shapefile_layerdef.GetFieldCount()):
        shapefile_fields.append(shapefile_layerdef.GetFieldDefn(i).GetName())        
        
    shapefile_data = {'shapefile': shapefile,
                      'type': shapefile_type,
                      'path': shapefile_path,
                      'name': shapefile_name,
                      'fields': shapefile_fields,
                      'spatialref': shapefile_spatialref,
                      'extents': shapefile_extents}
                      
    return shapefile_data

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
    
    extent_coords, center_coords, standard_parallels = get_mapcoords(shapefile_list)    
    
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

def set_displaycolormarker(shapefile_data, display_color = 'g', display_marker = 'o'):
    """   
    Set a color and marker to display in the shapefile_data dictionary.

        shapefile_data = {'shapefile': osgeo.ogr.DataSource,
                          'type': string of geometry type (POLYGON, POINT, etc.),
                          'path': string path including name of shapefile,
                          'name': string name of shapefile
                          'fields': list containing fields contained in shapefile}    
    
    *Parameters*:
        shapefile_data : dictionary containing general information about shapefile
        display_color : string of color used to display point, line, or polygon shapefiles on map plot
        display_marker : string of marker used to display point shapefiles on map plot
            
    *Return*:
        shapefile_info : dictionary containing general information about shapefile with added 'display_field' key and value

    """ 
    shapefile_data['display_color'] = display_color
    shapefile_data['display_marker'] = display_marker    
    
    return shapefile_data    
    
def set_displayfield(shapefile_data, display_field = None):
    """   
    Set a field to display in the shapefile_data dictionary.

        shapefile_data = {'shapefile': osgeo.ogr.DataSource,
                          'type': string of geometry type (POLYGON, POINT, etc.),
                          'path': string path including name of shapefile,
                          'name': string name of shapefile
                          'fields': list containing fields contained in shapefile}    
    
    *Parameters*:
        shapefile_data : dictionary containing general information about shapefile
        display_field : string of which field to display on map plot
            
    *Return*:
        shapefile_info : dictionary containing general information about shapefile with added 'display_field' key and value

    """ 
    if display_field in shapefile_data['fields']:
        shapefile_data['display_field'] = display_field
    else:
        shapefile_data['display_field'] = None
        print 'Field %s is not available in shapefile %s' % (display_field, shapefile_data['name'])
        print 'The following fields are in shapfile %s: ' % (shapefile_data['name'])
        print shapefile_data['fields']
        
    return shapefile_data

def main_printtiles():
    """
    Run as a script. Prompt user for global climate model shapefile and the 
    basin of interest shapefile.  Get and print the tiles associated with the 
    global climate model shapefile which are intersected by the basin shapefile.
    
    """ 
    
    # open a file dialog to get file     
    root = Tkinter.Tk() 
    file_format = [('Shapefile','*.shp')]  
    gcm_file = tkFileDialog.askopenfilename(title = 'Select a global climate model shapefile', filetypes = file_format)
    root.destroy()
    
    root = Tkinter.Tk() 
    file_format = [('Shapefile','*.shp')]  
    basin_file = tkFileDialog.askopenfilename(title = 'Select basin shapefile', filetypes = file_format)
    root.destroy()
    
    if gcm_file and basin_file:
        
        try:
            gcm_shapefile = osgeo.ogr.Open(gcm_file)
            basin_shapefile = osgeo.ogr.Open(basin_file)
    
            tiles = get_intersectedtiles(gcm_shapefile, basin_shapefile)    
            
            basin_shapefile.Destroy()
            gcm_shapefile.Destroy()
            
            print tiles
            
        except IOError as error:
            print 'Cannot read file!' + error.filename
            print error.message
            
        except IndexError as error:
            print 'Cannot read file! Bad file!'
            print error.message
            
        except ValueError as error:
            print error.message
                
    else:
        print '** Canceled **'


def main_plotshapefiles():
    """
    Run as a script. Prompt user for global climate model shapefile and the 
    basin of interest shapefile.  Get and print the tiles associated with the 
    global climate model shapefile which are intersected by the basin shapefile.
    
    """ 
    
    root = Tkinter.Tk() 
    file_format = [('Shapefile','*.shp')]  
    shp_files = tkFileDialog.askopenfilenames(title = 'Select a global climate model shapefiles', filetypes = file_format)
    shp_files = shp_files.split()
    root.destroy()
    
    display_field = 'Tile'
    colors_list = ['g', 'b', 'r', 'y', 'c', 'm', 'orange', 'k']
    colors_index = 0
    shapefile_list = []
    if shp_files:
        
        try:
            for shp_file in shp_files:
                shapefile = osgeo.ogr.Open(shp_file)
                shapefile_data = get_shapefiledata(shapefile = shapefile) 
                shapefile_data = set_displayfield(shapefile_data = shapefile_data, display_field = display_field)
                
                if colors_index > len(colors_list) - 1:
                    color = np.random.rand(3,)
                else:
                    color = colors_list[colors_index]

                shapefile_data = set_displaycolormarker(shapefile_data = shapefile_data, display_color = color)

                colors_index += 1                
                
                shapefile_list.append(shapefile_data)
            
            plot_map(shapefile_list, title_str = 'Global Climate Model') 
            

        except IOError as error:
            print 'Cannot read file!' + error.filename
            print error.message
            
        except IndexError as error:
            print 'Cannot read file! Bad file!'
            print error.message
            
        except ValueError as error:
            print error.message
                
    else:
        print '** Canceled **'

if __name__ == "__main__":
    
    # main scripts
    main_printtiles()
    #main_plotshapefiles()






