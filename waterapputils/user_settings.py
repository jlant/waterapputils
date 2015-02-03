"""
:Module: waterapputils.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: User settings for waterapputils.py

Note: If copying and pasting paths on Windows machines:
        1. Change '\' to '/' in each path variable
        or
        2. Place an 'r' in front of the path string variable; e.g. r"C:\Users\your-user-name\...\"

"""

# ------------------- WATER simulation information ---------------------- #
simulation_directory = "../data/sample-water-simulations/sample-batch-simulation"
is_batch_simulation = True
basin_shapefile_name = "Watersheds.shp"
basin_shapefile_id_field = "STAID"
basin_shapefile_area_field = "da_sqmi"                  # if no area field, leave blank like this: ""

# ------------------- Water use information ----------------------------- #
wateruse_centroids_shapefile = "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp"
wateruse_centroids_shapefile_id_field = "newhydroid"

wateruse_files = [
        "../data/wateruse-datafiles/010203-JFM-sample.txt", 
        "../data/wateruse-datafiles/040506-AMJ-sample.txt", 
        "../data/wateruse-datafiles/070809-JAS-sample.txt", 
        "../data/wateruse-datafiles/101112-OND-sample.txt",
]

wateruse_factor_file = "../data/wateruse-datafiles/wateruse-factors-sample.txt"

# ------------------- Global Climate Model information ------------------ #
gcm_delta_files = ["../data/deltas-gcm/Ppt.txt",
                   "../data/deltas-gcm/Tmax.txt",
                   "../data/deltas-gcm/PET.txt",
]                

gcm_delta_tile_shapefile = "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp"
gcm_delta_tile_shapefile_id_field = "Tile"

# ------------------- Output directory and file names ------------------- #
water_text_file_name = "WATER.txt"
water_database_file_name = "WATERSimulation.xml"

info_directory_name = "waterapputils-info"

watertxt_directory_name = "waterapputils-watertxt"
waterxml_directory_name = "waterapputils-waterxml"

wateruse_prepend_name = "WATERUSE-"
wateruse_directory_name = "waterapputils-wateruse"
wateruse_info_file_name = "wateruse_info.txt"
wateruse_non_intersecting_file_name = "wateruse_non_intersecting_centroids.txt"
sub_wateruse_info_file_name = "sub_wateruse_info.txt"

gcm_delta_prepend_name = ""
gcm_delta_directory_name = "waterapputils-gcmdelta"
gcm_delta_info_file_name = "gcm_delta_info.txt"
gcm_delta_non_intersecting_file_name = "gcm_delta_non_intersecting_tiles.txt"
sub_gcm_delta_info_file_name = "sub_gcm_delta_info.txt"
pet_timeseries_file_name = "pet-timeseries.txt"

ecoflow_directory_name = "waterapputils-ecoflow"
ecoflow_file_name = ""
ecoflow_drainage_area_file_name = "drainagearea.csv"
ecoflow_parameter_name = "Discharge + Water Use"

oasis_directory_name = "waterapputils-oasis"
oasis_file_name = "oasis.txt"


# -------------------- WATER shapefiles and Map Info -------------------- #
map_directory_name = "waterapputils-maps"

map_buffer_overview = 1.0
map_buffer_zoomed = 0.25

map_name_overview = "map-overview.png"
map_name_zoomed = "map-zoomed.png"

map_title_overview = "Overview map"
map_title_zoomed = "Closer look map"

map_colors_list = ["b", "r", "y", "r", "c", "y", "m", "orange", "aqua", "darksalmon", "gold", "k"]

water_shapefiles = {

    # outline of delaware river basin
    "drbbasin" : {"field": "", 
                  "color": "lightcoral",
                  "path" : "../data/spatial-datafiles/basins/drbbasin_nad83.shp",
    },

    # WATER batch simulation basin(s) shapefile
    "Watersheds" : {"field": basin_shapefile_id_field, 
                    "color": "green",
                    "path": "",
    },

    # WATER single simulation basin shapefile
    "basinMask" : {"field": "", 
                   "color": "green",
                   "path": "",
    },

    # WATER sample single simulation basin shapefile
    "basin0" : {"field": "", 
                "color": "green",
                "path": "../data/sample-water-simulations/sample-datafiles/basin0.shp",
    },

    # Water use centroids
    "wateruse" : {"field": "", 
                  "color": "aqua",
                  "path" : "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_nad83.shp"
    },

    # GCM tiles
    "CanES" : {"field": "Tile", 
               "color": "lightgreen",
               "path": "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp",
    },

    "GFDL" : {"field": "Tile", 
              "color": "lightgreen",
              "path": "../data/spatial-datafiles/gcm-tiles/GFDL_nad83.shp",
    },

    "GISS" : {"field": "Tile", 
              "color": "lightgreen",
              "path": "../data/spatial-datafiles/gcm-tiles/GISS_nad83.shp",
    },

    "NCAR" : {"field": "Tile", 
              "color": "lightgreen",
              "path": "../data/spatial-datafiles/gcm-tiles/NCAR_nad83.shp",
    },

    # WATER database shapefiles 
    "usgsgages" : {"field": "", 
                   "color": "k",
                   "path": "../data/spatial-datafiles/misc/usgsgages.shp",
    },

    "strm" : {"field": "", 
              "color": "blue",
              "path": "../data/spatial-datafiles/misc/strm.shp",
    },

    "rsvr" : {"field": "", 
              "color": "royalblue",
              "path": "../data/spatial-datafiles/misc/rsvr.shp",
    },
}


