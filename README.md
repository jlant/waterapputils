[![alt text](docs/_static/usgs-logo.png)](http://www.usgs.gov/)

waterapputils
=============

***
Description
-----------    

**waterapputils** is a tool used for analysing, processing, and updating model simulations from the [U.S. Geological Survey 
Indiana and Kentucky Water Science Centers (INKY)] WATER application. **waterapputils** is written in [Python](https://www
.python.org/), and adds new functionality, outside the WATER application, by allowing users to apply various future climate 
projections from a group of statistically downscaled global climate models ([GCMs]) available at the [USGS Derived Downscaled Climate Projection Portal] and water use data to model simulations.  
The WATER application is a graphical user interface, written in VB.NET, wrapped around a variant of the rainfall-runoff model 
called Topmodel (Topography based hydrological mode) by Keith Beven, Professor at Lancaster University. Topmodel estimates 
river discharge and spatial soil water saturation patterns for a particular catchment basin using topographic, climatic, and 
geological input data parameters. The original WATER application was developed by the [U.S. Geological Survey Indiana and 
Kentucky Water Science Centers (INKY)]. Referencesfor the WATER application include:

* [Williamson T.N., Odom K.R., Newson J.K., Downs A.C., Nelson Jr. H.L., Cinotto P.J., Ayers M.A. 2009. The Water Availability Tool for Environmental Resources (WATER)—A water-budget modeling approach for managing water-supply resources in Kentucky—Phase I—Data processing, model development, and application to non-karst areas, U.S. Geological Survey Scientific Investigations Report 2009-5248. pp. 34.](http://pubs.usgs.gov/sir/2009/5248/)
    
* [Williamson T.N., Taylor C.J., Newson J.K. 2013. Significance of Exchanging SSURGO and STATSGO Data When Modeling Hydrology in Diverse Physiographic Terranes. Soil Science Society of America Journal 77:877-889. DOI: 10.2136/sssaj2012.0069.](https://www.soils.org/publications/sssaj/abstracts/77/3/877)

Some sample highlights of **waterapputils** include:

* Processes WATER simulation output files (`txt` format).

* Processes WATER simulation database files that store information about a particular model simulation (`xml` format).

* Applies various statistically downscaled global climate models ([GCMs]) to model simulations for a particular watershed 
basin or set of watershed basins based on the spatial intersection of the watershed(s) of interest with the global climate 
change scenario coverage of interest.

* Applies water use data to model simulations for a particular for a particular watershed basin or set of watershed basins 
based on the spatial intersection of the watershed(s) of interest with the water use coverage.

* Generates plots of all parameters found in WATER output files (`txt` format) with simple statistics.
 
* Generates plots of timeseries parameters found in WATER simulation database files (`xml` format).

* Generates comparison and difference plots between two WATER simulation output files.

* Generates comparison and difference plots between two WATER simulation database files.

* Logs errors and tracebacks.

Version
-------

1.0.0

Command line arguments/options
------------------------------

| Commands          | Description |                                                                              
| --------          | ----------- |                                                                               
|`-h`               | show list of available commands |
|`-watertxt`        | list WATER simulation output file(s) to process; `WATER.txt` |
|`-watertxtfd`      | open file dialog window to select WATER simulation output file(s) to process; `WATER.txt` |
|`-watertxtcmp`     | list 2 WATER simulation output file(s) to compare; `WATER.txt` |
|`-watertxtcmpfd`   | open file dialog window to select 2 WATER simulation output file(s) to compare; `WATER.txt` |                        
|`-waterxml`        | list WATER simulation database file(s) to process; `WATERSimulation.xml` |
|`-waterxmlfd`      | open file dialog window to select WATER simulation database file(s) to process; `WATERSimulation.xml` |
|`-waterxmlcmp`     | list 2 WATER simulation database file(s) to compare; `WATERSimulation.xml` |
|`-waterxmlcmpfd`   | open file dialog window to select 2 WATER simulation database files to compare; `WATERSimulation.xml` | 
|`-applydeltas`     | apply global climate change deltas to WATER simulation database file(s); `WATERSimulation.xml`; details specified in `waterdelta_batch_variables.py` | 
|`-applysubdeltas`  | apply updated global climate change deltas from `_non_intersecting_basin_tiles.txt` to WATER simulation database file(s); `WATERSimulation.xml`; details specified in `waterdelta_batch_variables.py` | 
|`-applywateruse`   | apply water use data to WATER simulation output file(s); `WATER.txt`; details specified in `wateruse_batch_variables.py` | 
|`-applysubwateruse`| apply water use data from `_non_intersecting_basin_centroids.txt` to WATER simulation output file(s); `WATER.txt`; details specified in `wateruse_batch_variables.py` | 

Testing
-------

Tests for **waterapputils** were written using the [nose] library, and are contained in the *tests* directory. [nose] must be
installed in order to run tests. Automated tests can be run using the `nosetests` command at the project level directory (not 
within the *tests* directory, but the *waterapputils* directory containing the *tests* directory).  A successful test run 
will look something like the following:

```bash
$ pwd
/path/to/waterapputils	

$ nosetests
SETUP: deltatxt tests
........TEARDOWN: deltatxt tests
...
SETUP: waterxml tests
........TEARDOWN: waterxml tests
--------------------------------------------------
Ran 89 tests in 4.231s

OK
```

Repository/Project Layout
-------------------------

	bin/						        # executables/scripts
	data/						        # sample data files to use with software and associated information
		deltas-gcm/                     # statistically downscaled global climate model data
        spatial-datafiles/              # spatial data; shapefile format
        watertxt-datafiles/	    	    # sample WATER.txt files
        wateruse-batch-run/             # sample batch run output from WATER
        wateruse-datafiles/             # sample water use files
    	waterxml-datafiles/	    	    # sample WATERSimulation.xml files
	docs/						        # Sphinx code documentation
    tests/						        # tests
        deltas_tests.py                 # tests for deltas module
        helpers_tests.py                # tests for helper module
        spatialvectors_test.py          # tests for spatialvectors module
        watertxt_tests.py               # tests for watertxt module
        wateruse_tests.py               # tests for wateruse module
        waterxml_tests.py               # tests for waterxml module
    waterapputils/				        # directory containing code modules
        deltas.py                       # handles processing of global climate model data
        deltas_viewer.py                # handles view (plotting) of global climate model data
        helpers.py                      # helper functions
        spatialdata_viewer.py           # handles view (mapping) of spatial data; uses basemap library
        spatialvectors.py               # handles spatial data
        waterapputils.py                # main controller; calls respective module
        waterapputils_logging.py        # handles error logging
        waterdeltas_batch_variables.py  # user editable file for processing batch model simulations with climate model data
        watertxt.py                     # handles processing of WATER.txt simulation output files
        watertxt_viewer.py              # handles view (plotting) of WATER.txt simulation output files
        wateruse.py                     # handles processing of water use data
        wateruse_batch_variables.py     # user editable file for processing batch model simulations with water use data
        waterxml.py                     # handles processing of WATERSimulation.xml simulation database files
        waterxml_viewer.py              # handles view (plotting) of  WATERSimulation.xml simulation database files
    Makefile					        # makefile to help clean directories
	LICENSE.txt				            # USGS Software User Rights Notice
	README.md					        # README file
	requirements.txt			        # list of requirements/dependencies 
	setup.py					        # code for building, distributing, and installing modules

Code Documentation
------------------
COMING SOON
    
Requirements
------------
	python == 2.7.6
	numpy == 1.8.0
	matplotlib == 1.3.1
	nose == 1.3.0
    
Disclaimer and Notice
---------------------

	Please refer to the USGS Software User Rights Notice (LICENSE.txt or http://water.usgs.gov/software/help/notice/)
	for complete use, copyright, and distribution information. The USGS provides no warranty, expressed or implied, as to the
	correctness of the furnished software or the suitability for any purpose. The software has been tested, but as with any
	complex software, there could be undetected errors. Users who find errors are requested to report them to the USGS.

	References to non-USGS products, trade names, and (or) services are provided for information purposes only and do not
	constitute endorsement or warranty, express or implied, by the USGS, U.S. Department of Interior, or U.S. Government, as 
    to their suitability, content, usefulness, functioning, completeness, or accuracy.

	Although this program has been used by the USGS, no warranty, expressed or implied, is made by the USGS or the United
	States Government as to the accuracy and functioning of the program and related program material nor shall the fact of
	distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.

Author
------

    Jeremiah Lant
    Hydrologist 
    U.S. Geological Survey
    Kentucky Water Science Center
    Louisville, Kentucky 40299
    (502) 493-1949
    jlant@ugs.gov

[U.S. Geological Survey Indiana and Kentucky Water Science Centers (INKY)]:http://ky.water.usgs.gov/
[GCMs]:http://cida.usgs.gov/thredds/catalog.html?dataset=cida.usgs.gov/thredds/dcp/conus
[USGS Derived Downscaled Climate Projection Portal]:http://cida.usgs.gov/climate/derivative/
[nose]:https://nose.readthedocs.org/en/latest/