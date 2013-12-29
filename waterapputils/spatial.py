# -*- coding: utf-8 -*-
"""
:Module: spatial.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Functions to do spatial analysis on GIS datasets. 

"""

import os
import osgeo.ogr


# use polygon "Intersect" (ArcGIS -> Analysis Tools -> Overlay -> Intersect)
testbasin_poly = osgeo.ogr.Open(r'C:\Users\jlant\jeremiah\temp\testbasin.shp')
gcm_poly = osgeo.ogr.Open(r'C:\Users\jlant\jeremiah\projects\python-projects\waterapputils\data\deltas-gcm\CanES\shapefile\CanES.shp')

shapefile = gcm_poly
num_layers = shapefile.GetLayerCount()

print "Shapefile contains %d layers" % num_layers

print "-----"

for layerNum in range(num_layers) :
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()
    print "Layer %d has spatial reference %s" % (layerNum, spatialRef)
    print "Layer %d has %d features:" % (layerNum, numFeatures)
    print "-----"

data = {}
for featureNum in range(numFeatures):
    feature = layer.GetFeature(featureNum)
    featureName = feature.GetField("Tile")
    data.update({str(featureName): featureNum})
    print "Feature %d has name %s" % (featureNum, featureName)
    
#poly1 = osgeo.ogr.Geometry(gcm_poly)
#poly2 = osgeo.ogr.Geometry(testbasin_poly)

#intersection = poly1.Intersection(poly2)
intersection = gcm_poly.Intersection(testbasin_poly)
print intersection.ExportToWkt()
