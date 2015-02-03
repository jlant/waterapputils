General Guide and Tutorial
==========================

Processing WATER simulation output files - WATER.txt
----------------------------------------------------

Process WATER simulation output text files (``WATER.txt``).

**-watertxt**

::

    $ python waterapputils.py -watertxt [file1] [file2] ...

Processes ``WATER.txt`` file(s) and produces plots of each parameter for
each file. Plots are saved to an output directory named as
\*waterappputils-watertxt\*. The output directory
is created in the same directory as the respective ``WATER.txt`` file.

--------------

**-watertxtfd**

::

    $ python waterapputils.py -watertxtfd

Spawns a file dialog window to select ``WATER.txt`` file(s), then
processes the ``WATER.txt`` file(s) in the same manner as the
``-watertxt`` flag.

--------------

**-watertxtcmp**

::

    $ python waterapputils.py -watertxtcmp [file1] [file2]

Produces comparison plots of each respective parameter in two
``WATER.txt`` files. Plots are saved to an output directory named as
\*waterappputils-watertxt\*. The output directory is located in the same 
directory as the ``WATER.txt`` file.

--------------

**-watertxtcmpfd**

::

    $ python waterapputils.py -watertxtcmpfd

Spawns a file dialog window to select two ``WATER.txt`` files, then
compares and processes the ``WATER.txt`` files in the same manner as
using the ``-watertxtcmp`` flag.


Processing WATER simulation database file - WATERSimulation.xml
---------------------------------------------------------------

Process WATER simulation output database files
(``WATERSimulation.xml``).

::

    $ python waterapputils.py -waterxml [file]

Processes a ``WATERSimulation.xml`` file and produces plots timeseries
parameters and topographic wetness index values. Plots are saved to an
output directory named as \*waterappputils-watertxt\*.
The output directory is created in the same directory as the
``WATERSimulation.txt`` file.

--------------

::

    $ python waterapputils.py -waterxmlfd

Spawns a file dialog window to select a ``WATERSimulation.xml`` file,
then processes the ``WATERSimulation.xml`` in the same manner as using
the ``-waterxml`` flag.

--------------

**-waterxmlcmp**

::

    $ python waterapputils.py -waterxmlcmp [file1] [file2]

Produces comparison plots of each respective parameter in two
``WATERSimulation.xml`` files. Plots are saved to an output directory
named as \*waterappputils-waterxml\*.  The output directory is located 
in the same directory as the ``WATERSimulation.xml`` file.

--------------

**-waterxmlcmpfd**

::

    $ python waterapputils.py -waterxmlcmpfd

Spawns a file dialog window to select two ``WATERSimulation.xml`` files,
then compares and processes the ``WATERSimulation.xml`` files in the
same manner as using the ``-waterxmlcmp`` flag.


Applying water use to WATER simulations
---------------------------------------

Apply water use to a WATER simulation using the settings in the ``user_settings.py`` file.

::

    $ python waterapputils.py -applywateruse


Applies water use to a WATER simulation.  Details of the WATER simulation,
*single* or *batch* simulation, are contained in the ``user_settings.py`` file.
Additional output files are created for other software programs, namely,
OASIS and ecoflow programs.

To apply water use to a WATER simulation, information regarding
the location of a series of files and directories must be entered
in a file called ``user_settings.py`` located in the 
 ``waterapputils/waterapputils/`` directory.
The following main variables associated with applying water use that
are contained in the ``user_settings.py`` file:

::

    Variables                       Meaning
    ---------                       -------
             
    simulation_directory                    -   path to a WATER simulation directory
    is_batch_simulation                     -   boolean True or False
    basin_shapefile_name                    -   name of the basin(s) shapefile created by the WATER simulation; batch simulation = "Watersheds.shp"; single simulation = "basinMask.shp"
    basin_shapefile_id_field                -   unique field in the basin(s) shapefile used in the WATER simulation; e.g. batch simulation = "STAID" or batch simulation = "waterid"; single simulation = ""
    basin_shapefile_area_field              -   field in the basin(s) shapefile that contains basin area used to create a file containing basin areas (e.g. drainagearea.csv)
    wateruse_centroids_shapefile            -   path to the water use centroids shapefile; used when finding which water use points lie within a basin
    wateruse_centroids_shapefile_id_field   -   field in the water use centroids shapefile used to link to the water use text files specified in the ``wateruse_files`` variable
    wateruse_files                          -   list of paths to water use files 
    wateruse_factor_file                    -   path to the water use factor file


Instead of specifying the path to a WATER simulation in the ``user_settings.py`` file,
users can supply the path directly on the command line using the following command:
c
::

    $ python waterapputils.py -applywateruse -simdir <path-to-water-simulation-directory>

The above command applies water use to a WATER simulation using a simulation directory path specified on the 
command line instead of using the ``simulation_directory`` variable in the ``user_settings.py`` file.

