from dataclasses import dataclass, field
from enum import Enum
from http.client import HTTPConnection
from queue import Queue
from typing import Dict, List
from threading import Thread

from pydantic import BaseModel

from backend.exceptions.workstation import WorkstationException
from .workstation_store import WorkstationInfo, WorkstationSpecification

from ..exceptions import WorkstationNotFound
from ..utils import get_logger

logger = get_logger("Tasks controller")


class Operator(str, Enum):
    AND = "and"
    OR = "or"


class ConditionType(str, Enum):
    TIMEOUT = "timeout"
    EQUAL = "equal"
    LESS = "less"
    MORE = "more"
    MOREEQUAL = "moreequal"
    LESSEQUAL = "lessequal"


class Condition(BaseModel):
    type: ConditionType
    measurement: str
    field: str
    value: float


class Conditions(BaseModel):
    operator: Operator
    conditionlist: List[Condition]


class Task(BaseModel):
    action: str
    target: str
    value: float
    conditions: Conditions


def check_conditions(task: Task):
    # TODO checking conditions
    return True


def send_task(httpconnection: HTTPConnection, task: Task):
    # try:
    body = task.json()
    httpconnection.request("POST", "/task", body)
    response = httpconnection.getresponse()
    data = response.read()
    # except Exception as e:
    #     logger.debug(f"Error sending task {e}")
    #     return

    if response.status == 200:
        logger.debug("Successfully sent a task!")
    else:
        logger.debug("Error sending task")


def push_tasks_to_station(queue: Queue[Task], workstationData: WorkstationSpecification):
    httpconnection: HTTPConnection = HTTPConnection(
        workstationData.info.connector_address, workstationData.info.connector_port
    )
    print(workstationData)
    while True:
        task: Task = queue.get()
        logger.debug("Got task from the queue")
        if not check_conditions(task):
            return
            # TODO waiting till conditions are met
        send_task(httpconnection, task)


@dataclass
class TasksController:
    workstationsData: Dict[str, WorkstationSpecification]
    pushingThreads: Dict[str, Thread] = field(default_factory=dict)
    taskQueuesStore: Dict[str, Queue[Task]] = field(default_factory=dict)

    def __post_init__(self):
        logger.info("Task controller")

        for station in self.workstationsData:

            queue = Queue(maxsize=20)

            thread = Thread(
                target=push_tasks_to_station,
                args=(queue, self.workstationsData[station]),
            )
            thread.start()

            self.taskQueuesStore[station] = queue
            self.workstationsData[station] = self.workstationsData[station]
            self.pushingThreads[station] = thread

        logger.info(self.taskQueuesStore, self.workstationsData)

    def addTask(self, workstation: str, task: Task):
        try:
            self.taskQueuesStore[workstation].put(task)
        except KeyError:
            raise WorkstationNotFound

    def getQueue(self, workstation: str) -> List[Task]:
        try:
            return list(self.taskQueuesStore[workstation].queue)
        except KeyError:
            raise WorkstationNotFound
