[![alt text](docs/_static/usgs-logo.png)](http://www.usgs.gov/)

# waterapputils

***

## Description
  
**waterapputils** is a tool used for analyzing, processing, and updating model simulations from the [U.S. Geological Survey 
Indiana and Kentucky Water Science Centers (INKY)] WATER application. **waterapputils** is written in [Python](https://www
.python.org/), and adds new functionality, outside the WATER application, by allowing users to apply various future climate 
projections using a change-factor (delta) approach with data from the Coupled Model Intercomparison Project ([CIMP5]), and 
aggregated water use data to model simulations.  

The WATER application is a graphical user interface, written in VB.NET, wrapped around a variant of the rainfall-runoff model 
called Topmodel (Topography based hydrological mode) by Keith Beven, Professor at Lancaster University. Topmodel estimates 
river discharge and spatial soil water saturation patterns for a particular catchment basin using topographic, climatic, and 
geological input data parameters. The original WATER application was developed by the [U.S. Geological Survey Indiana and 
Kentucky Water Science Centers (INKY)]. References for the WATER application include:

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

## Version

1.0.0

## Command line arguments/options

| Commands              | Description |                                                                              
| --------              | ----------- |                                                                               
|`-h`                   | show list of available commands |
|`-watertxt`            | list WATER simulation output file(s) to process; `WATER.txt` |
|`-watertxtfd`          | open file dialog window to select WATER simulation output file(s) to process; `WATER.txt` |
|`-watertxtcmp`         | list 2 WATER simulation output file(s) to compare; `WATER.txt` |
|`-watertxtcmpfd`       | open file dialog window to select 2 WATER simulation output file(s) to compare; `WATER.txt` |                        
|`-waterxml`            | list WATER simulation database file(s) to process; `WATERSimulation.xml` |
|`-waterxmlfd`          | open file dialog window to select WATER simulation database file(s) to process; `WATERSimulation.xml` |
|`-waterxmlcmp`         | list 2 WATER simulation database file(s) to compare; `WATERSimulation.xml` |
|`-waterxmlcmpfd`       | open file dialog window to select 2 WATER simulation database files to compare; `WATERSimulation.xml` | 
|`-applygcmdeltas`      | apply global climate change deltas to WATER simulation database file(s); `WATERSimulation.xml`; details specified in `user_settings.py` | 
|`-applysubgcmdeltas`   | apply updated global climate change deltas from `sub_gcm_delta_info_file_name` variable in user_settings.py to WATER simulation database file(s); `WATERSimulation.xml`; details specified in `user_settings.py` | 
|`-applywateruse`       | apply water use data to WATER simulation output file(s); `WATER.txt`; details specified in `user_settings.py` | 
|`-applysubwateruse`    | apply water use data from `sub_wateruse_info_file_name` variable in user_settings.py to WATER simulation output file(s); `WATER.txt`; details specified in `user_settings.py` | 
|`-oasis`               | create output data file(s) for OASIS program; tab delimited file(s) of timeseries of discharge |
|`-ecoflowstationid`    | create output data file(s) for ecoflow program; comma separated file(s) of timeseries of discharge for a specific basin (station) id |
|`-ecoflowdaxml`        | create output data file(s) for ecoflow program; comma separated file(s) of basin (station) id and its respective drainage area in square miles calculated using data in the `WATERSimulation.xml`  |
|`-ecoflowdashp`        | create output data file(s) for ecoflow program; comma separated file(s) of basin (station) id and its respective drainage area in square miles calculated from the shapefile(s)  |
|`-outfilename`         | OPTIONAL : output filename to be used with `-ecoflowdaxml` or `-ecoflowdashp` commands in writing the drainage area comma separated file | 
|`-labelfield`          | OPTIONAL : label field name (basin number / station id) to be used with `-ecoflowdashp` command in writing the drainage area comma separated file; Default label field is the FID in the basin(s) shapefile | 
|`-areafield`           | OPTIONAL : area field name in a basin(s) shapefile to be used with `-ecoflowdashp` command in writing the drainage area comma separated file; Default action is to calculate area from the shapefile(s) |
|`-samplesingle`        | OPTIONAL : flag used with `-applywateruse`, `-applysubwateruse`, `-applygcmdeltas`, `-applysubgcmdeltas` to specify the use of the sample single simulation datasets |
|`-samplebatch`         | OPTIONAL : flag used with `-applywateruse`, `-applysubwateruse`, `-applygcmdeltas`, `-applysubgcmdeltas` to specify the use of the sample batch simulation datasets |
|`-simdir`              | OPTIONAL : flag used with `-applywateruse`, `-applysubwateruse`, `-applygcmdeltas`, `-applysubgcmdeltas` to specify a path to a specific WATER simulation instead of specifying it in `user_settings.py` |

## [run_sample_datasets.sh](run_sample_datasets.sh) - Run sample datasets 

The shell script [run_sample_datasets.sh](run_sample_datasets.sh) is a shell script that can be used to run automated tests 
and run many of the command line arguments using the [sample datasets](data/sample-water-simulations).  

### Usage:

```sh
$ run_sample_datasets.sh [option]
$ run_sample_datasets.sh [[[-txt] [-xml] [-wateruse] [-oasis] [-ecoflowstationid] [ecoflowdaxml] [-ecoflowdashp] [-gcmdelta] [-mapsim] [-all] [-tests] -makeclean] | [-h]]
```

The following are the command line arguments for the shell script [run_sample_datasets.sh](run_sample_datasets.sh):

| Commands              | Description |                                                                              
| --------              | ----------- |                                                                               
|`-h`                   | show list of available commands |
|`-txt`                 | run `-watertxt` and `-watertxtcmp` using the [sample WATER simulation output TEXT files](data/watertxt-datafiles) |
|`-xml`                 | run `-waterxml` and `-waterxmlcmp` using the [sample WATER simulation output XML files](data/waterxml-datafiles) |
|`-wateruse`            | run and apply [water use data](data/wateruse-datafiles) to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-subwateruse`         | run and apply substitute water use data to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-gcmdelta`            | run and apply [global climate model data](data/gcmdelta-datafiles) to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-subgcmdelta`         | run and apply substitute water use data to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-oasis`               | create an oasis formated water use output file using the [sample water use applied WATER TEXT file](data/sample-water-simulations/sample-datafiles/WATERUSE-WATER-basin0.txt) |
|`-ecoflowstationid`    | create an ecoflow formated water use output file using the [sample water use applied WATER TEXT file](data/sample-water-simulations/sample-datafiles/WATERUSE-WATER-basin0.txt) |
|`-ecoflowdaxml`        | create an ecoflow formated drainage area output file using the [sample WATER XML file](data/sample-water-simulations/sample-datafiles/WATERSimulation-basin0.xml) to calculate basin area |
|`-ecoflowdashp`        | create an ecoflow formated drainage area output file using the [sample basin shapefiles](data/sample-water-simulations/sample-datafiles/basin0.shp) |
|`-mapsim`              | create maps for [single and batch simulations](data/sample-water-simulations) | 
|`-all`                 | run (mostly) all commands; `-tests`, `-txt`, `-xml`, `-wateruse`, `-gcmdelta`, `-oasis`, `-ecoflowstationid`, `-ecoflowdaxml`, `-ecoflowdashp`, `mapsim` |
|`-tests`               | run units tests use nosetests |
|`-makeclean`           | cleans/removes all output of running sample dataset in in the [sample-water-simulations directory](data/sample-water-simulations) |

### Example:

```sh
$ run_sample_datasets.sh -wateruse
```

## [run_simulations.sh](run_simulations.sh) - Apply water use and gcm deltas to multiple WATER simulations

The shell script [run_simulations.sh](run_simulations.sh) is a shell script that can be used to automate
the processing of many WATER simulations. [run_simulations.sh](run_simulations.sh) can be used to apply 
water use and global climate change scenarios to multiple WATER simulations that are contained in the same directory.

### Usage:

```sh
$ run_simulations.sh [option] <path-to-simulations-directory>
$ run_simulations.sh [[[-applywateruse] [-applysubwateruse] [-applygcmdelta] [-applysubgcmdelta]] <path-to-simulations-directory> | [-h]]
```

| Commands              | Description |                                                                              
| --------              | ----------- |                                                                               
|`-h`                   | show list of available commands |
|`-applywateruse`       | run and apply [water use data](data/wateruse-datafiles) to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-applysubwateruse`    | run and apply substitute water use data to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-applygcmdelta`       | run and apply [global climate model data](data/gcmdelta-datafiles) to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |
|`-applysubgcmdelta`    | run and apply substitute water use data to sample WATER simulations; [single and batch simulations](data/sample-water-simulations) |

### Example:

```sh
$ run_simulations.sh -applywateruse path-to-simulations-directory
```

## Testing

Automated tests for **waterapputils** were written using the [nose] library, and are contained in the *tests* directory. [nose] must be
installed in order to run tests. Automated tests can be run using the `nosetests` command at the project level directory (not 
within the *tests* directory, but the *waterapputils* directory containing the *tests* directory).  A successful test run 
will look something like the following:

```sh
$ pwd
/path/to/waterapputils    

$ nosetests
SETUP: deltatxt tests
........TEARDOWN: deltatxt tests
...
SETUP: waterxml tests
........TEARDOWN: waterxml tests
--------------------------------------------------
Ran 91 tests in 1.049s

OK
```

## Repository/Project Layout

	bin/						            # executables/scripts
	data/						            # sample data files to use with software and associated information
		deltas-gcm/                         # statistically downscaled global climate model data
        sample-water-simulations            # sample WATER application simulations and datasets
            sample-batch-simulation         # sample WATER application batch run simulation
            sample-datasets                 # sample WATER application simulation datasets
            sample-single-simulation        # sample WATER applicaiton single run simulation
        spatial-datafiles/                  # spatial data; shapefile format
        watertxt-datafiles/	    	        # sample WATER.txt files
        wateruse-batch-run/                 # sample batch run output from WATER
        wateruse-datafiles/                 # sample water use files
    	waterxml-datafiles/	    	        # sample WATERSimulation.xml files
	docs/						            # Sphinx code documentation
    tests/						            # tests
        deltas_tests.py                     # tests for deltas module
        helpers_tests.py                    # tests for helper module
        spatialvectors_test.py              # tests for spatialvectors module
        watertxt_tests.py                   # tests for watertxt module
        wateruse_tests.py                   # tests for wateruse module
        waterxml_tests.py                   # tests for waterxml module
    waterapputils/				            # directory containing code modules
        deltas.py                           # handles processing of global climate model data
        deltas_viewer.py                    # handles view (plotting) of global climate model data
        gcm_delta_processing.py             # handles the global climate model delta factors processing using settings from the user_settings.py file
        helpers.py                          # helper functions
        spatialdata_viewer.py               # handles view (mapping) of spatial data; uses basemap library
        spatialvectors.py                   # handles spatial data
        specific_output_file_processing.py  # handles specific output file processing for external OASIS and Ecoflow programs
        user_settings.py                    # user settings to control and specify data inputs for water use and global climate model processing along with control of naming outputs
        water_files_processing.py           # handles the WATER application output and database file processing using settings from the user_settings.py file
        waterapputils.py                    # main controller; calls respective module
        waterapputils_logging.py            # handles error logging
        watertxt.py                         # handles processing of WATER.txt simulation output files
        watertxt_viewer.py                  # handles view (plotting) of WATER.txt simulation output files
        wateruse.py                         # handles processing of water use data
        wateruse_processing.py              # handles the water use processing using settings from the user_settings.py file
        waterxml.py                         # handles processing of WATERSimulation.xml simulation database files
        waterxml_viewer.py                  # handles view (plotting) of  WATERSimulation.xml simulation database files
    Makefile					            # makefile to help clean directories
	LICENSE.txt				                # USGS Software User Rights Notice
	README.md					            # README file
	requirements.txt			            # list of requirements/dependencies 
	setup.py					            # code for building, distributing, and installing modules
    run_sample_datasets.sh                  # bash script used to run specific or all sample datasets
    run_simulations.sh                      # bash script used to apply water use and/or climate change factors to multiple WATER simulations

## Code Documentation

Code documentation was made using [Sphinx] and is located [here](docs/_build/html/index.html).
    
## Requirements

	python == 2.7.6
	numpy == 1.8.0
	matplotlib == 1.3.1
	nose == 1.3.0
    
## Disclaimer and Notice


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

## Author


    Jeremiah Lant
    Hydrologist 
    U.S. Geological Survey
    Kentucky Water Science Center
    Louisville, Kentucky 40299
    (502) 493-1949
    jlant@usgs.gov

[U.S. Geological Survey Indiana and Kentucky Water Science Centers (INKY)]:http://ky.water.usgs.gov/
[CIMP5]:http://cmip-pcmdi.llnl.gov/cmip5/
[nose]:https://nose.readthedocs.org/en/latest/
[Sphinx]:http://sphinx-doc.org/
