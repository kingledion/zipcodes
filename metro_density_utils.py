# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 18:14:33 2016

@author: dhartig
"""
from math import sqrt, radians, cos, sin, asin
import numpy as np, mysql.connector

class BadDatabaseException(Exception):
    pass

class zipdata:
    
    def __init__(self, zipcode, x, y, pop, emp, pay, area, name, house):
        self._data = {'zipcode': zipcode, 'lat': float(x), 'lon': float(y), 'pop': int(pop), 'emp': int(emp), 'pay': int(pay), 'area': float(area), 'name': name, 'house': int(house)}
        
    def __getitem__(self, key):
        if key not in self._data:
            raise IndexError(key)
        return self._data[key]
        
    def __hash__(self):
        return int(self._data['zipcode'])
        
    def __eq__(self, other):
        return True if self._data['zipcode'] == other._data['zipcode'] else False
        
    def __repr__(self):
        return ";".join([str(self._data[k]) for k in self._orderedkeys()])
        
    def _orderedkeys(self):
        return ['zipcode', 'lat', 'lon', 'pop', 'emp', 'pay', 'area', 'name', 'house']
        
    def fields():
        return "zip_code, X(location), Y(location), pop, emp, emp_pay, area, name, households"
        
    def fromzip(cursor, zipcode):
        cursor.execute("SELECT " + zipdata.fields() + " from zipcodes WHERE zip_code LIKE '{0}';".format(zipcode))
        r = cursor.fetchall()
        if len(r) > 1:
            raise BadDatabaseException("More than one entry with zipcode {0} in database".format(zipcode))
        return zipdata(*r[0]) if r else None
        
def opendb():
    db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    cursor = db.cursor()
    return db, cursor
    
def get_nearby_zips(cursor, s_lon, s_lat, start_zip = None):
    start = "AND zip_code NOT LIKE '{0}'".format(start_zip) if start_zip else ""     
    query = "SELECT haversine(x(location), y(location), {4}, {5}) as dist, " + zipdata.fields() + " from zipcodes WHERE X(location) BETWEEN {0} AND {1} AND Y(location) BETWEEN {2} AND {3} {6} order by dist limit 50;"

    cursor.execute(query.format(s_lat - .5, s_lat + .5, s_lon - .5, s_lon + .5, s_lat, s_lon, start))
    
    return [(z[0], zipdata(*z[1:])) for z in cursor.fetchall()]  

def get_adjacent(cursor, startzip):
    
    lat, lon = (startzip['lat'], startzip['lon'])
    radius = sqrt(startzip['area'])
    return est_adjacent(cursor, lon, lat, startzip['zipcode'], radius )

def est_adjacent(cursor, s_lon, s_lat, startzip=None, src_radius=1):
    
    rlist = get_nearby_zips(cursor, s_lon, s_lat, startzip)
    
    zip_list = [({'x_dist': (z['lat']-s_lat)*111.045, 'y_dist': (z['lon']-s_lon)*111.045*np.cos(np.radians(s_lat)), 'dist': d*111.045, 'radius': sqrt(z['area'])}, z) for d, z in rlist]
    
    nearest_list = []

    for z, obj in zip_list:
        projs = [np.dot([z['x_dist'], z['y_dist']], [x['x_dist']/x['dist'], x['y_dist']/x['dist']]) for x, o in nearest_list]
        mp = max(projs) if projs else 0
        if  z['dist']/2 < (src_radius + z['radius']) and z['dist']/3 < (src_radius + z['radius'] - mp):
            nearest_list.append((z, obj))
                     
    return [o for x, o in nearest_list]
    
def est_density(cursor, lon, lat):
    
    adj = est_adjacent(cursor, lon, lat)

    data = [(haversine(z['lon'], z['lat'], lon, lat), z['pop']/z['area'], z['emp']/z['area'], z['pay']/z['area'], z['area'], z['zipcode']) for z in adj]
    
    dist_total = sum(d[4]/d[0] for d in data)
    popdensity = sum(d[1]*d[4]/d[0] for d in data)/dist_total
    empdensity = sum(d[2]*d[4]/d[0] for d in data)/dist_total
    paydensity = sum(d[3]*d[4]/d[0] for d in data)/dist_total
      
    return {'popdensity': popdensity, 'empdensity': empdensity, 'paydensity': paydensity}
    
    
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
    
    





    
