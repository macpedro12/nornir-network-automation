import sys
from importlib import import_module
from nornir import InitNornir

from src.database import database
from src.service_provider.service_provider import create_service
from src.rollback.rollback import rollback as rb

def new_service():
    
    service_info = create_service()
    database.database_insert(service_info)

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
        print('Please, select a function, ex: new_service')