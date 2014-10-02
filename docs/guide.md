***
`-watertxt`

```
$ python waterapputils.py -watertxt path/to/WATER.txt
```

Produces plots of every parameter in a WATER simulation output text file (`WATER.txt`).
Plots are saved to an output directory named as *filename*-output (`WATER-output`).
The output directory is located in the same directory as the WATER simulation output
text file (`WATER.txt`).

**Example**

```
$ python waterapputils.py -watertxt ../data/watertxt-datafiles/WATER_1981_2011.txt
```

will produce 

```
../data/watertxt-datafiles/WATER_1981_2011-output/*.png
```

***
`-watertxtfd`

```
$ python waterapputils.py -watertxtfd 
```

Spawns a file dialog window to select a WATER simulation output text file (`WATER.txt`). 
Produces plots of every parameter in a WATER simulation output text file (`WATER.txt`).
Plots are saved to an output directory named as *filename*-output (`WATER-output`).
The output directory is located in the same directory as the WATER simulation output
text file (`WATER.txt`).

***
`-waterxml` 

```
$ python waterapputils.py -waterxml path/to/WATERSimulation.xml
```

Produces plots of timeseries parameters and topographic wetness index values in the
WATER simulation database xml file (`WATERSimulation.xml`). Plots are saved to an output 
directory named as *filename*-output (`WATERSimulation-output`). The output directory is located in 
the same directory as the WATER simulation database xml file  (`WATERSimulation.xml`).

**Example**
```
$ python waterapputils.py -waterxml ../data/waterxml-datafiles/WATERSimulation_1981_2011.xml
```

will produce

```
../data/waterxml-datafiles/WATERSimulation_1981_2011-output/*.png
```


***
`-waterxmlfd`

```
$ python waterapputils.py -waterxmlfd 
```

spawns a file dialog window to select a WATER simulation database xml file (`WATERSimulation.xml`). 
Upon selection of a a WATER simulation database xml file (`WATERSimulation.xml`),
produces an output directory containing plots of timeseries parameters and topographic wetness
index values in the WATERSimulation.xml file in the same folder as the WATERSimulation.txt file.
