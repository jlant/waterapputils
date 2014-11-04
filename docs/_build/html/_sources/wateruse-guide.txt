Water Use Data Files
====================

The water use data files contain seasonal totals of median water use
values for each respective DEM-derived HUC12 basin. Basin centroids were
created to represent a respective water use point within a HUC12 basin.

The water use values are in units of million gallons per day (Mgal/day).
The water use values are divided into various categories:

-  return flow (RT) - positive values
-  withdrawal (WL) - negative values
-  transfer (T) - negative values

for different sources:

-  groundwater (Gw)
-  surfacewater (Sw)

**Seasons**

1. Winter - January, February, March (JFM)
2. Spring - April, May, June (AMJ)
3. Summer - July, August, September (JAS)
4. Autumn - October, November, December (OND)

--------------

Steps to Compute Total Water Use For Each Respective Basin
==========================================================

1. Find water use centroids that are contained within the basin
   boundaries.
2. Get all the water use contributions for those centroids that are
   contained within the basin boundaries.
3. Apply water use factors if a water use factors data file exists.
4. Sum all the water use contributions for each centroid (row sum)
5. Sum all the centroid's respective water use (column sum)
6. Apply conversion from million gallons per day (Mgal/day) to cubic
   feet per second (cfs) to the total water use. (1 million gallons per
   day = 1.54722865 cubic feet per second)

Example
-------

Consider the following sample water use data files.

**Sample water use data file**

::

    # JFM_WU                        
    # Units: Mgal/day       
    # sample data set   
    huc12    newhydroid    AqGwWL   CoGwWL  DoGwWL  InGwWL  IrGwWL
    20401010101    256     0        0        1        0        0
    20401010101    241     0        1        1       -1        1
    20401010101    222     1       -1        1        0       -1
    20401010101    220    -1        0        1       -1        1
    20401010101    12      0       -1        0        0        0
    20401010101    11     -1        0        0        0       -1
    20401010102    8       1        1        1        0        0

**Sample water factor file**

::

    # water use factors
    AqGwWL  CoGwWL  DoGwWL  InGwWL  IrGwWL
    1.5     1.5     1.5     1.5    1.5

where

    newhydroid - centroid id's AqGwWL, CoGwWL, DoGwWL, InGwWL, IrGwWL -
    various water use contributions

1) Let the following centroids be contained within a respective basin:

[256, 241, 222, 220]

2) Get all the water use contributions for those centroids that are
   contained within the basin boundaries.

::

    newhydroid  AqGwWL  CoGwWL  DoGwWL  InGwWL  IrGwWL
    256         0       0       1       0       0
    241         0       1       1      -1       1
    222         1      -1       1       0      -1
    220        -1       0       1      -1       1

3) Apply water use factors if a water use factors data file exists.

::

    newhydroid  AqGwWL  CoGwWL  DoGwWL  InGwWL  IrGwWL
    256         0       0       1.5     0       0
    241         0       1.5     1.5    -1.5     1.5
    222         1.5    -1.5     1.5     0      -1.5
    220        -1.5     0       1.5    -1.5     1.5

4) Sum all the water use contributions for each centroid (row sum)

::

    newhydroid  sum
    256         1.5
    241         3.0
    222         0.0
    220         0.0

5) Sum all the centroid's respective water use (column sum)

::

    total water use = 4.5 Mgal/day

6) Apply conversion from million gallons per day (Mgal/day) to cubic
   feet per second (cfs) to the total water use. (1 million gallons per
   day = 1.54722865 cubic feet per second)

::

    total water use = 6.96 cfs

