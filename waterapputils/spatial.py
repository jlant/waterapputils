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

def get_tiles(gcm_shapefile, basin_shapefile):
    """   
    Get the tiles associated with the global climate model shapefile (gcm_shp)
    which are intersected by the basin shapefile.
    
    *Parameters*:
        gcm_shapefile : osgeo.ogr.DataSource 
        basin_shapefile : osgeo.ogr.DataSource 

    *Return*:
        tiles : list of string tile numbers
        
    """    
    gcm_layer = gcm_shapefile.GetLayer(0)

    basin_layer = basin_shapefile.GetLayer(0)
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

def get_lonlat(shapefile):
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
    '''
    shp_layer = shapefile.GetLayer(0)
    spatial_ref = shp_layer.GetSpatialRef()
    shp_projection = spatial_ref.GetAttrValue('PROJECTION') 
    
    shp_feature = shp_layer.GetFeature(0)
    shp_geometry = shp_feature.GetGeometryRef()
    points = shp_geometry.GetGeometryRef(0)
    
    lon = []
    lat = []
    for i in xrange(points.GetPointCount()):
        lon.append(points.GetX(i))
        lat.append(points.GetY(i))
    
    lon = np.array(lon)
    lat = np.array(lat)
    '''
    
    return longitudes_all, latitudes_all, tiles_all

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
    
            tiles = get_tiles(gcm_shapefile, basin_shapefile)    
            
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
            
            gcm_lon, gcm_lat, gcm_tiles = get_lonlat(shapefile = gcm_shapefile)
            basin_lon, basin_lat, test = get_lonlat(shapefile = basin_shapefile)
            
            plt.figure(figsize = (12,10))
            
            buff = 10
            m = Basemap(projection = 'aea', llcrnrlon = np.min(gcm_lon) - buff, llcrnrlat = np.min(gcm_lat) - buff, 
                        urcrnrlon = np.max(gcm_lon) + buff, urcrnrlat = np.max(gcm_lat) + buff, 
                        lat_1 = np.mean(gcm_lat) - buff, lat_2 = np.mean(gcm_lat) + buff,
                        lon_0 = -65, resolution = 'h', area_thresh = 10000)    

            m.drawcoastlines()
            m.drawcountries()
            m.drawrivers(linewidth = 1, color = 'blue')
            m.drawstates()
            m.drawmapboundary(fill_color = 'aqua')
            m.fillcontinents(color = 'coral', lake_color = 'aqua')
            m.drawparallels(np.arange(-80., 81., 10.), labels = [1, 0, 0, 0])
            m.drawmeridians(np.arange(-180., 181., 10.), labels = [0, 0, 0, 1])

            for k in range(gcm_lon.shape[0]):
                for i in range(gcm_lon[k].shape[0]):
                    gcm_x, gcm_y = m(gcm_lon[k][i], gcm_lat[k][i])
                    m.plot(gcm_x, gcm_y, linewidth = 2, color = 'g')
                    gcm_xy = zip(gcm_x, gcm_y)       
                    gcm_poly = mpl.patches.Polygon(gcm_xy, facecolor = 'g', alpha = 0.5)            
                    plt.gca().add_patch(gcm_poly)
                    plt.text(np.mean(gcm_x), np.mean(gcm_y), gcm_tiles[k][i], color = 'k', fontsize = 12, fontweight = 'bold')
             
            for k in range(basin_lon.shape[0]):
                for i in range(basin_lon[k].shape[0]):
                    basin_x, basin_y = m(basin_lon[k][i], basin_lat[k][i])
                    m.plot(basin_x, basin_y, linewidth = 2, color = 'r')
                    basin_xy = zip(basin_x, basin_y)       
                    basin_poly = mpl.patches.Polygon(basin_xy, facecolor = 'r', alpha = 0.5)            
                    plt.gca().add_patch(basin_poly) 

            
            basin_dirname, basin_filename = os.path.split(os.path.abspath(basin_file))
            basin_path = '/'.join([basin_dirname, basin_filename.split('.')[0]])
            basin_path = str(basin_path)

            gcm_dirname, gcm_filename = os.path.split(os.path.abspath(gcm_file))
            gcm_filename = str(gcm_filename.split('.')[0])
            gcm_path = '/'.join([gcm_dirname, gcm_filename])
            gcm_path = str(basin_path)            
            
            '''
            s = m.readshapefile(basin_path, 'basin', drawbounds = False)
            for shape in m.basin:
                xx, yy = zip(*shape)
                m.plot(xx, yy, linewidth = 2, color = 'r')
            '''
            plt.title('Global Climate Model: ' + gcm_filename)
            plt.show()


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
    #main_printtiles()
    main_plotshapefiles()