The following is an example of part of the ``user_settings.py`` file for a *batch* simulation 
using the sample datasets contained in the data directory:

::

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


The following is an example of part of the ``user_settings.py`` file for a *single* simulation using the sample datasets:

::

    # ------------------- WATER simulation information ---------------------- #
    simulation_directory = "../data/sample-water-simulations/sample-single-simulation"
    is_batch_simulation = False
    basin_shapefile_name = "basinMask.shp"
    basin_shapefile_id_field = ""
    basin_shapefile_area_field = ""                  # if no area field, leave blank like this: ""

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


The information in the ``user_settings.py`` file is used to
apply water use to each respective basin in the respective simulation. The only exception
here is when a user specifies the path to a WATER simulation on the command line which will
overwrite the ``simulation_directory`` variable in the ``user_settings.py`` file.

The water use point(s), ``wateruse_centroids_shapefile``,
that are contained within a respective basin, ``basin_shapefile_name``,
are found from performing a spatial intersection.  The water use points found 
to be contained with a respective basin are mapped to the water use data files 
(``wateruse_files`` variable in ``user_settings.py`` file) and used to calculate 
monthly water use totals.

The following is an example WATER *batch* simulation **before** applying water use:

::

    WATER-batch-run/
        <basinid>/                  # directory containing data for a specific basin id in the batch simulation
            amask                   # ArcMap raster of agriculture area
            basinmask               # ArcMap raster of basin area
            fmask                   # ArcMap raster of forest area
            WATER.txt               # WATER simulation output file
            WATERAnnual.txt         # WATER simulation annual output file
            WATERMonth.txt          # WATER simulation monthly output file
            WATERSimulation.txt     # WATER simulation database file
        <basinid>/                  # directory containing data for a specific basin id in the batch run
        ...
        Water.txt                   # WATER output file with computed discharge and all other output parameters
        Watersheds.shp              # shapefile and all its associated data files (.dbf, .prj, .sbn, .sbx, .shp.xml, .shx)                         

The following is the directory structure **after** applying water use to a *batch* simulation:

::

    water-batch-dir/
        waterapputils-info/                             # information about applying water use to the simulation
            waterapputils_error.log                     # warnings or errors in processing simulation (created only if errors occur)
            wateruse_info.txt                           # information regarding intersected centroids and respective water use values per basin
            wateruse_non_intersecting_centroids.txt     # csv file to be filled by user concerning basins that do not intersect any water use centroid
        basin-1/
            WATERUSE-WATER.txt                          # file formatted the same as a typical WATER.txt file, but includes columns of Discharge + Water Use and Water Use
            waterapputils-wateruse/                     # directory holding plots of all parameters in WATERUSE-WATER.txt file
                *.png
        basin-2/                                        
            WATERUSE-WATER.txt                          # file formatted the same as a typical WATER.txt file, but includes columns of Discharge + Water Use and Water Use
            waterapputils-wateruse/                     # directory holding plots of all parameters in WATERUSE-WATER.txt file
                *.png

Results of applying water use to each basin in a WATER simulations are contained
within each respective basin directory in the ``waterapputils-wateruse`` directory.
The ``waterapputils-wateruse/`` directory contains plots of all the
parameters in the ``WATER.txt`` file.

Each respective basin directory (basin-1) contains an updated WATER simulation
output file (``WATERUSE-WATER.txt``) containing additional
columns of water use (cfs) and discharge + water use (cfs). In addition,
the updated WATER simulation file is processed and plots of each
parameter in the updated WATER simulation file are created and contained
in the ``waterapputils-wateruse/ `` directory.

Detailed information regarding applying water use to a WATER simulation are
contained in the ``waterapputils-info`` directory.
The ``waterapputils-info`` directory contains a file,
called ``wateruse_info.txt``, that contains details of which water use
points are contained with which basin with the corresponding (monthly) water use totals
applied to the the original discharge from the original WATER simulation.

Water use points that are not contained within any basin in a respective
WATER simulation are logged to a file called ``wateruse_non_intersecting_centroids.txt``
(Note: this file name can be edited using the ``wateruse_non_intersecting_file_name`` variable 
in the ``user_settings.py`` file). The ``wateruse_non_intersecting_centroids.txt`` is a 
comma-separated file that lists on each row the basin name (id) that does not contain any
water use points along with a *special* water use id of **000** meaning **0 water use** was
applied.  Users can edit this file by specifying the water use points to be applied to each
respective basin.  

The following is an example of the ``wateruse_non_intersecting_centroids.txt`` file
where **0 water use** was applied to a specific basin:

::

    basinid,newhydroid
    01414500,000      

To apply water use points (e.g. 100,101,102) to basinid 01414500, then a user would update the
``wateruse_non_intersecting_centroids.txt`` file to the following:

