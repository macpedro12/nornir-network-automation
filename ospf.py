from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

import sys
import os

from doc_nornir_files.processors import PrintResult, SaveResultToDict
from utils.rollback import rollback_point,rollback_diff
from utils.rollback import rollback as vlan_rollback

nr = InitNornir(config_file="config.yaml")
routers = nr.filter(F(area='2'))
devices = []
for host in routers.inventory.hosts:
    devices.append(str(host))

print(devices)

class Router:
    
    def __init__(self, name, interface_id, ip, mask) -> None:
        self._name = name
        self._interface_id = interface_id
        self._ip = ip
        self._mask = mask
    
    @property
    def name(self):
        return self._name
    
    @property
    def interface_id(self):
        return self._interface_id
    
    @property
    def ip(self):
        return self._ip
    
    @property
    def mask(self):
        return self._mask
        
device_one = Router(devices[0],"fastEthernet 1/0","192.168.10.1","255.255.255.252")
device_two = Router(devices[1],"fastEthernet 1/0","192.168.10.2","255.255.255.252")

device_obj_list = [device_one,device_two]

service_name = 'ospf'

sh_run_append = f"interface {device_one.interface_id}"

def device_connection (router_object: routers):

    service_id = rollback_point(service_name=service_name,sh_run_append=sh_run_append,devices_object=routers,devices=devices)
    
    for device in device_obj_list:
        
        router = router_object.filter(name=f'{device.name}')
        router.run(task=netmiko_send_config,config_commands=[f"interface {device.interface_id}",f"ip address {device.ip} {device.mask}",f"no shutdown"])
    
    rollback_diff(sh_run_append=sh_run_append,service_name=service_name,service_id=service_id,devices=devices,devices_object=routers)


def ospf_config (task: Task, router1_data: object, router2_data: object, ospf_area: int) -> Result:
    pass
    #task.run(task=netmiko_send_config,config_commands=[f"interface {router1_data.interface_id}",f"name {vlan_name}"])
    
#device_connection(router_object=routers)
vlan_rollback(devices_object=routers,service_name=service_name,service_id=1,devices=devices)