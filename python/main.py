import sys
from importlib import import_module
from nornir import InitNornir
from os import listdir

from src.database import database
from src.service_provider.service_provider import create_service as cs
from src.rollback.rollback import rollback as rb

def new_service(service):
    
    services_list = listdir("./python/src/service_provider/services/")
    service = str(service).replace(" ","").lower()
        
    if service in services_list:
        service_info = cs(service)
        database.database_insert(service_info)
    else:
        print(f"Service doesn't exist, follow the services available:\n", [service for service in services_list])

def rollback(id):
    
    rollback_status = rb(id)
    database.database_update(id,'status',rollback_status)
   
if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    try:
        globals()[args[1]](*args[2:])
    except IndexError:
        print('Please, select a function, ex: new_service "service"')
    except KeyError:
        print('Function do not exist, to create a new service use: new_service "service", to execute a rollback on service use: rollback id')