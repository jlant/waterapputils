# -*- coding: utf-8 -*-
"""
:Module: spatial.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Functions to do spatial analysis on GIS datasets. 

"""

import Tkinter, tkFileDialog
import osgeo.ogr

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
#        gcm_file = osgeo.ogr.Open(r'C:\Users\jlant\jeremiah\projects\python-projects\waterapputils\data\deltas-gcm\CanES\shapefile\CanEs.shp')
#        basin_file = osgeo.ogr.Open(r'C:\Users\jlant\jeremiah\temp\testbasin.shp')
#    
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

if __name__ == "__main__":
    
    # main scripts
    main_printtiles()






