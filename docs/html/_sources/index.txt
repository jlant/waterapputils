.. waterapputils documentation master file, created by
   sphinx-quickstart on Tue Apr 08 15:39:05 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

|alt text|

Welcome to waterapputils's documentation!
=========================================

**waterapputils** is a tool used for analyzing, processing, and updating
model simulations from the `U.S. Geological Survey Indiana and Kentucky
Water Science Centers (INKY) <http://ky.water.usgs.gov/>`__ WATER
application. **waterapputils** is written in
`Python <https://www.python.org/>`__, and adds new functionality,
outside the WATER application, by allowing users to apply various future
climate projections using a change-factor (delta) approach with data
from the Coupled Model Intercomparison Project
(`CIMP5 <http://cmip-pcmdi.llnl.gov/cmip5/>`__), and aggregated water
use data to model simulations.

The WATER application is a graphical user interface, written in VB.NET,
wrapped around a variant of the rainfall-runoff model called Topmodel
(Topography based hydrological mode) by Keith Beven, Professor at
Lancaster University. Topmodel estimates river discharge and spatial
soil water saturation patterns for a particular catchment basin using
topographic, climatic, and geological input data parameters. The
original WATER application was developed by the `U.S. Geological Survey
Indiana and Kentucky Water Science Centers
(INKY) <http://ky.water.usgs.gov/>`__. References for the WATER
application include:

-  `Williamson T.N., Odom K.R., Newson J.K., Downs A.C., Nelson Jr.
   H.L., Cinotto P.J., Ayers M.A. 2009. The Water Availability Tool for
   Environmental Resources (WATER)—A water-budget modeling approach for
   managing water-supply resources in Kentucky—Phase I—Data processing,
   model development, and application to non-karst areas, U.S.
   Geological Survey Scientific Investigations Report 2009-5248. pp.
   34. <http://pubs.usgs.gov/sir/2009/5248/>`__

-  `Williamson T.N., Taylor C.J., Newson J.K. 2013. Significance of
   Exchanging SSURGO and STATSGO Data When Modeling Hydrology in Diverse
   Physiographic Terranes. Soil Science Society of America Journal
   77:877-889. DOI:
   10.2136/sssaj2012.0069. <https://www.soils.org/publications/sssaj/abstracts/77/3/877>`__

Some sample highlights of **waterapputils** include:

-  Processes WATER simulation output files (``txt`` format).

-  Processes WATER simulation database files that store information
   about a particular model simulation (``xml`` format).

-  Applies various statistically downscaled global climate models
   ([GCMs]) to model simulations for a particular watershed basin or set
   of watershed basins based on the spatial intersection of the
   watershed(s) of interest with the global climate change scenario
   coverage of interest.

-  Applies water use data to model simulations for a particular for a
   particular watershed basin or set of watershed basins based on the
   spatial intersection of the watershed(s) of interest with the water
   use coverage.

-  Generates plots of all parameters found in WATER output files
   (``txt`` format) with simple statistics.

-  Generates plots of timeseries parameters found in WATER simulation
   database files (``xml`` format).

-  Generates comparison and difference plots between two WATER
   simulation output files.

-  Generates comparison and difference plots between two WATER
   simulation database files.

-  Logs errors and tracebacks.

-  A multi-threaded graphical user interface (GUI) called waterapputils_gui

A sample image from the GUI - applying water use to WATER output files with waterapputils_gui
---------------------------------------------------------------------------------------------
.. image:: _static/gui-wateruse.png

Overview
========

.. toctree::
   :maxdepth: 2
   
   overview.rst

Guides
======

.. toctree::
   :maxdepth: 2

   guide.rst


.. toctree::
   :maxdepth: 2

   wateruse-guide.rst


.. toctree::
   :maxdepth: 2

   gcmdeltas-guide.rst

   
Documentation
=============

.. toctree::
   :maxdepth: 2

   code.rst

   
Download
========

https://github.com/jlant-usgs/waterapputils
 
 
Gallery  
=======

.. toctree::
   :maxdepth: 2
   
   gallery.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |alt text| image:: _static/usgs-logo.png
   :target: http://www.usgs.gov/
