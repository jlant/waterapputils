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
import helpers

def create_output_dir(settings):
    """    
    Create the output directories and files needed to processes wateruse.

    Parameters
    ----------
    settings : dictionary
        Dictionary of user settings

    Returns
    -------
    map_dir : string
        string path to map directory

    Notes
    -----
    Uses settings set in user_settings.py 
    """   
    # create output directories   
    map_dir = helpers.make_directory(path = settings["simulation_directory"], directory_name = settings["map_directory_name"])    
    
    # print input and output information
    helpers.print_input_output_info( 
        input_dict = {"simulation_directory": settings["simulation_directory"],
                      "map_directory_name": settings["map_directory_name"],
        },
        output_dict = {" map_dir": map_dir}
    )

    return map_dir


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


def create_map(files_list, settings, title = None, is_visible = False, save_path = None, save_name = "map.png", shp_name = None, map_buffer = 1.0):
	"""
	Create a map use matplotlib's basemap using a list of shapefiles.

    Parameters
    ----------
    files_list : list
    	List of shapefiles to create a map with
    settings : dictionary
        Dictionary of user settings
    title : string
    	String title for map
    is_visible : bool
    	Boolean to show map
    save_path : string
    	String path to save map
    save_name : string
    	String name to save plot
    shp_name : string
    	String name of shapefile in the files_list to base the map extents from; if None, then maximum extents of all shapefiles in files_list are used
    map_buffer : float
    	Float value used to create a buffer around the map extents; units are in coordinate degrees
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


def create_simulation_map(settings):
	"""
	Create an overview and zoomed in map for a WATER simulation using 
	settings in user_settings.py.

    Parameters
    ----------
    settings : dictionary
        Dictionary of user settings
	"""

	map_dir = create_output_dir(settings)

	files_list_overview = [
		settings["water_shapefiles"]["drbbasin"]["path"],									# path to drb basin
		os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"]),	# path to basin shapefile for a simulation
	]

	files_list_zoomed = [
		settings["water_shapefiles"]["drbbasin"]["path"],									# path to drb basin
		os.path.join(settings["simulation_directory"], settings["basin_shapefile_name"]),	# path to basin shapefile for a simulation
		settings["water_shapefiles"]["strm"]["path"],									    # path to streams shapefile
		settings["water_shapefiles"]["rsvr"]["path"],									    # path to reservoir shapefile
		settings["water_shapefiles"]["usgsgages"]["path"],								    # path to usgs gages shapefile
	]

	shp_info_list_overview, display_fields_overview, colors_overview = get_shps_colors_fields(files_list = files_list_overview, settings = settings)
	shp_info_list_zoomed, display_fields_zoomed, colors_zoomed = get_shps_colors_fields(files_list = files_list_zoomed, settings = settings)
	
	# do not display the field for settings["basin_shapefile_name"] for the overview map
	display_fields_overview[1] = ""

	# plot overview map
	spatialdata_viewer.plot_shapefiles_map(
		shapefiles = shp_info_list_overview, 
		display_fields = display_fields_overview, 
		colors = colors_overview, 
		title = settings["map_title_overview"], 
		is_visible = False, 
		save_path = map_dir, 
		save_name = settings["map_name_overview"], 
		shp_name = None, 
		buff = settings["map_buffer_overview"],
	)

	# plot zoomed map
	spatialdata_viewer.plot_shapefiles_map(
		shapefiles = shp_info_list_zoomed, 
		display_fields = display_fields_zoomed, 
		colors = colors_zoomed, 
		title = settings["map_title_zoomed"], 
		is_visible = False, 
		save_path = map_dir, 
		save_name = settings["map_name_zoomed"], 
		shp_name = os.path.splitext(settings["basin_shapefile_name"])[0], 
		buff = settings["map_buffer_zoomed"],
	)

