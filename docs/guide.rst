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

Apply water use to a WATER simulation.

::

    $ python waterapputils.py -applywateruse

Applies water use data to a WATER simulation. 
An example WATER batch simulation has the following directory structure:

::

    WATER-batch-run/
        <basinid>/                  # directory containing data for a specific basin id in the batch run
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

At this time, in order to apply water use to a WATER simulation, 
information regarding the location of a series of files and
directories must be entered in a file called ``user_settings.py`` 
located in the ``waterapputils/waterapputils/`` directory.
The following variables are to be assigned in a ``user_settings.py`` file:

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


The following is an example of part of the ``user_settings.py`` file for a batch simulation using the sample datasets:

::

    # ------------------- WATER simulation information ---------------------- #
    simulation_directory = "../data/sample-water-simulations/sample-batch-simulation"
    is_batch_simulation = True
    basin_shapefile_name = "Watersheds.shp"
    basin_shapefile_id_field = "STAID"
    basin_shapefile_area_field = "da_sqmi"                  # if no area field, leave blank like this: ""

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
            "../data/wateruse-datafiles/101112-OND-sample.txt",
    ]

    wateruse_factor_file = "../data/wateruse-datafiles/wateruse-factors-sample.txt"


The following is an example of part of the ``user_settings.py`` file for a single simulation using the sample datasets:

::

    # ------------------- WATER simulation information ---------------------- #
    simulation_directory = "../data/sample-water-simulations/sample-single-simulation"
    is_batch_simulation = False
    basin_shapefile_name = "basinMask.shp"
    basin_shapefile_id_field = ""
    basin_shapefile_area_field = ""                  # if no area field, leave blank like this: ""

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
            "../data/wateruse-datafiles/101112-OND-sample.txt",
    ]

    wateruse_factor_file = "../data/wateruse-datafiles/wateruse-factors-sample.txt"


The information in the ``user_settings.py`` file is used to
apply water use to each respective basin in the respective simulation.

