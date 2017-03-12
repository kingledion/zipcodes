# -*- coding: utf-8 -*-

import metro_density_utils as mdu, csv, numpy as np
from rtree import index
from math import cos, radians, pi

db, cursor = mdu.opendb()

class station:
    
    def __init__(self, lat, lon, datadict = {}):
        self._data = datadict
        self._data['lat'] = float(lat)
        self._data['lon'] = float(lon)
        
    def __getitem__(self, key):
        if key not in self._data:
            raise IndexError(key)
        return self._data[key]
        
    def __setitem__(self, key, value):
        self._data[key] = value
        
    def __hash__(self):
        return hash((self._data['lat'], self._data['lon']))
        
    def __eq__(self, other):
        return True if self._data['lat'] == other._data['lat'] and  self._data['lon'] == other._data['lon'] else False

with open('/opt/school/stat672/subway/subwaygeo.csv', 'r') as csvin:
    rdr = csv.reader(csvin, delimiter = ';')
    
    idx = index.Index()
    stations = []
    
    for row in rdr:
        
        if len(row) > 2:
                   
            d = mdu.est_density(cursor, float(row[2]), float(row[1]))
            s = station(row[1], row[2], {**d, **{'name': row[0]}})     
            stations.append(s)
            idx.insert(0, (s['lon'], s['lat'], s['lon'], s['lat']), s)
            
    print("Density estimate and index built")
    

# calculate latitude degrees to 1 km
ns_deg = 1.0/110.574

            
for s in stations:
    n = 10000
    # calculate lon degrees to 1km
    ew_deg = 1.0/111.320/cos(radians(s['lat']))

    Theta = np.random.randn(n, 2)
    R = np.sqrt(np.random.rand(n))
    vectors = Theta * np.stack([R*ew_deg / np.linalg.norm(Theta, axis=1), R*ns_deg / np.linalg.norm(Theta, axis=1)], axis=1)
      
    count = sum(1 if [n for n in idx.nearest((v[0] + s['lon'], v[1] + s['lat'], v[0] + s['lon'], v[1] + s['lat']), objects='raw')][0] == s else 0 for v in vectors)
    # area of a 1km radius circle is pi
    print(s['name'], "{0:.2f}".format(count*pi/10000))
    s['area'] = count*pi/10000
    
printlist = sorted(stations, key=lambda x: x['area'] * (x['popdensity'] + x['empdensity']))

for s in printlist:
    print(s['name'], s['area'], s['popdensity'], s['empdensity'])


        


