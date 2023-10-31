from database.database import database_insert, database_get, database_delete
from database.get_device_config import get_last_id
from service_provider.service_provider import create_service

import datetime
import psycopg2

# It will retrieve the Edit IDs created for a service and return the last and the first one.
# If it has more edit ids than the range specified bellow, it will delete the last one and insert the new one. (This will happen in the edit function)
# The get_edit_ids function will check if the edit id list is full, depending on the answer return True of False, the first (Only if True) and the last edition IDs.
def get_edit_ids(id):
    
    edit_ids_range = 3
    
    
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor()
    
    
    cur.execute(f'SELECT service_id FROM services WHERE CAST(service_id as TEXT) LIKE \'2.%\' ORDER BY  service_id ASC ')    
    existing_ids = cur.fetchall()
    
    # To avoid running through the whole list of IDs more than one time, the ID will be inserted into a tuple.
    print(existing_ids)
    
    last_edit = float(existing_ids[-1][0])
    print(last_edit)
    
    new_edit = last_edit + 0.1
    print(new_edit)
    
    cur.close()
    conn.close()
    
    if len(existing_ids) >= edit_ids_range:
        
        edit_list_full = True
        oldest_edit = float(existing_ids[0][0])
        print(oldest_edit)
        return [edit_list_full,last_edit,new_edit,oldest_edit]
        
    
    else:
        edit_list_full = False
        return [edit_list_full,last_edit,new_edit]        
        

def edit(id):
    
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host='localhost', 
        port='5432' 
    ) 

    cur = conn.cursor()
    
    date = datetime.datetime.now()
    
    get_edit_response = get_edit_ids(id)
    
    if get_edit_response[0] == True:
        
        database_delete(get_edit_response[3])
        cur.execute('INSERT INTO services (service_id,service_applied,service_name,applied_config,initial_config,status,date) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                (get_edit_response[2],"testeInsertFull","teste","teste","teste","teste",date))
    
    else:
        cur.execute('INSERT INTO services (service_id,service_applied,service_name,applied_config,initial_config,status,date) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                (get_edit_response[2],"testeInsertvacancy","teste","teste","teste","teste",date))
    
    conn.commit()
 
    """ data = database_get(id)
    service_applied = data[1] """
    
    """ try:
        service_edit = create_service(service_applied)
        status = "Edited {id}"
    except:
        print("Not able to edit the service.")
    
    return [id,service_edit[1],service_edit[2],service_edit[3],service_edit[4],status,date] """
    
    
    
if __name__ == "__main__":
    print(edit(2))