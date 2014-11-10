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

waterbatch_directory = "../data/water-batch-run-datafiles/sample-batch-run-output/"
basin_shapefile = waterbatch_directory + "Watersheds.shp"
basin_field = "STAID"
subwateruse_file = waterbatch_directory + "_wateruse-batchrun-info/wateruse_non_intersecting_centroids.txt"
wateruse_files = ["../data/wateruse-datafiles/010203-JFM-sample.txt", 
                  "../data/wateruse-datafiles/040506-AMJ-sample.txt", 
                  "../data/wateruse-datafiles/070809-JAS-sample.txt", 
                  "../data/wateruse-datafiles/101112-OND-sample.txt"]                  
wateruse_factor_file =  "../data/wateruse-datafiles/wateruse-factors-sample.txt"
basin_centroids_shapefile = "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp"
