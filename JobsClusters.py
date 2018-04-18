#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from math import sin, cos, radians, asin, sqrt, pi

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

class Cluster:
    def __init__(self, name, zcode, jobs, area, lon, lat):
        self.employment = jobs
        self.centroidlongitude = lon
        self.centroidlatitude = lat
        self.ziplist = [zcode]
        self.latlonlist = [(lon, lat, area)]
        self.namelist = {name: jobs}
        
    def addZip(self, name, zcode, jobs, area, lon, lat):
        self.centroidlongitude = (self.centroidlongitude*self.employment + lon*jobs)/(self.employment + jobs)
        self.centroidlatitude = (self.centroidlatitude*self.employment + lat*jobs)/(self.employment + jobs)
        self.employment += jobs
        self.ziplist.append(zcode)
        self.latlonlist.append( (lon, lat, area) )
        self.namelist[name] = self.namelist.get(name, 0) + jobs

    def minRange(self, lon, lat):
        dists = [haversine(lon, lat, y, x) - sqrt(a/pi) for y, x, a in self.latlonlist]
        return min(dists)
    
    def centRange(self, lon, lat):
        return haversine(lon, lat, self.centroidlongitude, self.centroidlatitude)
    
    def getZips(self):
        return self.ziplist
    
    def getEmployment(self):
        return self.employment
    
    def isLinked(self, other):
        print("Comparing", self.ziplist[0], "with", other.getZips()[0])
        dists = [other.minRange(lon, lat) - sqrt(area/pi) for lon, lat, area in self.latlonlist]
        for d, z in zip(dists, self.ziplist):
            print(">>>", z, d)
        return min(dists) <= 1
    
    def _mergedata(self):
        return self.centroidlongitude, self.centroidlatitude, self.employment, self.latlonlist
    
    def getName(self):
        names = sorted(list(self.namelist.items()), key=lambda x: x[1], reverse=True)
        return names[0][0]
       
    def merge(self, other):
        lon, lat, jobs, lllist = other._mergedata()
        self.centroidlongitude = (self.centroidlongitude*self.employment + lon*jobs)/(self.employment + jobs)
        self.centroidlatitude = (self.centroidlatitude*self.employment + lat*jobs)/(self.employment + jobs)
        self.employment += jobs
        
        self.ziplist.extend(other.getZips())
        self.latlonlist.extend(lllist)
        
            
                
    
zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
zip_cursor = zip_db.cursor()

query = "SELECT name, zipcode, employment, area, Y(location), X(location)  FROM zipcodes WHERE (employment - population*2/3) > 0 ORDER BY (case when area > 0.1 then employment/area else employment*10 end) desc;"
zip_cursor.execute(query)
data = zip_cursor.fetchall()

clusters = []

for name, zcode, emp, area, lon, lat in data:
    print(zcode)
    nearby = [(i, c.minRange(lon, lat)) for i, c in enumerate(clusters) if c.centRange(lon, lat) < 10]
    if nearby:
        nearby = [(i, c.minRange(lon, lat)) for i, c in enumerate(clusters) if c.minRange(lon, lat) < sqrt(area/pi) + 1]
        if nearby:
            i, c = min(nearby, key = lambda x: x[1])
            print("Adding cluster to ", clusters[i].getZips()[0])
            clusters[i].addZip(name, zcode, emp, area, lon, lat)

        else:  
            print("Stand alone cluster", zcode)
            clusters.append(Cluster(name, zcode, emp, area, lon, lat))
            i = -1
            
        if len(nearby) > 1:
            for j, rng in nearby:
                if j != i and clusters[i].isLinked(clusters[j]):
                    print("Merging", clusters[i].getZips()[0], 'and', clusters[j].getZips()[0])
                    print(clusters[i].getZips())
                    print(clusters[j].getZips())
                    #input()
                    clusters[i].merge(clusters[j])
                    del clusters[j]
    else:
        print("Stand alone cluster", zcode)
        clusters.append(Cluster(name, zcode, emp, area, lon, lat))

        
clusters.sort(key= lambda c: c.getEmployment(), reverse=True)
for c in clusters:
    if c.getEmployment() > 100000:
        print(c.getEmployment(), c.getName())
        