# ------------------ Containers for waterapputils.py----------------------- #
settings = {
    "simulation_directory": simulation_directory,
    "is_batch_simulation": is_batch_simulation,
    "basin_shapefile_name": basin_shapefile_name,
    "basin_shapefile_id_field": basin_shapefile_id_field,
    "basin_shapefile_area_field": basin_shapefile_area_field,
	"water_text_file_name": water_text_file_name,
	"water_database_file_name": water_database_file_name,

    "wateruse_centroids_shapefile": wateruse_centroids_shapefile,
    "wateruse_centroids_shapefile_id_field": wateruse_centroids_shapefile_id_field,
    "wateruse_files": wateruse_files,
    "wateruse_factor_file": wateruse_factor_file,

    "gcm_delta_files": gcm_delta_files,
    "gcm_delta_tile_shapefile": gcm_delta_tile_shapefile,
    "gcm_delta_tile_shapefile_id_field": gcm_delta_tile_shapefile_id_field,

    "info_directory_name": info_directory_name,

    "watertxt_directory_name": watertxt_directory_name,
    "waterxml_directory_name": waterxml_directory_name,

    "wateruse_prepend_name": wateruse_prepend_name,
    "wateruse_directory_name": wateruse_directory_name,
    "wateruse_info_file_name": wateruse_info_file_name,
	"wateruse_non_intersecting_file_name": wateruse_non_intersecting_file_name,
	"sub_wateruse_info_file_name": sub_wateruse_info_file_name,
    
    "gcm_delta_prepend_name": gcm_delta_prepend_name,
    "gcm_delta_directory_name": gcm_delta_directory_name,
    "gcm_delta_info_file_name": gcm_delta_info_file_name,
    "gcm_delta_non_intersecting_file_name": gcm_delta_non_intersecting_file_name,
    "sub_gcm_delta_info_file_name": sub_gcm_delta_info_file_name,
    "pet_timeseries_file_name": pet_timeseries_file_name,

	"ecoflow_directory_name": ecoflow_directory_name,
    "ecoflow_file_name": ecoflow_file_name,
	"ecoflow_drainage_area_file_name": ecoflow_drainage_area_file_name,
    "ecoflow_parameter_name": ecoflow_parameter_name,
    
	"oasis_directory_name": oasis_directory_name,
	"oasis_file_name": oasis_file_name,

    "water_shapefiles": water_shapefiles,

    "map_buffer_overview": map_buffer_overview,
    "map_buffer_zoomed": map_buffer_zoomed,

    "map_name_overview":map_name_overview,
    "map_name_zoomed": map_name_zoomed,

    "map_title_overview": map_title_overview,
    "map_title_zoomed": map_title_zoomed,

    "map_colors_list": map_colors_list,

    "map_directory_name": map_directory_name,

}

