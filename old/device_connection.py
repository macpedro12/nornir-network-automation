from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from doc_nornir_files.processors import PrintResult, SaveResultToDict

import sys

from utils.rollback import rollback_point,rollback_diff
from utils.rollback import rollback as connection_rollback
from utils.convert_cidr import cidr_to_mask
from utils.post_checks import ping


devices = ['r4','r5']


nr = InitNornir(config_file="config.yaml")
routers = nr.filter(F(name=devices[0]) |  F(name=devices[1]))
device_0_config = "fastEthernet 1/0|192.168.50.1|30"
device_1_config = "fastEthernet 1/0|192.168.50.2|30"

#Object will be used to store config for each device, in the future will implemented user inputs, maybe making possibly to remove the devices list      
deviceDict = {}

deviceDict[devices[0]] = device_0_config
deviceDict[devices[1]] = device_1_config

service_name = 'deviceConnection'


'''
Differen between devices(list), device_obj_list(object) and devices_object_nornir(object)

devices(list) ==> List with the name of the hosts present in the nornir inventory after the filter, useful for applying diferent configs in the devices.
                  It's used to store the devices configured in the service 
                  Ex: Rollback, where we filter the show running result using the host from the list

deviceDict(dict) ==> Creates a Dict correlating the User Input configs to the devices

Deprecated - Not going to use objects anymore, it doesn't makes senses because we are not re-utilizing the objects. 
    device_obj_list(object) ==> List with the objects that carries info used in the service (Name, InterfaceID, IP, ...), it depends on the service.
                                device_0 = Router(devices[0],"fastEthernet 1/0","192.168.10.1","255.255.255.252")
                                Possibly going to the iteration of routers.inventory.hosts after the insertion of user inputs.
                                The Class and the device object highly depends on what is being configured with the service.
                                In the OSPF service, for example we need the name, interface_id, ip, mask and area from the device.
                            
devices_object(object) ==> Nornir object used to execute Tasks, netmiko tasks most of the time.

'''

#Used to store the part of the configuration that it's being altered by the service.
#It highly depends on the service, maybe in the future it will exist a more general way to store it.
#In this service, for example, we're storing what interface is being altered, because this service only change interface config.
#This list is used in the rollback file generation, the rollback filter what sh_run it will execute getting by the index of the loop for devices in devices.
sh_run_append = []
for device in devices:
    interfaceId = deviceDict[device].split('|')[0]
    sh_run_append.append(f"interface {interfaceId}")


def device_connection (service_name: str, sh_run_append: list, devices_object: object, devices: list):

    service_id = rollback_point(service_name=service_name,sh_run_append=sh_run_append,devices_object=routers,devices=devices)
    
    for device in devices:
        
        interface_id = deviceDict[device].split('|')[0]
        ip = deviceDict[device].split('|')[1]
        mask = cidr_to_mask(int(deviceDict[device].split('|')[2]))
        
        router = devices_object.filter(name=f'{device}')
        router.run(task=netmiko_send_config,config_commands=[f"interface {interface_id}","no shutdown",f"ip address {ip} {mask}"])
    
    rollback_diff(sh_run_append=sh_run_append,service_name=service_name,service_id=service_id,devices=devices,devices_object=routers)


def service():
    
    device_connection(service_name = service_name, sh_run_append = sh_run_append, devices_object = routers, devices = devices)
    
    ping(devices_object = routers, device = devices[0], ping_destination_device= devices[1], ping_destination_ip= deviceDict[devices[1]].split('|')[1])
    
def rollback(service_id: str):

    connection_rollback(devices_object=routers,service_name=service_name,service_id=service_id,devices=devices)

if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])