GCM Delta Guide
===============

GCM Delta data files
--------------------

The GCM delta files contain monthly delta factors for a specific parameter.  The parameters
include:

1. precipitation
2. temperature
3. PET

An example GCM delta file for precipitation is:

::

    Model   Scenario    Target  Variable    Tile    January February    March   April   May     June    July    August  September   October November    December
    CanESM2 rcp45       2030    Ppt         11      1       1           1       0       2       2       3       1       0           1       3           0
    CanESM2 rcp45       2030    Ppt         12      3       0           1       2       1       0       3       2       0           2       2           1
    CanESM2 rcp45       2030    Ppt         21      2       0           2       2       2       3       0       1       3           1       0           1
    CanESM2 rcp45       2030    Ppt         22      1       3           0       0       2       1       0       0       3           1       1           0
    CanESM2 rcp45       2030    Ppt         31      1       0           0       1       1       3       3       0       0           2       0           0
    CanESM2 rcp45       2030    Ppt         32      2       2           1       2       3       1       0       2       2           1       0           0                                           


The WATER simulation database file (``WATERSimuation.xml``) only contains timeseries of precipitation
and temperature and not PET.  Meaning that only GCM deltas for precipitation and temperature can be applied
to the ``WATERSimulation.xml`` file.