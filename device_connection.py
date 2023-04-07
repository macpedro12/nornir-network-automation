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


devices = ['r4','r5']


nr = InitNornir(config_file="config.yaml")
routers = nr.filter(F(name=devices[0]) |  F(name=devices[1]))


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

#Object will be used to store config for each device, in the future will implemented user inputs, maybe making possibly to remove the devices list      
device_0 = Router(devices[0],"fastEthernet 1/0","192.168.50.1","255.255.255.252")
device_1 = Router(devices[1],"fastEthernet 1/0","192.168.50.2","255.255.255.252")

device_obj_list = [device_0,device_1]

service_name = 'deviceConnection'


'''
Differen between devices(list), device_obj_list(object) and devices_object_nornir(object)

devices(list) ==> List with the name of the hosts present in the nornir inventory after the filter, useful for applying diferent configs in the devices.
                  Ex: Rollback, where we filter the show running result using the host from the list
                  Maybe it will leave after the insertion of User inputs, because it will be possible to create the object iterating routers.inventory.hosts

device_obj_list(object) ==> List with the objects that carries info used in the service (Name, InterfaceID, IP, ...), it depends on the service.
                            device_0 = Router(devices[0],"fastEthernet 1/0","192.168.10.1","255.255.255.252")
                            Possibly going to the iteration of routers.inventory.hosts after the insertion of user inputs.
                            The Class and the device object highly depends on what is being configured with the service.
                            In the OSPF service, for example we need the name, interface_id, ip, mask and area from the device.
                            
devices_object_nornir(object) ==> Nornir object used to execute Tasks, netmiko tasks most of the time.

'''

#Used to store the part of the configuration that it's being altered by the service.
#It highly depends on the service, maybe in the future it will exist a more general way to store it.
#In this service, for example, we're storing what interface is being altered, because this service only change interface config.
#This list is used in the rollback file generation, the rollback filter what sh_run it will execute getting by the index of the loop for devices in devices.
sh_run_append = []
for device in device_obj_list:
    sh_run_append.append(f"interface {device.interface_id}")


def device_connection (service_name: str, sh_run_append: list, devices_object_nornir: object, devices: list, device_obj_list: list):

    service_id = rollback_point(service_name=service_name,sh_run_append=sh_run_append,devices_object=routers,devices=devices)
    
    for device in device_obj_list:
        
        router = devices_object_nornir.filter(name=f'{device.name}')
        router.run(task=netmiko_send_config,config_commands=[f"interface {device.interface_id}","no shutdown",f"ip address {device.ip} {device.mask}"])
    
    rollback_diff(sh_run_append=sh_run_append,service_name=service_name,service_id=service_id,devices=devices,devices_object=routers)

def ping_post_check (devices_object_nornir: object, device_obj_list: list):

    for index, device in enumerate(device_obj_list):
        otherEnd_device = device_obj_list[index-1]
        router = devices_object_nornir.filter(name=f'{device.name}')
        result = router.run(task=netmiko_send_command,command_string=f"ping {otherEnd_device.ip}",read_timeout=60)
        
        if 'Success rate is 0 percent' in str(result[device.name][0]):
            print(f'It was not possible to ping {otherEnd_device.name}')
        else:
            print(f'{device.name} connected to {otherEnd_device.name}')



def service():
    
    device_connection(service_name = service_name, sh_run_append = sh_run_append, devices_object_nornir = routers, devices = devices, device_obj_list = device_obj_list)
    ping_post_check(devices_object_nornir = routers, device_obj_list = device_obj_list)
    
def rollback(service_id: str):

    connection_rollback(devices_object=routers,service_name=service_name,service_id=service_id,devices=devices)
    
if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])