::

    basinid,newhydroid
    01414500,100,101,102  

After updating the ``wateruse_non_intersecting_centroids.txt`` file, a user can apply the *substitute* water use 
points by applying the following command:

::

    $ python waterapputils.py -applysubwateruse

The above command uses the ``wateruse_non_intersecting_centroids.txt`` file
to apply water use to those basins that originally did not have any water use applied.
A new file, called ``sub_wateruse_info.txt``, is created in the ``waterapputils-info`` directory
that logs the information regarding the substitute water use applied.  The special output files for 
the OASIS and ecoflow programs are updated after applying substitute water use. 


Applying climate change factors to WATER batch runs
---------------------------------------------------

Apply climate change factors (GCM deltas) to WATER simulation batch runs.

::

    $ python waterapputils.py -applydeltas

Applies GCM deltas (factors) to a WATER simulation batch run.  Specifically, it
applies climate change factors (precipiation and temperature) to the WATER simulation 
database file ``WATERSimulation.xml``. In addition to updating the ``WATERSimulation.xml`` file,
a timeseries file of potential evapotranspiration (``PET``) values with the applied climate change 
factors is created.  Details about the WATER simulation, *single* or *batch* simulation, are contained in the
``user_settings.py`` file.

To apply climate change factors to a WATER simulation, information regarding
the location of a series of files and directories must be entered
in a file called ``user_settings.py`` located in the 
``waterapputils/waterapputils/`` directory.
The following main variables associated with applying climate change factors that
are contained in the ``user_settings.py`` file:

::

    Variables                       Meaning
    ---------                       -------
             
    simulation_directory                    -   path to a WATER simulation directory
    is_batch_simulation                     -   boolean True or False
    basin_shapefile_name                    -   name of the basin(s) shapefile created by the WATER simulation; batch simulation = "Watersheds.shp"; single simulation = "basinMask.shp"
    gcm_delta_files                         -   list of the GCM delta factor files to be used; PET = Potential Evapotranspiration, Ppt = Precipitation, Temp = Temperature

Instead of specifying the path to a WATER simulation in the ``user_settings.py`` file,
users can supply the path directly on the command line using the following command:

::

    $ python waterapputils.py -applygcmdeltas -simdir <path-to-water-simulation-directory>

The above command applies climate change factors to a WATER simulation using a simulation directory path specified on the 
command line instead of using the ``simulation_directory`` variable in the ``user_settings.py`` file.

The following is an example of part of the ``user_settings.py`` file for a *batch* simulation 
using the sample datasets contained in the data directory:

::

    # ------------------- WATER simulation information ---------------------- #
    simulation_directory = "../data/sample-water-simulations/sample-batch-simulation"
    is_batch_simulation = True
    basin_shapefile_name = "Watersheds.shp"
    basin_shapefile_id_field = "STAID"
    basin_shapefile_area_field = "da_sqmi"                  # if no area field, leave blank like this: ""

    # ------------------- Global Climate Model information ------------------ #
    gcm_delta_files = ["../data/deltas-gcm/Ppt.txt",
                       "../data/deltas-gcm/Tmax.txt",
                       "../data/deltas-gcm/PET.txt",
    ]                

    gcm_delta_tile_shapefile = "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp"
    gcm_delta_tile_shapefile_id_field = "Tile"


The following is an example of part of the ``user_settings.py`` file for a *single* simulation using the sample datasets:

::

    # ------------------- WATER simulation information ---------------------- #
    simulation_directory = "../data/sample-water-simulations/sample-single-simulation"
    is_batch_simulation = False
    basin_shapefile_name = "basinMask.shp"
    basin_shapefile_id_field = ""
    basin_shapefile_area_field = ""                  # if no area field, leave blank like this: ""

    # ------------------- Global Climate Model information ------------------ #
    gcm_delta_files = ["../data/deltas-gcm/Ppt.txt",
                       "../data/deltas-gcm/Tmax.txt",
                       "../data/deltas-gcm/PET.txt",
    ]                

    gcm_delta_tile_shapefile = "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp"
    gcm_delta_tile_shapefile_id_field = "Tile"


The information in the ``user_settings.py`` file is used to
apply climate change to each respective basin in the respective simulation. The only exception
here is when a user specifies the path to a WATER simulation on the command line which will
overwrite the ``simulation_directory`` variable in the ``user_settings.py`` file.

The global climate change tiles shapefile(``gcm_delta_tile_shapefile`` variable in ``user_settings.py``)
is used in performing a spatial intersection between the tiles and the respective WATER simulation
basin(s).  The tiles found to be intersected with a respective basin are mapped to the global climate change 
data files (``gcm_delta_files`` variable in ``user_settings.py`` file) and used to calculate 
monthly climate change factors.

