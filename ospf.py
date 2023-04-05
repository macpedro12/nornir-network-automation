from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result


from doc_nornir_files.processors import PrintResult, SaveResultToDict
from utils.rollback import rollback_point,rollback_diff
from utils.rollback import rollback as vlan_rollback


nr = InitNornir(config_file="config.yaml")

area = '2'
routers = nr.filter(F(area=area))

devices = []
for host in routers.inventory.hosts:
    devices.append(str(host))

class Router:
    
    def __init__(self, name, interface_id, ip, mask, area) -> None:
        self._name = name
        self._interface_id = interface_id
        self._ip = ip
        self._mask = mask
        self._area = area
    
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
    
    @property
    def area(self):
        return self._area

#Object will be used to store config for each device, in the future will implemented user inputs, maybe making possibly to remove the devices list      
device_0 = Router(devices[0],"fastEthernet 1/0","192.168.10.1","255.255.255.252",area)
device_1 = Router(devices[1],"fastEthernet 1/0","192.168.10.2","255.255.255.252",area)

device_obj_list = [device_0,device_1]

service_name = 'ospf'


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
   

def ospf_config (service_name: str, sh_run_append: list, devices_object_nornir: object, devices: list, device_obj_list: list):
    service_id = rollback_point(service_name=service_name,sh_run_append=sh_run_append,devices_object_nornir=routers,devices=devices)
    
    for device in device_obj_list:
        
        router = devices_object_nornir.filter(name=f'{device.name}')
        router.run(task=netmiko_send_config,config_commands=[f"interface {device.interface_id}",f"ip address {device.ip} {device.mask}",f"no shutdown"])
    
    rollback_diff(sh_run_append=sh_run_append,service_name=service_name,service_id=service_id,devices=devices,devices_object_nornir=routers)
    

#device_connection(devices_object_nornir=routers)
#ping_post_check(devices_object_nornir=routers)
#vlan_rollback(devices_object=routers,service_name=service_name,service_id=1,devices=devices)