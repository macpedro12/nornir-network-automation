import os
import shutil
import psycopg2

# This script will be used to update the database

def database_update(id, collumn_to_update, data):
    
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor()
    
    cur.execute(f"UPDATE services SET {collumn_to_update} = '{data}' WHERE service_id = {id}")

    conn.commit()
   
    cur.close()
    conn.close()

# This script will be used to create the database
def database_insert(service_info, update_collumn = ''):
    
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor() 
    
    cur.execute('INSERT INTO services (service_id,edit_id,service_applied,service_name,applied_config,initial_config,status) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                    (service_info[0],service_info[1],service_info[2],service_info[3],service_info[4],service_info[5],service_info[6]))

    conn.commit()
   
    cur.close()
    conn.close()

#Used to consult the database 
def database_get(id,collum = ''):
        
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor()
    
    cur.execute(f'SELECT service_id FROM services')    
    existing_ids = cur.fetchall()
    
    # To avoid running through the whole list of IDs more than one time, the ID will be inserted into a tuple.
    id_tuple = (int(id),)
    
    
    if id_tuple in existing_ids:

        if collum == '' :   
            
            cur.execute(f'SELECT * FROM services WHERE service_id = {id}')
            response = list(cur.fetchone())

        else:
            try:
                cur.execute(f'SELECT {collum} FROM services WHERE service_id = {id}')
                response = cur.fetchone()[0]
            except:
                print("Collumn doesn't exists, follow the collumns from the service table: 'service_id','service_name','applied_config','initial_config','status'. ")
            
        cur.close()
        conn.close()
        return response
            
    else:
        print("ID doesn't exist.")
       
if __name__ == "__main__":
   pass