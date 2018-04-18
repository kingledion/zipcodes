#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 17:05:56 2018

@author: dhartig
"""

import mysql.connector, numpy as np
from matplotlib import pyplot as plt

cnx = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
cursor = cnx.cursor()


def getDensPop(namelist):
    sums ={}
    names = ", ".join(["'{0}'".format(n) for n in namelist])
    cursor.execute("SELECT population, population/area as density from zipcodes where name in ({0}) order by density;".format(names))
    for p, d in cursor.fetchall():
        bn = int(d/10)
        sums[bn] = sums.get(bn, 0) + p
        
    rng = max(sums.keys()) + 1
        
    sums = [sums.get(i, 0) for i in range(rng)]
    cums = [sum(sums[i:]) for i in range(rng)]
    
    #print(namelist)
    #for i, s, c in zip(range(rng), sums, cums):
    #    print(i*10, s, c)
    #input()

    
    return cums


def getMedian(cums):
    med = cums[-1]/2
    medval = min(cums, key=lambda x: abs(x-med))
    idx = cums.index(medval)
    
    return med, medval, idx

    
cums_ny = getDensPop(['New York, NY', 'Brooklyn, NY', 'Bronx, NY'])
cums_la = getDensPop(['Los Angeles, CA'])
cums_chi = getDensPop(['Chicago, IL'])

print(len(cums_ny), len(cums_la), len(cums_chi))


rng = max([len(l) for l in [cums_ny, cums_la, cums_chi]])

# Pad list to appropriate length
for lst in [cums_ny, cums_la, cums_chi]:
    prepend = [0] * (rng - len(lst)) 
    lst += prepend
  

xs = [i*10 for i in range(rng)]

print(rng, len(xs), len(cums_ny), len(cums_la), len(cums_chi))

print("New York", *getMedian(cums_ny))
print("Los Angeles", *getMedian(cums_la))
print("Chicago", *getMedian(cums_chi))


plt.plot(xs, cums_ny, 'k-', xs, cums_la, 'b-', xs, cums_chi, 'r-')
plt.xlabel("Density", fontsize = 15)
plt.ylabel("Total population", fontsize=15)
plt.show()