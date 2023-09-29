from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_config

from importlib import import_module
import sys

from utils.convert_cidr import cidr_to_mask

nr = InitNornir(config_file="config.yaml")
# Get service name

# Later
""" service_name = str(input("Select the service: ")).replace(" ","")
service_name = service_name.lower()
print(service_name) """

service_name = "deviceconnection"
# Find out a way to import the functions using variables.
# Here we import the function that get the varibles for the service, then execute it.
# This will exclude the need for multiples 'if' conditions and make it easier to add new services config templates. 
service_var = import_module(f"service_config_templates.{service_name}").__getattribute__(f"{service_name}_var")
service_var = service_var()

service_template = import_module(f"service_config_templates.{service_name}").__getattribute__(f"{service_name}_template")

for device in service_var:
    
    router = nr.filter(name=f'{device}')
    command = service_template(device['interface'],device['ip'],device['mask'])
    router.run(task=netmiko_send_config,config_commands=[command])


print(service_var)

print(service_template)

print(service_name)

