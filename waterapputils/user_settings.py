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

# simulation information
simulation_directory = "../data/sample-water-simulations/sample-batch-simulation"
is_batch_simulation = True
basin_shapefile_name = "Watersheds.shp"
basin_shapefile_id_field = "STAID"
basin_shapefile_area_field = "da_sqmi"

# default names from WATER application
water_text_file_name = "WATER.txt"
water_database_file_name = "WATERSimulation.xml"

# ------------------- Water use information ----------------------------- #
wateruse_centroids_shapefile = "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp"
wateruse_centroids_shapefile_id_field = "newhydroid"
wateruse_files = [
	"../data/wateruse-datafiles/010203-JFM-sample.txt", 
    "../data/wateruse-datafiles/040506-AMJ-sample.txt", 
    "../data/wateruse-datafiles/070809-JAS-sample.txt", 
    "../data/wateruse-datafiles/101112-OND-sample.txt"
] 
wateruse_factor_file = "../data/wateruse-datafiles/wateruse-factors-sample.txt"

# ------------------- Output directory and file names ------------------- #
info_directory_name = "waterapputils-info"

watertxt_directory_name = "waterapputils-watertxt"
waterxml_directory_name = "waterapputils-waterxml"

wateruse_prepend_name = "WATERUSE"
wateruse_directory_name = "waterapputils-wateruse"
wateruse_info_file_name = "wateruse_info.txt"
wateruse_non_intersecting_file_name = "wateruse_non_intersecting_centroids.txt"
sub_wateruse_info_file_name = "sub_wateruse_info.txt"

gcm_delta_prepend_name = "GCMDELTA"
gcm_delta_directory_name = "waterapputils-gcmdelta"
gcm_delta_info_file_name = "gcm_delta_info.txt"
gcm_delta_non_intersecting_file_name = "gcm_delta_non_intersecting_tiles.txt"
sub_gcm_delta_info_file_name = "sub_gcm_delta_info.txt"

ecoflow_directory_name = "waterapputils-ecoflow"
ecoflow_file_name = ""
ecoflow_drainage_area_file_name = "drainagearea.csv"

oasis_directory_name = "waterapputils-oasis"
oasis_file_name = "oasis.txt"


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

	"ecoflow_directory_name": ecoflow_directory_name,
    "ecoflow_file_name": ecoflow_file_name,
	"ecoflow_drainage_area_file_name": ecoflow_drainage_area_file_name,
    
	"oasis_directory_name": oasis_directory_name,
	"oasis_file_name": oasis_file_name,
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

    "info_directory_name": "waterapputils-info",

    "watertxt_directory_name": "waterapputils-watertxt",
    "waterxml_directory_name": "waterapputils-waterxml",

    "wateruse_prepend_name": "WATERUSE",
    "wateruse_directory_name": "waterapputils-wateruse",
    "wateruse_info_file_name": "wateruse_info.txt",
    "wateruse_non_intersecting_file_name": "wateruse_non_intersecting_centroids.txt",
    "sub_wateruse_info_file_name": "sub_wateruse_info.txt",
    
    "gcm_delta_prepend_name": "GCMDELTA",
    "gcm_delta_directory_name": "waterapputils-gcmdelta",
    "gcm_delta_info_file_name": "gcm_delta_info.txt",
    "gcm_delta_non_intersecting_file_name": "gcm_delta_non_intersecting_tiles.txt",
    "sub_gcm_delta_info_file_name": "sub_gcm_delta_info.txt",

    "ecoflow_directory_name": "waterapputils-ecoflow",
    "ecoflow_file_name": "",
    "ecoflow_drainage_area_file_name": "drainagearea.csv",
    
    "oasis_directory_name": "waterapputils-oasis",
    "oasis_file_name": "oasis.txt",
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

    "info_directory_name": "waterapputils-info",

    "watertxt_directory_name": "waterapputils-watertxt",
    "waterxml_directory_name": "waterapputils-waterxml",

    "wateruse_prepend_name": "WATERUSE",
    "wateruse_directory_name": "waterapputils-wateruse",
    "wateruse_info_file_name": "wateruse_info.txt",
    "wateruse_non_intersecting_file_name": "wateruse_non_intersecting_centroids.txt",
    "sub_wateruse_info_file_name": "sub_wateruse_info.txt",
    
    "gcm_delta_prepend_name": "GCMDELTA",
    "gcm_delta_directory_name": "waterapputils-gcmdelta",
    "gcm_delta_info_file_name": "gcm_delta_info.txt",
    "gcm_delta_non_intersecting_file_name": "gcm_delta_non_intersecting_tiles.txt",
    "sub_gcm_delta_info_file_name": "sub_gcm_delta_info.txt",

    "ecoflow_directory_name": "waterapputils-ecoflow",
    "ecoflow_file_name": "",
    "ecoflow_drainage_area_file_name": "drainagearea.csv",
    
    "oasis_directory_name": "waterapputils-oasis",
    "oasis_file_name": "oasis.txt",
}
