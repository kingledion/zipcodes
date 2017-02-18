# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 18:14:33 2016

@author: dhartig
"""
from math import sqrt, pi
import numpy as np

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
        
    def fields():
        return "zip_code, X(location), Y(location), pop, emp, emp_pay, area, name, households"
        
    def fromzip(cursor, zipcode):
        cursor.execute("SELECT " + zipdata.fields() + " from zipcodes WHERE zip_code LIKE '{0}';".format(zipcode))
        r = cursor.fetchall()
        if len(r) > 1:
            raise BadDatabaseException("More than one entry with zipcode {0} in database".format(zipcode))
        return zipdata(*r[0]) if r else None
        
    
def get_nearby_zips(cursor, s_lat, s_lon, start_zip = None):
    start = "AND zip_code NOT LIKE '{0}'".format(start_zip) if start_zip else ""     
    query = "SELECT haversine(x(location), y(location), {4}, {5}) as dist, " + zipdata.fields() + " from zipcodes WHERE X(location) BETWEEN {0} AND {1} AND Y(location) BETWEEN {2} AND {3} {6} order by dist limit 50;"
    
    cursor.execute(query.format(s_lat - .5, s_lat + .5, s_lon - .5, s_lon + .5, s_lat, s_lon, start))
    
    return [(z[0], zipdata(*z[1:])) for z in cursor.fetchall()]
    
    
    

def get_adjacent(cursor, startzip):
    
    s_lat, s_lon = (startzip['lat'], startzip['lon'])
    src_radius = sqrt(startzip['area'])
    
    rlist = get_nearby_zips(cursor, s_lat, s_lon, startzip['zipcode'])
    
    zip_list = [({'x_dist': (z['lat']-s_lat)*111.045, 'y_dist': (z['lon']-s_lon)*111.045*np.cos(np.radians(s_lat)), 'dist': d*111.045, 'radius': sqrt(z['area'])}, z) for d, z in rlist]
    
    nearest_list = []

    for z, obj in zip_list:
        projs = [np.dot([z['x_dist'], z['y_dist']], [x['x_dist']/x['dist'], x['y_dist']/x['dist']]) for x, o in nearest_list]
        mp = max(projs) if projs else 0
        if  z['dist']/2 < (src_radius + z['radius']) and z['dist']/3 < (src_radius + z['radius'] - mp):
            nearest_list.append((z, obj))
        #print(pre, z['zip'], "{0:.2f}".format((src_radius + z['radius'] - mp)), "{0:.2f}".format(src_radius + z['radius']), "{0:.2f}".format(z['dist']), "{0:.2f}".format((src_radius + z['radius'] - mp)/z['dist']*3))
               
    return [o for x, o in nearest_list]
            
    #nearest_list = sorted(nearest_list, key = lambda z: (src_radius+z['radius'])/z['dist'], reverse = True)
    #for z in nearest_list:
    #    print("Proximity add", z['zip'], "{0:.2f}".format((src_radius+z['radius'])/z['dist']))
    
   # for z in zip_list:
   #     if z['zip'] not in nearest_set:
   #         projs = [np.dot([z['x_dist'], z['y_dist']], [x['x_dist']/x['dist'], x['y_dist']/x['dist']]) for x in nearest_list]
   #         truth = [x < y['dist']*1.25 for x, y in zip(projs, nearest_list)]
            #if all(truth) and z['dist'] < (src_radius + z['radius'])*4:
            #    nearest_list.append(z)
            #    print("Projection add", z['zip'])
            
            #for n, p in zip(nearest_list, projs):

            #    print("\t", n['zip'], "{0:.2f}".format(p), "{0:.2f}".format(n['dist']))
                
            
        
            
    #print(pre, z['zip'], ":", "{0:.2f}".format(z['dist']), "{0:.2f}".format(src_radius), "{0:.2f}".format(z['radius']))
    
    
    
def process_zip(zip_cursor, start_zip):
    
    zip_cursor.execute("SELECT X(location), Y(location) FROM zipcodes WHERE zip_code = {0};".format(start_zip))
    s_lat, s_lon = [float(x) for x in zip_cursor.fetchone()]
    

    
    zip_list = [(x[0], x[1], x[2], (x[1]-s_lat)*111.045, (x[2]-s_lon)*111.045*np.cos(np.radians(s_lat)), x[3]*111.045, x[4], x[5], x[6], x[7], x[8], x[9]) for x in zip_list]

    nearest_list = []
    
    for zcode, lat, lon, lat_d, lon_d, dist, pop, empl, emp_pay, area, name, house in zip_list:
        
        if len(nearest_list) > 0:
            calc_lim = np.average([x[3] for x in nearest_list])
        else:
            calc_lim = 0
        
        if len(zip_list) < 4:
            base_lim = np.average([x[3] for x in zip_list])
        else:
            base_lim = np.average([x[3] for x in zip_list[:4]])
        
        dist_lim = max(calc_lim, base_lim) * 4
        
        
        if nearest_list and dist > dist_lim: # once we are 5 times as far away as the average, give up

            break
        

        
        projs = [(np.dot([lat_d, lon_d], [x[1]/x[3], x[2]/x[3]]), x[3]) for x in nearest_list]
        truth = [x < y for x, y in projs]
        
            
        if len(truth) == 0 or np.all(truth):
            #print("Adding zip {0}".format(zcode))
            nearest_list.append((zcode, lat_d, lon_d, dist, pop, empl, emp_pay, area, lat, lon, house))
                        
               
    return [{'zcode': x[0], 'lat': x[8], 'lon': x[9], 'dist': x[3], 'pop': x[4], 'emp': x[5], 'emp_pay': x[6], 'area': x[7], 'name': x[8], 'households': x[10]} for x in nearest_list]
      
zip_assigns = {'75261': '76051',
               '60666': '60018',
               '06520': '06510',
               '08544': '08542',
               '13244': '13210',
               '27708': '27705',
               '28255': '28202',
               '37232': '37212',
               '37662': '37660',
               '39568': '39567',
               '46285': '46204',
               '48090': '48092',
               '55144': '55119',
               '60208': '60201',
               '61629': '61602',
               '61710': '61701',
               '66251': '66211',
               '72716': '72712',
               '76101': '76104',
               '77205': '77032',
               '78288': '78205',
               '84152': '84105',
               '84602': '84606',
               '64141': '64106',
               '10281': '10280',
               '15275': '15108',
               '17604': '17601',
               '06338': '06339',
               '90509': '90503',
               '10041': '10004',
               '60566': '60563',
               '30320': '30337',
               '17605': '17601',
               '54903': '54902',
               '01805': '01803',
               '03061': '03060',
               '06183': '06103',
               '08541': '08542',
               '10286': '10007',
               '16531': '16511',
               '18711': '18702',
               '19486': '19454',
               '19718': '19713',
               '19850': '19802',
               '21287': '21231',
               '22908': '22903',
               '24514': '24502',
               '26506': '26505',
               '27157': '27101',
               '27710': '27705',
               '29425': '29403',
               '29808': '29801',
               '30063': '30060',
               '33159': '33131',
               '37831': '37830',
               '40536': '40508',
               '45469': '45409',
               '48265': '48225',
               '48674': '48642',
               '50392': '50309',
               '52498': '52402',
               '54306': '54303',
               '55479': '55401',
               '60179': '60192',
               '60675': '60608',
               '68198': '68131',
               '71130': '71103',
               '75275': '75205',
               '77225': '77054',
               '77555': '77550',
               '78682': '78664',
               '80208': '80210',
               '80935': '80910',
               '84132': '84112',
               '84150': '84101',
               '91521': '91506',
               '91522': '91505',
               '93599': '93544',
               '94143': '94117',
               '60196': '60195',
               '83707': '83716',
               '10104': '10019',
               '17405': '17401',
               '10166': '10017',
               '95353': '95354',
               '83415': '83404',
               '10118': '10001',
               '10105': '10019',
               '67201': '67202',
               '07962': '07960',
               '08543': '08542',
               '91109': '91103',
               '84016': '84015',
               '50704': '50702',
               '95052': '95050',
               '19612': '19604',
               '28219': '28202',
               '70509': '70501',
               '55440': '55401',
               '74101': '74103'}




    
