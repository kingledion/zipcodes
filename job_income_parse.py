import csv, mysql.connector
import numpy as np

                             
# generator to return useful args from the csv, formatted appropriately
def csvArgs(row):
    for i in [row [6], row[11], row[18], row[19], row[20], row[21], row[22]]:
        try:
            r = int(i.replace(',', ''))
        except ValueError:
            if i == "#":
                r = 187200
            else:
                r = -1
        finally:
            yield r

def main():            
    parse_in()
    make_estimates()
 #   merge_metros()

def parse_in():
    # Declare database and cursor     
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    # Drop previously existing tables if they exists
    try:
        zip_cursor.execute("DROP TABLE income_data;")
    except mysql.connector.errors.ProgrammingError:
        pass
    
    try:
        zip_cursor.execute("DROP TABLE income_processed;")
    except mysql.connector.errors.ProgrammingError:
        pass
    
    query = "CREATE TABLE income_data (metro_code VARCHAR(8), name VARCHAR(64), occ_code VARCHAR(8),"
    query += " employment INT, mean INT, pct_10 INT, pct_25 INT, pct_50 INT, pct_75 INT, pct_90 INT);"
    zip_cursor.execute(query)
    
    query = 'INSERT INTO income_data (metro_code, name, occ_code, employment, mean, pct_10, pct_25, pct_50, pct_75, pct_90)'
    query += ' VALUES( "{0}", "{1}", "{2}", {3}, {4}, {5}, {6}, {7}, {8}, {9});'
    
    all_cities = set([])
    with open('MSA_M2015_dl.csv', 'r') as csv_in:
        csv_reader = csv.reader(csv_in, delimiter = ",", quotechar = '"')
        next(csv_reader)
        
        for row in csv_reader:
            
            first_city = row[2].split(",")[0]
            first_city = first_city.split("-")[0]  
            if first_city not in all_cities:
                print("Processing", first_city)
                all_cities.add(first_city)
            
            args = [row [6], row[11], row[18], row[19], row[20], row[21], row[22]]
            args = [i for i in csvArgs(row)]
            
            zip_cursor.execute(query.format(row[1], first_city, row[3], *args))
    
    zip_db.commit()
 
def make_estimates():
    
    # Declare database and cursor     
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
 
    # get a list of all metros and comparison fields
    zip_cursor.execute("SELECT metro_code FROM income_data WHERE occ_code = '00-0000' ORDER BY employment * mean DESC;" )   
    all_metros = [i[0] for i in zip_cursor.fetchall()]

    # metro name dict
    zip_cursor.execute("SELECT metro_code, name from income_data WHERE occ_code = '00-0000';")
    metro_names = {key: value for (key, value) in zip_cursor.fetchall()}
    
    
    # build a list of data to compare
    compare_data = {}
    for met in all_metros:
        print("Getting data for", metro_names[met])
        query = "SELECT occ_code, employment, mean FROM income_data WHERE metro_code = '{0}';".format(met)
        zip_cursor.execute(query)
        compare_data[met] = {}
        for row in zip_cursor:
            compare_data[met][row[0]+ "_emp"] = int(row[1])
            compare_data[met][row[0]+ "_mean"] = int(row[2])
            
    # for each metro select the 10 closest greater and less than in total economy, then calculate similarity scores for them, then put the top 5 scores into similar_metros
    similar_metros = {}
    for i in range(len(all_metros)):
        met_proc = all_metros[i]
        met_proc_d = compare_data[met_proc]
        first= max(0, i - 10)
        last  = min(len(all_metros), i + 10)
        working_list = []
        for met_comp in [x for x in all_metros[first:last] if x not in set([met_proc])]: # iterate over the 10 closest to the metro in question
            met_comp_d = compare_data[met_comp]
            a1 = []
            a2 = []
            for key in met_proc_d.keys() & met_comp_d.keys():
                if met_proc_d[key] >= 0 and met_comp_d[key] >= 0:
                    a1.append(float(met_proc_d[key]))
                    a2.append(float(met_comp_d[key]))
            
            working_list.append((met_comp, np.dot(a1, a2) / max(np.dot(a2, a2), np.dot(a1, a1)))) # scalar projection of a2 (the comparison) onto a1
        working_list = sorted(working_list, key=lambda x: x[1], reverse=True)
        similar_metros[met_proc] = [x[0] for x in working_list[0:5]]