The water use point(s), ``wateruse_centroids_shapefile```,
that lie within a respective basin, ``basin_shapefile_name``,
are found and used in the total water use calculation.

Results of applying water use to each basin in a WATER simulations are contained
within each respective basin directory in the ``waterapputils-wateruse``.
The following is the directory structure after processing a *batch* run:

::

    water-batch-dir/
        waterapputils-info/                             # information about applying water use to the batch run
            waterapputils_error.log                     # warnings or errors in processing batch run
            wateruse_info.txt                           # information regarding intersected centroids and respective water use values per basin
            wateruse_non_intersecting_centroids.txt     # csv file to be filled by user concerning basins that do not intersect any water use centroid
        basin-1/
            WATERUSE-WATER.txt                          # file formatted the same as a typical WATER.txt file, but includes columns of Discharge + Water Use and Water Use
            waterapputils-wateruse/                     # directory holding plots of all parameters in WATER.txt-with-wateruse.txt file
                *.png
        basin-2/                                        
            WATERUSE-WATER.txt                          # file formatted the same as a typical WATER.txt file, but includes columns of Discharge + Water Use and Water Use
            waterapputils-wateruse/                     # directory holding plots of all parameters in WATER.txt-with-wateruse.txt file
                *.png

The ``waterapputils-wateruse/`` directory contains plots of all the
parameters in the ``WATER.txt`` file.

Each respective basin directory (basin-1) contains an updated WATER simulation
output file (``WATERUSE-WATER.txt``) containing additional
columns of water use (cfs) and discharge + water use (cfs). In addition,
the updated WATER simulation file is processed and plots of each
parameter in the updated WATER simulation file are created and contained
in the ``waterapputils-wateruse/ `` directory.

Detailed information regarding applying water use to a batch run are
contained in a directory called ``waterapputils-info`` which is
created in the ``waterapputils-info`` directory specified in the
The ``waterapputils-info`` directory contains a summary file of the 
water use data applied and which water use points were used called ``wateruse_info.txt``.

# FIXME

If there are basins that do not intersect any water use points, then a file logging those
the non-intersection water use points (``waterapputils_error.log``) is
created, along with a comma-separated file
(``wateruse_non_intersecting_centroids.txt``) listing the specific
basins that do not intersect any water use points. To apply water use
point(s) to basins that originally do not intersect any water use
points, a user can edit the ``wateruse_non_intersecting_centroids.txt``
file and specify water use point(s) to be applied. To apply the
information specified in the ``wateruse_non_intersecting_centroids.txt``
to the batch run, the following command is used:

::

    $ python waterapputils.py -applysubwateruse

The above command uses the ``subwateruse_file`` variable in the
``user_settings.py`` file which specifies the location of the
``wateruse_non_intersecting_centroids.txt`` file.


Applying climate change factors to WATER batch runs
---------------------------------------------------

Apply climate change factors (GCM deltas) to WATER simulation batch runs.

::

    $ python waterapputils.py -applydeltas

Applies GCM deltas (factors) to a WATER simulation batch run.  Specifically, it
applies change factors to the WATER simulation database file ``WATERSimulation.xml``

At this time, in order to apply GCM deltas to a WATER simulation batch
run, information regarding the location of a series of files and
directories must be entered in a file called
``user_settings.py`` located in the
``waterapputils/waterapputils/`` directory
The following variables are to be assigned in a
``user_settings.py`` file:

::

    Variables                       Meaning
    ---------                       -------
             
    waterbatch_directory        -   path to a WATER batch run directory
    basin_shapefile             -   path to the basin shapefile used in the WATER batch run
    basin_field                 -   unique field in the basin shapefile used in the WATER batch run that names the batch run directories; e.g. STAID
    subwaterdeltas_file         -   path to substitute GCM delta file; used when basins in the basin shapefile do not intersect with GCM tile(s)
    delta_files                 -   list of paths to delta files to use 
    delta_shapefile             -   path to the GCM delta shapefile

The following is an example ``user_settings.py`` file:

::

    waterbatch_directory = "../data/water-batch-run-datafiles/sample-batch-run-output/"
    basin_shapefile = waterbatch_directory + "Watersheds.shp"
    basin_field = "STAID"
    subwaterdeltas_file = waterbatch_directory + "waterapputils-batchrun-info/gcmdelta_non_intersecting_centroids.txt"
    delta_files = ["../data/deltas-gcm/Ppt.txt",
                   "../data/deltas-gcm/Tmax.txt"]                
    delta_shapefile = "../data/spatial-datafiles/gcm-tiles/CanES_nad83.shp"


The information in the ``user_settings.py`` file is used to
apply GCM deltas to each respective basin in the batch run.

The intersection between each respective basin in the batch run and the
GCM tiles specify which deltas are applied. The tiles that
intersect a basin have there respective monthly GCM deltas averaged and
the averaged monthly GCM delta values are applied to the original WATER 
simulation database file ``WATERSimulation.xml``.

Results of applying GCM deltas to each basin in a batch run are contained
within each respective basin directory in the ``waterbatch_directory``.
The following is the directory structure after processing a batch run:

::

    water-batch-dir/
        waterapputils-batchrun-info/                            # information about applying water use to the batch run
            waterapputils_error.log                             # warnings or errors in processing batch run
            gcmdeltas_batchrun_info.txt-with-wateruse           # information regarding intersected centroids and respective water use values per basin
            gcmdeltas_non_intersecting_centroids.txt            # csv file to be filled by user concerning basins that do not intersect any water use centroid
        basin-1/
            WATERSimulation-updated-<basin_field>-<basinid>.xml # file formatted the same as a typical WATERSimulation.xml file, but has updated/altered climate parameters (precipitation and temperature)
            waterapputils-waterxml/                             # directory holding plots of all climate parameters in WATERSimulation-updated-<basin_field>-<basinid>.xml file
                *.png
        basin-2/                                        
            WATER.txt-with-wateruse.txt                         # file formatted the same as a typical WATERSimulation.xml file, but has updated/altered climate parameters (precipitation and temperature)
            waterapputils-wateruse/                             # directory holding plots of all parameters in WATERSimulation-updated-<basin_field>-<basinid>.xml file
                *.png

The ``waterapputils-waterxml/`` directory contains plots of all the
climate parameters in the ``WATERSimulation.xml`` file.

Each respective basin directory (basin-1) contains an updated WATER simulation
database file (``WATERSimulation-updated-<basin_field>-<basinid>.xml``) containing 
updated climate parameters. In addition,
the updated ``WATERSimulation-updated-<basin_field>-<basinid>.xml`` is processed and comparison plots
between the original ``WATERSimulation.xml`` file and the updated ``WATERSimulation-updated-<basin_field>-<basinid>.xml`` 
are created and contained in the ``waterapputils-waterxml/ `` directory.

Detailed information regarding applying GCM deltas to a batch run are
contained in a directory called ``waterapputils-batchrun-info`` which is
created in the ``waterbatch_directory`` specified in the
``user_settings.py`` file. The ``waterapputils_batch_info`` will
contain a summary file of the GCM deltas applied and which GCM
tiles were used. If there are basins
that do not intersect any water use points, then a file logging those
the non-intersecting GCM tiles (``waterapputils_error.log``) is
created, along with a comma-separated file
(``gcmdeltas_non_intersecting_tiles.txt``) listing the specific
basins that do not intersect any GCM tiles. To apply GCM deltas
to basins that originally do not intersect any GCM tile, a user 
can edit the ``gcmdeltas_non_intersecting_tiles.txt``
file and specify GCM delta tiles to be applied. To apply the
information specified in the ``gcmdeltas_non_intersecting_tiles.txt``
to the batch run, the following command is used:

::

    $ python waterapputils.py -applysubdeltas

The above command uses the ``subwateruse_file`` variable in the
``user_settings.py`` file which specifies the location of the
``gcmdeltas_non_intersecting_tiles.txt`` file.





