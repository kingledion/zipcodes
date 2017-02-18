# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:29:01 2017

@author: dhartig
"""

import mysql.connector, csv, re

def read_files():
    data = {}
    
    # open the database
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    try:
        zip_cursor.execute("DROP TABLE counties;")
    except mysql.connector.errors.ProgrammingError as e:
        pass

    query = "CREATE TABLE counties (id VARCHAR(8), name VARCHAR(32), state VARCHAR(32), area FLOAT, pop_2010 INT, pop_2000 INT, pop_1990 INT, pop_1980 INT, pop_1970 INT, pop_1960 INT, pop_1950 INT, pop_1940 INT, pop_1930 INT, pop_1920 INT,"
    query += " pop_1910 INT, pop_1900 INT, pop_1890 INT, pop_1880 INT, pop_1870 INT, pop_1860 INT, pop_1850 INT, pop_1840 INT, pop_1830 INT, pop_1820 INT, pop_1810 INT, pop_1800 INT, pop_1790 INT)"
    zip_cursor.execute(query)
    
    with open('data/county_geo.csv', 'r', encoding = 'latin-1') as f: 
        rdr = csv.reader(f, delimiter=',', quotechar = '"')
        next(rdr) # not using a dictreader, skip the column headers
        next(rdr)
        
        for line in rdr:
            county, state = line[2].split(",")
            cnt = county.split(" ")
            if len(cnt) > 3 and cnt[-3] == "City" and cnt[-2] == 'and':
                county = " ".join(cnt[:-3])
            elif len(cnt) > 2 and cnt[-2] == "Census":
                county =  " ".join(cnt[:-2])
            elif cnt[0] == "District" and cnt[1] == "of" and cnt[2] == "Columbia":
                county = "Washington DC"
            elif cnt[-1].upper() == "CITY" and state.strip() != "Virginia":
                county = " ".join(cnt)
            else:
                county = " ".join(cnt[:-1]) 
            #print({'id': line[1], 'name': county.strip().upper(), 'state': state.strip().upper(), 'area': float(line[6])/1000000})
            data[line[1]] = {'id': line[1], 'name': county.strip().upper(), 'state': state.strip().upper(), 'area': float(line[6])/1000000}
            
    print('done with geos')
    
    with open('data/county_census_2010.csv', 'r', encoding = 'latin-1') as f:
        rdr = csv.reader(f, delimiter=',', quotechar = '"')
        next(rdr)
        next(rdr)
        
        for line in rdr:
            data[line[1]]['pop_2010'] = line[3]
            
    print('done with 2010')
            
    with open('data/county_census_2000.csv', 'r', encoding = 'latin-1') as f:
        rdr = csv.reader(f, delimiter=',', quotechar = '"')
        next(rdr)
        next(rdr)
        
        for line in rdr:
            if line[1] in data:
                data[line[1]]['pop_2000'] = line[3]
            
    print('done with 2000')
    
    name_data = {data[key]['name']+data[key]['state']: data[key] for key in data}
    
    state_flag = False
    with open('data/county_census_pre1990.csv', 'r', encoding = 'latin-1') as f:
        rdr = csv.reader(f, delimiter=',', quotechar = '"')
        
        state = ""
        st_len = 0
        for line in rdr:
            #print(line)
            if line[0] and line[1] and line[1].strip() != '---':
                if state_flag:
                    state = line[0].strip().upper()
                    if state == "DIST. OF COLUMBIA":
                        state = "DISTRICT OF COLUMBIA"
                    state_flag = False
                elif line[0] in set(['County', 'Name', 'Subdivision', 'Parish']):
                    st_len = line.index("Notes")
                    state_flag = True
                else:
                    cnt = line[0].strip()
                    cnt = cnt.split(" ")
                    if len(cnt) > 3 and cnt[-3] == "City" and cnt[-2] == 'and':
                        county = " ".join(cnt[:-3])
                    elif len(cnt) > 2 and cnt[-2] == "Census":
                        county =  " ".join(cnt[:-2])
                    elif cnt[0] == "Dist." and cnt[1] == "of" and cnt[2] == "Columbia":
                        county = "Washington DC"
                    elif cnt[-1] == 'Borough':
                        county = " ".join(cnt[:-1])
                    else:
                        county = " ".join(cnt)
                    key = county.strip().upper()+state
                    d = {"pop_{0}".format(2000-10*i): int(line[i].replace(',', '')) for i in range(1,st_len) if line[i] and line[i].strip() != '---'}
                    #print(key, d)
                    if key in name_data:
                        name_data[key].update(d)

                    
                    
    
    ins = "INSERT INTO counties ({0}) VALUES ({1});"
    for i in data:
        dfields = data[i].keys()
        dvals = ['"' + str(data[i][x]) + '"' if x in set(['name', 'state']) else str(data[i][x]) for x in dfields]
        #print(ins.format(", ".join(dfields), ", ".join(dvals)))
        zip_cursor.execute(ins.format(", ".join(dfields), ", ".join(dvals)))
        
    zip_db.commit()
    
    
def naics_parse():
    
        # open the database
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    try:
        zip_cursor.execute("DROP TABLE county_emp;")
    except mysql.connector.errors.ProgrammingError as e:
        pass

    query = "CREATE TABLE county_emp (fips INT, naics INT, flag VARCHAR(8), emp INT, pay INT);"
    zip_cursor.execute(query)
    
    with open('data/cbp14co.txt', 'r') as f: 
        rdr = csv.reader(f, delimiter=',', quotechar = '"')
        next(rdr)
        
        insert_obj = {}
        old = None
        
        for line in rdr: 
            if not old:
                old = int(line[0] + line[1])
            iden = re.sub('-|/', '', line[2])
            iden = int(iden) if iden else ''
            if iden in set([11, 21, 22, 23, 31, 42, 44, 48, 51, 5112, 517, 518, 51913, 52, 53, 54, 5415, 55, 56, 61, 62, 71, 72, 81, 92]):
                new = int(line[0] + line[1])
                if new != old:
                    insert_old(zip_cursor, insert_obj, old)
                    old = new
                insert_obj[iden] = line
                
    zip_db.commit()
                    
            
def insert_old(cursor, obj, code):
    ins_string = "INSERT INTO county_emp (fips, naics, flag, emp, pay) VALUES (%s, %s, %s, %s, %s)"
    
    ins_data = [(code, k, obj[k][3], obj[k][5], obj[k][9]) for k in obj]
    
    cursor.executemany(ins_string, ins_data)
    
    print("Inserted", code)
    
    
    
    
                
        
        
    
naics_parse()
#read_files()