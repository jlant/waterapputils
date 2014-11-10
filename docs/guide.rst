General Guide
=============

Processing WATER simulation output files - WATER.txt
----------------------------------------------------

Process WATER simulation output text files (``WATER.txt``).

**-watertxt**

::

    $ python waterapputils.py -watertxt [file1] [file2] ...

Processes ``WATER.txt`` file(s) and produces plots of each parameter for
each file. Plots are saved to an output directory named as
\*\_waterapputils-output/filename-output\*. If an output text file name
is ``WATER-basin-0123.txt``, then the output directory would be named
``_waterapputils-output/WATER-basin-0123-output``. The output directory
is created in the same directory as the respective\ ``WATER.txt`` file.

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
\*\_waterapputils-output/filename1-vs-filename2-output\ *. If the
*\ filename1\* is ``WATER-basin-0123.txt`` and *filename2* is
``WATER-basin-456.txt``, then the output directory would be named
``_waterapputils-output/WATER-basin-0123-vs-WATER-basin-456-output``.
The output directory is located in the same directory as the
``WATER.txt`` file.

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
output directory named as \*\_waterapputils-output/filename-output\*. If
the output text file name is ``WATERSimulation-basin-0123.txt``, then
the output directory would be named
``_waterapputils-output/WATERSimulation-basin-0123-output``. The output
directory is created in the same directory as the
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
named as \*\_waterapputils-output/filename1-vs-filename2-output\ *. If
the *\ filename1\* is ``WATERSimulation-0123.txt`` and *filename2* is
``WATERSimulation-456.txt``, then the output directory would be named
``_waterapputils-output/WATERSimulation-0123-vs-WATERSimulation-456-output``.
The output directory is located in the same directory as the
``WATERSimulation.xml`` file.

--------------

**-waterxmlcmpfd**

::

    $ python waterapputils.py -waterxmlcmpfd

Spawns a file dialog window to select two ``WATERSimulation.xml`` files,
then compares and processes the ``WATERSimulation.xml`` files in the
same manner as using the ``-waterxmlcmp`` flag.


Applying water use to WATER batch runs
--------------------------------------

Apply water use to WATER simulation batch runs.

::

    $ python waterapputils.py -applywateruse

Applies water use data to a WATER simulation batch run. A WATER
simulation batch run has the following directory structure:

::

    WATER-batch-run/
        <basinid>/        # directory containing data for a specific basin id in the batch run
            amask         # ArcMap raster of agriculture area
            basinmask     # ArcMap raster of basin area
            fmask         # ArcMap raster of forest area
            WATER.txt     # WATER simulation output file
            WATERAnnual.txt        # WATER simulation annual output file
            WATERMonth.txt         # WATER simulation monthly output file
            WATERSimulation.txt    # WATER simulation database file
        <basinid>/        # directory containing data for a specific basin id in the batch run
        ...
        Water.txt         # ?
        Watersheds.shp    # shapefile and all its associated data files (.dbf, .prj, .sbn, .sbx, .shp.xml, .shx)                         # containing all the basins used in the batch run

At this time, in order to apply water use to a WATER simulation batch
run, information regarding the location of a series of files and
directories must be entered in a file called
``water_use_batch_variables.py`` located in the
``waterapputils/data/water-batch-run-datafiles/sample-user-files/``
directory. The following variables are to be assigned in a
``water_use_batch_variables.py`` file:

::

    Variables                       Meaning
    ---------                       -------
             
    waterbatch_directory        -   path to a WATER batch run directory
    basin_shapefile             -   path to the basin shapefile used in the WATER batch run
    basin_field                 -   unique field in the basin shapefile used in the WATER batch run that names the batch run directories; e.g. STAID
    subwateruse_file            -   path to substitute water use file; used when basins in the basin shapefile do not intersect with water use centroids
    wateruse_files              -   list of paths to water use files to use
    wateruse_factor_file        -   path to the water use factor file
    basin_centroids_shapefile   -   path to the water use centroids shapefile

The following is an example ``water_batch_variables.py`` file:

::

    waterbatch_directory = "../data/water-batch-run-datafiles/sample-batch-run-output/"
    basin_shapefile = waterbatch_directory + "Watersheds.shp"
    basin_field = "STAID"
    subwateruse_file = waterbatch_directory + "/_waterapputils_non_intersecting_basin_centroids.txt"
    wateruse_files = ["../data/wateruse-datafiles/010203-JFM-sample.txt", 
                      "../data/wateruse-datafiles/040506-AMJ-sample.txt", 
                      "../data/wateruse-datafiles/070809-JAS-sample.txt", 
                      "../data/wateruse-datafiles/101112-OND-sample.txt"]                  
    wateruse_factor_file =  "../data/wateruse-datafiles/wateruse-factors-sample.txt"
    basin_centroids_shapefile = "../data/spatial-datafiles/wateruse-centroids/wateruse_centroids_sample_nad83.shp"

The information in the ``water_use_batch_variables.py`` file is used to
apply water use to each respective basin in the batch run.

The intersection between each respective basin in the batch run and the
points that specify the rough approximate location of water use data are
found. The water use point(s) that intersect a respective basin are
totaled and applied to the original WATER simulation output file
``WATER.txt``.

Results of applying water use to each basin in a batch run are contained
within each respective basin directory in the ``waterbatch_directory``.
Two directories, ``_waterapputils-output`` and ``_wateruse-output``,
that contain detailed results and plots of applying water use are
created in each respective basin directory.

::

    water-batch-dir/
        _wateruse-batchrun-info/        # information about applying water use to the batch run
            _waterapputils_error.log
            wateruse_batchrun_info.txt
            wateruse_non_intersecting_centroids.txt
        basin-1/
            
        basin-2/

The ``_waterapputils-output`` directory contains plots of all the
parameters in the ``WATER.txt`` file.

The ``_wateruse-output`` directory contains an updated WATER simulation
output file (``WATER.txt-with-wateruse.txt``) containing additional
columns of water use (cfs) and discharge + water use (cfs). In addition,
the updated WATER simulation file is processed and plots of each
parameter in the updated WATER simulation file are created and contained
in the ``_waterapputils-output/WATER.txt-with-wateruse.txt-output``
directory.

Detailed information regarding applying water use to a batch run are
contained in a directory called ``_wateruse_batch_info`` which is
created in the ``waterbatch_directory`` specified in the
``water_batch_variables.py`` file. The ``_wateruse_batch_info`` will
contain a summary file of the water use data applied and which water use
points were used (``wateruse_batchrun_info.txt``). If there are basins
that do not intersect any water use points, then a file logging those
the non-intersection water use points (``_waterapputils_error.log``) is
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
``water_batch_variables.py`` file which specifies the location of the
``wateruse_non_intersecting_centroids.txt`` file.
