from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

import os

from doc_nornir_files.processors import PrintResult, SaveResultToDict

nr = InitNornir(config_file="config.yaml")
switch = nr.filter(F(groups__contains="switch"))
devices = []
for host in switch.inventory.hosts:
    devices.append(str(host))
    print(devices)


""" vlan_id = int(input("Vlan ID:"))
vlan_name = str(input("Vlan Name:"))
interface_id = str(input("Interface ID:")) """

def rollback(task: Task, vlan_id: int, interface_id: int) -> Result:
    
    task.run(task=netmiko_send_config,config_commands=[f"no vlan {vlan_id}"])
    
    task.run(task=netmiko_send_config,config_commands=[f"interface FastEthernet {interface_id}",f"switchport mode access",f"no switchport access vlan {vlan_id}"])
    
    return Result (
        host=task.host,
        result=f"Rollback executed with success"
    )

def add_vlan(task: Task, vlan_id: int, vlan_name: str) -> Result:
    
    task.run(task=netmiko_send_config,config_commands=[f"vlan {vlan_id}",f"name {vlan_name}"])
    
    return Result (
        host = task.host,
        result=f"Vlan {vlan_name}:{vlan_id} added to {task.host}"
    )
    
def add_itf_to_vlan(task: Task, vlan_id: int, interface_id: str) -> Result:
    
    task.run(task=netmiko_send_config,config_commands=[f"interface FastEthernet {interface_id}",f"switchport mode access",f"switchport access vlan {vlan_id}"])
    return Result (
        host = task.host,
        result=f"Vlan {vlan_id} added to {task.host} interface {interface_id}"
    )
    
def full_vlan(task: Task,vlan_id: int, interface_id: str,vlan_name: str) -> Result:
    
    task.run(task=add_vlan,vlan_id=vlan_id,vlan_name=vlan_name)
    task.run(task=add_itf_to_vlan,vlan_id=vlan_id,interface_id=interface_id)
    
def rollback_point(task: Task,vlan_id: int, interface_id: str) -> Result:
    
    service_id = rollback_database(service_name=task.name,devices=devices)
    
    list_interface = vlan_rollback_block(service_id=service_id,vlan_id=vlan_id)
    list_vlan = interface_rollback_block(service_id=service_id,interface_id=interface_id)
    
    print(list_vlan)
    
    return Result (
        host=task.host,
        result=f"{list_interface}\n{list_vlan}",
    )

data = {}

def vlan_rollback_block(service_id: int, vlan_id: str):
    
    for host in devices:
        vlan_rollback = switch.run(name="VLAN Config",task=netmiko_send_command,command_string=f"sh vlan-switch id {vlan_id}")

        list_vlan = str(vlan_rollback[f"{host}"][0])
        list_vlan = " ".join(str(list_vlan.replace("-","")).split())
        list_vlan = list_vlan.split()[:6]
        
        rollback_command_file_vlan = open(f"./rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/vlanId.txt",'a+')
        
        if 'not' in list_vlan:
            rollback_command_file_vlan.write(f"no vlan {vlan_id}")
        else:
            rollback_command_file_vlan.write(f"vlan {list_vlan[4]}\n")
            rollback_command_file_vlan.write(f" name {list_vlan[5]}")
        
        rollback_command_file_vlan.close()
    return " VLAN FILE "
    
def interface_rollback_block(service_id: int, interface_id: str):
    
    for host in devices:
        
        interface_rollback = switch.run(name="Interface Config",task=netmiko_send_command,command_string=f"show running-config interface FastEthernet {interface_id}")
        
        list_interface = str(interface_rollback[f"{host}"][0]).splitlines()
        list_interface = list_interface[4:7]
        
        rollback_command_file_itf = open(f"./rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/ItfId.txt",'a+')
        
        for commands in list_interface:
            rollback_command_file_itf.write(f"{commands}\n")
        
        rollback_command_file_itf.close()
    return " ITF FILE "

def rollback_database(service_name: str, devices: list) -> Result:
    service_name = service_name.lower()
    print(service_name)
    for host in devices:
        
        if os.path.exists(f"./rollback/rollback_{service_name}"):
            
            last_service = os.listdir(f"./rollback/rollback_{service_name}")
            
            if not last_service:
                service_id = 1
            elif host in last_service[-1]:
                service_id = int(str(last_service[-1]).split("_")[2]) + 1
            else:
                service_id = int(str(last_service[-1]).split("_")[2])
                
            os.mkdir(f"./rollback/rollback_vlan/rollback_vlan_{service_id}_{host}")
        else:
            service_id = 1
            os.makedirs(f"./rollback/rollback_vlan/rollback_vlan_{service_id}_{host}")
        
    
    return service_id

service_name = 'vlan'
switch_processors = switch.with_processors([SaveResultToDict(data),PrintResult()]) 
result = switch.run(name=service_name,task=rollback_point,vlan_id=200,interface_id="1/2")
print(result)
print(result['sw1'][0])

