from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_config

import json
from importlib import import_module

from database.get_device_config import get_initial_config, get_last_id

# Used as the main function for service implementation.
# Service Selection, Number of Devices and Devices Names are in every service creation.
# Specific variables will be inserted depending on the selected service.

def create_service():
    
    nr = InitNornir(config_file="config.yaml")
    # Get service name

    # Service Selection
    service_selected = str(input("Select the service (Default = Device Connection): ") or "Device Connection").replace(" ","")
    service_selected = service_selected.lower()

    service_id = get_last_id() + 1
    service_name = str(input("Name of the service (Default = Test): ") or "Test")
    
    device_number = int(input("Number of devices being configured (Default = 2): ") or 1)
    loop_var = 1
    device_list = []

    while device_number >= loop_var:
        device_list.append(str(input(f"Enter the {loop_var}º device: ") or f"r{loop_var}"))
        loop_var+=1
        
    # Found out a way to import the functions using variables.
    # Here we import the function that get the varibles for the service, then execute it.
    # This will exclude the need for multiples 'if' conditions and make it easier to add new services config templates.
    
    #Added the try and except, because of errors when calling this function in main.py
    try: 
        service_config = import_module(f"src.service_provider.services.{service_selected}.{service_selected}").__getattribute__(f"{service_selected}")
    except:
        service_config = import_module(f"services.{service_selected}.{service_selected}").__getattribute__(f"{service_selected}")
        

    # Used to store the configs from the device
    # Ex: {'r1':'config_x','r2':'config_y'}
    initial_config_dict = {}
    applied_config_dict = {}
    
    for device in device_list:
        
        print(f"Initializing the configuration of the Device {device}")
        router = nr.filter(name=f'{device}')
        config = service_config(device)
        config_to_apply = []
        
        for line in config.split('\n'):
            config_to_apply.append(line)
        
        initial_config = get_initial_config(device_name=device,nornir_device_object=nr,configs_to_apply=config_to_apply)
        initial_config_dict[device] = initial_config
        initial_config_json = json.dumps(initial_config_dict)
        
        router.run(task=netmiko_send_config,config_commands=config_to_apply)
        
        applied_config_dict[device] = config_to_apply
        applied_config_json = json.dumps(applied_config_dict)
        
        print(f"End of the configuration of the Device {device}")
        service_status = "Applied"
        
    return [service_id,service_name,applied_config_json,initial_config_json,service_status]

if __name__ == "__main__":
   pass