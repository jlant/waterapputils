# Purpose: Simple file to hold the variables required for a water use batch run.

################ EDIT BELOW #######################
# path to WATER batch run directory
waterbatch_directory = "../data/wateruse-batch-run/Batch01440400/"

# path to the basin shapefile used in the WATER batch run
basin_shapefile = "../data/wateruse-batch-run/Batch01440400/Watersheds.shp"

# path to output directory that will contain all the output (updated WATER*.txt files containing water use data, along with plots of updated WATER*.txt file)
output_directory = "../data/wateruse-batch-run/Batch01440400/output"


######### DO NOT NEED TO EDIT BELOW UNLESS YOU MOVE THESE FILES #######
# list of paths to water use files to use
wateruse_files = ["../data/wateruse-datafiles/S1_JFM_WU_2014jul7.txt", 
                  "../data/wateruse-datafiles/S2_AMJ_WU_2014jul7.txt", 
                  "../data/wateruse-datafiles/S3_JAS_WU_2014jul7.txt", 
                  "../data/wateruse-datafiles/S4_OND_WU_2014jul7.txt"]  

# path to the water use factor file                 
wateruse_factor_file =  "../data/wateruse-datafiles/wateruse_factors.txt"

# path to the basin centroids shapefile
basin_centroids_shapefile = "../data/spatial-datafiles/basins/dem_basin_centroids.shp"

# field in the basin shapefile used in the WATER batch run to link to water use files
basin_field = "Id"

 
  


