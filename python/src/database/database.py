import os
import shutil
import psycopg2

from database.service_object import Service

def database_connection():
    
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor()
        
    cur.execute('INSERT INTO service (service_id,service_name,applied_config,initial_config,status) VALUES (%s,%s,%s,%s,%s)',
                (1,'teste-service','ip 19.1.1.1','no ip','applied'))
    
    """     INSERT INTO service
    (service_id,service_name,applied_config,initial_config,status)
    VALUES(2,'teste-service2','ip 19.1.1.12','no ip2','applied2');
    """
    cur.execute('SELECT * FROM service')
    rows = cur.fetchall() 
    
    print(rows)
    
    cur.close()
    conn.close()

# This script will be used to create the database
# Another script will handle the rollback
def database_insert(id,device,service_config):
        
    # 1. Generate Service ID
    
    # 2. Generate applied config
    
    # 3. Generate service rollback config or get previous config
    
    print()

#Used to consult the database 
def database_get(id,device,service_config):
        
    # 1. Generate Service ID
    
    # 2. Generate applied config
    
    # 3. Generate service rollback config or get previous config
    
    print()