"""
Purpose: File of variables required to apply global climate delta factors to a WATER 
         simulation batch run.

Variables                       Meaning
---------                       -------
         
waterbatch_directory        -   path to a WATER batch run directory
basin_shapefile             -   path to the basin shapefile used in the WATER batch run
basin_field                 -   unique field in the basin shapefile used in the WATER batch run that names the batch run directories; e.g. STAID
subwaterdeltas_file         -   path to substitute water deltas file; used when basins in the basin shapefile do not intersect with climate gcm shapefiles
delta_files                 -   list of paths to delta files to use
delta_shapefile             -   path to the water use centroids shapefile

Note: If copying and pasting paths on Windows machines:
        1. Change '\' to '/' in each path variable, or
        2. Place an 'r' in front of the path string variable; e.g. r"C:\Users\your-user-name\...\"

"""

waterbatch_directory = "../data/water-batch-run-datafiles/sample-batch-run-output/"
basin_shapefile = waterbatch_directory + "Watersheds.shp"
basin_field = "STAID"
subwaterdeltas_file = waterbatch_directory + "/waterapputils_non_intersecting_basin_centroids.txt"
delta_files = ["../data/deltas-gcm/CanES/RCP45/2030/Ppt.txt",
               "../data/deltas-gcm/CanES/RCP45/2030/Tmax.txt"]                
delta_shapefile = "../data/spatial-datafiles/gcm-tiles/CanES.shp"






 



