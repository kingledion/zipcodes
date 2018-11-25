#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 14:47:19 2018

@author: dhartig
"""

from small_zip_assignments import zip_assigns
from functools import reduce
import re, numpy as np, parse_functions as pf, pandas as pd

fields = ['population', 
                  'employment']

def build_dataframe():
    
    #print(pf.read_geography().items())
    geo_data = [(k, v, re.findall("\d+\.\d+", v['location'])) for k, v in pf.read_geography().items()]
    geo_data = [(k, v['area'], float(match[0]), -1*float(match[1])) for k, v, match in geo_data]
    geo_data = pd.DataFrame(geo_data, columns=["zipcode", "area", "lat", "lon"])
    
    pop_data = [(k, v['population']) for k, v in pf.read_population().items()]
    pop_data = pd.DataFrame(pop_data, columns=["zipcode", "population"])
    
    emp_data = [(k, v['name'], v['employment'], v['emp_pay']) for k, v in pf.read_employment().items()]
    emp_data = pd.DataFrame(emp_data, columns=["zipcode", "name", "employment", "total_pay"])
    
    data = reduce(lambda left, right: pd.merge(left, right, how = 'outer', on = 'zipcode'), [geo_data, pop_data, emp_data])
    data = data[data.name.notnull()]
    data = data[data.name != "Unclassified"]
    
    data.set_index('zipcode', inplace=True)
    
    return data

def merge_data(data, primary, toadd):
    keys = ['population', 'employment', 'total_pay']
    #list((set(primary.keys()) | set(toadd.keys())) - set(['zipcode', 'name', 'location']))
    for k in keys:
         data.at[primary, k] += data.at[toadd, k]       
        
#        if k in primary and k in toadd:
#            primary[k] = primary[k] + toadd[k]
#        elif k in toadd:
#            primary[k] = toadd[k]

def assign_zips(data):
    for key in zip_assigns:
        if ~np.isnan(data.at[key, 'population']):
            print("This one has a pop! {0}".format(key))
            input()
        else:
            merge_data(data, zip_assigns[key], key)
            data.drop(key, inplace=True)
            
    return data

def integer_columns(data):
    
    data['population'] = pd.to_numeric(data['population'], downcast="integer")
    data['employment'] = pd.to_numeric(data['employment'], downcast="integer")
    data['total_pay'] = pd.to_numeric(data['total_pay'], downcast="integer")
    
    return data

def fix_no_geo_data(data):
    
    print()
    
    nonames = data[np.isnan(data.area)].groupby('name').sum()
    hasnames = data[~np.isnan(data.area)]
    hasnames = hasnames.fillna(0)
    
    count = 0
    for t in nonames.itertuples():
        count += 1
        name, emp, pay = (t[0], t.employment, t.total_pay)
        
        comps = hasnames[hasnames.name == name]
        
        
        if len(comps.index) > 0:
             
            comps = comps.assign(density=pd.Series((comps.population + comps.employment)/comps.area))
            if len(comps[comps.area > 3.14]) > 0:
                dens_cutoff = max(comps[comps.area > 3.14].density)/2
            else:
                dens_cutoff = 0
            
            addto = comps[comps.density > dens_cutoff]
            
            addlen = len(addto.index)
            
            for idx in list(addto.index):
            
                hasnames.at[idx, 'employment'] += emp/addlen
                hasnames.at[idx, 'total_pay'] += pay/addlen
                
        prog = count/len(nonames.index)
        print("\rResolving null areas: [{0:10s}] {1:.1f}%".format('#' * int(prog * 10) , prog*100), end="", flush=True)
            
    print()
    return hasnames
        

    



def main():
    data = build_dataframe()
    #print(data.loc[data.index.intersection(['27708', '27705', '75261', '76051'])]) 
    #print()
    
    data = assign_zips(data)
    #print(data.loc[data.index.intersection(['27708', '27705', '75261', '76051'])])   
    #print()
    print(data.loc[data['name'] == "New Orleans, LA", :])
    
    data = fix_no_geo_data(data)
    
    data = data.sort_values("employment")
    #print(data)
    #print()
    
    data = integer_columns(data)
    #print(data)
    
    print(data.loc[data['name'] == "New Orleans, LA", :])
    
    
    
    
main()