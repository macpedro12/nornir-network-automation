from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command

def ping (devices_object: object, device: str, ping_destination_device: str ,ping_destination_ip: str):

    router = devices_object.filter(name=f'{device}')
    result = router.run(task=netmiko_send_command,command_string=f"ping {ping_destination_ip}",read_timeout=60)
    
    if 'Success rate is 0 percent' in str(result[device][0]):
        print(f'It was not possible to ping {ping_destination_device} - {ping_destination_ip}')
    else:
        print(f'{device} connected to {ping_destination_device} - {ping_destination_ip}')