# Purpose: Simple file to hold the variables required for a water use batch run.

# path to WATER batch run directory
waterbatch_directory = r"C:\Users\jlant\jeremiah\temp\water-delaware-river-basin\2014-08-11_test_wateruse_no_intersection"

# path to the basin shapefile used in the WATER batch run
basin_shapefile = r"C:\Users\jlant\jeremiah\temp\spatial_files/waterbasin_small_couple.shp"

# field in the basin shapefile used in the WATER batch run to link to water use files
basin_field = "STAID"

# path to substitute water use file - use when basins do not intersect with centroids used for water use batch
subwateruse_file = waterbatch_directory + "/_waterapputils_non_intersecting_basin_centroids.txt"

# list of paths to water use files to use
wateruse_files = ["../data/wateruse-datafiles/S1_JFM_WU_2014jul7.txt", 
                  "../data/wateruse-datafiles/S2_AMJ_WU_2014jul7.txt", 
                  "../data/wateruse-datafiles/S3_JAS_WU_2014jul7.txt", 
                  "../data/wateruse-datafiles/S4_OND_WU_2014jul7.txt"]  

# path to the water use factor file                 
wateruse_factor_file =  "../data/wateruse-datafiles/wateruse_factors.txt"

# path to the basin centroids shapefile
basin_centroids_shapefile = r"C:\Users\jlant\jeremiah\temp\spatial_files/dem_basin_centroids_small.shp"



 
  


