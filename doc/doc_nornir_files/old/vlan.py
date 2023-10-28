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
switch = nr.filter(F(groups__contains="switch"))
devices = []
for host in switch.inventory.hosts:
    devices.append(str(host))


""" vlan_id = int(input("Vlan ID:"))
vlan_name = str(input("Vlan Name:"))
interface_id = str(input("Interface ID:")) """



def add_vlan(task: Task, vlan_id: int, vlan_name: str) -> Result:
    
    task.run(task=netmiko_send_config,config_commands=[f"vlan {vlan_id}",f"name {vlan_name}"])
    
    return Result (
        host = task.host,
        result=f"Vlan {vlan_name}:{vlan_id} added to {task.host}"
    )
    
def add_itf_to_vlan(task: Task, vlan_id: int, interface_id: str) -> Result:
    commands = [f"interface FastEthernet {interface_id}",f"switchport mode access",f"switchport access vlan {vlan_id}"]
    task.run(task=netmiko_send_config,config_commands=commands)
    return Result (
        host = task.host,
        result=commands
    )

def full_vlan(task: Task,vlan_id: int, interface_id: str,vlan_name: str) -> Result:
    
    task.run(task=add_vlan,vlan_id=vlan_id,vlan_name=vlan_name)
    task.run(task=add_itf_to_vlan,vlan_id=vlan_id,interface_id=interface_id)
        
    return Result (
        host=task.host,
        result="Added Interface Config"
    )



vlan_id=300
interface_id="1/2"
service_name = 'vlan'

#This service provides configs to Interface
#Show running config will run:   
sh_run_append = f"interface FastEthernet {interface_id}"

def service_vlan():
    
    service_id = rollback_point(service_name=service_name,vlan_id=vlan_id,sh_run_append=sh_run_append,devices_object=switch,devices=devices)

    switch.run(name=service_name,task=full_vlan,vlan_id=vlan_id,interface_id=interface_id,vlan_name="ChangeTeste")

    rollback_diff(sh_run_append=sh_run_append,service_name=service_name,service_id=service_id,devices=devices,devices_object=switch)

#Choosed to keep the rollback in the service file, because it's easier to call the parameters
def rollback(service_id: int):
    
    vlan_rollback(devices_object=switch,devices=devices,service_name=service_name,service_id=service_id)


#Needed this to be able to call the service creation and the rollback
#It will be usefull when the edit option is developed
if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])



