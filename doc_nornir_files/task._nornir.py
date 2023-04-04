from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError

import logging

nr = InitNornir(config_file="config.yaml" )
#Filter by group
#router = nr.filter(F(groups__contains="routers"))    

switch = nr.filter(F(groups__contains="switch"))

def say(task: Task, text: str) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} say {text}"
    )
    

def count(task: Task, number: int) -> Result:
    return Result(
        host=task.host,
        result=f"{[n for n in range(0,number)]}"
    )

    
def greet_and_count(task: Task, number: int) -> Result:
    task.run(
        name="Greeting is the polite thing to do",
        severity_level=logging.DEBUG,
        task=say,
        text="hi!",
    )

    task.run(
        name="Counting beans",
        task=count,
        number=number,
    )
    task.run(
        name="We should say bye too",
        severity_level=logging.DEBUG,
        task=say,
        text="bye!",
    )

    # let's inform if we counted even or odd times
    even_or_odds = "even" if number % 2 == 0 else "odd"
    return Result(
        host=task.host,
        result=f"{task.host} counted {even_or_odds} times!",
    )

#If you want to execute a Task filtering the devices, first you need to filter with nr.filter and pass to a variable. 
#Then you call the task with the variable as shown below.
#It's also possible to select the result of a specific device or even a single task.

result=switch.run(name='Greet and Count',task=greet_and_count,number=8)
#print_result(result['sw1'], severity_level=logging.DEBUG)

#severity_level is used to flag task with any severity_levels, only tasks marked as INFO and ERROR shows in the output, 
#unless you pass the severity_level as parameter in print_result

#result is a dic where the keys are the hosts and inside of every key is a list with the results of the tasks.
#print(result['sw1'][0])
#print(result['sw2'])
print(result)

#Check if the taks changed anything in the system or failed
#print("changed: ",result['sw2'].changed)
#print("failed: ",result.failed)
#Check the hosts which failed a task
#print(result.failed_hosts)
#Check the failed Task
#print(result['sw2'].exception)
#Check the Exception
#print(result['sw2'][0].exception)


def hi(task=Task) -> Result:
    return Result(host=task.host,result=f"{task.host.name} hey dumbfuck, i'm still here")

#Nornir stores the devices who failed a task and don't call them in the next run
#Unless you include on_failed=True
#on_good=False exclude the hosts without error
""" result = switch.run(task=hi,on_failed=False,on_good=True)
print_result(result) """

#Nornir stores the failed devices in nr.data.failed_hosts

print(nr.data.failed_hosts)

""" try:
    result = switch.run(
        task=greet_and_count,
        number=5,
    )
except NornirExecutionError:
    print("ERROR!!!") """