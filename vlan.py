from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

import os

from doc_nornir_files.processors import PrintResult, SaveResultToDict
from utils.rollback import rollback_point,rollback,rollback_diff

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
    
    rollback_point(task=task,service_name=service_name,vlan_id=vlan_id,interface_id=interface_id,devices_object=switch,devices=devices)
    
    #task.run(task=add_vlan,vlan_id=vlan_id,vlan_name=vlan_name)
    task.run(task=add_itf_to_vlan,vlan_id=vlan_id,interface_id=interface_id)
    
    rollback_diff(interface_id="1/2",service_id=1,devices=devices,devices_object=switch)
    

rollback(devices_object=switch,devices=devices,service_id=1)



service_name = 'vlan'
""" result = switch.run(name=service_name,task=full_vlan,vlan_id=300,interface_id="1/2",vlan_name="ChangeTeste")
print(result)
 """

