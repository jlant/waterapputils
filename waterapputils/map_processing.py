# -*- coding: utf-8 -*-
"""
:Module: map_processing.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles the processing of creating a map using basemap.
"""

__version__   = "1.0.0"
__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import os
import sys
import osgeo

# my modules
import spatialvectors
import spatialdata_viewer


def get_shps_colors_fields(files_list, settings):
	"""
	Return shapefiles, projected to WGS84 (if needed) and 
	lists of map display fields and colors corresponding to 
	each shapefile.

    Parameters
    ----------
    files_list : list
    	List of shapefiles to create a map with
    settings : dictionary
        Dictionary of user settings
	"""
	# reproject all shapefiles
	shp_reproj_list = spatialvectors.reproject(shapefiles = files_list)

	shp_info_list = []
	display_fields = []
	colors = []
	colors_index = 0
	for shapefile in shp_reproj_list:
	    shp = osgeo.ogr.Open(shapefile)    

	    shp_info = spatialvectors.fill_shapefile_dict(shapefile = shp)
	    shp_info_list.append(shp_info)

	    for key, values in settings["water_shapefiles"].iteritems():
	        if key in shp_info["name"].split("_")[0]:
	        	display_fields.append(values["field"])
	        	colors.append(values["color"])

	    if not colors:
			display_fields.append("")
			colors.append(settings["map_colors_list"][colors_index])
			colors_index += 1

	return shp_info_list, display_fields, colors

def create_map(files_list, settings, title = "A map!", is_visible = False, save_path = os.getcwd(), save_name = "map.png", shp_name = None, map_buffer = 1.0):
	"""
	Create a map use matplotlib's basemap using a list of shapefiles.

    Parameters
    ----------
    files_list : list
    	List of shapefiles to create a map with
    settings : dictionary
        Dictionary of user settings
	"""

	shp_info_list, display_fields, colors = get_shps_colors_fields(files_list, settings)

	spatialdata_viewer.plot_shapefiles_map(
		shapefiles = shp_info_list, 
		display_fields = display_fields, 
		colors = colors, 
		title = title, 
		is_visible = is_visible, 
		save_path = save_path, 
		save_name = save_name, 
		shp_name = shp_name, 
		buff = map_buffer,
	)

	# spatialdata_viewer.plot_shapefiles_map(
	# 	shapefiles = shp_info_list, 
	# 	display_fields = display_fields, 
	# 	colors = colors, 
	# 	title = settings["map_title_zoomed"], 
	# 	is_visible = False, 
	# 	save_path = os.getcwd(), 
	# 	save_name = "map.png", 
	# 	shp_name = "Watersheds", 
	# 	buff = settings["map_buffer_zoomed"],
	# )

