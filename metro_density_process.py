# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 18:14:33 2016

@author: dhartig
"""

import mysql.connector, numpy as np, metro_density_utils as mdu
from metro_density_assignments import list_of_all


def test_main():
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    for r in mdu.get_adjacent(zip_cursor, mdu.zipdata.fromzip(zip_cursor, '10017')):
        print(r['name'], r['zipcode'])
        
def main():
    
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    summary = []
    
    for start, name in list_of_all:
    
        ret = build_min_area(zip_cursor, start, 25)
        summary.append([name] + [int(x) for x in ret])
        print(name)
        
    #summary = sorted(summary, key = lambda x: x[1] + x[2], reverse = True)
        
    #colwidth = max(len(str(word)) for row in summary for word in row) + 2
    for row in summary:
        print("|".join(str(word) for word in row))#str(word).ljust(colwidth) for word in row))
        
def main2():
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    build_min_area(zip_cursor, 44114, 1000)


def build_min_area(cursor, stringzip, threshold):
    

    
    nextzip = mdu.zipdata.fromzip(cursor, str(stringzip))
    if not nextzip:
        print("Cannot find starting zip {0}".format(stringzip))
        return None

    built = []         
    to_add = set([])
    used = set([nextzip])
    
    while not built or sum([z['area'] for z in built])  < threshold:
        #print("Adding", nextzip['name'], nextzip['zipcode'])
        #print()
        
        built.append(nextzip)
        adj = set(mdu.get_adjacent(cursor, nextzip))
        to_add.update(adj - used)
        used.update(adj)     
              
        sortlist = [((z['emp'] + z['pop'])/z['area'], np.mean([np.linalg.norm([(z['lat'] - y['lat'])*111.045, (z['lon'] - y['lon'])*111.045*np.cos(np.radians(y['lat']))]) for y in built]), z) for z in to_add]
        sortlist = sorted(sortlist, key = lambda x: x[0]/x[1])
        
        #for dens, dist, z in sortlist:
        #    print("\t".join([str(x) for x in [z['name'], z['zipcode'], dens, dist]]))
                   
        nextzip = sortlist[-1][2]
        to_add.remove(nextzip)
        
    
    #printing = [[str(y[x]) for x in ['name', 'zipcode', 'pop', 'emp', 'area']] for y in built] 
    #summary = ["TOTAL", ""] + [str(sum(x)) for x in zip(*((z['pop'], z['emp'], z['area']) for z in built))]
    #colwidth = max(len(word) for row in printing for word in row) + 2
    #for row in printing:
    #    print("".join(word.ljust(colwidth) for word in row))
        
    #print("".join(word.ljust(colwidth) for word in summary))
        
    return [sum(x) for x in zip(*((z['pop'], z['emp'], z['pay']) for z in built))]



        

def build_min_density(zip_db, zip_cursor, start_zip, threshold, done):
    zip_cursor.execute("SELECT zip_code, pop, emp, area, (pop + emp)/area FROM zipcodes WHERE zip_code = {0};".format(start_zip))
        
    process_next = []
    final_list = zip_cursor.fetchall()
    
    while start_zip:
        #print(">>>Starting {0}".format(start_zip))
        nearest = process_zip(zip_cursor, start_zip)
        done.add(start_zip)
        process_next.extend([(x[0], x[1], x[2], x[3], x[4]) for x in nearest if x[0] not in done and x[0] not in set([x[0] for x in process_next])])
        process_next  = sorted(process_next, key = lambda x: x[4], reverse = True)
        working_zip = process_next.pop(0)
        
        #if working_zip[4] < threshold:
        current_area = sum([x[3] for x in final_list])
        if  current_area + working_zip[3] > threshold:
            ratio = (float(threshold) - float(current_area)) / working_zip[3]
            final_list.append((working_zip[0], ratio * working_zip[1], ratio * working_zip[2], threshold - current_area, working_zip[4]))
            start_zip = False
        else:
            final_list.append(working_zip)
            start_zip = working_zip[0]
            
        
    return ([sum([x[1] for x in final_list]), sum([x[2] for x in final_list]), sum([x[3] for x in final_list])], set([x[0] for x in final_list]))
            



main()

    
