import ipaddress
cidr = 1

n = 8 - cidr%8
a = 0
idx = 0

while idx < n:
    
    a = a + 2**idx
    idx = idx + 1

if cidr == 32:
    wildcard = ipaddress.ip_address(f'0.0.0.0')
elif cidr//8 == 3 or cidr==24:
    wildcard = ipaddress.ip_address(f'0.0.0.{a}')
elif cidr//8 == 2 or cidr==16:
    wildcard = ipaddress.ip_address(f'0.0.{a}.255')
elif cidr//8 == 1 or cidr==16:
    wildcard = ipaddress.ip_address(f'0.{a}.255.255')
else:
    wildcard = ipaddress.ip_address(f'{a}.255.255.255')



print(wildcard)       
       
