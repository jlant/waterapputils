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


water_database_shapefiles = ["usgsgages", "cnty", "climbasins", "strm", "rsvr"]

water_shapefiles = {
	"Watersheds" : {"field": "STAID", 
			        "color": "lightgreen",
	},

	"usgsgages" : {"field": "gage", 
				   "color": "k",
	},

	"cnty" : {"field": "COUNTY", 
			  "color": "lightcoral",
	},

}

def create_map(files_list, settings):
	"""

	"""
	# reproject all shapefiles
	shp_reproj_list = spatialvectors.reproject(shapefiles = files_list)

	# plot all shapefiles
	if shp_reproj_list:
	    shp_info_list = []
	    display_fields = []
	    colors = []
	    for shapefile in shp_reproj_list:
	        shp = osgeo.ogr.Open(shapefile)    

	        shp_info = spatialvectors.fill_shapefile_dict(shapefile = shp)
	        shp_info_list.append(shp_info)

	        for key, values in water_shapefiles.iteritems():

		        if key in shp_info["name"].split("_")[0]:
		        	display_fields.append(values["field"])
		        	colors.append(values["color"])

	    spatialdata_viewer.plot_shapefiles_map(shapefiles = shp_info_list, display_fields = display_fields, colors = colors, title = "A map!", is_visible = True, save_path = None, shp_idx = None)

