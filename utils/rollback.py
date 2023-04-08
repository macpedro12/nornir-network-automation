from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

import os
import shutil

#Gets the rollback file and execute it with the netmiko_senconfig
def rollback(devices_object: object,service_name: str, service_id: int, devices: list):
    
    for host in devices:
        
        single_host_object = devices_object.filter(name=f'{host}')
        print(single_host_object)
        last_service = os.listdir(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}")
        
        for command_file in last_service:
            single_host_object.run(task=netmiko_send_config,config_file=f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}/{command_file}")
        
        #Delete Service Folder
        shutil.rmtree(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}")
        
    print(f"Rollback executed with success")
    
#Main point of the generation of the rollback file
def rollback_point(service_name: str, sh_run_append: str,devices_object: object, devices: list):
    
    service_name = service_name.lower()
    
    service_id = get_last_id(service_name=service_name)
    rollback_database(service_name=service_name,devices=devices,service_id=service_id)
    
    #vlan_rollback_block(service_id=service_id,vlan_id=vlan_id,devices_object=devices_object,devices=devices)
    general_rollback_block(service_id=service_id, service_name=service_name,sh_run_append=sh_run_append,devices_object=devices_object,devices=devices)
    
    return service_id

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

#Rollback config block generator for Interface ID (In the future this may be a general config generator, since most of the configs will be pulled from the show running-config command)    
def general_rollback_block(service_id: int, service_name: str, sh_run_append: str, devices_object: object, devices: list):
    
    for index, host in enumerate(devices):
        
        rollback_command_file_itf = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}/GeneralConfig.txt",'a+')
        
        if type(sh_run_append) is list:
            general_rollback = devices_object.run(task=netmiko_send_command,command_string=f"show running-config {sh_run_append[index]}")
        else:
            general_rollback = devices_object.run(task=netmiko_send_command,command_string=f"show running-config {sh_run_append}")

        #Execute the show run on both devices, but filter the result by host
        command_list = str(general_rollback[f"{host}"][0]).splitlines()
        command_list = command_list[4:]
        
        if command_list == []:
            rollback_command_file_itf.write(f"no {sh_run_append}")
        else:
            #Removes 'end' from the command file - netmiko_send_config already does that
            del command_list[-1]
                    
            for commands in command_list:
                rollback_command_file_itf.write(f"{commands}\n")
        
        rollback_command_file_itf.close()
    return "ITF FILE"

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
    for host in devices:
        if os.path.exists(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}"):          
            os.mkdir(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}")
            
        else:
            os.makedirs(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}")

#Function used to compare the initial config retrieved before executing the service and the new config after the execution
#The diff will see if the the new config exists in the old config, if a old config has changed and if a new config has been implemented.          
def rollback_diff(sh_run_append: str, service_name:str, service_id: int, devices: list, devices_object: object):
    for index, host in enumerate(devices):
        #Uses the file used to store the old config
        initial_config = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}/GeneralConfig.txt",'r')       
        initial_config_list = initial_config.readlines()
        initial_config_list = [sub.replace("\n","") for sub in initial_config_list] 
        initial_config.close()
        
        if len(initial_config_list)==1 and 'no' in initial_config_list[0]:
            
            print('Keeping the same file') 
            
        else:
        
            if type(sh_run_append) is list:
                new_config = devices_object.run(name="Interface Config",task=netmiko_send_command,command_string=f"show running-config {sh_run_append[index]}")
            else:
                new_config = devices_object.run(name="Interface Config",task=netmiko_send_command,command_string=f"show running-config {sh_run_append}")
                
            #Execute the show run on both devices, but filter the result by host
            new_config_list = str(new_config[f"{host}"][0]).splitlines()
            new_config_list = new_config_list[4:]
            #Removes 'end' from the command file - netmiko_send_config already does that
            del new_config_list[-1]
                
            
            #New rollback file
            new_rollback_file = open(f"/mnt/c/Users/Pedro/Desktop/nornir/utils/rollback/rollback_{service_name}/rollback_{service_name}_{service_id}_{host}/GeneralConfig.txt",'w')
            for command in new_config_list:
                combined_list = "\t".join(initial_config_list)
                #Check if the new config is in the old configuration.
                if command.strip() in initial_config_list:
                    new_rollback_file.write(f"{command}\n")
                
                #Check if the new config is a changed version of the old config.
                #Ex: Old - speed 10  New - speed 100
                #Gets the speed str, checks if is in the list and gets its match.
                #Probably will need further improvements 
                elif command.strip().split(" ")[0] in combined_list:
                    command = command.strip().split(" ")[0]
                    match = [sub for sub in initial_config_list if command in sub]
                    new_rollback_file.write(f"{match[0]}\n")
                
                #Check if the new config is really new lol     
                elif command.strip() not in initial_config_list:
                    new_rollback_file.write(f"no {command.strip()}\n")
            #Check if a interface was in a shutdown state, it wasn't possible to get this config in the diff, because the show running don't displays 'no shutdown'    
            if "shutdown" in combined_list:
                    new_rollback_file.write(f"shutdown\n")
                    
            new_rollback_file.close()

