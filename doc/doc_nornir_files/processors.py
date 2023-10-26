from typing import Dict
from nornir import InitNornir

from nornir.core import Nornir
from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Result, Task

nr = InitNornir(config_file="config.yaml")

class PrintResult:
    def task_started(self, task: Task):
        print(f'>>> starting {task.name}')
    
    def task_completed(self, task:Task, result: AggregatedResult):
        print(f'>>> completed {task.name}')
        
    def task_instance_started(self, task: Task, host: Host) -> None:
        pass

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        print(f"  - {host.name}: - {result.result}")

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass  # to keep example short and sweet we ignore subtasks

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass  # to keep example short and sweet we ignore subtasks
    
class SaveResultToDict:
    def __init__(self, data: Dict[str, None]) -> None:
        self.data = data

    def task_started(self, task: Task) -> None:
        self.data[task.name] = {}
        self.data[task.name]["started"] = True

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        self.data[task.name]["completed"] = True

    def task_instance_started(self, task: Task, host: Host) -> None:
        self.data[task.name][host.name] = {"started": True}

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        self.data[task.name][host.name] = {
            "completed": True,
            "result": result.result,
        }

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass  # to keep example short and sweet we ignore subtasks

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass  # to keep example short and sweet we ignore subtasks
    
def greeter(task: Task, greet: str) -> Result:
    return Result(host=task.host, result=f"{greet}! my name is {task.host.name}")

""" data = {}

nr_with_processors = nr.with_processors([SaveResultToDict(data),PrintResult()])

nr_with_processors.run(
    name="hi!",
    task=greeter,
    greet="hi",
)

nr_with_processors.run(
    name="bye!",
    task=greeter,
    greet="bye",
)

print(data) """