
import shapefile
import pyproj
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial


sf = shapefile.Reader("/opt/zipcodes/specific_cities/StatistischeBezirkeAachen.shp")

codes = []
names = []
areas = []

for i in sf.shapeRecords():
	codes.append(i.record[0])
	names.append(i.record[1])
	s = shape(i.shape.__geo_interface__)
	#print(s)
	proj = partial(pyproj.transform, pyproj.Proj(init='epsg:25832'), pyproj.Proj(init='epsg:3857'))
	areas.append(transform(proj, s).area/1000000/1.601/1.601)

padding = max(len(n) for n in names) + 2

for n, a, c in zip(names, areas, codes):
	print("{2} {0} {1}".format(n.ljust(padding), a, str(c) + "   "))

