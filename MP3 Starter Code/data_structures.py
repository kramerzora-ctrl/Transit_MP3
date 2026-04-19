from dataclasses import dataclass
from typing import Any

@dataclass
class BusTask:
    """Bus tasks with origin and destination locations and start and end times.
    Records the time (if any) the Bus Task visits Berkeley BART.
    Calculates task duration if one is not provided during instantiation."""
    
    origin: str
    start_time: Any
    destination: str
    end_time: Any
    time_at_berkeley_BART: Any = None
    task_direction: Any = None
    task_duration: Any = None

    def __post_init__(self):
        if not self.task_duration:
            self.task_duration = self.end_time - self.start_time
        if (('NB' in self.origin) or ('SB' in self.origin)):
            if ('NB' in self.origin):
                self.task_direction = "NB"
            else:
                self.task_direction = "SB"
            self.origin = self.origin[:-3]
            
                
        if (('NB' in self.destination) or ('SB' in self.destination)):
            self.destination = self.destination[:-3]

    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time
    
    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination
    
    def get_task_duration(self):
        return self.task_duration
    
    def get_time_at_berkeley_BART(self):
        return self.time_at_berkeley_BART
    
    def passes_berkeley_bart(self):
        return self.time_at_berkeley_BART is not None


class BusRun:
    '''Data structure for storing the BusTasks that make up a BusRun. 
    Essentially a wrapper for a list/queue: functionality to view the first or latest/last task in the queue,
    can add tasks (to the back) or use add_front to append a task to the front of the queue.
    Use get_task_list to access the full list of BusTasks for a given BusRun.'''

    def __init__(self):
        self.task_list = list()

    def add_back(self, bus_task):
        self.task_list.append(bus_task)

    def add_front(self, bus_task):
        self.task_list = [bus_task] + self.task_list

    def is_empty(self):
        return len(self.task_list) == 0
    
    def get_first_task(self):
        if not self.is_empty():
            return self.task_list[0]
        else:
            return None

    def get_last_task(self):
        return self.get_latest_task()
    
    def get_latest_task(self):
        if not self.is_empty():
            return self.task_list[-1]
        else:
            return None
        
    def get_task_list(self):
        return self.task_list

    def print_tasks(self):
        for task in self.task_list:
            print(task)




@dataclass
class DriverTask:
    '''DriverTask object used to track origin and destination location and start and end times for each
    Driver Task. Time spent driving can be added during instantiation (used to keep track of wasted driver hours).
    Task duration is calculated upon instantiation.'''
    origin: str
    start_time: 0
    destination: str
    end_time: 0
    time_spent_driving: 0

    def __post_init__(self):
        self.task_duration = self.end_time - self.start_time

    def get_start_time(self):
        return self.start_time
    def get_end_time(self):
        return self.end_time
    
    def get_origin(self):
        return self.origin
    
    def get_destination(self):
        return self.destination
    
    def get_task_duration(self):
        return self.task_duration
    
    def get_time_spent_driving(self):
        return self.time_spent_driving
    



class DriverJob:
    def __init__(self, shift_length=8):
        '''Identical functionality to BusRun object (i.e., a queue/list) but with an added shift_length parameter that is set during instantiation (input as hours, stored as minutes).
        Use get_shift_length() to access the DriverJob's shift_length'''
        self.task_list = list()
        self.shift_length = shift_length*60

    def add_back(self, driver_task):
        self.task_list.append(driver_task)

    def get_shift_length(self):
        return self.shift_length
    
    def get_first_task(self):
        if not self.is_empty():
            return self.task_list[0]
        else:
            return None

    def get_last_task(self):
        return self.get_latest_task()
    
    def get_latest_task(self):
        if not self.is_empty():
            return self.task_list[-1]
        else:
            return None
        
    def get_task_list(self):
        return self.task_list
    
    def is_empty(self):
        return len(self.task_list) == 0
    
    def print_tasks(self):
        for task in self.task_list:
            print(task)
    