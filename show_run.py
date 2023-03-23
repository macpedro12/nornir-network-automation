from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
switch = nr.filter(F(groups__contains="switch"))
router = nr.filter(F(groups__contains="routers"))

result = switch.run(task=netmiko_send_command,command_string="show running-config interface fastEthernet 0/0")
print_result(result)
