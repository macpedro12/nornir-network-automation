from utils.convert_cidr import cidr_to_mask

def deviceconnection_var():
    
    # Get service variables

    ## Get Devices Names

    # Later
    # device1 = input("First device name: ")
    # device2 = input("Second device name: ")
    # cidr = input("Enter the CIDR: ")

    device1 = 'r1'
    device2 = 'r6'
    cidr = 30

    ## Get config

    # Later
    # device1_interface = input("First device interface: ")
    # device1_ip = input("First device IPv4: ")
    # device2_interface = input("Second device interface: ")
    # device2_ip = input("Second device IPv4: ")

    device1_interface = 'fastEthernet1/1'
    device1_ip = '10.10.10.1'
    device2_interface = 'fastEthernet0/1'
    device2_ip = '10.10.10.2'
    
    device1_var = {
        'device_name':device1,
        'interface':device1_interface,
        'ip':device1_ip,
        'mask': str(cidr_to_mask(cidr))
    }
    
    device2_var = {
        'device_name':device2,
        'interface':device2_interface,
        'ip':device2_ip,
        'mask': str(cidr_to_mask(cidr))
    }
        
    return [device1_var,device2_var]

def deviceconnection_template(interface,ip_address,mask):

    command = f'''
interface {interface}
  ip address {ip_address} {mask}
  no shutdown'''
  
    return command