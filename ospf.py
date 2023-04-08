from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_config

import sys

from utils.rollback import rollback_point,rollback_diff
from utils.rollback import rollback as ospf_rollback
from utils.convert_cidr import cidr_to_wildcard
from utils.post_checks import ping


#Services Variables

service_name = 'ospf'

devices = ['r2','r3']
#IP/CIDR/AREA
device_0_routes = ['192.168.40.0/30/1','192.168.20.0/30/0']
device_1_routes = ['192.168.30.0/30/0','192.168.20.0/30/0']
proccess_id = 1

nr = InitNornir(config_file="config.yaml")
routers = nr.filter(F(name=devices[0]) |  F(name=devices[1]))

routesDict = {}

routesDict[devices[0]] = device_0_routes
routesDict[devices[1]] = device_1_routes


sh_run_append = f"router ospf {proccess_id}"

def ospf_config (service_name: str, sh_run_append: list, devices_object: object, devices: list):
    
    service_id = rollback_point(service_name=service_name,sh_run_append=sh_run_append,devices_object=routers,devices=devices)
    
       
    for device in devices:
        
        for route in routesDict[device]:
            
            ip = route.split('/')[0]
            wildcard = cidr_to_wildcard(int(route.split('/')[1]))
            area = route.split('/')[2]
            
            router = devices_object.filter(name=f'{device}')
            router.run(task=netmiko_send_config,config_commands=[f"router ospf {proccess_id}",f"network {ip} {wildcard} area {area}"])
    
    rollback_diff(sh_run_append=sh_run_append,service_name=service_name,service_id=service_id,devices=devices,devices_object=routers)

def service():
    
    ospf_config(service_name=service_name,sh_run_append=sh_run_append,devices_object=routers,devices=devices)

def rollback(service_id: int):
    
    ospf_rollback(devices_object=routers,service_name=service_name,service_id=service_id,devices=devices)
    
    
if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])