#        print(metro_names[met_proc], "closest are:", [metro_names[x] for x in similar_metros[met_proc]])

     
    rep_labels = ['employment', 'mean', 'pct_10', 'pct_25', 'pct_50', 'pct_75', 'pct_90']
    query1 = "SELECT DISTINCT occ_code FROM income_data WHERE metro_code = '{0}'"
    query2 = "SELECT employment, mean, pct_10, pct_25, pct_50, pct_75, pct_90 FROM income_data WHERE metro_code = {0} and occ_code = '{1}';"
    query3 = "SELECT {0} FROM income_data WHERE metro_code in ({1}) AND occ_code = '{2}';"
    insert = "UPDATE income_data SET {0} = {1} WHERE metro_code = {2} and occ_code = '{3}';"
    for met in all_metros:
        print("Making replacements for", metro_names[met])
        zip_cursor.execute(query1.format(met))
        for occ in [x[0] for x in zip_cursor.fetchall()]:
            zip_cursor.execute(query2.format(met, occ))
            occ_data = zip_cursor.fetchone()
            for i in range(len(occ_data)):
                if occ_data[i] < 0:
                    zip_cursor.execute(query3.format(rep_labels[i], ", ".join(similar_metros[met]), occ))
                    val_data = [x[0] for x in zip_cursor.fetchall() if x[0] >= 0]
                    if len(val_data) == 0:
                        val_to_use = 50 #if there are zero in the comparables, there still have to be at least SOME in this metro area...50 is as good as anything
                    else:
                        val_to_use = np.average(val_data)
                    zip_cursor.execute(insert.format(rep_labels[i], val_to_use, met, occ))
                    print("Replacing {0} in {1} in {2} with {3}".format(rep_labels[i], occ, metro_names[met], val_to_use))
        print("Done with {0}".format(metro_names[met]))
        zip_db.commit()
                     
#def calculate_scores():
        
           
           # CAN'T USE THIS!!! NOT UNTIL COST OF LIVING IS CALCULATED!!!
def merge_metros():
    # Declare database and cursor     
    zip_db = mysql.connector.connect(user='dbuser', password='dbpass', database='zipcode')
    zip_cursor = zip_db.cursor()
    
    # metro name dict
    zip_cursor.execute("SELECT metro_code, name from income_data WHERE occ_code = '00-0000';")
    metro_names = {key: value for (key, value) in zip_cursor.fetchall()}
    
    rep_labels = ['employment', 'mean', 'pct_10', 'pct_25', 'pct_50', 'pct_75', 'pct_90']
    query1 = "SELECT occ_code, employment, mean, pct_10, pct_25, pct_50, pct_75, pct_90 FROM income_data WHERE metro_code = {0}"
    insert = "UPDATE income_data SET {0} WHERE metro_code = {1} and occ_code = '{2}';"
    
    for top_id in id_map:
        print("Top city is {0}".format(metro_names[str(top_id)]))
        print("Merge cities are {0}".format([metro_names[str(x)] for x in id_map[top_id]]))
        data_to_add = {}
        for metro_id in [top_id] + id_map[top_id]:
            print("Getting data for {0}".format(metro_names[str(metro_id)]))
            zip_cursor.execute(query1.format(metro_id))
            for line in zip_cursor.fetchall():
                new_count = int(line[1])
                new_incomes = np.asarray(line[2:], dtype=int) 
                if line[0] in data_to_add:
                    old_count = data_to_add[line[0]][0]
                    old_incomes = np.asarray(data_to_add[line[0]][1:], dtype=int)
                    
                    new_incomes = (new_incomes * new_count + old_incomes * old_count) // (new_count + old_count)
                    new_count = old_count + new_count

                data_to_add[line[0]] = np.concatenate((np.asarray([new_count]), new_incomes), axis=1)
           
        print("Writing data for {0}".format(metro_names[str(top_id)]))
        for l in data_to_add:
            string_data = [str(x) for x in data_to_add[l]]
            formatted_data = ["{0} = {1}".format(x, y) for x, y in zip(rep_labels, string_data)]
            zip_cursor.execute(insert.format(", ".join(formatted_data), top_id, l))
        zip_db.commit()

            
        # CURRENTLY THE OLD METROS ARE LEFT AS IS AND NOT DELETED!!!!
                
       
            
            
main()                       
