# Water use calculation steps for each respective basin

1. Find all intersecting water use centroids; centroids that are contained within the basin boundaries.
2. Get all the water use contributions for each of the intersecting centroids and apply water use factors. 
3. Sum all the water use contributions for each centroid
4. Sum the water use for each centroid 

**Sample water use data file - 010203-JFM-sample.txt**
```
# JFM_WU																								
# Units: Mgal/day																								
# sample data set
huc12	newhydroid	AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL	LvGwWL	MiGwWL	ReGwWL	TeGwWL	WsGwWL	AqSwWL	CoSwWL	InSwWL	IrSwWL	MiSwWL	TeSwWL	WsSwWL	InGwRT	InSwRT	STswRT	WSgwRT	WSunkTR	WStrans
20401020101	440	-1	1	1	-1	1	1	1	1	1	0	-1	1	1	0	1	0	0	0	1	-1	0	-1	0
20401020104	390	0	-1	1	1	0	0	-1	-1	1	-1	-1	-1	0	0	0	-1	1	1	0	0	-1	1	-1
20401040302	262	0	1	0	0	0	0	1	-1	0	0	0	1	0	1	1	-1	1	-1	0	0	1	1	0
20401020201	257	-1	0	-1	0	-1	1	-1	1	1	0	1	-1	1	-1	1	-1	0	1	0	0	0	1	-1
20401040301	220	0	-1	0	0	1	1	1	0	-1	0	0	1	0	0	-1	1	1	1	1	0	1	-1	-1
20401020304	149	1	1	-1	1	-1	1	0	-1	1	-1	1	0	1	1	-1	0	1	1	-1	0	0	-1	-1
20401020303	61	1	1	0	0	0	-1	1	1	1	0	1	1	1	1	0	1	0	-1	-1	1	0	1	1
20401020302	22	0	-1	1	1	1	1	0	1	0	1	0	1	-1	1	-1	-1	1	0	1	-1	0	-1	-1
```

**Sample water use factors**
```
# water use factors																									
AqGwWL	CoGwWL	DoGwWL	InGwWL	IrGwWL	LvGwWL	MiGwWL	ReGwWL	TeGwWL	WsGwWL	AqSwWL	CoSwWL	InSwWL	IrSwWL	MiSwWL	TeSwWL	WsSwWL	InGwRT	InSwRT	STswRT	WSgwRT	WSunkTR	WStrans
1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	1.5	
```

---
# January, Feburary, March (JFM)

| newhydroid       | water use total|                                                                              
| ----------       | ----------- 	|		                                                                               
|440               | 6 				|
|390               | -3				|
|262               | 5 				|
|257               | 0 				|
|220               | 4 				|
|149               | 2 				|
|61                | 10				|
|22                | 3				|


# April, May, June (AMJ)

| newhydroid       | water use total|                                                                              
| ----------       | ----------- 	|		                                                                               
|440               | 0 				|
|390               | 2				|
|262               | -2				|
|257               | -6				|
|220               | 4				|
|149               | 1 				|
|61                | 4				|
|22                | -3				|

# July, August, September (JAS)

| newhydroid       | water use total|                                                                              
| ----------       | ----------- 	|		                                                                               
|440               | -2 			|
|390               | -3				|
|262               | 1				|
|257               | -5				|
|220               | 0				|
|149               | 0 				|
|61                | 1				|
|22                | -3				|

# October, November, December (OND)

| newhydroid       | water use total|                                                                              
| ----------       | ----------- 	|		                                                                               
|440               | -3 			|
|390               | 1				|
|262               | -1				|
|257               | 0				|
|220               | -3				|
|149               | 5				|
|61                | -4				|
|22                | -3				|