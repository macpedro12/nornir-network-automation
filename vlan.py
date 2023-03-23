from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

from doc_nornir_files.processors import PrintResult, SaveResultToDict

nr = InitNornir(config_file="config.yaml")
switch = nr.filter(F(groups__contains="switch") & F(site="switch1"))

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

    vlan_rollback = task.run(name="VLAN Config",task=netmiko_send_command,command_string=f"sh vlan-switch id {vlan_id}")
    
    list_vlan = str(vlan_rollback[0])
    list_vlan = " ".join(str(list_vlan.replace("-","")).split())
    list_vlan = list_vlan.split()[:6]
    
    rollback_command_file_vlan = open('./rollback_vlan/vlanId.txt','w+')
    
    if 'not' in list_vlan:
        rollback_command_file_vlan.write(f"no vlan {vlan_id}")
    else:
        rollback_command_file_vlan.write(f"vlan {list_vlan[4]}")
        rollback_command_file_vlan.write(f" name {list_vlan[5]}")
    
    rollback_command_file_vlan.close()
    
    interface_rollback = task.run(name="Interface Config",task=netmiko_send_command,command_string=f"show running-config interface FastEthernet {interface_id}")
    
    list_interface = str(interface_rollback[0]).splitlines()
    list_interface = list_interface[4:7]
    
    rollback_command_file_itf = open('./rollback_vlan/ItfId.txt','w+')
    
    for commands in list_interface:
        rollback_command_file_itf.write(f"{commands}\n")
    
    rollback_command_file_itf.close()
    
    return Result (
        host=task.host,
        result=f"{list_interface}\n{list_vlan}"
    )

data = {}

switch_processors = switch.with_processors([SaveResultToDict(data),PrintResult()]) 
result = switch.run(name="Point",task=rollback_point,vlan_id=200,interface_id="1/2")
print(result['sw1'][0])