The following is an example WATER *batch* simulation **before** applying climate change factors:

::

    WATER-batch-run/
        <basinid>/                  # directory containing data for a specific basin id in the batch simulation
            amask                   # ArcMap raster of agriculture area
            basinmask               # ArcMap raster of basin area
            fmask                   # ArcMap raster of forest area
            WATER.txt               # WATER simulation output file
            WATERAnnual.txt         # WATER simulation annual output file
            WATERMonth.txt          # WATER simulation monthly output file
            WATERSimulation.txt     # WATER simulation database file
        <basinid>/                  # directory containing data for a specific basin id in the batch run
        ...
        Water.txt                   # WATER output file with computed discharge and all other output parameters
        Watersheds.shp              # shapefile and all its associated data files (.dbf, .prj, .sbn, .sbx, .shp.xml, .shx)                         

The following is the directory structure **after** applying climate change factors to a *batch* simulation:

::

    water-batch-dir/
        waterapputils-info/                             # information about applying climate change factors to a simulation
            waterapputils_error.log                     # warnings or errors in processing simulation (created only if errors occur)        
            gcmdelta_info.txt                           # information regarding intersected tiles and respective climate change factor values per basin
            gcmdelta_non_intersecting_centroids.txt     # csv file to be filled by user concerning basins that do not intersect any global climate change tiles
        basin-1/
            GCMDELTA-WATERSimulation.xml                # file formatted the same as a typical WATERSimulation.xml file, but includes climate factored precipitation and temperature data
            pet-timeseries.txt                         # potential evapotranspiration timeseries file with climate change factors applied; ``pet_timeseries_file_name`` file in ``user_settings.py`` 
            waterapputils-gcmdelta/                     # directory holding plots of all relevant parameters in the GCMDELTA-WATERSimulation.xml file
                *.png
        basin-2/                                        
            GCMDELTA-WATERSimulation.xml                # file formatted the same as a typical WATERSimulation.xml file, but includes climate factored precipitation and temperature data
            pet-timeseries.txt                         # potential evapotranspiration timeseries file with climate change factors applied; ``pet_timeseries_file_name`` file in ``user_settings.py`` 
            waterapputils-gcmdelta/                     # directory holding plots of all relevant parameters in the GCMDELTA-WATERSimulation.xml file
                *.png

Results of applying climate change factors to each basin in a WATER simulations are contained
within each respective basin directory in the ``waterapputils-gcmdelta`` directory.
The ``waterapputils-gcmdelta/`` directory contains plots of all the relevant
parameters in the WATERSimulation.xml file.

Each respective basin directory (basin-1) contains an updated WATER simulation
database file (``GCMDELTA-WATERSimulation.xml``) containing climate factored precipitation
and temperature data. In addition, the updated WATER database file is processed and plots of each
parameter in the updated GCMDELTA-WATERSimulation.xml file are created and contained
in the ``waterapputils-gcmdelta/ `` directory.

Detailed information regarding applying climate change factors to a WATER simulation are
contained in the ``waterapputils-info`` directory. The ``waterapputils-info`` directory contains a file,
called ``gcmdelta_info.txt``, that contains details of which climate change tiles
are intersected by each basin with the corresponding (monthly) climate change factors
applied to the the original precipitation and temperature from the original WATERSimulation.xml file.

Although unlikely, any global climate change tiles that are not intersected by a basin in a respective
WATER simulation are logged to a file called ``gcmdelta_non_intersecting_tiles.txt``
(Note: this file name can be edited using the ``gcmdelta_non_intersecting_file_name`` variable 
in the ``user_settings.py`` file). The ``gcmdelta_non_intersecting_centroids.txt`` is a 
comma-separated file that lists on each row the basin name (id) that does not intersect any
global climate change tiles along with a *special* tile id of **000** meaning no climate change factors
were applied.  Users can edit this file by specifying the tile ids to be applied to each
respective basin.  

The following is an example of the ``gcmdelta_non_intersecting_tiles.txt`` file
where no climate change factors were applied to a specific basin:

::

    basinid,Tile
    01414500,000      

To apply climate factor tiles (e.g. 10,11,12) to basinid 01414500, then a user would update the
``gcmdelta_non_intersecting_tiles.txt`` file to the following:

::

    basinid,Tile
    01414500,10,11,12  

After updating the ``gcmdelta_non_intersecting_tiles.txt`` file, a user can apply the *substitute*  
climate change tiles by applying the following command:

::

    $ python waterapputils.py -applysubgcmdeltas

The above command uses the ``gcmdelta_non_intersecting_tiles.txt`` file
to apply climate change factors to those basins that originally did not have any factors applied.
A new file, called ``sub_gcmdelta_info.txt``, is created in the ``waterapputils-info`` directory
that logs the information regarding the substitute factors applied.   
