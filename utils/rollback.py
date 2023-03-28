from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

import os

#Gets the rollback file and execute it with the netmiko_senconfig
def rollback(devices_object: object, service_id: int, devices: list):
    
    for host in devices:
        
        single_host_object = devices_object.filter(name=f'{host}')
        print(single_host_object)
        last_service = os.listdir(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}")
        
        for command_file in last_service:
            single_host_object.run(task=netmiko_send_config,config_file=f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/{command_file}")
        
    return f"Rollback executed with success"
    
#Main point of the generation of the rollback file
def rollback_point(task: Task,service_name: str,vlan_id: int, interface_id: str,devices_object: object, devices: list) -> Result:

    service_id = get_last_id(service_name=service_name)
    rollback_database(service_name=task.name,devices=devices,service_id=service_id)
    
    #list_vlan= vlan_rollback_block(service_id=service_id,vlan_id=vlan_id,devices_object=devices_object,devices=devices)
    list_interface = interface_rollback_block(service_id=service_id,interface_id=interface_id,devices_object=devices_object,devices=devices)

    
    return Result (
        host=task.host,
        result=f"{list_interface}\n",
    )

#Rollback config block generator for vlan config
def vlan_rollback_block(service_id: int, vlan_id: str,devices_object: object, devices: list):
    
    for host in devices:
        vlan_rollback = devices_object.run(name="VLAN Config",task=netmiko_send_command,command_string=f"sh vlan-switch id {vlan_id}")

        list_vlan = str(vlan_rollback[f"{host}"][0])
        list_vlan = " ".join(str(list_vlan.replace("-","")).split())
        list_vlan = list_vlan.split()[:6]
        rollback_command_file_vlan = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/vlanId.txt",'a+')
        
        if 'not' in list_vlan:
            rollback_command_file_vlan.write(f"no vlan {vlan_id}")
        else:
            rollback_command_file_vlan.write(f"vlan {list_vlan[4]}\n")
            rollback_command_file_vlan.write(f" name {list_vlan[5]}")
        
        rollback_command_file_vlan.close()
    return " VLAN FILE "

#Rollback config block generator for Interface ID (In the future this may be a general config generator, since most of the configs will be pushed from the show running-config command)    
def interface_rollback_block(service_id: int, interface_id: str, devices_object: object, devices: list):
    
    for host in devices:
        
        interface_rollback = devices_object.run(name="Interface Config",task=netmiko_send_command,command_string=f"show running-config interface FastEthernet {interface_id}")
        
        list_interface = str(interface_rollback[f"{host}"][0]).splitlines()
        list_interface = list_interface[4:]
        #Removes 'end' from the command file - netmiko_send_config already does that
        del list_interface[-1]
        
        rollback_command_file_itf = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/ItfId.txt",'a+')
        
        for commands in list_interface:
            rollback_command_file_itf.write(f"{commands}\n")
        
        rollback_command_file_itf.close()
    return " ITF FILE "

#Function to get the last used Service ID
def get_last_id(service_name: str):
    if os.path.exists(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}"):
        
        last_service = os.listdir(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}")
        print(last_service)
        if not last_service:
            service_id = 1
        else:
            service_id = int(str(last_service[-1]).split("_")[2]) + 1
            
    else:
        service_id = 1
    
    return service_id

#Function used to generate the service rollback folders to each different device
def rollback_database(service_name: str, devices: list, service_id: int) -> Result:
    service_name = service_name.lower()
    print(service_name)
    for host in devices:
        if os.path.exists(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}"):          
            os.mkdir(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}")
            
        else:
            os.makedirs(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}")
            
def rollback_diff(interface_id: str, service_id: int, devices: list, devices_object: object):
    for host in devices:
        initial_config = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/ItfId.txt",'r')
        initial_config_list = initial_config.readlines()
        initial_config_list = [sub.replace("\n","") for sub in initial_config_list] 
        print(initial_config_list)
        initial_config.close()
        
        new_config = devices_object.run(name="Interface Config",task=netmiko_send_command,command_string=f"show running-config interface FastEthernet {interface_id}")
        
        new_config_list = str(new_config[f"{host}"][0]).splitlines()
        new_config_list = new_config_list[4:]
        #Removes 'end' from the command file - netmiko_send_config already does that
        del new_config_list[-1]
        new_rollback_file = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_vlan/rollback_vlan_{service_id}_{host}/ItfId.txt",'w')
        for command in new_config_list:
           
            combined_list = "\t".join(initial_config_list)
    
            if command.strip() in initial_config_list:
                new_rollback_file.write(f"{command}\n")
                print(f"{command} ========== AQUI 11")
                
            elif command.strip().split(" ")[0] in combined_list:
                
                command = command.strip().split(" ")[0]
                match = [sub for sub in initial_config_list if command in sub]
                
                new_rollback_file.write(f"{match[0]}\n")
                print(f"{match[0]} ========== AQUI 222")
                
            elif command.strip not in initial_config_list:
                new_rollback_file.write(f"no {command.strip()}\n")
                print(f"{command} ========== AQUI 3333")
                
        new_rollback_file.close()
        