sample_single_settings = {
    "simulation_directory": "../data/sample-water-simulations/sample-single-simulation",
    "is_batch_simulation": False,
    "basin_shapefile_name": "basinMask.shp",
    "basin_shapefile_id_field": "",
    "basin_shapefile_area_field": "",

    "water_text_file_name": "WATER.txt",
    "water_database_file_name": "WATERSimulation.xml",

    "wateruse_centroids_shapefile": "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp",
    "wateruse_centroids_shapefile_id_field": "newhydroid",
    "wateruse_files": [
        "../data/wateruse-datafiles/010203-JFM-sample.txt", 
        "../data/wateruse-datafiles/040506-AMJ-sample.txt", 
        "../data/wateruse-datafiles/070809-JAS-sample.txt", 
        "../data/wateruse-datafiles/101112-OND-sample.txt"],
    "wateruse_factor_file": "../data/wateruse-datafiles/wateruse-factors-sample.txt",

    "gcm_delta_files": ["../data/deltas-gcm/Ppt.txt", "../data/deltas-gcm/Tmax.txt", "../data/deltas-gcm/PET.txt"],
    "gcm_delta_tile_shapefile": "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp",
    "gcm_delta_tile_shapefile_id_field": "Tile",

    "info_directory_name": "waterapputils-info",

    "watertxt_directory_name": "waterapputils-watertxt",
    "waterxml_directory_name": "waterapputils-waterxml",

    "wateruse_prepend_name": "WATERUSE-",
    "wateruse_directory_name": "waterapputils-wateruse",
    "wateruse_info_file_name": "wateruse_info.txt",
    "wateruse_non_intersecting_file_name": "wateruse_non_intersecting_centroids.txt",
    "sub_wateruse_info_file_name": "sub_wateruse_info.txt",
    
    "gcm_delta_prepend_name": "GCMDELTA-",
    "gcm_delta_directory_name": "waterapputils-gcmdelta",
    "gcm_delta_info_file_name": "gcm_delta_info.txt",
    "gcm_delta_non_intersecting_file_name": "gcm_delta_non_intersecting_tiles.txt",
    "sub_gcm_delta_info_file_name": "sub_gcm_delta_info.txt",
    "pet_timeseries_file_name": "pet-timeseries.txt",

    "ecoflow_directory_name": "waterapputils-ecoflow",
    "ecoflow_file_name": "",
    "ecoflow_drainage_area_file_name": "drainagearea.csv",
    "ecoflow_parameter_name": "Discharge + Water Use",
    
    "oasis_directory_name": "waterapputils-oasis",
    "oasis_file_name": "oasis.txt",

    "water_shapefiles": water_shapefiles,

    "map_buffer_overview": map_buffer_overview,
    "map_buffer_zoomed": map_buffer_zoomed,

    "map_name_overview":map_name_overview,
    "map_name_zoomed": map_name_zoomed,

    "map_title_overview": map_title_overview,
    "map_title_zoomed": map_title_zoomed,

    "map_colors_list": map_colors_list,

    "map_directory_name": map_directory_name,
}

sample_batch_settings = {
    "simulation_directory": "../data/sample-water-simulations/sample-batch-simulation",
    "is_batch_simulation": True,
    "basin_shapefile_name": "Watersheds.shp",
    "basin_shapefile_id_field": "STAID",
    "basin_shapefile_area_field": "da_sqmi",
    "water_text_file_name": "WATER.txt",
    "water_database_file_name": "WATERSimulation.xml",

    "wateruse_centroids_shapefile": "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp",
    "wateruse_centroids_shapefile_id_field": "newhydroid",
    "wateruse_files": [
        "../data/wateruse-datafiles/010203-JFM-sample.txt", 
        "../data/wateruse-datafiles/040506-AMJ-sample.txt", 
        "../data/wateruse-datafiles/070809-JAS-sample.txt", 
        "../data/wateruse-datafiles/101112-OND-sample.txt"],
    "wateruse_factor_file": "../data/wateruse-datafiles/wateruse-factors-sample.txt",


    "gcm_delta_files": ["../data/deltas-gcm/Ppt.txt", "../data/deltas-gcm/Tmax.txt", "../data/deltas-gcm/PET.txt",],
    "gcm_delta_tile_shapefile": "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp",
    "gcm_delta_tile_shapefile_id_field": "Tile",

    "info_directory_name": "waterapputils-info",

    "watertxt_directory_name": "waterapputils-watertxt",
    "waterxml_directory_name": "waterapputils-waterxml",

    "wateruse_prepend_name": "WATERUSE-",
    "wateruse_directory_name": "waterapputils-wateruse",
    "wateruse_info_file_name": "wateruse_info.txt",
    "wateruse_non_intersecting_file_name": "wateruse_non_intersecting_centroids.txt",
    "sub_wateruse_info_file_name": "sub_wateruse_info.txt",
    
    "gcm_delta_prepend_name": "GCMDELTA-",
    "gcm_delta_directory_name": "waterapputils-gcmdelta",
    "gcm_delta_info_file_name": "gcm_delta_info.txt",
    "gcm_delta_non_intersecting_file_name": "gcm_delta_non_intersecting_tiles.txt",
    "sub_gcm_delta_info_file_name": "sub_gcm_delta_info.txt",
    "pet_timeseries_file_name": "pet-timeseries.txt",

    "ecoflow_directory_name": "waterapputils-ecoflow",
    "ecoflow_file_name": "",
    "ecoflow_drainage_area_file_name": "drainagearea.csv",
    "ecoflow_parameter_name": "Discharge + Water Use",

    "oasis_directory_name": "waterapputils-oasis",
    "oasis_file_name": "oasis.txt",

    "water_shapefiles": water_shapefiles,

    "map_buffer_overview": map_buffer_overview,
    "map_buffer_zoomed": map_buffer_zoomed,

    "map_name_overview":map_name_overview,
    "map_name_zoomed": map_name_zoomed,

    "map_title_overview": map_title_overview,
    "map_title_zoomed": map_title_zoomed,

    "map_colors_list": map_colors_list,

    "map_directory_name": map_directory_name,
}
