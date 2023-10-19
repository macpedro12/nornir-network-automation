from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_config

from importlib import import_module
import sys

from utils.convert_cidr import cidr_to_mask

nr = InitNornir(config_file="config.yaml")
# Get service name

# Later
service_name = str(input("Select the service (Default = Device Connection): ") or "Device Connection").replace(" ","")
service_name = service_name.lower()
print(service_name)

device_number = int(input("Number of devices being configured (Default = 2): ") or 1)
loop_var = 1
device_list = []

while device_number >= loop_var:
    device_list.append(str(input(f"Enter the {loop_var}º device: ") or f"r{loop_var}"))
    loop_var+=1
    
# Find out a way to import the functions using variables.
# Here we import the function that get the varibles for the service, then execute it.
# This will exclude the need for multiples 'if' conditions and make it easier to add new services config templates. 
service_command = import_module(f"service_config.{service_name}").__getattribute__(f"{service_name}")

for device in device_list:
    
    print(f"Initializing the configuration of the Device {device}")
    router = nr.filter(name=f'{device}')
    command = service_command()
    new_command = []
    
    for line in command.split('\n'):
        new_command.append(line)
        
    router.run(task=netmiko_send_config,config_commands=new_command)

    print(f"End of the configuration of the Device {device}")


