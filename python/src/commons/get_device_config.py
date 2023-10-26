import psycopg2
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")
device = 'r1'
command = ['interface FastEthernet0/1']

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
    
def get_initial_config(device_name,nornir_device_object,command):
    
    
    router = nornir_device_object.filter(name=f'{device}')
    config = router.run(task=netmiko_send_command,command_string=f"show running-config")
    
    configs = str(config[f"{device}"][0]).splitlines()
    
    idx1 = 0
    idx2 = 9999999
    idx3 = 0
    
    for idx, config in enumerate(configs):
        
        if command[0] == config:
            idx2 = idx1
            
        if config == '!' and idx > idx2:
            break
        
        idx1+=1
        idx3+=1
    
    configs = configs[idx2:idx3]
    print(configs)

get_initial_config(device,nr,command)