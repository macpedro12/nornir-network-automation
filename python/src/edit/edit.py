from database.database import database_insert, database_get
from service_provider.service_provider import create_service

import glob

def edit(id):
    
    

    data = database_get(id)
    service_applied = data[1]
    applied_service = data[2]
    
    service_edit = create_service(service_applied)
    
    
if __name__ == "__main__":
    edit(2)