import json
from nornir_netmiko import netmiko_send_config
 
from database.database import database_get, database_insert

# It will use dafault on the root config to remove all the config, the it will insert the initial config back to the device.
# In the future it will be created a function to handle multiple services configuring the same root config.

def rollback(id):
    
    applied_config = json.loads(database_get(id,'applied_config'))
    initial_config = json.loads(database_get(id,'initial_config'))
    
    for device in applied_config.keys(): #Can use initial_config too, both of them have the same key values.
        print(applied_config[device][0])
        
        
    return applied_config, initial_config

print(rollback(3))
