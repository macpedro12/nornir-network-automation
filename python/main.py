import sys
from importlib import import_module

from src.database import database
from src.database import get_device_config
from src.service_provider.service_provider import create_service

def new_service():
    
    service_info = create_service()
    database.database_insert(service_info)

    
    
if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])