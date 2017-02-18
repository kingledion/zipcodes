# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 13:16:50 2017

@author: dhartig
"""

import mysql.connector, csv
from county_assignments import *

def build_pop():

    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
        
    groups = {}
    
    for group in assign_list:
        entries = assign_list[group]
        
        zip_cursor.execute("SELECT * FROM counties WHERE id IN ({0});".format(", ".join([str(x) for x in entries])))
        data = zip_cursor.fetchall()
        
        if len(entries) > len(data):
            print(len(entries), "entries and", len(data), "found for", group)
              
        groups[group] = [sum([x[i] if x[i] else 0 for x in data]) for i in range(3, len(data[0]))]
        
        if group in ["Las Vegas", "Phoenix", "Tucson", "Bakersfield", "Fresno", "Inland Empire", "Reno-Carson City"]:
            groups[group][0] = 12000
            
    
    
    g = sorted([(x, groups[x][0], groups[x][1]/groups[x][0]) for x in groups], key = lambda x: x[2], reverse = True)
    
    with open('/home/dhartig/Desktop/counties.csv', 'w') as csvout:
        writer = csv.writer(csvout, delimiter = ',', quotechar = '"')
        for entry in g:
            w = groups[entry[0]]
            if w[0] < 9000:
                print(entry[0], "area is", w[0])
            y = [entry[0]] + [w[0]] + [w[i]/w[0] for i in range(1, len(w))]
            writer.writerow(y)
            
def build_econ():
    
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    groups = []
    
    for group in assign_list:
        entries = assign_list[group]
        
        zip_cursor.execute("SELECT pay, flag, emp FROM county_emp WHERE fips IN ({0}) AND naics = 31;".format(", ".join([str(x) for x in entries])))  
        data = zip_cursor.fetchall()
        if any([x[0] == 0 for x in data]):
            avg_pay = float(sum([x[0] for x in data]))/sum([x[2] for x in data])
            extra_pay = sum([num_size[x[1]] for x in data if x[0] == 0])*avg_pay
            man_sum = sum([x[0] for x in data]) + extra_pay
        else:
            man_sum = sum([x[0] for x in data])
            
            
        zip_cursor.execute("SELECT pay, flag, emp, naics FROM county_emp WHERE fips IN ({0}) AND naics IN (5112, 518, 51913, 5415);".format(", ".join([str(x) for x in entries])))  
        data = {}        
        for entry in zip_cursor.fetchall():
            if entry[-1] in data:
                data[entry[-1]].append(entry[:-1])
            else:
                data[entry[-1]] = [entry[:-1]]
        comp_sum = 0
        for key in data:
            if any([x[0] == 0 for x in data[key]]):
                try:
                    avg_pay = float(sum([x[0] for x in data[key]]))/sum([x[2] for x in data[key]])
                except ZeroDivisionError:
                    avg_pay = nation_pay[int(key)]
                extra_pay = sum([num_size[x[1]] for x in data[key] if x[0] == 0])*avg_pay
                comp_sum += sum([x[0] for x in data[key]]) + extra_pay
            else:
                comp_sum += sum([x[0] for x in data[key]])
                    
        
        
        zip_cursor.execute("SELECT pop_2010 FROM counties WHERE id IN ({0});".format(", ".join([str(x) for x in entries])))
        pop_sum = sum([x[0] for x in zip_cursor.fetchall()])
        
        groups.append((group, pop_sum, man_sum, comp_sum))
        
    g = sorted(groups, key = lambda x: x[1], reverse = True)
    
    with open('/home/dhartig/Desktop/manufacturing.csv', 'w') as csvout:
        writer = csv.writer(csvout, delimiter = ',', quotechar = '"')
        for entry in g:
            writer.writerow(entry)
    
build_econ()
    