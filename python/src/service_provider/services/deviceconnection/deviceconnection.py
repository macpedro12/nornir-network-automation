from jinja2 import FileSystemLoader, Environment
from commons.convert_cidr import cidr_to_mask



def deviceconnection():
    
    # Get service variables

    ## Get Devices Names

    # Later
    cidr = int(input("Enter the CIDR (Default = 30): ") or 30)

    """ device = 'r1'
    cidr = 30 """

    ## Get config

    # Later
    device_interface = str(input("First device interface (Default = fastEthernet1/0): ") or "fastEthernet1/0")
    device_ip = str(input("First device IPv4 (Default = 10.10.10.1) : ") or "112.123.10.1")

    """ device_interface = 'fastEthernet1/1'
    device_ip = '10.10.10.1' """
    file_loader = FileSystemLoader('python/src/service_provider/services/deviceconnection/template')
    env = Environment(loader=file_loader)
    template_file = 'deviceconnection.txt'
    
    template = env.get_template(template_file)
    
    content = template.render(
        interface = device_interface,
        ip_address = device_ip,
        mask = str(cidr_to_mask(cidr))
    )

    print(content)
    
    return content

if __name__ == "__main__":
   deviceconnection()