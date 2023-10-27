import os
import shutil
import psycopg2

from database.service_object import Service

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
def database_get(id,device,service_config):
        
    # 1. Generate Service ID
    
    # 2. Generate applied config
    
    # 3. Generate service rollback config or get previous config
    
    print()