# Purpose: Simple file to hold the variables required for a water global climate delta batch run.

################ EDIT BELOW #######################
# path to global climate delta files
delta_files = ["../data/deltas-gcm/CanES/RCP45/2030/Ppt.txt",
               "../data/deltas-gcm/CanES/RCP45/2030/Tmax.txt"]
            
# path to shapefile associated with climate model
delta_shapefile = "../data/spatial-datafiles/gcm-tiles/CanES.shp"

# path to the basin shapefile used in the WATER batch run
basin_shapefile = "../data/wateruse-batch-run/Batch01440400/Watersheds.shp"

# field in the basin shapefile used in the WATER batch run to link to water use files
basin_field = "Id"

# path to WATER batch run directory
waterbatch_directory = "../data/wateruse-batch-run/Batch01440400/"



 



