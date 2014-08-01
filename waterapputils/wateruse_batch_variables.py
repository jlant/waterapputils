# Purpose: Simple file to hold the variables required for a water use batch run.

# path to WATER batch run directory
waterbatch_directory = "C:/Users/jlant/jeremiah/temp/water-delaware-river-basin/2014-06-06_testbatch_clean/"

# path to output directory that will contain all the output (updated WATER*.txt files containing water use data, along with plots of updated WATER*.txt file)
output_directory = "C:/Users/jlant/jeremiah/temp/water-delaware-river-basin/2014-08-01_testing/wateruse/output/"

# list of paths to water use files to use
wateruse_files = ["../data/wateruse-datafiles/test_JFM.txt", 
                  "../data/wateruse-datafiles/test_AMJ.txt", 
                  "../data/wateruse-datafiles/test_JAS.txt", 
                  "../data/wateruse-datafiles/test_OND.txt"] 
                  
# path to the water use factor file                 
wateruse_factor_file =  "../data/wateruse-datafiles/test_wateruse_factors.txt"

# path to the basin centroids shapefile
basin_centroids_shapefile = "../data/spatial-datafiles/basins/dem_basin_centroids_proj_wgs.shp"

# path to the basin shapefile used in the WATER batch run
basin_shapefile = "../data/spatial-datafiles/basins/waterbasin_multi_clean_proj_wgs.shp"

# field in the basin shapefile used in the WATER batch run to link to water use files
basin_field = "STAID"

 
  


