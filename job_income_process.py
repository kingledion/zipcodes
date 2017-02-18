
import mysql.connector

from job_income_constants import id_map, cost_of_living, occupation_full_code, metro_splits
                  
                  

def get_occ_list(data_from_server):
    return [(x, occupation_full_code[x]) for x in data_from_server]
    

def get_occ_options():
    option_list  = [key for key in occupation_full_code]
    return option_list
    
    
    
    
    
    

def get_numbers_for_occ(occ_list, base_threshold):
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()	
    
    data = {}
    
    metro_list = sorted(cost_of_living.keys())

    query = "SELECT * FROM income_data WHERE metro_code = {0} and occ_code in ({1})"
    for metro_key in metro_list:
        metro_data = {}
         
        threshold = 100 / cost_of_living.get(metro_key, 100) * base_threshold
        
        for oc in occ_list:
    
            zip_cursor.execute(query.format(metro_key, ", ".join(["'"+x+"'" for x in oc[1]])))
            for line in zip_cursor: 
                metro_data['name'] = line[1]
       
                if int(line[5]) > threshold:
                    perc = 0.95 # make this better!!!!!
                elif int(line[6]) > threshold:
                    perc = (int(line[6]) - threshold) / (int(line[6]) - int(line[5])) * .15 + .75
                elif int(line[7]) > threshold:
                    perc = (int(line[7]) - threshold) / (int(line[7]) - int(line[6])) * .25 + .5
                elif int(line[8]) > threshold:
                    perc = (int(line[8]) - threshold) / (int(line[8]) - int(line[7])) * .25 + .25   
                elif int(line[9]) > threshold:
                    perc = (int(line[9]) - threshold) / (int(line[9]) - int(line[8])) * .15 + .10
                else:
                    perc = int(line[9]) / threshold * .1
                
                prev = metro_data.get(oc[0], (0, 0, 0.0))
                metro_data[oc[0]] = (prev[0] + int(int(line[3]) * perc), prev[1] + line[3], prev[2] + float(line[4] * line[3])/1000000)
            
        print("Adding {0} to data".format(metro_key))
        data[metro_key] = metro_data

    return data
    

# Merge metro areas
def merge_metros(data):
    
    for top_id in id_map:
    
        for to_merge in id_map[top_id]:
            for occ_key in data[to_merge].keys():
                if occ_key != 'name':
                    prev = data[top_id].get(occ_key, (0, 0, 0.0))
                    mer = data[to_merge].get(occ_key, (0, 0, 0.0))
                    data[top_id][occ_key] = (prev[0] + mer[0], prev[1] + mer[1], prev[2] + mer[2])
           
            data.pop(to_merge)
            
    for split_id in metro_splits:
        first, second = metro_splits[split_id]
        for occ_key in data[split_id].keys():
            if occ_key != 'name':
                data[first][occ_key] = data[first].get(occ_key, 0) + data[split_id].get(occ_key, 0) / 2
                data[second][occ_key] = data[second].get(occ_key, 0) + data[split_id].get(occ_key, 0) / 2
                
        data.pop(split_id)
            
    return data
        
def add_total_column(data):
    for metro_key in data:
        data[metro_key]['Total'] = [sum(y) for y in [data[metro_key][x] for x in data[metro_key] if x != 'name']]
        
    return data
               

def output_to_file(data, fields):
    #fields = []
    #fields.append('Total')
    out_file = '/opt/apps/zipcodes/output.csv'
#    categories = [('Software', 'comp'), ('Computer Support', 'csupp'), ('Computer Hardware', 'hard'), ('Applied Math', 'math'), ('Biotech', 'bio'), 
#                  ('Chem and Mats', 'mats'), ('Engineering', 'eng'), ('Finance', 'fin'), ('Law', 'law'), ('Medical', 'med'), ('Business Operations', 'bus'), ('Total', 'tot')]
    f = open(out_file, 'w')
    #print([(metro_key, data[metro_key].get('Total', (0, 0, 0.0))) for metro_key in data])
    #sorted_list = sorted([(metro_key, data[metro_key].get('Total', (0, 0, 0.0)[0])) for metro_key in data], key = lambda x: x[1], reverse=True)
    
    f.write("Name|" + "|||".join(fields))
    f.write("\n")
    for row in data:
        metro_data = data[row]
        #print(metro_data)
        f.write(metro_data.get('name', 'UNKNOWN NAME') + "|")
        f.write("|".join(["|".join([str(y) for y in metro_data.get(x, (0, 0, 0))]) for x in fields]))
        f.write("\n")
        



