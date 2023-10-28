import os
import shutil
import psycopg2

# This script will be used to create the database
def database_insert(service_info):
    
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor()
        
    cur.execute('INSERT INTO service (service_id,service_name,applied_config,initial_config,status) VALUES (%s,%s,%s,%s,%s)',
                (service_info[0],service_info[1],service_info[2],service_info[3],service_info[4]))
    

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
    
    if collum == '' :    
        cur.execute(f'SELECT * FROM service WHERE service_id = {id}')
        response = list(cur.fetchone())
    else:
        try:
            cur.execute(f'SELECT {collum} FROM service WHERE service_id = {id}')
            response = cur.fetchone()[0]
        except:
            print("Collumn doesn't exists, follow the collumns from the service table: 'service_id','service_name','applied_config','initial_config','status'. ")
    
    try:
        
        cur.close()
        conn.close()
        return response
        
    except:
        
        cur.close()
        conn.close()
        pass
       
if __name__ == "__main__":
   pass