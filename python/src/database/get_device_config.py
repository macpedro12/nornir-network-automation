import psycopg2
from nornir_netmiko import netmiko_send_command
   
# Search in the database the last ID used by a service. 
def get_last_id():
    conn = psycopg2.connect( 
        dbname='postgres', 
        user='admin', 
        password='admin123', 
        host="localhost", 
        port="5432" 
    ) 

    cur = conn.cursor()

    cur.execute('SELECT service_id FROM service ORDER BY service_id DESC LIMIT 1')
    last_id = cur.fetchone() 
    
    cur.close()
    conn.close()
    
    return last_id[0]

# Gets the whole router configuration and filter for the first config of the service.
# OBS: Still working on the best way to get the initial config. 
# Routers with imense quantity of configuration would make this proccess slower.
# Also, now we're getting the whole tree from a root config, ex: interface fastEthernet0/0.
# This will probably causes errors if other services changes something especific in one of the branches of an already changed root config.
# In the future will be developed a code that verifies if that config is already applied by a service.
# But for now, this is the best global option that we have, since some configurations have different ways to show then. 
    
def get_initial_config(device_name,nornir_device_object,configs_to_apply): 
    
    
    # Gets all the running configuration from the router
    # [TODO] Check if it's faster to load from the Postgres database or directly from the device. If Postgres is faster, create a new table to store the whole device configuration. 
    #        It can also stores, services applied to then and other configs.
    
    router = nornir_device_object.filter(name=f'{device_name}')
    config = router.run(task=netmiko_send_command,command_string=f"show running-config")

    full_running_config = str(config[f"{device_name}"][0]).splitlines()
    initial_config = []
    
    root_configs = []
 
    for config in configs_to_apply:
        if config[0] != ' ':
            root_configs.append(config)
    
    # Check if the root config that it will be applied is in the actual running config.   
    for config in root_configs:
        
        if config in full_running_config:
            
            initial_config.append(config)
            configIndex = full_running_config.index(config) + 1
            
            # If the root config is there, gets all branches below and add to the initial_config list.
            for runningConfig in full_running_config[configIndex:]:
                if runningConfig[0] == ' ':
                    initial_config.append(runningConfig)
                else:
                    break
    
    
                
    return initial_config
    
if __name__ == "__main__":
   pass