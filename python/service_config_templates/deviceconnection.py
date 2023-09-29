from utils.convert_cidr import cidr_to_mask

def deviceconnection_template(interface,ip_address,mask):

    template = f'''
interface {interface}
  ip address {ip_address} {mask}
  no shutdown'''

    return template

def deviceconnection_var():
    
    # Get service variables

    ## Get Devices Names

    # Later
    cidr = int(input("Enter the CIDR (Default = 30): ") or 30)

    """ device = 'r1'
    cidr = 30 """

    ## Get config

    # Later
    device_interface = str(input("First device interface (Default = fastEthernet1/0): ") or "fastEthernet1/0")
    device_ip = str(input("First device IPv4 (Default = 10.10.10.1) : ") or "10.10.10.1")

    """ device_interface = 'fastEthernet1/1'
    device_ip = '10.10.10.1' """
    
    device_var = {
        'interface':device_interface,
        'ip':device_ip,
        'mask': str(cidr_to_mask(cidr))
    }
        
    return device_var

def deviceconnection_command():

    var = deviceconnection_var()
    command = deviceconnection_template(var['interface'],var['ip'],var['mask'])
  
    return command