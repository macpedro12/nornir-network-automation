import json
from nornir_netmiko import netmiko_send_config
from nornir import InitNornir
 
from database.database import database_get

# It will use dafault on the root config to remove all the config, the it will insert the initial config back to the device.
# In the future it will be created a function to handle multiple services configuring the same root config.

def rollback(id):
    
    nr = InitNornir(config_file="config.yaml")
    
    status = database_get(id,'status')
    
    # Check if the configuration is applied.
    if status == "Applied":
        
        applied_config = json.loads(database_get(id,'applied_config'))
        initial_config = json.loads(database_get(id,'initial_config'))    
           
        for device in applied_config.keys(): #Can use initial_config too, both of them have the same key values.
            
            router = nr.filter(name=f'{device}')
            rollback_applied = router.run(task=netmiko_send_config,config_commands=f"default {applied_config[device][0]}")
            rollback_to_initial = router.run(task=netmiko_send_config,config_commands=initial_config[device])
                    
            if "TCP connection to device failed." in str(rollback_applied[device][0]):
                print(f'Unable to connect to the device {device}')
                status = "Rollback Failed"
            else:
                print(f"Rollback executed with success")
                status = "Rollback Executed"
    else:
        
        print("Unable to rollback non-applied service.")
        
    return status



if __name__ == "__main__":
   pass