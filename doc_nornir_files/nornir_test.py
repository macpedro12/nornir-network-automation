from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

print(nr.filter(site="switch").inventory.hosts.keys())

print(type(nr.inventory.hosts))

for host in nr.inventory.hosts:
    print(host)
    print(f"Hostname {host}: {nr.inventory.hosts[f'{host}'].hostname}")
    print(f"Domain {host}: {nr.inventory.hosts[f'{host}']['domain']}")

def hello_world(task: Task) -> Result:
    return Result(
        host = task.host,
        result = f"{host} says hello world"
    )
result = nr.run(task=hello_world)

print_result(result)