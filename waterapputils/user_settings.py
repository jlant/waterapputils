"""
Purpose: File of variables required to apply water use to a WATER 
         simulation batch run.

Variables                       Meaning
---------                       -------
         
waterbatch_directory        -   path to a WATER batch run directory
basin_shapefile             -   path to the basin shapefile used in the WATER batch run
basin_field                 -   unique field in the basin shapefile used in the WATER batch run that names the batch run directories; e.g. STAID
subwateruse_file            -   path to substitute water use file; used when basins in the basin shapefile do not intersect with water use centroids
wateruse_files              -   list of paths to water use files to use
wateruse_factor_file        -   path to the water use factor file
basin_centroids_shapefile   -   path to the water use centroids shapefile

Note: If copying and pasting paths on Windows machines:
        1. Change '\' to '/' in each path variable, or
        2. Place an 'r' in front of the path string variable; e.g. r"C:\Users\your-user-name\...\"

"""

# ------------------- WATER simulation information ---------------------- #

# batch simulation
# simulation_directory = "../data/sample-water-simulations/sample-batch-simulation"
# is_batch_simulation = True
# basin_shapefile_name = "Watersheds.shp"
# basin_shapefile_id_field = "STAID"
# basin_shapefile_area_field = "da_sqmi"

# single simulation
simulation_directory = "../data/sample-water-simulations/sample-single-simulation"
is_batch_simulation = False
basin_shapefile_name = "basinMask.shp"
basin_shapefile_id_field = "FID"
basin_shapefile_area_field = ""

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
ecoflow_drainage_area_file_name = "drainagearea.csv"

oasis_directory_name = "waterapputils-oasis"
oasis_file_name = "oasis.txt"


# ------------------ Container for waterapputils.py----------------------- #
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
	"ecoflow_drainage_area_file_name": ecoflow_drainage_area_file_name,
    
	"oasis_directory_name": oasis_directory_name,
	"oasis_file_name": oasis_file_name,
}