Water Use Guide
===============

Water use data files
--------------------

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
----------------------------------------------------------

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

Example - using sample randomly generated data
------------------------------------------------

Consider the following sample water use data files.

**Sample water use data file for winter season**

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

**Column details**

* huc12 - HUC 12 id values

* newhydroid - id values for water use centroids

* AqGwWL, CoGwWL, DoGwWL, InGwWL, IrGwWL - various water use contributions


**Sample water factor file**

::

    # water use factors
    AqGwWL  CoGwWL  DoGwWL  InGwWL  IrGwWL
    1.5     1.5     1.5     1.5    1.5


**Compute total water use**

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

The same steps are followed for the spring, summer, autumn seasons for each respective seasonal water use file.

**Applying seasonal total water use to a WATER output simulation file (WATER.txt)**

Let the following table be the water use totals for each season:

+-----------+---------+------------------------+
| Month     | Season  | Water Use Total (cfs)  |
+===========+=========+========================+
| January   | JFM     | 6.96                   |
+-----------+---------+------------------------+
| Feburary  | JFM     | 6.96                   |
+-----------+---------+------------------------+
| March     | JFM     | 6.96                   |
+-----------+---------+------------------------+
| April     | AMJ     | 7.50                   |
+-----------+---------+------------------------+
| May       | AMJ     | 7.50                   |
+-----------+---------+------------------------+
| June      | AMJ     | 7.50                   |
+-----------+---------+------------------------+
| July      | JAS     | -0.5                   |
+-----------+---------+------------------------+
| August    | JAS     | -0.5                   |
+-----------+---------+------------------------+
| September | JAS     | -0.5                   |
+-----------+---------+------------------------+
| October   | OND     | 2.25                   |
+-----------+---------+------------------------+
| November  | OND     | 2.25                   |
+-----------+---------+------------------------+
| December  | OND     | 2.25                   |
+-----------+---------+------------------------+

Let the following be part of a sample WATER output simulation file (WATER.txt):

::

    Date    Discharge (cfs)
    1/1/2014    100
    ...
    3/31/2014   200
    4/1/2014    200
    ...
    6/30/2014   50
    7/1/2014    50
    ...
    9/30/2014   80
    10/1/2014   80
    ...
    12/31/2014  150

Applying the seasonal water use totals from the table above results in the following 
updated WATER output simulation file (WATER.txt):

::

    Date    Discharge (cfs) Discharge + Water Use (cfs) Water Use (cfs)
    1/1/2014    100         106.96                      6.96
    ...         ...         ...                         ...
    3/31/2014   200         206.96                      6.96
    4/1/2014    200         207.50                      7.50
    ...         ...         ...                         ...
    6/30/2014   50          57.50                       7.50
    7/1/2014    50          49.50                       -0.5
    ...         ...         ...                         ...
    9/30/2014   80          79.50                       -0.5
    10/1/2014   80          82.25                       2.25
    ...         ...         ...                         ...
    12/31/2014  150         152.25                      2.25